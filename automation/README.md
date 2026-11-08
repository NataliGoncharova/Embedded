# Automation — Python / Pytest (Webinar 6)

Копія тестового фреймворку з репозиторію [NataliGoncharova/Embedded](https://github.com/NataliGoncharova/Embedded) (`PythonTest/automation`), яким перевірялась навчальна прошивка `homework_buggy` у Wokwi. Вимоги до пристрою — [device_requirements.md](device_requirements.md).

## Склад

| Файл | Призначення |
|---|---|
| [device.py](device.py) | клас `Device`: підключення через `serial.serial_for_url` (COM-порт або `rfc2217://`), `command_raw()` з timeout → `TimeoutError`, `command()` з розбором JSON → `AssertionError` при невалідному JSON |
| [conftest.py](conftest.py) | фікстури: одне підключення на модуль; autouse-фікстура `RESET` до і після кожного тесту |
| [tests/test_boundaries.py](tests/test_boundaries.py) | `SET PWM`: валідні межі, збереження значення, невалідні межі, некоректний формат, порожнє значення |
| [tests/test_relay.py](tests/test_relay.py) | `SET LED ON/OFF` |
| [tests/test_reset.py](tests/test_reset.py) | `RESET` повертає LED і PWM у безпечний стан |
| [tests/test_sensor.py](tests/test_sensor.py) | `GET TEMP` повертає валідний JSON і температуру в −40…80 |
| [tests/test_status.py](tests/test_status.py) | `PING`, `STATUS` |
| [tests/test_timeout.py](tests/test_timeout.py) | невідома команда без відповіді → `TimeoutError`, а не вічне очікування |

## Що додала я (за історією git)

Базовий набір курсу закомічено 2026-10-24 (`start`). Мої зміни — коміти `ac609c0` (2026-10-28, «add new boundary tests») і `bed1539` (2026-10-30, «Update conftest.py»):

| Зміна | Навіщо (вимога) |
|---|---|
| `test_pwm_saved_valid_boundaries` [1, 99] — `SET PWM N`, потім `STATUS` | перевірити, що значення не лише прийняте, а й збережене (req. 2, 5) |
| `test_pwm_malformed_values` [`aa`, `1.5`, `$#@!%^^&`] | негативні значення формату (req. 6) |
| `test_pwm_empty_values` — `SET PWM` без значення | очікується `UNKNOWN_COMMAND` (req. 8) |
| `test_reset.py`: тест `test_reset_restores_safe_state` з базового набору розділено на два — для LED і для PWM | кожен FAIL вказує на одну причину (req. 7) |
| `conftest.py`: підключення `scope="module"` + autouse-фікстура `RESET` до і після кожного тесту | контрольований precondition і cleanup |
| `device.py`: `print(f"Device response: {raw}")` у `command()` | сира відповідь пристрою потрапляє в pytest-вивід як evidence |
| `device.py`: timeout за замовчуванням 1.0 → 2.0 s | у тестах використовується значення з `conftest.py` (`timeout=1.0`) |

Разом додано **6 параметризованих / негативних кейсів** (2 + 3 + 1) — завдання вимагало щонайменше 5.

## Результат прогону

За звітом [Python_Automation_Honcharova.docx](../evidence/W6_Pytest/Python_Automation_Honcharova.docx): 20 записаних результатів — 13 PASS / 7 FAIL; 6 FAIL класифіковано як дефекти прошивки, 1 (`test_ping`, `TimeoutError`) — як проблему тесту. Скріншоти pytest — у [`evidence/W6_Pytest/`](../evidence/W6_Pytest/).

> У наборі 21 тест-кейс: у журналі виконання немає рядка для `test_pwm_valid_boundaries[99]`.

## Запуск

Потрібна запущена симуляція `homework_buggy` у Wokwi для VS Code (у `wokwi.toml`: `rfc2217ServerPort = 4000`).

```bash
cd automation
python -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
export DEVICE_PORT=rfc2217://localhost:4000
python -m pytest -v
```

Для фізичної ESP32: `DEVICE_PORT` = COM-порт плати (Serial Monitor має бути закритий). Без `DEVICE_PORT` тести пропускаються (`pytest.skip`).
