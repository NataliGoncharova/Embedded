# Final Test Matrix

Кожен рядок зв'язує **Risk → Level → Test → Environment → Expected → Evidence → Regression → Status**.
Ризики описані в [MASTER_TEST_PLAN.md §7](MASTER_TEST_PLAN.md#7-quality-risks); evidence ID — у [EVIDENCE_INDEX.md](EVIDENCE_INDEX.md); дефекти — у [BUG_REPORTS.md](BUG_REPORTS.md).
Префікс тесту вказує вебінар і оригінальний ID із домашньої роботи (наприклад `W3 TC-08`).

## Зведення покриття

| Risk | Priority | Тестів | PASS | FAIL | Blocked / Not run | Висновок по ризику |
|---|---|---:|---:|---:|---:|---|
| R01 Bounce / noise → зайва дія | P1 | 8 | 4 | 3 | 1 | **Не закрито** |
| R02 CLI / протокол команд | P1 | 39 | 30 | 9 | 0 | **Не закрито** |
| R03 Втрата I²C → зависання | P1 | 4 | 1 | 2 | 1 (REQ-09…12) | **Не закрито** |
| R04 Небезпечний стан actuator після reset | P1 | 5 | 2 | 3 | 0 | **Не закрито** |
| R05 Interrupted save | P1 | 1 | 0 | 1 | 0 | **Не закрито** |
| R06 Втрата мережі / reconnect | P2 | 4 | 3 | 1 | 0 | Частково (storm) |
| R07 Buffer overflow / duplicates | P1 | 5 | 2 | 3 | 0 | **Не закрито** |
| R08 Витік пам'яті | P1 | 1 | 0 | 1 | 0 | **Не закрито** |
| R09 Кінцевий вимикач не зупиняє рух | P1 | 7 | 5 | 1 | 1 | **Не закрито** |
| R10 Невалідні дані сенсора | P2 | 2 | 1 | 1 | 0 | Частково |
| R11 Тривалість deep sleep | P2 | 1 | 0 | 1 | 0 | Не закрито |
| R12 Індикація стану | P3 | 3 | 0 | 3 | 0 | Не закрито (Low) |

> R02 включає 22 кейси W3 і 17 pytest-тестів W6; решта 3 тести W6 віднесені до R04 (2 × `test_reset`) і R10 (`test_sensor`). W6 `test_ping` (FAIL) класифіковано як **Test**-проблему, а не дефект firmware.

---

## R01 — Bounce або шум на вході створює зайву logical event / action

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W2 TC-01 | System | Normal press: одне натискання | Wokwi + logger | 1 press → 1 logical → 1 action | RAW 94 / LOGICAL 1 / ACTIONS 1 · E03 | Yes (manual) | PASS |
| W2 TC-02 | Protocol / System | Bounce: порівняння D0 RAW і D1 LOGICAL | Wokwi logic analyzer | D1 змінюється 1 раз на press | D0 > D1; 1 press = 1 D1 event = 1 action · E03 | Yes (manual) | PASS |
| W2 TC-03 | System | Long press 2–5 s | Wokwi + logger | немає повторних events | RAW 98 / LOGICAL 1 / ACTIONS 1 · E03 | Yes (manual) | PASS |
| W2 TC-04 | System | 5 швидких натискань | Wokwi + logger | 5 → 5 → 5 | RAW 610 / LOGICAL 5 / ACTIONS 5 · E03 | Yes (manual) | PASS |
| W2 TC-05 | System / negative | Короткий імпульс NOISE | Wokwi + logger | RAW дозволено, logical/action = 0 | RAW 1 → LOGICAL 1 → ACTION 1 · E03, E04 · W2 BR-01 | Yes (manual) | **FAIL** |
| W2 TC-06 | System / negative | NOISE під час critical operation | Wokwi + logger | без додаткової дії | 1 press + шум → LOGICAL 2, ACTIONS 2 (RAW 173) · E03, E04 · W2 BR-02 | Yes (manual) | **FAIL** |
| W2 TC-07 | Boundary | BVA тривалості імпульсу 1/5/10/20/29/30/31/50 ms | Wokwi | рівно 1 logical event | не виконано: testability limitation симулятора | — | NOT RUN |
| W5 T02 | System / reliability | 20 натискань кнопки | Wokwi (VS Code) | рівно 20 подій | `counter` 0 → 24 · E12, E13 · W5 BUG-01 | Yes (manual) | **FAIL** |

## R02 — UART CLI / протокол команд приймає некоректні дані або падає

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W3 TC-01 | Interface | `help` | Wokwi | 8 команд | 8 команд · E06 | Yes (manual) | PASS |
| W3 TC-02 | Component | `set speed 200` | Wokwi | `OK: speed=200` | як очікувано · E06 | Yes (manual) | PASS |
| W3 TC-03, 05, 06, 07 | Component / BVA | speed 0, 1, 255, 254 | Wokwi | `OK: speed=N` | як очікувано · E06 | Yes (manual) | PASS (4) |
| W3 TC-04, 09 | Component / BVA | speed −1, 257 | Wokwi | `ERROR: speed out of range` | як очікувано · E06 | Yes (manual) | PASS (2) |
| W3 TC-08 | Component / BVA | `set speed 256` | Wokwi | `ERROR: speed out of range` | `OK: speed=255` (значення змінено) · E06 · W3 BUG-01 | Yes (manual) | **FAIL** |
| W3 TC-10 | Component | `set timeout 33` | Wokwi | `OK: timeout=33` | як очікувано · E06 | Yes (manual) | PASS |
| W3 TC-11 | Component / BVA | `set timeout 0` | Wokwi | `ERROR: timeout out of range` | `OK: timeout=0` · E06 · W3 BUG-02 | Yes (manual) | **FAIL** |
| W3 TC-12…15 | Component / BVA | timeout 1, 2, 59, 60 | Wokwi | `OK: timeout=N` | як очікувано · E06 | Yes (manual) | PASS (4) |
| W3 TC-16 | Component / BVA | timeout 61 | Wokwi | `ERROR: timeout out of range` | як очікувано · E06 | Yes (manual) | PASS |
| W3 TC-17 | Interface / length | рядок 41 символ | Wokwi | `ERROR: command too long` | `*** SYSTEM FAULT *** input line boundary failure`, `rst:0xc (SW_CPU_RESET)`, reboot · E06 · W3 BUG-03 | Yes (manual) | **FAIL** |
| W3 TC-18, 19 | Functional | `led on`, `led off` | Wokwi | LED=ON / LED=OFF | як очікувано · E06 | Yes (manual) | PASS (2) |
| W3 TC-20 | Negative | `/ \ \| ; : , . [ ] { }` | Wokwi | ERROR | `OK` · E06 · W3 BUG-04 | Yes (manual) | **FAIL** |
| W3 TC-21 | Stress input | 4× `status` + 4× `help` поспіль | Wokwi | 4 + 4 відповіді | як очікувано · E06 | Yes (manual) | PASS |
| W3 TC-22 | Negative | `STATUS` (верхній регістр) | Wokwi | `ERROR: unknown command` | команда виконана · E06 · W3 BUG-05 | Yes (manual) | **FAIL** |
| W6 T-01…03 | Component / BVA | `SET PWM` 0, 1, 50 | pytest + RFC2217 | OK | OK · E17 | Yes (auto) | PASS (3) |
| W6 T-04 | Component / BVA | `SET PWM 100` | pytest + RFC2217 | OK | `{"status":"ERROR","code":"INVALID_VALUE"}` · E18 · W6 BUG-01 | Yes (auto) | **FAIL** |
| W6 T-05 | Component | `SET PWM 1; STATUS` | pytest + RFC2217 | pwm=1 | pwm=2 · E18 · W6 BUG-02 | Yes (auto) | **FAIL** |
| W6 T-06 | Component | `SET PWM 99; STATUS` | pytest + RFC2217 | pwm=99 | pwm=252 · E18 · W6 BUG-02 | Yes (auto) | **FAIL** |
| W6 T-07…09 | Negative / BVA | PWM −1, 101, 999 | pytest + RFC2217 | ERROR | ERROR · E17 | Yes (auto) | PASS (3) |
| W6 T-10…13 | Negative | PWM `aa`, `1.5`, `$#E!%^^&`, порожнє | pytest + RFC2217 | ERROR | ERROR · E17 | Yes (auto) | PASS (4) |
| W6 T-14 | Functional | `test_led_on_off` | pytest + RFC2217 | OK | OK · E17 | Yes (auto) | PASS |
| W6 T-18 | Interface | `test_ping` | pytest + RFC2217 | OK | `TimeoutError: No response for command: PING` — класифіковано **Test** · E17 | Yes (auto) | FAIL (Test) |
| W6 T-19 | Interface | `test_status` | pytest + RFC2217 | OK | OK · E17 | Yes (auto) | PASS |
| W6 T-20 | Interface / negative | `test_no_response_becomes_timeout` | pytest + RFC2217 | timeout | timeout · E17 | Yes (auto) | PASS |

## R03 — Втрата I²C-периферії → MCU зависає, немає retry/recovery

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W4 #1–5 | Protocol | FAULT OFF: транзакції 0x68 (W 0x6B 0x00; W 0x41 → Sr → R 0xEF 0x5C) | Wokwi + VCD / PulseView | ACK…NACK(останній байт читання) | збігається з очікуваним; `[DATA] Temperature: 24.00 C`, `Main loop alive` · E07 | Yes (manual) | PASS |
| W4 #6 | Protocol / fault injection | FAULT ON | Wokwi + VCD / PulseView | firmware логує помилку і **main loop продовжує роботу** | перший NACK на +11425 ns (адреса 0x69); `[E][Wire.cpp:499] requestFrom(): i2cWriteReadNonStop returned Error -1`; main loop зупинився · E07, E08 · W4 BUG-01 | Yes (manual) | **FAIL** |
| W4 recovery | Recovery | FAULT OFF після помилки | Wokwi | ACK і відновлення даних | UART порожній, I²C порожньо, main loop не працює; retry немає · E07 | Yes (manual) | **FAIL** |
| W4 REQ-09…12 | Recovery | retry / recovery вимоги | Wokwi | — | BLOCKED через зависання MCU | — | BLOCKED |

## R04 — Після hang / WDT / RESET actuator не в безпечному стані

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W5 T04 | Recovery | `hang` | Wokwi (VS Code) | WDT reset ≲ 5 s | `task_wdt` → `rst:0x8 (TG1WDT_SYS_RESET)`, `reset_reason=INT_WDT`; від `PRE_HANG` до `POST_BOOT` 5.514 s (включно з boot), WDT timeout 4000 ms · E10 | Yes (manual) | PASS |
| W5 T07 | Recovery / reliability | hang → recovery ×10 | Wokwi (VS Code) | повертається в ACTIVE щоразу | у лозі 15 циклів `hang` → `INT_WDT`, кожен 5.514–5.515 s до `POST_BOOT`; STATUS після циклів `"state":"ACTIVE"` · E11 | Yes (manual) | PASS |
| W5 T05 | Recovery / safety | `relay on; hang` | Wokwi (VS Code) | після WDT relay = OFF | `{"reset_reason":"INT_WDT","relay":true,...}` · E15 · W5 BUG-03 | Yes (manual) | **FAIL** |
| W6 T-15 | Component / safety | `SET LED ON; RESET; STATUS` | pytest + RFC2217 | led=false | led=true (pwm=255) · E18 · W6 BUG-03 | Yes (auto) | **FAIL** |
| W6 T-16 | Component / safety | `SET PWM 5; RESET; STATUS` | pytest + RFC2217 | pwm=0 | pwm=12 · E18 · W6 BUG-03 | Yes (auto) | **FAIL** |

## R05 — Interrupted save → невалідний persistent state

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W5 T06 | Persistence / fault injection | `status; powerloss; status; relay on; status; powerloss; status` | Wokwi (VS Code) | лише старий або новий валідний стан | `counter` 0 → 100 і 101 → 201 після `powerloss` (`reset_reason=SOFTWARE_RESET`) · E16 · W5 BUG-04 | Yes (manual) | **FAIL** |

## R06 — Втрата мережі: відновлення та reconnect storm

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W7 R1 | Network | Scenario A: NET DOWN → NET UP, перевірка станів | Wokwi network model | observable DISCONNECTED / CONNECTING / CONNECTED / BACKOFF | всі 4 стани в лозі; CONNECTED → DISCONNECTED → BACKOFF → CONNECTING → BACKOFF / CONNECTED · E19 | Yes (manual) | PASS |
| W7 RISK-02 | Network | STATUS і SEND під час NET DOWN | Wokwi network model | нода не зависає | STATUS відповів під час NET DOWN (`net=BACKOFF`, attempts 61 і 158); SEND приймались · E19, E20 | Yes (manual) | PASS |
| W7 R5 | Recovery | NET UP | Wokwi network model | CONNECTED + flush буфера | CONNECTED через 8 мс після `network restored`; buffer=0 · E19, E20 | Yes (manual) | PASS |
| W7 R2 | Network | спостереження retry ~20 s | Wokwi network model | backoff зростає, без storm | `retry=1 backoff_ms=500`, далі завжди 50; 188 спроб за 21,0 s; медіанний інтервал 50 мс · E19 · W7 BUG-02 | Yes (manual) | **FAIL** |

## R07 — Offline buffer: мовчазна втрата та дублікати

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W7 R3 (Scen. B) | Network | NET DOWN, SEND ×5, NET UP | Wokwi network model | queued 1…5, flush усіх | `queued id=1…5`, count 1/8…5/8; flush_end count=0 · E20 | Yes (manual) | PASS |
| W7 Scen. C-8 | Boundary | SEND ×8 при NET DOWN | Wokwi network model | count 8/8, dropped 0 | count 8/8, dropped 0 · E21 | Yes (manual) | PASS (межа) |
| W7 Scen. C-9 | Boundary | SEND ×9 при NET DOWN | Wokwi network model | count ≤ 8, dropped=1, flush id 2–9 | `count=9/8`, `dropped_total=0`; id=1 зник без обліку; id=9 ×4, id=2–8 ×2; sent=18 · E22 · W7 BUG-04 | Yes (manual) | **FAIL** |
| W7 Scen. C-12 | Boundary | SEND ×12 при NET DOWN | Wokwi network model | count ≤ 8, dropped=4, flush id 5–12 | count до 12/8, dropped=0; id=1–4 зникли; id=9–12 ×4, id=5–8 ×2; sent=24 · E23 · W7 BUG-04 | Yes (manual) | **FAIL** |
| W7 R6 (Scen. E) | Network | підрахунок `[MQTT] publish id=` після flush | Wokwi network model | кожен ID рівно 1 раз, duplicates=0 | кожен ID ×2: 5 SEND → sent=10, duplicates=5 (також 8 SEND → sent=16); у CONNECTED дублів немає · E20, E21 · W7 BUG-01 | Yes (manual) | **FAIL** |

## R08 — Систематичне падіння free heap

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W7 R7 (Scen. D) | Reliability / memory | `STRESS 100` × 13 + STATUS після кожної | Wokwi network model | heap коливається, без систематичного падіння | 350868 → 246600 Б (−104268, −29,7%); ≈ −8000 Б на ітерацію (≈80 Б/повідомлення) без відновлення; без повідомлень heap сталий · E24 · W7 BUG-03 | Yes (manual) | **FAIL** |

## R09 — Gate state machine: кінцевий вимикач не зупиняє рух

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W1 TC-01 | Component | OPEN з CLOSED | Wokwi | OPENING, OPEN relay ON | як очікувано · E01 | Yes (manual) | PASS |
| W1 TC-02 | Component / safety | LIMIT_OPEN під час OPENING | Wokwi | OPEN, обидва relays OFF | стан лишається OPENING, OPEN relay = ON; `OPEN LIMIT DETECTED` повторюється · E01, E02 · W1 BR-01 | Yes (manual) | **FAIL** |
| W1 TC-03 | Component | CLOSE з OPEN | Wokwi | CLOSING | стан OPEN не досягнуто | — | BLOCKED |
| W1 TC-04 | Component | LIMIT_CLOSE під час CLOSING | Wokwi | CLOSED, relays OFF | як очікувано · E01 | Yes (manual) | PASS |
| W1 TC-07, 08 | Component | OPEN / CLOSE з STOPPED | Wokwi | OPENING / CLOSING | як очікувано · E01 | Yes (manual) | PASS (2) |
| W1 TC-09 | Component / negative | OPEN у стані ERROR | Wokwi | рух не починається | як очікувано · E01 | Yes (manual) | PASS |

## R10 — Несправний сенсор / невалідні дані

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W5 T01 | Recovery | від'єднати DHT22 | Wokwi (VS Code) | явна помилка сенсора | STATUS `"sensor_ok":false`; команда `sensor` вивела `temp=0.0C humidity=0.0%` · E09 | Yes (manual) | PASS |
| W6 T-17 | Interface | `GET TEMP` | pytest + RFC2217 | валідний JSON | `{"status":"OK","temperature":24.5` (без `}`) · E18 · W6 BUG-04 | Yes (auto) | **FAIL** |

## R11 — Тривалість deep sleep

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W5 T03 | System / timing | `sleep 5` | Wokwi (VS Code) | wake через 4.25–5.75 s | `PRE_SLEEP 17.247 s` → `POST_SLEEP 18.615 s` = 1.368 s, `reset_reason=DEEP_SLEEP` · E14 · W5 BUG-02 | Yes (manual) | **FAIL** |

## R12 — Індикація не відповідає стану

| ID | Level | Test / Method | Environment | Expected | Actual / Evidence | Regression? | Status |
|---|---|---|---|---|---|---|---|
| W1 TC-05 | Component | STOP під час OPENING | Wokwi | STOPPED, усі індикатори OFF | OPEN LED = ON · E01, E02 · W1 BR-02 | Yes (manual) | **FAIL** |
| W1 TC-06 | Component | STOP під час CLOSING | Wokwi | STOPPED, усі індикатори OFF | OPEN LED = ON · E01, E02 · W1 BR-03 | Yes (manual) | **FAIL** |
| W1 TC-10 | Component | RESET з ERROR | Wokwi | STOPPED, індикатори OFF | OPEN LED = ON · E01, E02 · W1 BR-04 | Yes (manual) | **FAIL** |
