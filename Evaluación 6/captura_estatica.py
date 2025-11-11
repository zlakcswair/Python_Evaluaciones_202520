import cv2
from procesador import procesar_imagen, registrar_placa

# --- CAMBIA ESTO PARA PROBAR LAS 3 ---
# nombre_archivo = 'placa1.jpg' 
# nombre_archivo = 'placa2.jpg'
nombre_archivo = 'placa4.jpg'
# -------------------------------------

print(f"Procesando imagen '{nombre_archivo}'...")
imagen = cv2.imread(nombre_archivo)

# La función ahora devuelve dos cosas: la placa (o None) y la imagen B/N
placa, imagen_depuracion = procesar_imagen(imagen)

# Mostramos la imagen B/N que usó Tesseract
cv2.imshow('Imagen B/N para OCR', imagen_depuracion)

if placa:
    print(f"Placa detectada: {placa}")
    registrar_placa(placa)
    
    cv2.putText(imagen, placa, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
    cv2.imshow('Imagen Procesada', imagen)
else:
    print("No se pudo detectar una placa en la imagen.")
    cv2.imshow('Imagen Original (Fallo)', imagen)

# Pausa para ver los resultados
cv2.waitKey(0)
cv2.destroyAllWindows()