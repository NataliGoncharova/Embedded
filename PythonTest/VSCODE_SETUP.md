# Запуск прошивок у VS Code

У цьому архіві є дві окремі PlatformIO-прошивки:

- `demo_firmware/` — справна демонстраційна прошивка.
- `homework_buggy/` — навчальна прошивка з навмисними дефектами.

## Налаштування
1. Встановіть VS Code.
2. У VS Code встановіть розширення **PlatformIO IDE**.
3. Відкрийте саме папку `demo_firmware` або `homework_buggy` — ту, в якій лежить `platformio.ini`.
4. Дочекайтеся встановлення платформи та бібліотеки DHTesp.
5. Виконайте PlatformIO: **Build**.
6. Для фізичної ESP32 підключіть плату й виконайте **Upload**. Для симуляції Wokwi встановіть розширення Wokwi, виконайте Build і запустіть симуляцію.
7. Serial Monitor: 115200 baud.

## Python-тести
У сусідній папці `automation` виконайте `python -m pip install -r requirements.txt`, потім задайте порт. Наприклад, у PowerShell: `$env:DEVICE_PORT="COM5"`. Запускайте тести з каталогу `automation`: `pytest -v`.

**Важливо:** не відкривайте той самий COM-порт одночасно в Serial Monitor і Python.

## Запуск Python-тестів проти Wokwi
Симуляція Wokwi не створює COM-порт у Windows. Натомість, поки симуляція запущена, її UART доступний за адресою `rfc2217://localhost:4000` (налаштовано в `wokwi.toml`).

1. Відкрийте `demo_firmware` (або `homework_buggy`) у VS Code, виконайте **PlatformIO: Build** і запустіть **Wokwi: Start Simulator**. Не ставте симуляцію на паузу.
2. В іншому вікні/терміналі перейдіть у папку `automation` і активуйте venv:
   - PowerShell: `.venv\Scripts\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
3. Задайте порт:
   - PowerShell: `$env:DEVICE_PORT="rfc2217://localhost:4000"`
   - macOS/Linux: `export DEVICE_PORT=rfc2217://localhost:4000`
4. Запустіть тести: `python -m pytest -v`

Якщо бачите `ModuleNotFoundError: No module named 'serial'` — venv не активований або не виконано `python -m pip install -r requirements.txt`. Запускайте тести саме як `python -m pytest`, щоб використовувався Python з venv.

## Зміна в навчальній прошивці
У `homework_buggy` додано затримку 1200 мс у відповіді на `PING`, щоб дефект відповідав опису в `instructor/INSTRUCTOR_GUIDE.md` і був помітний клієнту з timeout 1 секунду. Інші навчальні дефекти залишено навмисно.

## Виправлення схеми Wokwi
У `diagram.json` піни плати `wokwi-esp32-devkit-v1` мають назви з літерою D. Раніше були вказані `esp:15` та `esp:2`, через що DHT22 і LED фактично не були під'єднані (`GET TEMP` повертав помилку датчика). Тепер: DHT22 → `esp:D15`, LED → `esp:D2`. Якщо у вас стара копія — замініть ці назви вручну.
