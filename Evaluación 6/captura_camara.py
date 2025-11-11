import cv2
from procesador import procesar_imagen, registrar_placa

# Iniciar camara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se puede abrir la cámara.")
    exit()

print("\n--- Reconocimiento de Placas ---")
print("Presiona 'c' para capturar y procesar la imagen.")
print("Presiona 'q' para salir.")
print("----------------------------------\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar frame.")
        break

    # Mostrar video
    cv2.imshow('Camara - (c) capturar (q) salir', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        print("Procesando...")
        placa_detectada = procesar_imagen(frame)
        
        if placa_detectada:
            print(f"Placa detectada: {placa_detectada}")
            registrar_placa(placa_detectada)
            
            # Mostrar la placa detectada en el frame
            cv2.putText(frame, placa_detectada, (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            cv2.imshow('Placa Detectada', frame)
        else:
            print("No se detectó una placa clara.")

    elif key == ord('q'):
        print("Saliendo...")
        break

# Limpieza
cap.release()
cv2.destroyAllWindows()