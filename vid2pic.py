import cv2
import os
import sys

#display available video files in the folder "videos"
print(os.listdir(r"videos"))
if not os.listdir(r"videos"):
    sys.exit("the folder 'videos' does not contain any .mp4 files")

#make new folder frames, if it already exist then pass
os.makedirs(r"frames", exist_ok=True)
names = []

for file in os.listdir(r"videos"):
    if file.endswith(".mp4"):
        names.append(file[:-4])
        os.makedirs(f"frames\{file[:-4]}", exist_ok=True)
print(names)


for n in names:
    name = n
    cap = cv2.VideoCapture(f"videos\{name}.mp4")
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret: break
        cv2.imwrite(f"frames/{name}/{name}{count:04d}.jpg", frame)
        count += 1

cap.release()