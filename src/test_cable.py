import cv2
import numpy as np
from cv2 import bgsegm_BackgroundSubtractorMOG as MOG

# memo:
# // 白黒輪郭画像の内でランダムサンプリング
# mask = []
# white_pixs = extract_white_pixs(binary_image)
# for _ in range(N):
#   # *_seg = [[seg1の座標たち], [seg2の座標たち], ..., [segnの座標たち]]
#   white_seg, black_seg = detect_surround_segments(white_pixs[rand], rad)
# 　# 連結成分の大きさでfilterする必要
# if len(white_seg) == 1 and len(black_seg) == 2:  # ・・・ケーブルなので白部分のピクセルをマスクに入れる
#     for i in white_seg:
#       mask.extends(i)

np.set_printoptions(threshold=np.inf)

VIDEO_PATH = '../videos/test_cable_short.avi'

cap = cv2.VideoCapture(VIDEO_PATH)
wait_sec = int(1000 / cap.get(cv2.CAP_PROP_FPS))
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


frames = []
res, frame = cap.read()
model: MOG = cv2.bgsegm.createBackgroundSubtractorMOG()
ind = 2
while res:
    ind += 1
    print('{}/{}'.format(ind, length), end='\r')
    mask = model.apply(frame)
    frame[mask == 0] = 0
    frames.append(frame)
    res, frame = cap.read()

print()

# for ind, frame in enumerate(frames):
#     # cv2.imshow('hai', frame)
#     # cv2.waitKey(1000)
#     d1, d2, d3 = frame.shape
#     if ind == 6:

f = frame[6]
white_pixs = np.argwhere(f != [0, 0, 0])
white_pixs = np.unique(white_pix[:, [0, 1]], axis=0)


def get_crop_rect(cnt_x, cnt_y, size):
    # box = (left, upper, right, lower)
    return (cntx-size, cnt_y+size, cntx+size, cnt_y-size)
