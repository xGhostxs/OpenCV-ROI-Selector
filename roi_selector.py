import cv2
import numpy as np

drawing = False
start_point = None
end_point = None
roi_defined = False

def draw_rectangle(event, x, y, flags, param):
    global drawing, start_point, end_point, roi_defined

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
        end_point = None
        roi_defined = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        roi_defined = True

cap = cv2.VideoCapture(0)
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', draw_rectangle)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if start_point and end_point:
        cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)

    if roi_defined and start_point and end_point:
        x1, y1 = start_point
        x2, y2 = end_point
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        selected_region = frame[y1:y2, x1:x2]
        if selected_region.size > 0:
            cv2.imshow("Selected Region", selected_region)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
