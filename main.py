#This is the main branch where the final version of the code will be merged into after revision
import cv2, sys

def main():
    """
    This program utalizes the openCV/cv2 open Python library to capture, recognize student's face via a webcam.
    Once a student's face is detected in the trained data, we can automatically update a spreadsheet that contains all the students' attendance status.
    """

    #live camera 
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        # 0, 1 
        if not ret:
            sys.exit("ERROR: Something went wrong while trying to capture your webcam.")
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) == ord("q"):
            break
    
    cap.release()
    cv2.destroyAllWindows()

    #encoding
    


    # drawRect(frame)
    
    return 0


def drawRect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (1, 255, 1), 2)

    return

if __name__ == "__main__":
    main()
