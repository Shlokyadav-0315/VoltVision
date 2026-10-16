import cv2

cam = cv2.VideoCapture(0)      # 0 = default webcam
ok, frame = cam.read()         # take one photo
cam.release()

if ok:
    cv2.imwrite("test.jpg", frame)
    print("Saved test.jpg")
else:
    print("Could not read the camera")