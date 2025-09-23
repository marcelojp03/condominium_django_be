import cv2

#Usa 0 o 1 según cómo DroidCam esté configurado
cap = cv2.VideoCapture(1)  # Usa el índice correcto para DroidCam

while True:
    ret, frame = cap.read()
    if not ret:
        print(" No se pudo capturar imagen")
        break

    # Rotar el frame si está desfasado
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    cv2.imshow("DroidCam Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        cv2.imwrite("rostro.jpg", frame)
        print(" Imagen guardada como rostro.jpg")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




