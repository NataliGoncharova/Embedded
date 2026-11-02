# Release Decision — Smart IoT Safety Controller

## Build / Version

Навчальні збірки firmware, на яких зібрано evidence (усі — BUGGY, симулятор Wokwi):

| Підсистема | Ідентифікатор збірки |
|---|---|
| Smart Gate (W1) | `SMART GATE CONTROLLER` (Wokwi) |
| Debounce (W2) | ESP32 DevKit v1, Build: GOOD / BUGGY → BUGGY |
| UART CLI (W3) | `UART CLI HOMEWORK DEVICE v2.0` |
| I²C (W4) | `=== WEBINAR 4: I2C PRACTICE / BUGGY ===` |
| Recovery (W5) | BUGGY, `ELF file SHA256: f9dc9c5a6b4fba7e` |
| Automation (W6) | DEMO / BUGGY |
| Network (W7) | `homework_buggy` (Wokwi у VS Code) |

## Executive Summary

Тестування охопило 7 підсистем у симуляції: 80 перевірок у Final Test Matrix (W1 — 10, W2 — 7, W3 — 22, W4 — 4, W5 — 7, W6 — 20, W7 — 10), 24 оформлені дефекти, з них **6 Critical**. Пристрій коректно проходить happy path, валідні межі та відновлюється після WDT і після втрати мережі. Проте відкриті дефекти зачіпають безпеку actuator (relay/LED/PWM лишаються ввімкненими після reset або на кінцевому вимикачі), цілісність даних (зіпсований persistent state, мовчазна втрата та дублі телеметрії) і доступність (зависання при втраті I²C, витік heap). **Рекомендація — NO-GO.**

## Exit Criteria Status

| Criterion | Target | Actual | Status |
|---|---|---|---|
| Critical tests executed | 100% | усі P1-сценарії виконано, крім W2 TC-07 (BVA тривалості імпульсу — testability limitation) і заблокованих W4 REQ-09…12, W1 TC-03 | ❌ |
| Critical tests pass | 100% pass | FAIL по всіх P1-ризиках: R01, R02, R03, R04, R05, R07, R08, R09 | ❌ |
| Critical open defects | 0 | 6 (W1 BR-01, W4 BUG-01, W5 BUG-03, W5 BUG-04, W6 BUG-03, W7 BUG-03) | ❌ |
| Recovery scenarios | pass | WDT reset PASS (W5 T04, 15 циклів T07); NET UP → CONNECTED PASS (W7 R5); але safe state після WDT FAIL (T05), powerloss FAIL (T06), I²C recovery FAIL (W4) | ❌ |
| Regression | pass | pytest W6: 13 PASS / 7 FAIL (6 Firmware, 1 Test) | ❌ |
| Memory stability | без систематичного падіння | 350868 → 246600 Б за 13 ітерацій | ❌ |
| Evidence complete | yes | для кожного FAIL є лог / трейс / скріншот / pytest output (див. EVIDENCE_INDEX) | ✅ |

## Open Critical / Major Risks

| Risk | Що відомо (evidence) | Чому блокує |
|---|---|---|
| R04 Небезпечний стан actuator | `INT_WDT` + `"relay":true` (E15); `RESET` → led=true, pwm=12 (E18) | після аварії пристрій лишає навантаження ввімкненим — safety |
| R09 Кінцевий вимикач | OPEN relay = ON після LIMIT_OPEN (E02) | рух не зупиняється на кінцевій позиції — safety |
| R05 Interrupted save | counter 0 → 100 після `powerloss` (E16) | стан після збою живлення невалідний, і це не детектується |
| R03 I²C fault | Error −1, main loop зупинився, без recovery (E07) | одна відмова периферії вимикає весь пристрій |
| R08 Memory leak | −8000 Б на 100 повідомлень без відновлення (E24) | нода гарантовано відмовить з часом |
| R07 Buffer | dropped=0 при реальній втраті; кожен ID ×2…×4 (E20–E23) | телеметрія неповна і спотворена, а лічильники це приховують |
| R01 Input noise | шум під час critical operation → додаткова дія (E03, E04); 24 події на 20 натискань (E13) | несанкціонована дія actuator |
| R02 CLI | 41 символ → reboot; некоректні значення приймаються (E06) | будь-який зовнішній ввід може перезавантажити пристрій або зіпсувати конфігурацію |
| R06 Reconnect storm | 188 спроб за 21 s, backoff 50 мс (E19) | навантаження на broker / батарею (Major, не safety) |

## Residual Risks

Навіть після виправлення дефектів лишаються неперевіреними: поведінка на реальному залізі (механічний bounce, фізичне від'єднання DHT22, таймінги sleep), реальні збої Wi-Fi/MQTT і масовий reconnect, час до відмови при витоку heap (потрібні прогони 8–72 год), втрата буфера при reboot, SPI, інтеграція підсистем в одній збірці. Повний перелік — [MASTER_TEST_PLAN.md §16](MASTER_TEST_PLAN.md#16-residual-risks).

## Recommendation

- [ ] GO
- [ ] GO WITH RISKS
- [x] **NO-GO**

## Rationale

Рішення не базується на відсотку PASS. Значна частина функціональних і граничних перевірок проходить (наприклад, у W3 — 17 з 22, у W6 — 13 з 20), але FAIL зосереджені саме на ризиках з найвищим impact:

1. **Safety** — три незалежні шляхи, де actuator лишається активним після події, яка мала його вимкнути (WDT reset, команда RESET, кінцевий вимикач). Такий дефект не може бути прийнятим residual risk.
2. **Data integrity** — і persistent state, і телеметрія можуть бути зіпсовані без жодного сигналу в лічильниках (`dropped=0`, `dropped_total=0`).
3. **Availability** — пристрій зависає при першій помилці I²C і поступово вичерпує heap.

Для перегляду рішення потрібно: 0 open Critical; PASS для W5 T05, T06, W4 FAULT ON/OFF, W1 TC-02, W7 сценаріїв C, D, E; 20/20 pytest; повторний regression за [MASTER_TEST_PLAN.md §13](MASTER_TEST_PLAN.md#13-regression-strategy); перевірки на real hardware з розділу Residual Risks.

---

## QA Conclusion

Firmware на всіх навчальних збірках коректно обробляє нормальні сценарії (натискання кнопки, валідні команди й межі, переходи станів воріт, відновлення після watchdog і після втрати мережі). Проте тестування з fault injection, граничними та негативними входами виявило 24 дефекти, з яких 6 Critical. Найважливіші з них стосуються безпечного стану actuator після аварійного reset, цілісності збережених даних і телеметрії та довготривалої стабільності (витік пам'яті, зависання при помилці I²C). Висновки підкріплені логами, трейсами, pytest-виводом і відтворюваністю 5/5, 100% або N/N. Усі перевірки виконано в симуляції, тож реальна електрика, механіка і мережа залишаються residual risk. Рішення — **NO-GO** до виправлення Critical-дефектів і повторного regression.
