import cv2 as cv
import os
import numpy as np

DATA_DIR = "D:/face_rec/face_rec_CF/face_data"

faces = []
labels = []
label_map = {}
current_id = 0

for person in os.listdir(DATA_DIR):
    person_path = os.path.join(DATA_DIR, person)

    if not os.path.isdir(person_path):
        continue

    label_map[current_id] = person

    for image_name in os.listdir(person_path):
        image_path = os.path.join(person_path, image_name)

        img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

        if img is None:
            continue

        faces.append(img)
        labels.append(current_id)

    current_id += 1

recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))

recognizer.save("trainer.yml")

with open("labels.txt", "w") as f:
    for k, v in label_map.items():
        f.write(f"{k},{v}\n")

print("Training complete!")