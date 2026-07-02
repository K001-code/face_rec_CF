import face_recognition
import os
import pickle


# Path to the folder containing sub-folders of images
dataset_path = r"frames"
known_encodings = []
known_names = []

# Loop through each person's folder
for person_name in os.listdir(dataset_path):
    person_dir = os.path.join(dataset_path, person_name)
    if not os.path.isdir(person_dir):
        continue
        
    # Loop through each image in the person's folder
    for image_name in os.listdir(person_dir):
        image_path = os.path.join(person_dir, image_name)
        
        # Load and encode the face
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        # Make sure a face was found in the image
        if len(face_encodings) > 0:
            known_encodings.append(face_encodings[0])
            known_names.append(person_name)
            print(f"Encoded: {image_name} for {person_name}")

# Save the encodings and names to a file
data = {"encodings": known_encodings, "names": known_names}
with open("face_encodings.pickle", "wb") as f:
    pickle.dump(data, f)

print("Encoding complete and saved to face_encodings.pickle")
