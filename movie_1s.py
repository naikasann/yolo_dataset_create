import cv2
from os import makedirs, startfile
from os.path import splitext, dirname, basename, join
import os

foldername = "images"

def save_frames(video_path, startnumber=0, ext="jpg"):
    savenumber = startnumber

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return
    idx = 0
    while cap.isOpened():
        idx += 1
        ret, frame = cap.read()
        if ret:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == 1:  # 0秒のフレームを保存
                cv2.imwrite("/train/image_{}.{}".format(str(savenumber), ext),frame)
                savenumber += 1
            elif idx < cap.get(cv2.CAP_PROP_FPS):
                continue
            else:  # 1秒ずつフレームを保存
                second = int(cap.get(cv2.CAP_PROP_POS_FRAMES)/idx)
                filled_second = str(second).zfill(4)
                cv2.imwrite("/train/{}.{}".format(str(savenumber), ext),frame)
                savenumber += 1
                idx = 0
        else:
            break

    return savenumber

videoname = 0
videolist = os.listdir(foldername)
for video in videolist:
    videopath = os.path.join(foldername, video)
    videoname = save_frames(videopath, videoname)