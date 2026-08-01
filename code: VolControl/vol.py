import glob
import time
import subprocess
import serial

BAUDIOS = 115200
ultimo = -1


def buscar_puerto():
    puertos = sorted(glob.glob("/dev/ttyACM*"))
    if not puertos:
        puertos = sorted(glob.glob("/dev/ttyUSB*"))
    return puertos[0] if puertos else None


while True:
    puerto = buscar_puerto()

    if puerto is None:
        print("Esperando ESP32...")
        time.sleep(1)
        continue

    try:
        print(f"Conectado a {puerto}")

        ser = serial.Serial(puerto, BAUDIOS, timeout=1)

        # Esperar a que el ESP32 termine de iniciar
        time.sleep(2)
        ser.reset_input_buffer()

        while True:
            linea = ser.readline().decode(errors="ignore").strip()

            if not linea:
                continue

            try:
                volumen = int(linea)
            except ValueError:
                continue

            volumen = max(0, min(100, volumen))

            if abs(volumen - ultimo) >= 2:
                subprocess.run(
                    [
                        "wpctl",
                        "set-volume",
                        "@DEFAULT_AUDIO_SINK@",
                        f"{volumen}%"
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

                ultimo = volumen

    except (serial.SerialException, OSError):
        print("ESP32 desconectado.")
        try:
            ser.close()
        except:
            pass

        time.sleep(1)
