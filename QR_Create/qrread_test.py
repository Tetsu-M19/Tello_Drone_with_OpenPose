import cv2
import numpy as np

image_path = 'qrcode_flipback.png'

### test ###
font = cv2.FONT_HERSHEY_SIMPLEX

def function_qrdec_cv2(img_bgr):

    # QRCodeDetectorインスタンス生成
    qrd = cv2.QRCodeDetector()

    # QRコードデコード
    retval, decoded_info, points, straight_qrcode = qrd.detectAndDecodeMulti(img_bgr)

    if retval:
        points = points.astype(np.int)

        dec_inf_list = []

        for dec_inf, point in zip(decoded_info, points):
            if dec_inf == '':
                continue

            # QRコード座標取得
            x = point[0][0]
            y = point[0][1]

            # QRコードデータ
            print('dec:', dec_inf)
            img_bgr = cv2.putText(img_bgr, dec_inf, (x, y-6), font, .3, (0, 0, 255), 1, cv2.LINE_AA)

            dec_inf_list.append(dec_inf)

            # バウンディングボックス
            img_bgr = cv2.polylines(img_bgr, [point], True, (0, 255, 0), 1, cv2.LINE_AA)
            
    if 'flip' in dec_inf_list and 'back' in dec_inf_list:
        print(dec_inf_list)

    cv2.imshow('image', img_bgr)
    cv2.waitKey(0)

img_BGR = cv2.imread(image_path, cv2.IMREAD_COLOR)
function_qrdec_cv2(img_BGR)