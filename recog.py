# This is the main branch where the final version of the code will be merged into after revision
import cv2
import sys
import pickle
import face_recognition
import numpy as np

def main():
    """
    This program utilizes openCV/cv2 and face_recognition libraries to capture 
    and recognize students' faces via a webcam. Strict tolerance is enforced 
    to reduce false positives for unrecognized faces.
    """
    
    # ADJUST STRICTNESS HERE: Lower value = stricter matching (fewer false positives)
    # 0.6 is default. 0.45 is strict. 0.40 is extremely strict.
    STRICT_TOLERANCE = 0.40

    # 1. Load the known face encodings and names from the pickle file
    try:
        with open("face_encodings.pickle", "rb") as f:
            known_data = pickle.load(f)
        known_encodings = known_data["encodings"]
        known_names = known_data["names"]
        print(f"Successfully loaded {len(known_names)} known face(s).")
    except FileNotFoundError:
        sys.exit("ERROR: 'face_encodings.pickle' file not found. Please ensure it is in the same directory.")
    except Exception as e:
        sys.exit(f"ERROR: Could not load pickle file. {e}")

    # 2. Initialize live camera 
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        sys.exit("ERROR: Could not open webcam.")

    while True:
        ret, frame = cap.read()
        if not ret:
            sys.exit("ERROR: Something went wrong while trying to capture your webcam.")
        
        # 3. Process the frame for face recognition
        # Convert image from BGR (OpenCV default) to RGB (face_recognition default)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find all faces and their encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        # Loop through each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            
            # Default state: Assume the person is "Unknown" (Red bounding box)
            name = "Unknown"
            color = (0, 0, 255)  
            
            # Calculate exact Euclidean face distances to our database
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            
            if len(face_distances) > 0:
                # Find the index of the absolute closest matching face
                best_match_index = np.argmin(face_distances)
                shortest_distance = face_distances[best_match_index]
                
                # Check if the closest face passes our custom strict tolerance threshold
                if shortest_distance <= STRICT_TOLERANCE:
                    name = known_names[best_match_index]
                    color = (0, 255, 0)  # Green color for verified match
                    
                    # Optional console log to help you fine-tune the system:
                    print(f"Matched {name} with distance: {shortest_distance:.4f}")
            
            # 4. Draw box and write the name on top of the rectangle
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Write the name (or "Unknown") 10 pixels above the box
            cv2.putText(
                frame, 
                name, 
                (left, top - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, 
                color, 
                2, 
                cv2.LINE_AA
            )
            
        # Display the video frame
        cv2.imshow("Camera", frame)
        
        # Break the loop when "q" is pressed
        if cv2.waitKey(1) == ord("q"):
            break
    
    # Clean up resources
    cap.release()
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main()