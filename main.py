import cv2
import numpy as np
import tensorflow as tf

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(
    model_path="model/model_unquant.tflite"
)
interpreter.allocate_tensors()

# Get model input/output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load labels
with open("model/labels.txt", "r") as f:
    class_names = [line.strip().split(" ", 1)[1] for line in f.readlines()]

# Open webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Resize image to model input size
    img = cv2.resize(frame, (224, 224))

    # Convert to float32
    img = np.asarray(img, dtype=np.float32)

    # Normalize (-1 to 1)
    img = (img / 127.5) - 1

    # Add batch dimension
    img = np.expand_dims(img, axis=0)

    # Run inference
    interpreter.set_tensor(
        input_details[0]["index"],
        img
    )

    interpreter.invoke()

    prediction = interpreter.get_tensor(
        output_details[0]["index"]
    )

    index = np.argmax(prediction)
    confidence = float(prediction[0][index])

    index = np.argmax(prediction)
    confidence = float(prediction[0][index])

    if confidence < 0.90:
        class_name = "Unknown"
    else:
        class_name = class_names[index]

    text = f"{class_name} ({confidence:.2f})"

    cv2.putText(
        frame,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Face Recognition", frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()