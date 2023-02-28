import pyqrcode as qrcode
import cv2
import numpy as np
from PIL import Image
# from qrcode.image.styledpil import StyledPilImage

move_text = "flip"
FILE_PNG = f'qrcode_{move_text}.png'
image_path = FILE_PNG

# QRコード作成
code = qrcode.create(f'{move_text}', error='Q', version=3, mode='binary')
code.png(FILE_PNG, scale=10, module_color=[0, 0, 0, 120], background=[255, 255, 255])

qrImage = Image.open(image_path)
width, height = qrImage.size

# How big the logo we want to put in the qr code png
logo_size = 50

qrImage = qrImage.convert("RGBA")

logo = Image.open(f'{move_text}.png')

# Calculate xmin, ymin, xmax, ymax to put the logo
xmin = ymin = int((width / 2) - (logo_size / 2))
xmax = ymax = int((width / 2) + (logo_size / 2))

# resize the logo as calculated
logo = logo.resize((xmax - xmin, ymax - ymin))

# put the logo in the qr code
qrImage.paste(logo, (xmin, ymin, xmax, ymax))
qrImage.save(image_path)



### test ###
font = cv2.FONT_HERSHEY_SIMPLEX

def function_qrdec_cv2(img_bgr):

    # QRCodeDetectorインスタンス生成
    qrd = cv2.QRCodeDetector()

    # QRコードデコード
    retval, decoded_info, points, straight_qrcode = qrd.detectAndDecodeMulti(img_bgr)

    if retval:
        points = points.astype(np.int)

        for dec_inf, point in zip(decoded_info, points):
            if dec_inf == '':
                continue

            # QRコード座標取得
            x = point[0][0]
            y = point[0][1]

            # QRコードデータ
            print('dec:', dec_inf)
            img_bgr = cv2.putText(img_bgr, dec_inf, (x, y-6), font, .3, (0, 0, 255), 1, cv2.LINE_AA)

            # バウンディングボックス
            img_bgr = cv2.polylines(img_bgr, [point], True, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow('image', img_bgr)
    cv2.waitKey(0)

img_BGR = cv2.imread(image_path, cv2.IMREAD_COLOR)
function_qrdec_cv2(img_BGR)