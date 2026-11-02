# Embedded QA Portfolio Case Study — Smart IoT Safety Controller

*Nataliia Honcharova · курс Embedded QA, вебінари 1–8*

## 1. Project

Навчальний IoT-контролер на ESP32: зчитує кнопку, DHT22 і MPU6050 (I²C), керує relay і LED, приймає команди по UART, передає телеметрію через мережеву модель MQTT з offline-буфером, відновлюється через watchdog і зберігає стан. Кожну підсистему я тестувала на окремій навчальній збірці з навмисно закладеними дефектами (BUGGY) у симуляторі Wokwi.

## 2. My QA Goal

Підтримати release-рішення: чи передбачувано поводиться пристрій не лише в happy path, а й при шумі на входах, некоректних командах, помилках шини, зависанні, втраті живлення, втраті мережі та тривалому навантаженні — і чи можна це довести evidence, а не відсотком PASS.

## 3. System Overview

`Inputs` (кнопка GPIO4/GPIO18, DHT22 GPIO15, MPU6050 0x68 на GPIO21/22, кінцеві вимикачі) → `ESP32 firmware` (state machines, UART CLI 115200, task WDT 4000 ms, persistent state, network FSM, buffer на 8 повідомлень) → `Outputs` (relay GPIO5, LED GPIO2, gate relays і LED-індикація). Зовнішні залежності: MQTT broker (модель `NET DOWN/UP`), host з Python/pytest через RFC2217.
Схема та деталі — [MASTER_TEST_PLAN.md §2](MASTER_TEST_PLAN.md#2-system-overview).

## 4. Critical Risks

| # | Ризик (failure mode → impact) | Чому критичний |
|---|---|---|
| R04 | Після WDT reset / RESET actuator лишається ввімкненим | пряма загроза safety: аварія не вимикає навантаження |
| R09 | Кінцевий вимикач не зупиняє двигун воріт | механічне пошкодження / травма |
| R05 | Переривання запису дає невалідний persistent state | після збою живлення пристрій працює з хибними даними |
| R03 | Помилка I²C заморожує MCU | одна відмова сенсора вимикає весь пристрій |
| R08 | Систематичний витік heap | відмова в полі гарантована, питання лише часу |
| R07 | Буфер мовчки губить і дублює телеметрію | дані неповні, а лічильники це приховують |
| R01 | Шум/bounce викликає зайву дію | несанкціоноване спрацювання actuator |

Повний реєстр (12 ризиків з impact / probability / priority) — [MASTER_TEST_PLAN.md §7](MASTER_TEST_PLAN.md#7-quality-risks).

## 5. Test Strategy

| Ризик | Level | Метод | Environment |
|---|---|---|---|
| R01 | System | порівняння RAW / LOGICAL / ACTION, D0 vs D1, серії натискань, шум під час critical operation | Wokwi + logic analyzer |
| R02 | Component / Interface | BVA (N−1 / N / N+1), negative, input length, case sensitivity; автоматизація pytest | Wokwi; Python + pytest |
| R03 | Protocol / Recovery | FAULT ON/OFF, аналіз I²C-трейсу + firmware log | Wokwi + VCD / PulseView |
| R04, R05, R10, R11 | Recovery / fault injection | `hang`, 15 циклів hang/recovery, `relay on; hang`, `powerloss`, DHT disconnect, `sleep 5` | Wokwi (VS Code) |
| R06, R07 | Network | NET DOWN/UP, SEND × 5 / 8 / 9 / 12, підрахунок message ID | Wokwi network model |
| R08 | Reliability | 13 × `STRESS 100`, тренд heap | Wokwi network model |

Трасованість по кожному тесту — [FINAL_TEST_MATRIX.md](FINAL_TEST_MATRIX.md).

## 6. Key Scenarios

1. **Relay після watchdog** (W5 T05): `relay on` → `hang` → WDT reset. Очікувалось relay OFF; фактично `reset_reason=INT_WDT`, `"relay":true`.
2. **Interrupted save** (W5 T06): `powerloss` під час збереження. Очікувався старий або новий стан; фактично `counter` 0 → 100, потім 101 → 201.
3. **Втрата I²C-периферії** (W4): FAULT ON. Трейс: останній ACK на +8950 ns, перший NACK на адресу 0x69 на +11425 ns; firmware: `i2cWriteReadNonStop returned Error -1`, після чого main loop мовчить, а FAULT OFF не відновлює роботу.
4. **Межа offline-буфера** (W7 Scenario C): 8 / 9 / 12 SEND при NET DOWN. На 9 і 12 count виходить за 8 (9/8, 12/8), `dropped=0`, найстаріші ID зникають без обліку, решта публікуються по 2–4 рази.
5. **Memory stability** (W7 Scenario D): 13 × `STRESS 100` — heap 350868 → 246600 Б з кроком ≈ −8000 Б; контрольний прогін без повідомлень — heap сталий.
6. **Шум під час critical operation** (W2 TC-06): одне натискання + шум → 2 logical events і 2 actions.

## 7. Automation

20 pytest-тестів (Python 3.15, pytest 9.1.1, pyserial 3.5) працюють з пристроєм у Wokwi через `DEVICE_PORT=rfc2217://localhost:4000`: `test_boundaries.py` (PWM 0/1/50/100, збереження 1/99, невалідні −1/101/999, `aa`, `1.5`, спецсимволи, порожнє), `test_relay.py`, `test_reset.py`, `test_sensor.py`, `test_status.py`, `test_timeout.py`.
Моя робота у W6: розгорнути середовище й підключити Python до Wokwi, запустити базовий набір курсу, доповнити його, провести triage кожного FAIL, зібрати evidence і оформити bug reports.
Що я додала до фреймворку (коміти `ac609c0`, `bed1539` у [NataliGoncharova/Embedded](https://github.com/NataliGoncharova/Embedded)):
- 6 параметризованих boundary/negative кейсів: збереження PWM 1 / 99 через `STATUS`, некоректний формат `aa` / `1.5` / `$#@!%^^&`, порожнє значення;
- розділення перевірки `RESET` на два тести — окремо для LED і для PWM;
- autouse-фікстуру з `RESET` до і після кожного тесту (контрольований precondition і cleanup) та одне serial-підключення на модуль;
- вивід сирої відповіді пристрою (`Device response: ...`) у pytest-лог як evidence.

Код — [`automation/`](automation/), опис — [automation/README.md](automation/README.md).
Результат: 13 PASS / 7 FAIL. Кожен FAIL класифіковано (Test / Environment / Communication / Requirement / Firmware): 6 — Firmware, 1 (`test_ping`, `TimeoutError`) — Test.
**Роль у стратегії:** набір перевіряє контракт команд і відповідей (межі, невалідний ввід, безпечний стан після RESET, валідність JSON), тому він є автоматизованим regression після кожної зміни firmware. Поведінка, що залежить від фізики чи часу (bounce, WDT, мережа, heap), у курсі перевірялась вручну з логами.

## 8. Fault Injection

| Fault | Як вводився | Як перевірявся recovery | Результат |
|---|---|---|---|
| Шум на вході | вхід NOISE (W2) | лічильники RAW / LOGICAL / ACTIONS | шум породжує дію — FAIL |
| Втрата I²C-периферії | перемикач FAULT (W4) | трейс + firmware log, FAULT OFF | зависання без recovery — FAIL |
| Від'єднання сенсора | DHT22 disconnect (W5) | STATUS `sensor_ok` | `sensor_ok:false` — PASS |
| Зависання firmware | `hang` (W5) | `reset_reason`, STATUS, 15 циклів | WDT reset працює — PASS; relay лишається ON — FAIL |
| Втрата живлення під час запису | `powerloss` (W5) | STATUS до / після | невалідний counter — FAIL |
| Втрата мережі / broker | `NET DOWN` / `NET UP` (W7) | `[NET] state=...`, STATUS, flush | відновлення PASS; storm, дублі, втрати — FAIL |
| Навантаження | `STRESS 100` × 13 (W7) | heap у STATUS після кожної ітерації | витік — FAIL |

## 9. Evidence

26 evidence-записів (E01–E26): serial-логи з таймстемпами, reset-логи, VCD-трейс із декодером, pytest-вивід з сирими відповідями пристрою, логи з message ID, таблиця heap по ітераціях, відео 20 натискань, код pytest-фреймворку. Індекс — [EVIDENCE_INDEX.md](EVIDENCE_INDEX.md), файли — [`evidence/`](evidence/).

## 10. Findings

24 дефекти: 6 Critical, 12 Major/High, 2 Medium, 4 Minor/Low ([BUG_REPORTS.md](BUG_REPORTS.md)). Найважливіші:

- **Safety:** relay ON після `INT_WDT` (W5); `RESET` не повертає LED/PWM у 0 (W6); OPEN relay ON після LIMIT_OPEN (W1).
- **Data integrity:** `powerloss` → counter +100 (W5); кожне буферизоване повідомлення публікується двічі, а на межі буфера найстаріші зникають з `dropped=0` (W7).
- **Availability:** зависання при помилці I²C (W4); витік ≈80 Б на повідомлення (W7); reboot від 41-символьного рядка (W3).
- **Observability:** лічильники W7 не відображають реальність (`dropped=0` при втратах; `duplicates` недооцінює повтори: 9 SEND → `duplicates=9` при 10 зайвих publish).

## 11. Regression

Після кожної зміни — pytest-набір W6 (20 тестів). Додатково за зоною зміни: CLI → W3 TC-01…22; входи → W2 TC-01…06 і W5 T02; reset / watchdog / actuator → W5 T04, T05, T07, W1 TC-02/TC-04; persistence → W5 T06; I²C → W4 FAULT ON/OFF; network stack → W7 сценарії A–E. Деталі — [MASTER_TEST_PLAN.md §13](MASTER_TEST_PLAN.md#13-regression-strategy).

## 12. Limitations

- Усе виконано в симуляції Wokwi; реальне залізо не використовувалось.
- Мережа рветься бінарно (`NET DOWN`); реальні збої Wi-Fi / MQTT, QoS і масовий reconnect не перевірялись.
- Найдовший прогін — 13 ітерацій `STRESS 100`; час до відмови від витоку heap невідомий.
- Reboot ноди з непорожнім буфером не перевірявся.
- BVA тривалості імпульсу кнопки не виконано через обмеження симулятора (W2 TC-07).
- W4 REQ-09…REQ-12 (retry / recovery) заблоковані зависанням MCU.
- SPI не тестувався; підсистеми не тестувались разом в одній збірці.
- Паузи між retry у кілька секунд під час вводу команд (W7) не пояснені — можливий артефакт симулятора.

## 13. Release / Quality Conclusion

**NO-GO.** Відкрито 6 Critical дефектів, три з яких — про те, що actuator лишається ввімкненим після події, яка мала його вимкнути. Обґрунтування та статус Exit Criteria — [RELEASE_DECISION.md](RELEASE_DECISION.md).

## 14. What I Would Improve Next

Наступні кроки, які я визначила в домашніх роботах:

1. **Real hardware (W5):** фізично від'єднати DHT22 і перевірити `sensor_ok:false` та безпечний стан relay; перевірити bounce на реальній механічній кнопці.
2. **Real Wi-Fi / MQTT (W7):** розрізнити падіння AP, недоступність broker, збій DNS, слабкий сигнал і часткові втрати пакетів; виміряти retry за годинником пристрою; перевірити, чи QoS/ack самі не створюють дублів.
3. **Довгі прогони 8–72 год (W7):** тренд heap за годинами при реалістичній частоті публікацій, мінімальний вільний heap, поведінка watchdog при вичерпанні пам'яті.
4. **Reboot і втрата живлення (W7):** чи потрібно зберігати буфер у flash; reboot під час flush; збереження лічильника message ID.
5. **Нестабільна мережа (W7):** швидкі цикли NET DOWN / NET UP і SEND під час flush; масовий reconnect багатьох нод після рестарту broker.
Додатково для цього портфоліо:

6. **Автоматизація:** перенести ручні кейси W3 і сценарії W5 T05, W7 C/D/E у pytest, щоб вони входили в regression.
7. **SPI та інтеграція:** зняти SPI-трейс і перевірити підсистеми разом в одній збірці.
