# Defect Log — зведений журнал дефектів (W1–W7)

Усього оформлено **24 bug reports** у 7 домашніх роботах. Повні звіти (кроки, preconditions, environment, скріншоти) — у файлах, на які посилається колонка Evidence.

| Severity (уніфікована) | Кількість | Дефекти |
|---|---:|---|
| Critical | 6 | W1 BR-01, W4 BUG-01, W5 BUG-03, W5 BUG-04, W6 BUG-03, W7 BUG-03 |
| Major / High | 12 | W2 BR-01, W2 BR-02, W3 BUG-02, W3 BUG-03, W5 BUG-01, W5 BUG-02, W6 BUG-01, W6 BUG-02, W6 BUG-04, W7 BUG-01, W7 BUG-02, W7 BUG-04 |
| Medium | 2 | W3 BUG-01, W3 BUG-04 |
| Minor / Low | 4 | W1 BR-02, W1 BR-03, W1 BR-04, W3 BUG-05 |

Шкала severity у W1–W3 — Critical / High / Medium / Low, у W5–W7 — Critical / Major / Medium / Minor; тут High ≡ Major, Low ≡ Minor. Для W6 BUG-03 у звіті вказано «Critical/High» — у зведенні віднесено до Critical (порушено вимогу безпечного стану).

---

## Critical

| ID | Risk | Title | Requirement | Expected | Actual | Repro | Evidence |
|---|---|---|---|---|---|---|---|
| W1 BR-01 | R09 | LIMIT_OPEN під час OPENING не зупиняє рух | R6: LIMIT_OPEN під час OPENING вимикає OPEN relay і переводить систему в OPEN | State=OPEN; обидва relays OFF | State лишається OPENING; OPEN relay = ON; `OPEN LIMIT DETECTED` повторюється | 5/5 | E02 |
| W4 BUG-01 | R03 | System freezes indefinitely after I2C bus error | REQ-08 | помилка в лозі, main loop працює далі | `i2cWriteReadNonStop returned Error -1`, main loop не виконується; після FAULT OFF відновлення немає | 5/5 | E07, E08 |
| W5 BUG-03 | R04 | Hung command: the relay is on after reset | R5 Watchdog: actuator після аварійного reset має бути OFF | relay OFF після WDT | `reset_reason=INT_WDT`, `"relay":true` | 100% | E15 |
| W5 BUG-04 | R05 | Powerloss: the counter increases by 100 | R6 Interrupted save: лише старий або новий валідний стан | counter 0 або 1 | counter 0 → 100; 101 → 201 | 100% | E16 |
| W6 BUG-03 | R04 | RESET command: the safe output state is not restored | 7: `RESET` restores safe output state LED/PWM OFF/0 | led=false; pwm=0 | led=true (pwm=255); pwm=12 після `SET PWM 5; RESET` | 100% | E18 |
| W7 BUG-03 | R08 | Free heap падає ≈ 8000 Б за ітерацію STRESS 100 і не відновлюється | R7 Memory stability | heap коливається біля baseline 350868 | 350868 → 246600 (−29,7%) за 13 ітерацій; ≈80 Б на повідомлення | 13/13 | E24 |

## Major / High

| ID | Risk | Title | Requirement | Expected | Actual | Repro | Evidence |
|---|---|---|---|---|---|---|---|
| W2 BR-01 | R01 | Short noise pulse запускає дію | AC 4: короткий нестабільний імпульс не запускає action | RAW дозволено; без logical/action | RAW 1; logical 1; action 1 | 5/5 | E03, E04 |
| W2 BR-02 | R01 | Noise during critical operation створює додаткову дію | AC 5: шум під час critical operation не створює logical action | без додаткової події | додаткова logical event і action (LOGICAL 2, ACTIONS 2) | 5/5 | E03, E04 |
| W3 BUG-02 | R02 | `set timeout 0` не повертає out of range | REQ-05: поза 1..60 — ERROR, timeout не змінюється | `ERROR: timeout out of range` | `OK: timeout=0` | 5/5 | E06 |
| W3 BUG-03 | R02 | Рядок 41 символ перезавантажує пристрій | REQ-11, REQ-12 | `ERROR: command too long` | `*** SYSTEM FAULT ***`, `rst:0xc (SW_CPU_RESET)`, reboot | 5/5 | E06 |
| W5 BUG-01 | R01 | Один клік створює кілька logical events | R3 Button: один натиск — не більше однієї події | 20 подій на 20 натискань | counter = 24 | 100% | E12, E13 |
| W5 BUG-02 | R11 | Неправильна тривалість sleep | R4: deep sleep ≈ N s, похибка ±15% | wake через 4.25–5.75 s | 1.368 s | 100% | E14 |
| W6 BUG-01 | R02 | `SET PWM 100` відхиляється | 5: `SET PWM N` приймає 0…100 включно | OK | `{"status":"ERROR","code":"INVALID_VALUE"}` | 100% | E18 |
| W6 BUG-02 | R02 | STATUS показує інший PWM, ніж встановлено | 5 | pwm=1; pwm=99 | pwm=2; pwm=252 | 100% | E18 |
| W6 BUG-04 | R10 | `GET TEMP` повертає невалідний JSON | 3: `GET TEMP` → valid JSON | `{"status":"OK","temperature":24.5}` | `{"status":"OK","temperature":24.5` | 100% | E18 |
| W7 BUG-01 | R07 | Flush після NET UP публікує кожне повідомлення двічі | R6 Duplicates | sent=5, duplicates=0 | sent=10, duplicates=5 | 3/3 | E20, E21 |
| W7 BUG-02 | R06 | Reconnect storm: retry кожні 50 мс | R2 Auto-reconnect з backoff | інтервал зростає | `backoff_ms=500`, далі завжди 50; 188 спроб за 21 s | 6/6 | E19 |
| W7 BUG-04 | R07 | Буфер виходить за capacity, drop не рахується | R4 Buffer boundary: capacity 8, DROP_OLDEST, drop observable | count ≤ 8; dropped=1 (9 SEND) / 4 (12 SEND) | 9/8 і 12/8; dropped=0; найстаріші ID зникли без обліку; ID повторно публікуються | 2/2 | E22, E23 |

## Medium

| ID | Risk | Title | Requirement | Expected | Actual | Repro | Evidence |
|---|---|---|---|---|---|---|---|
| W3 BUG-01 | R02 | `set speed 256` не повертає out of range | REQ-03: поза 0..255 — ERROR, speed не змінюється | `ERROR: speed out of range` | `OK: speed=255` | 5/5 | E06 |
| W3 BUG-04 | R02 | Рядок лише зі спецсимволів повертає OK | REQ-08 | ERROR | OK | 5/5 | E06 |

## Minor / Low

| ID | Risk | Title | Requirement | Expected | Actual | Repro | Evidence |
|---|---|---|---|---|---|---|---|
| W1 BR-02 | R12 | STOP під час OPENING: OPEN LED світиться | R14: LED відповідають стану | усі індикатори OFF у STOPPED | OPEN LED = ON | 5/5 | E02 |
| W1 BR-03 | R12 | STOP під час CLOSING: OPEN LED світиться | R14 | усі індикатори OFF | OPEN LED = ON | 5/5 | E02 |
| W1 BR-04 | R12 | RESET з ERROR: OPEN LED світиться | R14 | індикатори OFF | OPEN LED = ON | 5/5 | E02 |
| W3 BUG-05 | R02 | `STATUS` у верхньому регістрі виконується | REQ-06: команди case-sensitive | `ERROR: unknown command` | команда виконана | 5/5 | E06 |

> Примітка щодо W1, W2 і W3: у вихідних .xlsx поле Reproducibility відображається як дата `05.05.2026` — Excel автоматично перетворив введене `5/5` на дату. У цьому журналі значення наведено як 5/5.
