# Portfolio Defense Brief (5–7 хв)

## Таймінг

| Час | Блок | Що сказати (факти) |
|---|---|---|
| 0:00–0:45 | Product / System | ESP32-контролер: кнопка, DHT22, MPU6050 по I²C → firmware зі state machine, WDT 4000 ms, persistent state, мережевим FSM і буфером на 8 повідомлень → relay і LED. Керування по UART, автоматизація по RFC2217. Кожна підсистема — окрема BUGGY-збірка у Wokwi. |
| 0:45–1:45 | Critical Risks | Найнебезпечніше — actuator, що лишається ввімкненим після аварії (R04, R09). Далі — зіпсовані дані (R05, R07) і втрата доступності (R03 I²C, R08 heap). |
| 1:45–3:00 | Test Strategy | Кожен ризик → рівень → метод: fault injection (`hang`, `powerloss`, FAULT, NET DOWN), протокольний трейс для I²C, BVA і negative для CLI, тренд heap замість одного значення, pytest як regression. |
| 3:00–4:15 | Evidence + Findings | `INT_WDT` + `"relay":true` в одному STATUS; heap 350868 → 246600 за 13 ітерацій; 9 SEND → `count=9/8`, `dropped=0`, id=1 зник; перший NACK на +11425 ns і далі тиша в лозі. Разом 24 дефекти, 6 Critical. |
| 4:15–5:15 | Regression / Limitations | Regression за зоною зміни (MTP §13). Не перевірено: реальне залізо, реальна мережа, прогони 8–72 год, reboot з буфером, SPI, інтеграція підсистем. |
| 5:15–6:00 | Release Decision | NO-GO: не через відсоток PASS, а через 6 Critical, три з яких — safety. |

## 90-second story

**Product** — IoT-контролер на ESP32, що керує relay за даними сенсорів і шле телеметрію в MQTT.
**Risk** — найкритичніше, щоб після будь-якої аварії навантаження вимикалось, а дані не псувались мовчки.
**Strategy** — я вводила збої навмисно: зависання, втрату живлення під час запису, обрив I²C, обрив мережі, тривале навантаження — і фіксувала стан до й після.
**Evidence** — reset-логи з `reset_reason`, STATUS JSON, I²C-трейс, логи з message ID, тренд heap, pytest-вивід.
**Finding** — після watchdog reset relay лишається ON; `powerloss` збільшує counter на 100; буфер губить повідомлення з `dropped=0`; heap падає на ≈80 Б на повідомлення.
**Decision** — NO-GO до виправлення 6 Critical і повторного regression.

## Відповіді на контрольні питання (на основі виконаних робіт)

| Питання | Відповідь |
|---|---|
| Чому автоматизовано саме ці тести? | Набір W6 перевіряє контракт команд (межі, невалідний ввід, RESET, JSON) — це детерміновані перевірки, які мають запускатися після кожної зміни firmware. До базового набору я додала перевірку збереження PWM через STATUS (саме вона знайшла 1 → 2 і 99 → 252), некоректний формат і порожнє значення, а RESET розділила на LED і PWM, щоб кожен FAIL мав одну причину. |
| Як забезпечено precondition / cleanup? | autouse-фікстура в `conftest.py` надсилає `RESET` до і після кожного тесту; підключення одне на модуль. |
| Чому інші не автоматизовані? | Bounce, WDT, мережа та heap у курсі перевірялись вручну з логами; кандидати на автоматизацію — W3 CLI, W5 T05, W7 C/D/E (MTP §13). |
| Що Wokwi не може довести? | механічний bounce, електрику, реальні таймінги, реальні збої Wi-Fi/MQTT, знос flash (MTP §5, §10). |
| Як доведено, що reset = успішний recovery? | не лише факт reboot: `reset_reason=INT_WDT`, повернення в `"state":"ACTIVE"` у 15 циклах — і окремо перевірено стан actuator, де recovery виявився небезпечним (`"relay":true`). |
| Як відрізнити firmware bug від test/environment issue? | класифікація FAIL з W6: Test / Environment / Communication / Requirement / Firmware. `test_ping` (TimeoutError) — Test, решта 6 — стабільна невідповідність вимозі, 100%. |
| Який regression після зміни network stack? | W7 сценарії A (reconnect/backoff), B (5 SEND), C (8/9/12 SEND), E (дублі), D (STRESS ≥ 10 ітерацій). |
| Що робити, якщо всі tests PASS, але evidence неповний? | не закривати Exit Criteria: «Evidence complete» — окремий критерій (MTP §12). |
| Який residual risk прийнятний, а який — ні? | неприйнятні — safety (actuator) і мовчазна втрата даних; прийнятний з планом перевірки — невідомий час до відмови в реальних умовах після виправлення витоку, поки йдуть прогони 8–72 год. |
| Чому W7 BUG-03 Critical? | за визначенням severity W7: «нода перестає працювати з часом» = Critical; 13/13 ітерацій без відновлення. |
| Що перевірити на real hardware перед production? | DHT22 disconnect і relay, механічна кнопка, retry за годинником пристрою, QoS-дублі, heap за 8–72 год, reboot з буфером (CASE_STUDY §14). |
