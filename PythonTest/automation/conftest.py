import os
import time
import pytest
from device import Device

# 1. Створюємо підключення ОДИН РАЗ на весь модуль (файл з тестами)
@pytest.fixture(scope="module")
def device_connection():
    port = os.getenv("DEVICE_PORT")
    if not port:
        pytest.skip("Set DEVICE_PORT, e.g. COM5, /dev/ttyUSB0 or rfc2217://localhost:4000 (Wokwi)")
    
    dev = Device(port, timeout=1.0)
    yield dev
    
    # Закриваємо порт лише тоді, коли всі тести у файлі завершилися
    dev.close()

# 2. Автоматично скидаємо стан Wokwi перед та після кожного тесту
@pytest.fixture(autouse=True)
def auto_reset_device(device_connection):
    # Виконується ПЕРЕД кожним тестом
    try:
        device_connection.command("RESET")
        time.sleep(0.5)  # Пауза, щоб мікроконтролер встиг перезавантажитися
    except Exception as e:
        pytest.fail(f"Failed to reset device before test: {e}")
        
    yield
    
    # Виконується ПІСЛЯ кожного тесту
    try:
        device_connection.command("RESET")
    except Exception:
        pass  # Ігноруємо помилки очищення, щоб не ховати основні помилки тесту

# 3. Фікстура-прослойка для сумісності (щоб ваші тести не довелося переписувати)
@pytest.fixture
def device(device_connection):
    return device_connection


# import os
# import pytest
# from device import Device

# @pytest.fixture
# def device():
#     port = os.getenv("DEVICE_PORT")
#     if not port:
#         pytest.skip("Set DEVICE_PORT, e.g. COM5, /dev/ttyUSB0 or rfc2217://localhost:4000 (Wokwi)")
#     dev = Device(port, timeout=1.0)
#     yield dev
#     try:
#         dev.command("RESET")
#     finally:
#         dev.close()
