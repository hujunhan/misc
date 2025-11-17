import cv2
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt

# 1. 读取图像
img_path = "/Users/hu/Downloads/WechatIMG4181.jpg"
img = cv2.imread(img_path)
orig = img.copy()

# 2. 转为灰度并放大，提高识别率
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
scale = 2
h, w = gray.shape
gray = cv2.resize(gray, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)

# 3. 自适应二值化
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10
)

# 4. OCR 获取每个文本框的位置和内容
data = pytesseract.image_to_data(
    thresh, output_type=pytesseract.Output.DICT, config="--psm 11"
)

# 5. 在原图上绘制检测到的框和文字
for i, text in enumerate(data["text"]):
    if text.strip():  # 仅对非空文本框绘制
        x, y, w_box, h_box = (
            data["left"][i] // scale,
            data["top"][i] // scale,
            data["width"][i] // scale,
            data["height"][i] // scale,
        )
        # 绘制矩形框
        cv2.rectangle(orig, (x, y), (x + w_box, y + h_box), (0, 0, 255), 2)
        # 标注文字
        cv2.putText(
            orig,
            text,
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )

# 6. 显示结果
orig_rgb = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(12, 12))
plt.imshow(orig_rgb)
plt.axis("off")
plt.title("OCR 检测框示例")
plt.show()
