# coding:utf-8

# https://www.cnblogs.com/aby321/p/11805789.html
"""
照片尺寸，宽*高（单位：像素）
1寸照片：295*413
2寸照片：413*626
5寸照片（横版）：1500*1050
6寸照片（横版）：1800*1200
"""
import io

from PIL import Image, ImageDraw
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPixmap
from PIL.ImageQt import ImageQt

WIDTH_1IN = 295
HEIGHT_1IN = 413

WIDTH_2IN = 413
HEIGHT_2IN = 626

WIDTH_5IN = 1500
HEIGHT_5IN = 1050

# 非全景6寸照片
WIDTH_6IN = 1950
HEIGHT_6IN = 1300


def cut_photo(photo, choice):
    """
    将照片按照比例进行裁剪成1寸、2寸
    :param photo: 待处理的照片
    :param choice: <int> 1代表1寸，2代表2寸
    :return: 处理后的照片
    """
    width = photo.size[0]  # 宽
    height = photo.size[1]  # 高
    rate = height / width
    if choice == 1:
        if rate < (HEIGHT_1IN / WIDTH_1IN):
            x = (width - int(height / HEIGHT_1IN * WIDTH_1IN)) / 2
            y = 0
            cutted_photo = photo.crop((x, y, x + (int(height / HEIGHT_1IN * WIDTH_1IN)), y + height))

        else:
            x = 0
            y = (height - int(width / WIDTH_1IN * HEIGHT_1IN)) / 2
            cutted_photo = photo.crop((x, y, x + width, y + (int(width / WIDTH_1IN * HEIGHT_1IN))))
        return cutted_photo

    if choice == 2:
        if rate < (HEIGHT_2IN / WIDTH_2IN):
            x = (width - int(height / HEIGHT_2IN * WIDTH_2IN)) / 2
            y = 0
            cutted_photo = photo.crop((x, y, x + (int(height / HEIGHT_2IN * WIDTH_2IN)), y + height))

        else:
            x = 0
            y = (height - int(width / WIDTH_2IN * HEIGHT_2IN)) / 2
            cutted_photo = photo.crop((x, y, x + width, y + (int(width / WIDTH_2IN * HEIGHT_2IN))))

        return cutted_photo


def resize_photo(photo, choice):
    '''
    缩放照片
    :param photo: 待处理的照片
    :param choice: <int> 1代表1寸，2代表2寸
    :return: 处理后的照片
    '''
    if choice == 1:
        resized_photo = photo.resize((WIDTH_1IN, HEIGHT_1IN))
        return resized_photo
    if choice == 2:
        resized_photo = photo.resize((WIDTH_2IN, HEIGHT_2IN))
        return resized_photo


def layout_photo_5_1(photo, color=(255, 255, 255)):
    """
    在5寸照片上排版1寸照片
    :param photo: 待处理照片1寸
    :param color: 背景色
    :return: 处理后的照片
    """
    bk = Image.new("RGB", [WIDTH_5IN, HEIGHT_5IN], color)
    draw = ImageDraw.Draw(bk)  # 创建画笔
    draw.line([(0, HEIGHT_5IN / 2), (WIDTH_5IN, HEIGHT_5IN / 2)], fill=128)  # 横线
    draw.line([(WIDTH_5IN * 0.25, 0), (WIDTH_5IN * 0.25, HEIGHT_5IN)], fill=128)  # 第1条竖线
    draw.line([(WIDTH_5IN * 0.5, 0), (WIDTH_5IN * 0.5, HEIGHT_5IN)], fill=128)  # 第2条竖线
    draw.line([(WIDTH_5IN * 0.75, 0), (WIDTH_5IN * 0.75, HEIGHT_5IN)], fill=128)  # 第3条竖线

    focus_point = [0.125 * WIDTH_5IN, 0.25 * HEIGHT_5IN]
    start_point = [focus_point[0] - 0.5 * WIDTH_1IN, focus_point[1] - 0.5 * HEIGHT_1IN]
    for i in range(0, 2):
        for k in range(0, 4):
            bk.paste(photo, (int(start_point[0] + (k * WIDTH_5IN / 4)), int(start_point[1] + 0.5 * i * HEIGHT_5IN)))
    return bk


def layout_photo_5_2(photo, color=(255, 255, 255)):
    """
    在5寸照片上排版1寸照片
    :param photo: 待处理照片1寸
    :param color: 背景色
    :return: 处理后的照片
    """
    bk = Image.new("RGB", [HEIGHT_5IN,WIDTH_5IN], color)
    # 创建画笔
    draw = ImageDraw.Draw(bk)
    draw.line([(0, WIDTH_5IN / 2), (WIDTH_5IN, WIDTH_5IN / 2)], fill=128)  # 横线
    draw.line([(HEIGHT_5IN * 0.5, 0), (HEIGHT_5IN * 0.5, WIDTH_5IN)], fill=128)  # 竖线
    focus_point = [0.25 * HEIGHT_5IN, 0.25 * WIDTH_5IN]
    start_point = [focus_point[0] - 0.5 * WIDTH_2IN, focus_point[1] - 0.5 * HEIGHT_2IN]
    # print(focus_point,start_point)
    for i in range(0, 2):
        for k in range(0, 2):
            bk.paste(photo, (int(start_point[0] + (k * HEIGHT_5IN / 2)), int(start_point[1] + 0.5 * i * WIDTH_5IN)))
    return bk


def layout_photo_5_mix(photo1, photo2, color=(255, 255, 255)):
    """
    在5寸照片上混合排版1寸、2寸照片
    :param photo1: 待处理照片1寸
    :param photo2: 待处理照片2寸
    :param color: 背景色
    :return: 处理后的照片
    """
    bk = Image.new("RGB", [WIDTH_5IN, HEIGHT_5IN], color)
    # 创建画笔
    draw = ImageDraw.Draw(bk)
    draw.line([(0, HEIGHT_5IN / 2), (WIDTH_5IN, HEIGHT_5IN / 2)], fill=128)  # 横线
    draw.line([(WIDTH_5IN * 0.25, 0), (WIDTH_5IN * 0.25, HEIGHT_5IN)], fill=128)  # 第1条竖线
    draw.line([(WIDTH_5IN * 0.5, 0), (WIDTH_5IN * 0.5, HEIGHT_5IN)], fill=128)  # 第2条竖线

    focus_point = [0.125 * WIDTH_5IN, 0.25 * HEIGHT_5IN]
    start_point = [focus_point[0] - 0.5 * WIDTH_1IN, focus_point[1] - 0.5 * HEIGHT_1IN]
    focus_point2 = [0.75 * WIDTH_5IN, 0.25 * HEIGHT_5IN]
    start_point2 = [focus_point2[0] - 0.5 * HEIGHT_2IN, focus_point2[1] - 0.5 * WIDTH_2IN]

    for i in range(0, 2):
        for k in range(0, 2):
            bk.paste(photo1, (int(start_point[0] + (k * WIDTH_5IN / 4)), int(start_point[1] + 0.5 * i * HEIGHT_5IN)))

    bk.paste(photo2, (int(start_point2[0]), int(start_point2[1])))
    bk.paste(photo2, (int(start_point2[0]), int(start_point2[1] + 0.5 * HEIGHT_5IN)))
    return bk


def layout_photo_6_1(photo, color=(255, 255, 255)):
    """
    在6寸照片上排版2寸照片
    :param photo: 待处理照片1寸
    :param color: 背景色
    :return: 处理后的照片
    """
    bk = Image.new("RGB", [HEIGHT_6IN, WIDTH_6IN], color)  # 竖版排版
    # 创建画笔
    draw = ImageDraw.Draw(bk)
    draw.line([(0, WIDTH_6IN * 0.25), (WIDTH_6IN, WIDTH_6IN * 0.25)], fill=128)  # 横线
    draw.line([(0, WIDTH_6IN * 0.5), (WIDTH_6IN, WIDTH_6IN * 0.5)], fill=128)  # 横线
    draw.line([(0, WIDTH_6IN * 0.75), (WIDTH_6IN, WIDTH_6IN * 0.75)], fill=128)  # 横线
    draw.line([(HEIGHT_6IN * 0.25, 0), (HEIGHT_6IN * 0.25, WIDTH_6IN)], fill=128)  # 竖线
    draw.line([(HEIGHT_6IN * 0.5, 0), (HEIGHT_6IN * 0.5, WIDTH_6IN)], fill=128)  # 竖线
    draw.line([(HEIGHT_6IN * 0.75, 0), (HEIGHT_6IN * 0.75, WIDTH_6IN)], fill=128)  # 竖线
    focus_point = [0.125 * HEIGHT_6IN, 0.125 * WIDTH_6IN]
    start_point = [focus_point[0] - 0.5 * WIDTH_1IN, focus_point[1] - 0.5 * HEIGHT_1IN]
    # print(focus_point,start_point)
    for i in range(0, 4):
        for k in range(0, 4):
            bk.paste(photo, (int(start_point[0] + (k * HEIGHT_6IN / 4)), int(start_point[1] + i * 0.25 * WIDTH_6IN)))
    return bk


def layout_photo_6_2(photo, color=(255, 255, 255)):
    """
    在6寸照片上排版2寸照片
    :param photo: 待处理照片2寸
    :param color: 背景色
    :return: 处理后的照片
    """
    bk = Image.new("RGB", [WIDTH_6IN, HEIGHT_6IN], color)
    # 创建画笔
    draw = ImageDraw.Draw(bk)
    draw.line([(0, HEIGHT_6IN / 2), (WIDTH_6IN, HEIGHT_6IN / 2)], fill=128)  # 横线
    draw.line([(WIDTH_6IN * 0.25, 0), (WIDTH_6IN * 0.25, HEIGHT_6IN)], fill=128)  # 第1条竖线
    draw.line([(WIDTH_6IN * 0.5, 0), (WIDTH_6IN * 0.5, HEIGHT_6IN)], fill=128)  # 第2条竖线
    draw.line([(WIDTH_6IN * 0.75, 0), (WIDTH_6IN * 0.75, HEIGHT_6IN)], fill=128)  # 第3条竖线
    focus_point = [0.125 * WIDTH_6IN, 0.25 * HEIGHT_6IN]
    start_point = [focus_point[0] - 0.5 * WIDTH_2IN, focus_point[1] - 0.5 * HEIGHT_2IN]
    for i in range(0, 2):
        for k in range(0, 4):
            bk.paste(photo, (int(start_point[0] + (k * WIDTH_6IN / 4)), int(start_point[1] + 0.5 * i * HEIGHT_6IN)))
    return bk


def layout_photo_6_mix1(photo1, photo2, color=(255, 255, 255)):
    """
    在6寸照片上混合排版1寸、2寸照片
    :param photo1: 待处理照片1寸
    :param photo2: 待处理照片2寸
    :param color: 背景色
    :return: 处理后的照片
    """
    bk = Image.new("RGB", [WIDTH_6IN, HEIGHT_6IN], color)
    # 创建画笔
    draw = ImageDraw.Draw(bk)
    draw.line([(0, HEIGHT_6IN * 0.5), (WIDTH_6IN, HEIGHT_6IN / 2)], fill=128)  # 横线
    draw.line([(0, HEIGHT_6IN * 0.25), (WIDTH_6IN * 0.5, HEIGHT_6IN * 0.25)], fill=128)  # 短横线
    draw.line([(0, HEIGHT_6IN * 0.75), (WIDTH_6IN * 0.5, HEIGHT_6IN * 0.75)], fill=128)  # 短横线
    draw.line([(WIDTH_6IN * 0.25, 0), (WIDTH_6IN * 0.25, HEIGHT_6IN)], fill=128)  # 第1条竖线
    draw.line([(WIDTH_6IN * 0.5, 0), (WIDTH_6IN * 0.5, HEIGHT_6IN)], fill=128)  # 第2条竖线
    draw.line([(WIDTH_6IN * 0.75, 0), (WIDTH_6IN * 0.75, HEIGHT_6IN)], fill=128)  # 第3条竖线
    focus_point = [0.125 * WIDTH_6IN, 0.125 * HEIGHT_6IN]
    start_point = [focus_point[0] - 0.5 * HEIGHT_1IN, focus_point[1] - 0.5 * WIDTH_1IN]
    for i in range(0, 4):
        for k in range(0, 2):
            bk.paste(photo1,
                     (int(start_point[0] + (0.25 * k * WIDTH_6IN)), int(start_point[1] + 0.25 * i * HEIGHT_6IN)))
    focus_point2 = [0.625 * WIDTH_6IN, 0.25 * HEIGHT_6IN]
    start_point2 = [focus_point2[0] - 0.5 * WIDTH_2IN, focus_point2[1] - 0.5 * HEIGHT_2IN]
    for i in range(0, 2):
        for k in range(0, 2):
            bk.paste(photo2,
                     (int(start_point2[0] + (0.25 * k * WIDTH_6IN)), int(start_point2[1] + 0.5 * i * HEIGHT_6IN)))
    return bk


def layout_photo_6_mix2(photo1, photo2, color=(255, 255, 255)):
    """
    在6寸照片上混合排版1寸、2寸照片
    :param photo1: 待处理照片1寸
    :param photo2: 待处理照片2寸
    :param color: 背景色
    :return: 处理后的照片
    """
    bk = Image.new("RGB", [HEIGHT_6IN, WIDTH_6IN], color)  # 竖版排版
    # 创建画笔
    draw = ImageDraw.Draw(bk)

    draw.line([(350, 0), (350, WIDTH_6IN)], fill=128)  # 竖线
    draw.line([(700, 0), (700, WIDTH_6IN)], fill=128)  # 竖线

    draw.line([(0, WIDTH_6IN * 0.25), (700, WIDTH_6IN * 0.25)], fill=128)  # 横线1
    draw.line([(0, WIDTH_6IN * 0.5), (700, WIDTH_6IN * 0.5)], fill=128)  # 横线2
    draw.line([(0, WIDTH_6IN * 0.75), (700, WIDTH_6IN * 0.75)], fill=128)  # 横线3
    draw.line([(700, WIDTH_6IN / 3), (HEIGHT_6IN, WIDTH_6IN / 3)], fill=128)  # 横线4
    draw.line([(700, WIDTH_6IN * 2 / 3), (HEIGHT_6IN, WIDTH_6IN * 2 / 3)], fill=128)  # 横线5

    focus_point = [0.5 * 350, 0.125 * WIDTH_6IN]
    start_point = [focus_point[0] - 0.5 * WIDTH_1IN, focus_point[1] - 0.5 * HEIGHT_1IN]

    # print(focus_point,start_point)
    for i in range(0, 4):
        for k in range(0, 2):
            bk.paste(photo1, (int(start_point[0] + (k * 350)), int(start_point[1] + i * 0.25 * WIDTH_6IN)))

    focus_point2 = [0.5 * HEIGHT_6IN + 350, WIDTH_6IN / 6]
    start_point2 = [focus_point2[0] - 0.5 * WIDTH_2IN, focus_point2[1] - 0.5 * HEIGHT_2IN]
    for i in range(0, 3):
        bk.paste(photo2, (int(start_point2[0]), int(start_point2[1] + i * WIDTH_6IN / 3)))
    return bk


def bytes_to_qimage(image_content):
    img = QImage()
    assert img.loadFromData(image_content)
    return img


def fill_background_color(im, fill_color):

    im = im.convert("RGBA")  # it had mode P after DL it from OP
    if im.mode in ('RGBA', 'LA'):
        background = Image.new(im.mode[:-1], im.size, fill_color)
        background.paste(im, im.split()[-1])  # omit transparency
        im = background
    return im.convert("RGB")


def design_photo(image, size, color=(255, 255, 255)):
    if size == 's1x5':
        return layout_photo_5_1(resize_photo(cut_photo(image, 1), 1), color=color)
    elif size == 's1x6':
        return layout_photo_6_1(resize_photo(cut_photo(image, 1), 1))
    elif size == 's2x5':
        return layout_photo_5_2(resize_photo(cut_photo(image, 2), 2))
    elif size == 's2x6':
        return layout_photo_6_2(resize_photo(cut_photo(image, 2), 2))
    elif size == 's5max':
        return layout_photo_5_mix(resize_photo(cut_photo(image, 1), 1),
                                  resize_photo(cut_photo(image, 2), 2).rotate(90, expand=True),
                                  color=color)
    elif size == 's6max':
        return layout_photo_6_mix1(resize_photo(cut_photo(image, 1), 1).rotate(90, expand=True),
                                   resize_photo(cut_photo(image, 2), 2),
                                   color=color)
    raise Exception("not support image size %s" % size)


def pilow_image_to_qt_pixmap(image):
    """
    pillow image to qt  qimage
    实际测试中发现这个有问题

    """
    qim = ImageQt(image)
    return QPixmap.fromImage(qim)


def pil2pixmap(im):
    """
    pillow image to qt  pixmap
    """
    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    # Bild in RGBA konvertieren, falls nicht bereits passiert
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    pixmap = QtGui.QPixmap.fromImage(qim)
    return pixmap


def bytes_to_pillow_image(image_data):
    return Image.open(io.BytesIO(image_data))


def main():
    im = Image.open(r'D:\dsf.jpg')
    width = im.size[0]
    height = im.size[1]
    rate = height / width
    # .save('5_1.jpg')
    layout_photo_5_2(resize_photo(cut_photo(im, 2), 2)).save('5_2.jpg')
    # layout_photo_6_1(resize_photo(cut_photo(im, 1), 1)).save('6_1.jpg')
    # layout_photo_6_2(resize_photo(cut_photo(im, 2), 2)).save('6_2.jpg')
    # layout_photo_5_mix(resize_photo(cut_photo(im, 1), 1), resize_photo(cut_photo(im, 2), 2).rotate(90, expand=True)).save(
    #     '5_1_mix.jpg')
    # layout_photo_6_mix1(resize_photo(cut_photo(im, 1), 1).rotate(90, expand=True), resize_photo(cut_photo(im, 2), 2)).save(
    #     '6_mix1.jpg')
    # layout_photo_6_mix2(resize_photo(cut_photo(im, 1), 1), resize_photo(cut_photo(im, 2), 2)).save('6_mix2.jpg')



if __name__ == "__main__":
    main()
