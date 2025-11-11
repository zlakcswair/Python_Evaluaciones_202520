import cv2
import pytesseract
import datetime
import re

# Dejamos la ruta, ya sabemos que es importante
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def procesar_imagen(imagen):
    # Pasos de procesamiento
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    filtro = cv2.GaussianBlur(gris, (5, 5), 0)
    
    config_linea = '--psm 7' # Una linea
    config_bloque = '--psm 6' # Un bloque

    # --- INTENTO 1: ADAPTIVE (31, 5) - SIN LANG ---
    # (Parámetros (31, 5) en lugar de (11, 2) que generaban ruido)
    print("Intento 1: Adaptativo (31,5) / psm 6")
    umbral_adaptativo1 = cv2.adaptiveThreshold(filtro, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 5)
    
    # --- CAMBIO IMPORTANTE ---
    # Usamos config_bloque en lugar de config_linea
    texto_adaptativo1 = pytesseract.image_to_string(umbral_adaptativo1, config=config_bloque)
    
    print(f"Texto crudo: '{texto_adaptativo1}'")
    placa_adaptativa1 = re.sub(r'[^A-Z0-9]', '', texto_adaptativo1).upper()
    
    match_adaptativo1 = re.search(r'[A-Z]{3}[0-9]{3}', placa_adaptativa1)
    if match_adaptativo1:
        placa_final = match_adaptativo1.group(0)
        print(f"Detectado con Adaptativo (31,5): {placa_final}")
        return placa_final, umbral_adaptativo1

    # --- INTENTO 2: ADAPTIVE INVERTIDO (31, 5) - SIN LANG ---
    print("Intento 1 falló. Intento 2: Adaptativo INV (31,5) / psm 6")
    umbral_adaptativo_inv1 = cv2.adaptiveThreshold(filtro, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 5)

    # --- CAMBIO IMPORTANTE ---
    # Usamos config_bloque en lugar de config_linea
    texto_adaptativo_inv1 = pytesseract.image_to_string(umbral_adaptativo_inv1, config=config_bloque)

    print(f"Texto crudo: '{texto_adaptativo_inv1}'")
    placa_adaptativa_inv1 = re.sub(r'[^A-Z0-9]', '', texto_adaptativo_inv1).upper()

    match_adaptativo_inv1 = re.search(r'[A-Z]{3}[0-9]{3}', placa_adaptativa_inv1)
    if match_adaptativo_inv1:
        placa_final = match_adaptativo_inv1.group(0)
        print(f"Detectado con Adaptativo INV (31,5): {placa_final}")
        return placa_final, umbral_adaptativo_inv1

    # --- INTENTO 3: OTSU (Para placa1.jpg) - SIN LANG ---
    print("Intento 2 falló. Intento 3: Otsu / psm 6")
    ret, umbral_otsu = cv2.threshold(filtro, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Este es el que funcionó para placa1.jpg
    texto_otsu = pytesseract.image_to_string(umbral_otsu, config=config_bloque)

    print(f"Texto crudo: '{texto_otsu}'")
    placa_otsu = re.sub(r'[^A-Z0-9]', '', texto_otsu).upper()

    match_otsu = re.search(r'[A-Z]{3}[0-9]{3}', placa_otsu)
    if match_otsu:
        placa_final = match_otsu.group(0)
        print(f"Detectado con Otsu: {placa_final}")
        return placa_final, umbral_otsu

    # Si todos fallan
    print("Todos los métodos fallaron.")
    # Devolvemos el primer umbral (adaptativo) solo para depuración
    return None, umbral_adaptativo1


def registrar_placa(placa):
    try:
        # Modo 'a' para agregar al final (append)
        with open('placas.csv', 'a', newline='') as f:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            
            # Escribir la nueva línea
            f.write(f"{timestamp},{placa}\n")
            print(f"Registro guardado: {placa}")
            
    except IOError:
        print("Error al escribir en el archivo.")

# Simple chequeo al iniciar
try:
    with open('placas.csv', 'a') as f:
        if f.tell() == 0:
            # Archivo nuevo, escribir encabezado
            f.write('FechaHora,PlacaDetectada\n')
except IOError:
    print("No se pudo crear o verificar placas.csv")