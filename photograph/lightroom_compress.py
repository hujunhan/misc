#!/usr/bin/env python3

import os
import subprocess
import argparse
import shutil
import time
from concurrent.futures import ThreadPoolExecutor

# --- START CONFIGURATION ---
# --- 请根据你的系统路径修改此部分 ---

# 1. 基本路径
BASE_SOURCE_DIR = "/Volumes/SSK/LightroomLocal"
BASE_TARGET_DIR = "/Volumes/SSK/LightroomDNG"

# 2. 可执行文件路径
# Mac: "/Applications/Adobe DNG Converter.app/Contents/MacOS/Adobe DNG Converter"
# Windows: r"C:\Program Files\Adobe\Adobe DNG Converter.exe"
DNG_CONVERTER_EXE = (
    "/Applications/Adobe DNG Converter.app/Contents/MacOS/Adobe DNG Converter"
)

# 确保 "HandBrakeCLI" 在你的系统 PATH 中，或者在此处提供完整路径
# Mac (if installed via Homebrew): "HandBrakeCLI"
# Windows: r"C:\Program Files\HandBrake\HandBrakeCLI.exe"
HANDBRAKE_CLI_EXE = "HandBrakeCLI"

# 3. 压缩设置
# HandBrake 预设名称 (必须与你在 HandBrake GUI 中保存的名称完全一致)
HANDBRAKE_PRESET = "iPhone Compress"
# 当 GUI 预设不可用时，始终从本地 JSON 预设文件导入
# 参考命令: HandBrakeCLI --preset-import-file ~/Downloads/iPhoneCompress.json -Z "iPhone Compress"
# 可通过环境变量 HANDBRAKE_PRESET_FILE 覆盖此路径
HANDBRAKE_PRESET_FILE = os.path.expanduser(
    os.getenv("HANDBRAKE_PRESET_FILE", "~/Downloads/iPhoneCompress.json")
)
# HandBrake 输出文件的扩展名
HANDBRAKE_VIDEO_EXT = ".mp4"

# DNG Converter 命令行参数 (使用高画质JXL有损压缩)
# [cite: 48]
DNG_ARGS = [
    "-p1",
    "-mp",  # [cite: 33] 多文件并行处理
    "-dng1.7",  # [cite: 45] 使用 DNG 1.7 规范以支持 JXL
    "-jxl",
    "-lossy",  # [cite: 32] 启用有损压缩
    "-fl",
]

# 4. 文件类型定义
# 添加你相机产生的所有 RAW 文件扩展名
RAW_EXTENSIONS = {
    ".dng",
    ".cr3",
    ".arw",
    ".nef",
    ".cr2",
    ".raf",
    ".orf",
    ".rw2",
    ".pef",
    ".srw",
    ".raw",
}
# 添加你所有的视频文件扩展名
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".mpg", ".mpeg", ".avi", ".mts", ".m2ts"}

# 不需要拷贝到目标目录的“其他文件”扩展名（例如 XMP/XML 辅助文件）
EXCLUDE_COPY_EXTENSIONS = {".xmp", ".xml"}

# 5. 并行处理
# 同时运行多少个 HandBrake 视频压缩任务
# (建议设置为你 CPU 核心数的一半或全部)
MAX_VIDEO_WORKERS = 4

# --- END CONFIGURATION ---


def format_duration(seconds: float) -> str:
    """将秒格式化为易读的时长字符串，如 1h 2m 3.45s。"""
    ms = seconds - int(seconds)
    seconds_int = int(seconds)
    h, rem = divmod(seconds_int, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m {s + ms:.2f}s"
    if m:
        return f"{m}m {s + ms:.2f}s"
    return f"{s + ms:.2f}s"


def format_size(num_bytes: int) -> str:
    """将字节数格式化为人类可读的字符串（KB/MB/GB/TB）。"""
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)}{unit}"
            return f"{size:.2f}{unit}"
        size /= 1024.0


def get_dir_size(path: str) -> int:
    """递归计算文件夹大小（包含所有文件）。遇到无权限或损坏文件时跳过。"""
    total = 0
    for root, _, files in os.walk(path):
        for name in files:
            fp = os.path.join(root, name)
            try:
                # 跳过断开的符号链接
                if os.path.islink(fp):
                    continue
                total += os.path.getsize(fp)
            except Exception:
                # 安静跳过无法读取大小的文件
                pass
    return total


def _safe_getsize(fp: str) -> int:
    try:
        return os.path.getsize(fp)
    except Exception:
        return 0


def process_raw_files(raw_files_list, target_base_dir):
    """
    使用 -mp 标志一次性调用 DNG Converter 处理所有 RAW 文件。
    """
    if not raw_files_list:
        print("INFO: 未找到 RAW 文件，跳过 DNG 转换。")
        return

    print(f"🚀 开始处理 {len(raw_files_list)} 个 RAW 文件 (使用 -mp 并行)...")

    # [cite_start]# [cite: 33] -d 参数指定输出目录
    command = [DNG_CONVERTER_EXE, "-d", target_base_dir]
    command.extend(DNG_ARGS)
    command.extend(raw_files_list)  # [cite: 13, 53] 将所有文件作为参数附加在最后

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ DNG 转换完成。所有文件已保存到: {target_base_dir}")
        print(
            "   注意: DNG Converter 会将所有文件平铺到目标根目录，不会保留子文件夹结构。"
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: DNG Converter 转换失败。")
        print(f"   错误信息: {e.stderr}")
    except FileNotFoundError:
        print(f"❌ ERROR: 未找到 DNG Converter 执行文件。")
        print(f"   请检查路径: {DNG_CONVERTER_EXE}")


def process_video_file(file_paths):
    """
    处理单个视频文件，供 ThreadPoolExecutor 调用。
    """
    source_path, target_path = file_paths
    base_name = os.path.basename(source_path)
    print(f"  -> 正在转换视频: {base_name} ...")

    t0 = time.perf_counter()

    # 确保预设文件存在
    if not os.path.isfile(HANDBRAKE_PRESET_FILE):
        dt = time.perf_counter() - t0
        print(
            f"  ❌ 预设文件不存在: {HANDBRAKE_PRESET_FILE}，请确认路径或设置环境变量 HANDBRAKE_PRESET_FILE。 ({format_duration(dt)})"
        )
        return False, dt

    command = [
        HANDBRAKE_CLI_EXE,
        "-i",
        source_path,
        "-o",
        target_path,
        "--preset-import-file",
        HANDBRAKE_PRESET_FILE,
        "-Z",
        HANDBRAKE_PRESET,
    ]

    try:
        # 使用 capture_output 隐藏 HandBrake 大量的日志输出
        subprocess.run(command, check=True, capture_output=True, text=True)
        dt = time.perf_counter() - t0
        print(f"  ✓ 完成视频: {os.path.basename(target_path)} ({format_duration(dt)})")
        return True, dt
    except subprocess.CalledProcessError as e:
        dt = time.perf_counter() - t0
        print(f"  ❌ 转换视频失败: {base_name} ({format_duration(dt)})")
        print(f"     错误: {e.stderr}")
        return False, dt
    except FileNotFoundError:
        dt = time.perf_counter() - t0
        print(f"❌ ERROR: 未找到 HandBrakeCLI 执行文件。 ({format_duration(dt)})")
        print(f"   请检查路径: {HANDBRAKE_CLI_EXE}")
        return False, dt


def main():
    parser = argparse.ArgumentParser(
        description="自动化 Lightroom 归档压缩工作流。",
        epilog="示例: python3 compress_archive.py event1",
    )
    # 允许从命令行传入相对路径（相对于 BASE_SOURCE_DIR/BASE_TARGET_DIR）
    default_folder = "Event/2023_NewYear"
    parser.add_argument(
        "folder",
        nargs="?",
        default=default_folder,
        help="要处理的相册相对路径（相对于 BASE_SOURCE_DIR/BASE_TARGET_DIR）",
    )

    args = parser.parse_args()

    folder_name = args.folder
    source_dir = os.path.join(BASE_SOURCE_DIR, folder_name)
    target_dir = os.path.join(BASE_TARGET_DIR, folder_name)

    t_total_start = time.perf_counter()

    # --- 1. 路径和文件夹检查 ---
    if not os.path.isdir(source_dir):
        print(f"❌ ERROR: 源文件夹不存在: {source_dir}")
        print(f"   请确保你已从 Lightroom 下载了此相册。")
        return

    target_dir_pre_exists = os.path.exists(target_dir)
    if not target_dir_pre_exists:
        print(f"INFO: 目标文件夹不存在，正在创建: {target_dir}")
        os.makedirs(target_dir)
    else:
        print(f"INFO: 目标文件夹已存在: {target_dir}")
    # 记录开始时目标文件夹大小（用于提示是否已有历史内容）
    target_size_before = get_dir_size(target_dir)

    # --- 2. 遍历文件并分类 ---
    print(f"🔍 正在扫描 {source_dir} ...")
    t_scan_start = time.perf_counter()

    raw_files_to_process = []
    video_files_to_process = []
    other_files_to_copy = []

    for root, dirs, files in os.walk(source_dir):
        # 计算相对路径，以便在目标位置创建同样的子文件夹结构
        relative_path = os.path.relpath(root, source_dir)

        # 确保目标子文件夹存在 (用于视频和"其他文件")
        target_subdir = os.path.join(target_dir, relative_path)
        if not os.path.exists(target_subdir):
            os.makedirs(target_subdir)

        for file in files:
            file_name, file_ext = os.path.splitext(file)
            file_ext_lower = file_ext.lower()
            source_file_path = os.path.join(root, file)

            if file_ext_lower in RAW_EXTENSIONS:
                raw_files_to_process.append(source_file_path)

            elif file_ext_lower in VIDEO_EXTENSIONS:
                target_file_name = file_name + HANDBRAKE_VIDEO_EXT
                target_file_path = os.path.join(target_subdir, target_file_name)
                video_files_to_process.append((source_file_path, target_file_path))

            else:
                # 其它文件 (JPG, PNG 等) 直接拷贝，但排除 .xmp/.xml 这类辅助文件
                if file_ext_lower in EXCLUDE_COPY_EXTENSIONS:
                    continue
                target_file_path = os.path.join(target_subdir, file)
                other_files_to_copy.append((source_file_path, target_file_path))

    t_scan = time.perf_counter() - t_scan_start
    print(f"   > 找到 {len(raw_files_to_process)} 个 RAW 文件。")
    print(f"   > 找到 {len(video_files_to_process)} 个视频文件。")
    print(f"   > 找到 {len(other_files_to_copy)} 个其他文件 (JPG 等)。")
    print(f"   > 扫描耗时: {format_duration(t_scan)}")
    print("-" * 30)

    # --- 3. 执行 DNG 转换 ---
    # (一次性调用)
    t_dng_start = time.perf_counter()
    process_raw_files(raw_files_to_process, target_dir)
    t_dng = time.perf_counter() - t_dng_start
    print(f"⏱️ DNG 转换阶段用时: {format_duration(t_dng)}")
    print("-" * 30)

    # --- 4. 执行视频转换 ---
    # (使用线程池并行处理)
    if not video_files_to_process:
        print("INFO: 未找到视频文件，跳过视频转换。")
    else:
        print(
            f"🚀 开始处理 {len(video_files_to_process)} 个视频文件 (使用 {MAX_VIDEO_WORKERS} 个并行任务)..."
        )
        t_vid_start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=MAX_VIDEO_WORKERS) as executor:
            results = list(executor.map(process_video_file, video_files_to_process))
        t_vid_wall = time.perf_counter() - t_vid_start
        success_cnt = sum(1 for ok, _ in results if ok)
        total_video_cpu_time = sum(dt for _, dt in results)
        avg_video_time = (total_video_cpu_time / len(results)) if results else 0.0
        print("✅ 视频转换完成。")
        print(
            f"   > 成功 {success_cnt}/{len(results)} 个，阶段用时(墙钟): {format_duration(t_vid_wall)}，平均每个(累计): {format_duration(avg_video_time)}"
        )
    print("-" * 30)

    # --- 5. 拷贝其他文件 ---
    if not other_files_to_copy:
        print("INFO: 未找到其他文件，跳过拷贝。")
    else:
        print(f"🚀 正在拷贝 {len(other_files_to_copy)} 个其他文件 (JPG...)")
        t_copy_start = time.perf_counter()
        copied_count = 0
        for src, dest in other_files_to_copy:
            try:
                shutil.copy2(src, dest)  # copy2 保留元数据
                copied_count += 1
            except Exception as e:
                print(f"  ❌ 拷贝失败: {os.path.basename(src)} -> {e}")
        t_copy = time.perf_counter() - t_copy_start
        print(f"✅ 成功拷贝 {copied_count} 个文件。用时: {format_duration(t_copy)}")
    print("-" * 30)

    t_total = time.perf_counter() - t_total_start
    print(f"🎉 全部任务完成! 压缩后的文件位于: {target_dir}")
    print(
        f"⏳ 总耗时: {format_duration(t_total)} (扫描 {format_duration(t_scan)} | DNG {format_duration(t_dng)} | 视频 {format_duration(t_vid_wall) if 't_vid_wall' in locals() else '0.00s'} | 拷贝 {format_duration(t_copy) if 't_copy' in locals() else '0.00s'})"
    )

    # --- 6. 大小对比与节省统计 ---
    print("-" * 30)
    print("📦 正在计算大小对比，请稍候…")

    # 源文件夹总大小（包含所有文件，含 .xmp/.xml 等）
    src_total_bytes = get_dir_size(source_dir)
    # 目标文件夹总大小
    dst_total_bytes = get_dir_size(target_dir)

    # 分项统计（源端）
    raw_src_bytes = sum(_safe_getsize(fp) for fp in raw_files_to_process)
    vid_src_bytes = sum(_safe_getsize(src) for src, _ in video_files_to_process)
    other_src_bytes = sum(_safe_getsize(src) for src, _ in other_files_to_copy)

    # 分项统计（目标端）
    # RAW 转换后的 DNG（注意 DNG Converter 平铺输出到 target_dir 根目录及其子目录，按后缀统计）
    raw_dst_bytes = 0
    for root, _, files in os.walk(target_dir):
        for name in files:
            if os.path.splitext(name)[1].lower() == ".dng":
                raw_dst_bytes += _safe_getsize(os.path.join(root, name))
    # 视频转换后的文件（根据已确定的目标路径）
    vid_dst_bytes = 0
    for _, dst in video_files_to_process:
        vid_dst_bytes += _safe_getsize(dst)
    # 其他文件（拷贝后的实际大小）
    other_dst_bytes = 0
    for _, dst in other_files_to_copy:
        other_dst_bytes += _safe_getsize(dst)

    def pct_reduce(old: int, new: int) -> str:
        if old <= 0:
            return "0.00%"
        return f"{(1.0 - (new / old)) * 100.0:.2f}%"

    print("📊 大小对比：")
    print(f"   源文件夹: {format_size(src_total_bytes)}")
    if target_dir_pre_exists and target_size_before > 0:
        print(
            f"   目标文件夹: {format_size(dst_total_bytes)} (开始前已有 {format_size(target_size_before)}，本次新增约 {format_size(max(dst_total_bytes - target_size_before, 0))})"
        )
    else:
        print(f"   目标文件夹: {format_size(dst_total_bytes)}")
    print(
        f"   总体节省: {format_size(max(src_total_bytes - dst_total_bytes, 0))} ({pct_reduce(src_total_bytes, dst_total_bytes)})"
    )

    print("   —— 分项 ——")
    print(
        f"   RAW:   {format_size(raw_src_bytes)} -> {format_size(raw_dst_bytes)}，节省 {format_size(max(raw_src_bytes - raw_dst_bytes, 0))} ({pct_reduce(raw_src_bytes, raw_dst_bytes)})"
    )
    print(
        f"   视频:  {format_size(vid_src_bytes)} -> {format_size(vid_dst_bytes)}，节省 {format_size(max(vid_src_bytes - vid_dst_bytes, 0))} ({pct_reduce(vid_src_bytes, vid_dst_bytes)})"
    )
    print(
        f"   其他:  {format_size(other_src_bytes)} -> {format_size(other_dst_bytes)}，节省 {format_size(max(other_src_bytes - other_dst_bytes, 0))} ({pct_reduce(other_src_bytes, other_dst_bytes)})"
    )


if __name__ == "__main__":
    main()
