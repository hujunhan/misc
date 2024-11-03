import cv2
import cv2
import json


def read_rectangles_from_json(json_file_path, image_width, image_height):
    rectangles = []

    with open(json_file_path, 'r') as file:
        data = json.load(file)

        for annotation in data['shapes']:
            cls = annotation['label']

            # 只处理类别为0的矩形框
            if cls == 'panel':
                x1, y1 = int(annotation['points'][0][0]), int(annotation['points'][0][1])
                x2, y2 = int(annotation['points'][2][0]), int(annotation['points'][2][1])
                # 添加矩形框到列表中
                rectangles.append((x1, y1, x2, y2))

    return rectangles


def generate_minimum_square(x1, y1, x2, y2):
    # 计算宽度和高度
    w = x2 - x1
    h = y2 - y1

    # 找到最短边
    min_side = min(w, h)

    # 计算矩形框的中心点
    center_x = x1 + w // 2
    center_y = y1 + h // 2

    # 计算正方形的左上角坐标
    square_x1 = center_x - min_side // 2
    square_y1 = center_y - min_side // 2

    # 计算正方形的右下角坐标
    square_x2 = square_x1 + min_side
    square_y2 = square_y1 + min_side

    # 确保正方形不会超出图像边界
    square_x1 = max(0, square_x1)
    square_y1 = max(0, square_y1)
    square_x2 = min(square_x2, center_x * 2)
    square_y2 = min(square_y2, center_y * 2)

    return square_x1, square_y1, square_x2, square_y2


def draw_rectangles_and_squares(image, rectangles):
    squares = []
    for rect in rectangles:
        x1, y1, x2, y2 = rect
        square_x1, square_y1, square_x2, square_y2 = generate_minimum_square(x1, y1, x2, y2)

        # 绘制原始矩形框
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 绘制最小正方形
        cv2.rectangle(image, (square_x1, square_y1), (square_x2, square_y2), (255, 0, 0), 2)

        # 保存最小正方形的坐标
        squares.append((square_x1, square_y1, square_x2, square_y2))

    return image, squares

def save_squares_to_txt(squares, txt_file_path):
    with open(txt_file_path, 'w') as file:
        for square in squares:
            square_x1, square_y1, square_x2, square_y2 = square
            file.write(f"{square_x1} {square_y1} {square_x2} {square_y2}\n")


def rectangle2square(image_path,json_file_path,txt_file_path):

    image = cv2.imread(image_path)
    image_height, image_width = image.shape[:2]

    # 读取矩形框数据
    rectangles = read_rectangles_from_json(json_file_path, image_width, image_height)

    # 在图像上绘制矩形框和最小正方形
    result_image, squares = draw_rectangles_and_squares(image, rectangles)

    # 保存最小正方形的坐标到TXT文件
    # txt_file_path = "C:/Users/QS/Desktop/zivida/1-7/test_datasets/1/1_template_bbox.txt"  # 保存坐标的TXT文件路径
    save_squares_to_txt(squares, txt_file_path)

    # 显示结果图像
    # cv2.imshow("Image with Rectangles and Squares", result_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 保存结果图像
    # output_path = "C:/Users/QS/Desktop/zivida/1-7/test_datasets/1/1_show_template_bbox.png"  # 保存结果图像的路径
    # cv2.imwrite(output_path, result_image)


