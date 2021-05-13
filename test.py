import cv2
import numpy as np

class VideoFrameIsEmpty(Exception):
    pass


def load_video(path: str) -> cv2.VideoCapture:
    "load video to OpenCV"
    def get_frame_length(video: cv2.VideoCapture) -> float:
        "get number of frame in video"
        return video.get(cv2.CAP_PROP_FRAME_COUNT)

    video = cv2.VideoCapture(path)
    if get_frame_length(video) == 0:
        raise VideoFrameIsEmpty
    else:
        return video


def get_frame_length(video: cv2.VideoCapture) -> float:
    "get video size as number of frames"
    return video.get(cv2.CAP_PROP_FRAME_COUNT)


def each_cons(arr: list, n: int) -> list:
    "Ruby Array#each_cons(n)"
    return [arr[i:i+n] for i in range(len(arr)-n+1)]


def xor_image(im1: np.ndarray, im2: np.ndarray) -> np.ndarray:
    "xor 2 images"
    return cv2.bitwise_xor(im1, im2)


def show_image(image: np.ndarray, window_name: str) -> None:
    "open window and show image"
    cv2.imshow(window_name, image)

def count_moved_dots(frames: np.ndarray) -> list:
    moved_dots = []    
    for fr in frames:
        cnt = 0
        for dots in fr:
            cnt += sum(1 if x != [0, 0, 0] else 0 for x in dots.tolist())
            
        moved_dots.append(cnt)

    return moved_dots


def main():
    PATH = './contextA.avi'
    video = load_video(PATH)
    frames = []
    wait_sec = int(1000 / video.get(cv2.CAP_PROP_FPS))
    video_len = get_frame_length(video)
    show = False
    if input("show windows?(if wanna show {} frames, type 'y')".format(video_len)).rstrip() == 'y':
        show = True

    # MOG - a background substract algorithm (from opencv-contrib)
    # See: http://personal.ee.surrey.ac.uk/Personal/R.Bowden/publications/avbs01/avbs01.pdf
    # Also: https://docs.opencv.org/master/d6/da7/classcv_1_1bgsegm_1_1BackgroundSubtractorMOG.html

    model = cv2.bgsegm.createBackgroundSubtractorMOG()
    while True:
        ret, frame = video.read()
        if not ret:
            break

        mask = model.apply(frame)
        frame[mask == 0] = 0
        frames.append(frame)
        if show:
            show_image(frame, "masked frame")
            cv2.waitKey(wait_sec)

    cv2.destroyAllWindows()

    # useless???
    # measure moving again
    xor_frames = []
    video.release()
    for x, y in each_cons(frames, 2):
        f = xor_image(x, y)
        xor_frames.append(f)
        if show:
            show_image(f, "xored frame")
            cv2.waitKey(wait_sec)

    c = count_moved_dots(xor_frames)

    print(len(c))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

    cv2.destroyAllWindows()
