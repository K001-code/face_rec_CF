#This is the main branch where the final version of the code will be merged into after revision
import cv2, sys

def main():
    """
    This program utalizes the openCV/cv2 open Python library to capture, recognize student's face via a webcam.
    Once a student's face is detected in the trained data, we can automatically update a spreadsheet that contains all the students' attendance status.
    """
<<<<<<< HEAD
    while True:
        ret, frame = webCam()
=======
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        # 0, 1 
>>>>>>> 21169f4130c8e4e5fa6b5787b3a8976476fbd48d
        if not ret:
            sys.exit("ERROR: Something went wrong while trying to capture your webcam.")
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) == ord("q"):
            break
<<<<<<< HEAD
    drawRect(frame)
=======
    cap.release()
    cv2.destroyAllWindows()
        
    # drawRect(frame)
>>>>>>> 21169f4130c8e4e5fa6b5787b3a8976476fbd48d
    
    return 0


def drawRect(frame):
    #your code here
    return

if __name__ == "__main__":
    main()
