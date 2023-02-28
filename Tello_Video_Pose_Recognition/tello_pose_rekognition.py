import socket
import threading
import cv2
import time
import numpy as np
from tello_pose import Tello_Pose
from VideoCapture import VideoCapture


# データ受け取り用の関数
def udp_receiver():
    global battery_text
    global time_text
    global status_text

    while True: 
        try:
            data, server = sock.recvfrom(1518)
            resp = data.decode(encoding="utf-8").strip()
            # レスポンスが数字だけならバッテリー残量
            if resp.isdecimal():    
                battery_text = "Battery:" + resp + "%"
            # 最後の文字がsなら飛行時間
            elif resp[-1:] == "s":
                time_text = "Time:" + resp
            else: 
                status_text = "Status:" + resp
        except:
            pass

# 問い合わせ
def ask():
    while True:
        try:
            sock.sendto('battery?'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
        time.sleep(1)

        try:
            sock.sendto('time?'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
        time.sleep(1)


# 離陸
def takeoff():
    try:
        sock.sendto('takeoff'.encode(encoding="utf-8"), TELLO_ADDRESS)
    except:
        pass
# 着陸
def land():
    try:
        sock.sendto('land'.encode(encoding="utf-8"), TELLO_ADDRESS)
    except:
        pass
# 上昇(cm)
def up(distance):
    try:
        sock.sendto(f'up {str(distance)}'.encode(encoding="utf-8"), TELLO_ADDRESS)
        # print("上昇")
    except:
        pass
# 下降(cm)
def down(distance):
    try:
        sock.sendto(f'down {str(distance)}'.encode(encoding="utf-8"), TELLO_ADDRESS)
        # print("下降")
    except:
        pass
# 前に進む(cm)
def forward(distance):
    try:
        sock.sendto(f'forward {str(distance)}'.encode(encoding="utf-8"), TELLO_ADDRESS)
        # print("前に進む")
    except:
        pass
# 後に進む(cm)
def back(distance):
    try:
        sock.sendto(f'back {str(distance)}'.encode(encoding="utf-8"), TELLO_ADDRESS)
        # print("後ろへ進む")
    except:
        pass
# 右に進む(cm)
def right(distance):
    try:
        sock.sendto(f'right {str(distance)}'.encode(encoding="utf-8"), TELLO_ADDRESS)
        # print("右に進む")
    except:
        pass
# 左に進む(cm)
def left(distance):
    try:
        sock.sendto(f'left {str(distance)}'.encode(encoding="utf-8"), TELLO_ADDRESS)
        # print("左に進む")
    except:
        pass
# 右回りに回転(deg)
def cw(degree):
        try:
            sock.sendto(f'cw {str(degree)}'.encode(encoding="utf-8"), TELLO_ADDRESS)
            # print("右回り")
        except:
            pass
# 左回りに回転(deg)
def ccw(degree):
    try:
        sock.sendto(f'ccw {str(degree)}'.encode(encoding="utf-8"), TELLO_ADDRESS)
        # print("左回り")
    except:
        pass

def flipback():
    try:
        sock.sendto(f'flip b'.encode(encoding="utf-8"), TELLO_ADDRESS)
    except:
        pass

def flipforward():
    try:
        sock.sendto(f'flip f'.encode(encoding="utf-8"), TELLO_ADDRESS)
    except:
        pass

def detect_max_object(img):

    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img)

    maxSize = 800

    try:
        for i in range(1, nlabels):
            if stats[i][4] > maxSize:
                maxSize = stats[i][4]
                maxNumber = i

        return stats[maxNumber], centroids[maxNumber]

    except:
        pass


def detect_color(img):    

    try:
        # HSV色空間に変換
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hsv = cv2.bilateralFilter(hsv, 5, 50, 100)  
        
        # 緑色のHSVの値域1
        # hsv_min = np.array([30, 64, 80])
        # hsv_max = np.array([70, 100, 100])
        hsv_min = np.array([30,64,30])
        hsv_max = np.array([90,255,255])
        
        # 緑色領域のマスク
        imgMask = cv2.inRange(hsv, hsv_min, hsv_max)
        
        stats, centroid = detect_max_object(imgMask)

        # マスキング処理
        imgMasking = cv2.bitwise_and(img, img, mask=imgMask)

        return imgMasking, stats, centroid

    except:
        pass

font = cv2.FONT_HERSHEY_SIMPLEX

def function_qrdec_cv2(img_bgr):
    try:
        # QRCodeDetectorインスタンス生成
        qrd = cv2.QRCodeDetector()
        
        dec_inf_list = ['None']

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
                # print('dec:', dec_inf)
                img_bgr = cv2.putText(img_bgr, dec_inf, (x, y-6), font, .3, (0, 0, 255), 1, cv2.LINE_AA)

                # バウンディングボックス
                img_bgr = cv2.polylines(img_bgr, [point], True, (0, 255, 0), 1, cv2.LINE_AA)

                if dec_inf_list[0] == 'None':
                    dec_inf_list[0] = dec_inf
                else:
                    dec_inf_list.append(dec_inf)

            # print(dec_inf)
            
        return img_bgr, dec_inf_list

    except:
        pass

    # cv2.imshow('image', img_bgr)
    # cv2.waitKey(0)

# Tello側のローカルIPアドレス(デフォルト)、宛先ポート番号(コマンドモード用)
TELLO_IP = '192.168.10.1'
# TELLO_IP = '10.17.44.12'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# Telloからの映像受信用のローカルIPアドレス、宛先ポート番号
TELLO_CAMERA_ADDRESS = 'udp://@0.0.0.0:11111'
# TELLO_CAMERA_ADDRESS = 'udp://@10.17.44.3:11111'

command_text = "None"
battery_text = "Battery:"
time_text = "Time:"
status_text = "Status:"
mode_text = "None"

# pose recognition
my_tello_pose = Tello_Pose()

# record the coordinates of the nodes in the pose recognition skeleton     
points = []
#list of all the possible connections between skeleton nodes        
POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]

# キャプチャ用のオブジェクト
cap = None

# データ受信用のオブジェクト備
response = None

# 通信用のソケットを作成
# ※アドレスファミリ：AF_INET（IPv4）、ソケットタイプ：SOCK_DGRAM（UDP）
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 自ホストで使用するIPアドレスとポート番号を設定
sock.bind(('', TELLO_PORT))

# 問い合わせスレッド起動
ask_thread = threading.Thread(target=ask)
ask_thread.setDaemon(True)
ask_thread.start()

# 受信用スレッドの作成
recv_thread = threading.Thread(target=udp_receiver, args=())
recv_thread.daemon = True
recv_thread.start()

# コマンドモード
sock.sendto('command'.encode('utf-8'), TELLO_ADDRESS)

time.sleep(1)

# カメラ映像のストリーミング開始
sock.sendto('streamon'.encode('utf-8'), TELLO_ADDRESS)

time.sleep(1)

if cap is None:
    cap = VideoCapture(TELLO_CAMERA_ADDRESS)

if not cap.isOpened():
    cap.isOpened()

markerChaseFlag = False
poseRecognitionFlag = False
qrDetectFlag = False

maxFrames = 0
numDiffTime = 0
fps = 0

while True:

    if maxFrames == 0:
        timeStart = time.time()

    frame = cap.read()

    # 動画フレームが空ならスキップ
    if frame is None:
        continue

    frame_height, frame_width = frame.shape[:2]
    # frame = cv2.resize(frame, (int(frame_width/2), int(frame_height/2)))


    ##### マーカ追跡モード #####
 
    if markerChaseFlag:
        try:
            _, objectStats, objectCentroid = detect_color(frame)

            objectCenter_x = int((objectStats[0] * 2 + objectStats[2]) / 2)
            objectCenter_y = int((objectStats[1] * 2 + objectStats[3]) / 2)

            objectSize = objectStats[4]

            x0 = objectStats[0]
            y0 = objectStats[1]
            x1 = objectStats[0] + objectStats[2]
            y1 = objectStats[1] + objectStats[3]
            cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 255), thickness=3)

            correctArea_x0 = int(frame_width / 2 - 100)
            correctArea_y0 = int(frame_height / 2 - 100)
            correctArea_x1 = int(frame_width / 2 + 100)
            correctArea_y1 = int(frame_height / 2 + 100)
            cv2.rectangle(frame, (correctArea_x0, correctArea_y0), (correctArea_x1, correctArea_y1), (0, 255, 0), thickness=3)

            cv2.circle(frame, (int(objectCenter_x), int(objectCenter_y)), 3, (255, 255, 255), thickness=3)


            # ブジェクトが画像の左側に位置していたら、反時計回りに旋回する
            if objectCenter_x < correctArea_x0:
                ccw(3)
                command_text = "ccw"
            # オブジェクトが画像の右側に位置していたら、時計回りに旋回する
            elif objectCenter_x > correctArea_x1:
                cw(3)
                command_text = "cw"
            # オブジェクトが画像の上側に位置していたら、上昇する
            elif objectCenter_y < correctArea_y0:
                up(20)
                command_text = "up"
            # オブジェクトが画像の下側に位置していたら、下降する
            elif objectCenter_y > correctArea_y1:
                down(20)
                command_text = "down"
            # オブジェクトの面積が小さい場合、前進する
            elif objectSize < 10000:
                forward(20)
                command_text = "Forward"
            # オブジェクトの面積が大きい場合、後進する
            elif objectSize > 30000:
                back(20)
                command_text = "Back"

        except:
            command_text = "None"
            pass

    ##### ポーズ推測モード #####

    elif poseRecognitionFlag:

        # smoothing filter
        poseFrame = cv2.bilateralFilter(frame, 5, 50, 100)  

        points.append(None)               
        # process pose-recognition                
        cmd_pose, draw_skeleton_flag, points = my_tello_pose.detect(poseFrame)

        for i in range(15):
            if draw_skeleton_flag == True:
                cv2.circle(frame, points[i], 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.putText(frame, "{}".format(i), points[i], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,lineType=cv2.LINE_AA)       
        # Draw Skeleton
        for pair in POSE_PAIRS:
            partA = pair[0]
            partB = pair[1]
            if points[partA] and points[partB]:
                cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2)
                cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
        
        # print(f"cmd:{cmd_pose}")

        if cmd_pose == 'flipback':
            flipback()
            command_text = 'flipback'
        elif cmd_pose == 'flipforward':
            flipforward()
            command_text = 'flipforward'
        elif cmd_pose == 'land':
            land()
            command_text = 'land'

    ##### QRコード検知モード ######
        
    elif qrDetectFlag:
        frame, cmd_qr= function_qrdec_cv2(frame)

        # print(cmd_qr)

        if len(cmd_qr) == 1 and 'back' in cmd_qr:
            back(20)
            command_text = 'back'

        elif 'flip' in cmd_qr and 'back' in cmd_qr:
            flipback()
            command_text = 'flipback'


    maxFrames += 1

    if maxFrames == 30:
        timeEnd = time.time()
        diffTime = timeEnd - timeStart
        # print(f"経過時間：{diffTime}")
        fps = maxFrames / diffTime
        maxFrames = 0

    # 送信したコマンドを表示
    cv2.putText(frame,
            text="Cmd:" + command_text,
            org=(10, 20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=1,
            lineType=cv2.LINE_4)
    # バッテリー残量を表示
    cv2.putText(frame,
            text=battery_text,
            org=(10, 40),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=1,
            lineType=cv2.LINE_4)
    # 飛行時間を表示
    cv2.putText(frame,
            text=time_text,
            org=(10, 60),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=1,
            lineType=cv2.LINE_4)
    # ステータスを表示
    cv2.putText(frame,
            text=status_text,
            org=(10, 80),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=1,
            lineType=cv2.LINE_4)
    # modeを表示
    cv2.putText(frame,
            text="Mode:" + mode_text,
            org=(10, 100),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=1,
            lineType=cv2.LINE_4)
     # fpsを表示
    cv2.putText(frame,
            text="fps:" + str(int(fps)),
            org=(10, 120),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=1,
            lineType=cv2.LINE_4)
    

    # カメラ映像を画面に表示
    cv2.imshow('Tello Camera View', frame)

    # キー入力を取得
    key = cv2.waitKey(10)

    # qキーで着陸して終了
    if key == ord('q'):
        land()
        break
    # wキーで前進
    elif key == ord('w'):
        forward(20)
        command_text = "Forward"
    # sキーで後進
    elif key == ord('s'):
        back(20)
        command_text = "Back"
    # aキーで左進
    elif key == ord('a'):
        left(20)
        command_text = "Left"
    # dキーで右進
    elif key == ord("d"):
        right(20)
        command_text = "Right"
    # jキーで離陸
    elif key == ord('j'):
        takeoff()
        command_text = "Take off"
    # kキーで着陸
    elif key == ord('k'):
        land()
        command_text = "Land"
    # hキーで上昇
    elif key == ord('h'):
        up(20)
        command_text = "Up"
    # lキーで下降
    elif key == ord('l'):
        down(20)
        command_text = "Down"
    # uキーで左回りに回転
    elif key == ord('u'):
        ccw(20)
        command_text = "Ccw"
    # iキーで右回りに回転
    elif key == ord('i'):
        cw(20)
        command_text = "Cw"
    elif key == ord('m'):
        markerChaseFlag = not bool(markerChaseFlag)
        if markerChaseFlag:
            mode_text = "marker chase mode"
        else:
            mode_text = "None"
    elif key == ord('p'):
        poseRecognitionFlag = not bool(poseRecognitionFlag)
        if poseRecognitionFlag:
            mode_text = "pose recognition mode"
        else:
            mode_text = "None"
    elif key == ord('c'):
        qrDetectFlag = not bool(qrDetectFlag)
        if qrDetectFlag:
            mode_text = "qr code detect mode"
        else:
            mode_text = "None"


del VideoCapture
cv2.destroyAllWindows()

# ビデオストリーミング停止
sock.sendto('streamoff'.encode('utf-8'), TELLO_ADDRESS)
