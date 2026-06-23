import cv2 as cv
import sys 

def main() :
    c = cv.VideoCapture(0)

    def draw(f):
        gray = cv.cvtColor(f, cv.COLOR_BGR2GRAY)

        face = cv.CascadeClassifier(
            cv.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        faces = face.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            cv.rectangle(f, (x, y), (x+w, y+h), (0, 0, 255), 2)

    while True:
        r, f = c.read()

        if not r:
            break

        draw(f)

        cv.imshow("Webcam", f)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    c.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
