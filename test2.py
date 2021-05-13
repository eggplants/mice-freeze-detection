import cv2

cap = cv2.VideoCapture("contextA.avi")
wait_secs = int(1000 / cap.get(cv2.CAP_PROP_FPS))

model = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    mask = model.apply(frame)
    # 背景の画素は黒 (0, 0, 0) にする。
    frame[mask == 0] = 0

    cv2.imshow("Frame (Only Forground)", frame)
    cv2.waitKey(wait_secs)

cap.release()
cv2.destroyAllWindows()
