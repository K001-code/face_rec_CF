 #This is the main branch where the final version of the code will be merged into after revision
import cv2, sys

def cdmain():
    """
    This program utalizes the openCV/cv2 open Python library to capture, recognize student's face via a webcam.
    Once a student's face is detected in the trained data, we can automatically update a spreadsheet that contains all the students' attendance status.
    """
    ret, frame = webCam()
    if not ret:
        sys.exit("ERROR: Something went wrong while trying to capture your webcam.")
    drawRect(frame)
    
    return 0


def webCam():
    cap = cv2.VideoCapture(0)
    return cap.read()

def drawRect(frame):
    #your code here
    return

if __name__ == "__main__":
    main()
#fndjssjfbdsjfdsf