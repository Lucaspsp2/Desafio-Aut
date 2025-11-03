import os
import time
from datetime import datetime

def start_recording(driver):
    """
    Inicia gravação de vídeo da sessão Appium.
    """
    try:
        driver.start_recording_screen()
        print("🎥 Iniciando gravação de vídeo...")
    except Exception as e:
        print(f"⚠️ Falha ao iniciar gravação: {e}")

def stop_recording(driver, product_name, save_on_error=False):
    """
    Para gravação e salva ou descarta conforme o resultado.
    """
    try:
        raw_data = driver.stop_recording_screen()

        # Cria pasta logs/videos se não existir
        os.makedirs("logs/videos", exist_ok=True)

        if save_on_error:
            # Timestamp único pra não sobrescrever
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            safe_name = "".join(c if c.isalnum() else "_" for c in product_name)
            file_path = f"logs/videos/{safe_name}_{timestamp}.mp4"
            with open(file_path, "wb") as f:
                import base64
                f.write(base64.b64decode(raw_data))
            print(f"💾 Vídeo salvo em: {file_path}")
        else:
            print("🧹 Teste passou — vídeo descartado.")

    except Exception as e:
        print(f"⚠️ Falha ao encerrar gravação: {e}")

