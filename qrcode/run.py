#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 生成指定二维码

import qrcode
import qrcode.image.svg
import os

DataMin = 100000
DataMax = 100000

saveSvg = True  # 是否保存svg的图片
qr = qrcode.QRCode(
    version=1,  # version：参数是（1-40）的整数，该参数用来控制二维码的尺寸
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # err_correction 参数控制生成二维的误差
    box_size=10,
    border=4,
)
qr.make(fit=True)
factory = qrcode.image.svg.SvgImage

if not os.path.exists('svg'):
    os.makedirs('svg')

if not os.path.exists('img'):
    os.makedirs('img')

for data in range(DataMin, DataMax + 1):
    qr.add_data('http://zhangxiaoyue.vip')
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('img/%d.png' % data)
    qr.clear()

    # 是否保存svg的二维码
    if saveSvg:
        img2 = qrcode.make(data, image_factory=factory)
        img2.save('svg/%d.svg' % data)
