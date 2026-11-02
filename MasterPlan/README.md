# Smart IoT Safety Controller — Embedded QA Case Study

*Nataliia Honcharova · фінальне портфоліо курсу Embedded QA*

## What this repository demonstrates

Як я перевіряла, чи IoT-контролер на ESP32 поводиться безпечно й передбачувано **поза happy path** — при шумі на входах, некоректних командах, помилці I²C, зависанні firmware, втраті живлення, втраті мережі й тривалому навантаженні — і як з evidence виходить release-рішення. Ланцюжок: **Risk → Test → Evidence → Decision**.

## System

ESP32 DevKit V1 · входи: кнопка, DHT22, MPU6050 (I²C 0x68), кінцеві вимикачі · виходи: relay, LED, gate relays · UART CLI 115200 (text + JSON) · task watchdog 4000 ms · persistent state · мережевий FSM + offline-буфер на 8 повідомлень (MQTT-модель) · host-автоматизація Python/pytest через RFC2217.
Кожна підсистема тестувалась на окремій навчальній збірці (BUGGY) у Wokwi. Схема — [MASTER_TEST_PLAN.md §2](MASTER_TEST_PLAN.md#2-system-overview).

## Main quality risks

- **Actuator не в безпечному стані** після WDT reset, команди RESET або кінцевого вимикача (R04, R09).
- **Зіпсований persistent state** після переривання запису (R05).
- **Зависання MCU** при втраті I²C-периферії (R03).
- **Витік пам'яті** при тривалій роботі (R08).
- **Мовчазна втрата та дублі телеметрії** в offline-буфері (R07).
- **Зайві дії від шуму / bounce** (R01) і **некоректний ввід CLI** (R02).

## Test strategy

- [MASTER_TEST_PLAN.md](MASTER_TEST_PLAN.md) — scope, 12 ризиків з пріоритетами, рівні, середовища, entry/exit criteria, regression, evidence strategy.
- [FINAL_TEST_MATRIX.md](FINAL_TEST_MATRIX.md) — 80 перевірок, кожна прив'язана до ризику та evidence.

## Key evidence

| Що доводить | Evidence |
|---|---|
| relay ON після `INT_WDT` | [bug03_relay_after_wdt_2.png](evidence/W5_Recovery/bug03_relay_after_wdt_2.png) |
| heap 350868 → 246600 за 13 × STRESS 100 | [STRESS.log](evidence/W7_Network/STRESS.log) |
| втрата і дублі message ID у буфері | [SEND_BUFFER_9.log](evidence/W7_Network/SEND_BUFFER_9.log), [BUFFER.log](evidence/W7_Network/BUFFER.log) |
| перший NACK і зависання при I²C fault | [i2c_first_nack.png](evidence/W4_I2C/i2c_first_nack.png), [firmware_log_fault_on.png](evidence/W4_I2C/firmware_log_fault_on.png) |
| RESET не повертає safe state | [pytest_reset_led.png](evidence/W6_Pytest/pytest_reset_led.png), [pytest_reset_pwm.png](evidence/W6_Pytest/pytest_reset_pwm.png) |

Повний індекс (E01–E26) — [EVIDENCE_INDEX.md](EVIDENCE_INDEX.md).

## Key findings

24 дефекти: **6 Critical**, 12 Major/High, 2 Medium, 4 Minor/Low — [BUG_REPORTS.md](BUG_REPORTS.md).
Критичні: relay ON після watchdog reset; RESET лишає LED увімкненим і PWM ≠ 0; OPEN relay не вимикається на кінцевому вимикачі; `powerloss` збільшує counter на 100; зависання при помилці I²C; витік ≈80 Б heap на кожне повідомлення.

## Automation

Pytest-фреймворк для JSON-протоколу пристрою (Python 3.15, pytest 9.1.1, pyserial 3.5) — код у [`automation/`](automation/), оригінальний репозиторій — [NataliGoncharova/Embedded](https://github.com/NataliGoncharova/Embedded).
Перевіряє межі та збереження PWM, невалідний ввід, LED, RESET, GET TEMP, STATUS, timeout. До базового набору курсу я додала 6 параметризованих boundary/negative кейсів, окремі тести RESET для LED і PWM, фікстуру `RESET` до і після кожного тесту та вивід сирої відповіді пристрою в лог.
Результат прогону: 13 PASS / 7 FAIL, кожен FAIL класифіковано (6 Firmware, 1 Test) — [Python_Automation_Honcharova.docx](evidence/W6_Pytest/Python_Automation_Honcharova.docx).

```bash
cd automation && python -m pip install -r requirements.txt
export DEVICE_PORT=rfc2217://localhost:4000   # симуляція homework_buggy запущена у Wokwi
python -m pytest -v
```

Деталі — [automation/README.md](automation/README.md).

## Limitations

Усе виконано в симуляції Wokwi. Потребують real hardware / real network: механічний bounce, фізичне від'єднання сенсора, реальні таймінги sleep, реальні збої Wi-Fi/MQTT і масовий reconnect, прогони 8–72 год для оцінки часу до відмови, reboot з непорожнім буфером. SPI не тестувався.

## Conclusion

**NO-GO.** Більшість нормальних і граничних сценаріїв проходить, але відкриті Critical-дефекти зачіпають безпеку actuator, цілісність даних і довготривалу стабільність — [RELEASE_DECISION.md](RELEASE_DECISION.md).

---

### Структура репозиторію

| Файл | Призначення |
|---|---|
| [MASTER_TEST_PLAN.md](MASTER_TEST_PLAN.md) | Master Test Plan (17 розділів за шаблоном курсу) |
| [FINAL_TEST_MATRIX.md](FINAL_TEST_MATRIX.md) | Risk → Test → Evidence → Status |
| [EVIDENCE_INDEX.md](EVIDENCE_INDEX.md) | індекс доказів E01–E26 |
| [BUG_REPORTS.md](BUG_REPORTS.md) | зведений журнал 24 дефектів |
| [CASE_STUDY.md](CASE_STUDY.md) | case study: problem → risks → strategy → evidence → decision |
| [RELEASE_DECISION.md](RELEASE_DECISION.md) | Exit Criteria status, рекомендація, QA Conclusion |
| [DEFENSE_BRIEF.md](DEFENSE_BRIEF.md) | план усного захисту 5–7 хв і відповіді на контрольні питання |
| [`automation/`](automation/) | Python/Pytest фреймворк і тести (W6) |
| [`evidence/`](evidence/) | оригінальні артефакти домашніх робіт W1–W7 |

### Відповідність Portfolio Review Sheet

| Пункт | Де |
|---|---|
| README повний | цей файл |
| System Scope описаний | MASTER_TEST_PLAN §2, §4, §5 |
| 5+ Quality Risks | MASTER_TEST_PLAN §7 (12 ризиків) |
| Master Test Plan | MASTER_TEST_PLAN.md |
| Test Matrix | FINAL_TEST_MATRIX.md |
| Evidence Package | EVIDENCE_INDEX.md + `evidence/` |
| 3+ Bug Reports | BUG_REPORTS.md (24) + оригінали в `evidence/` |
| Pytest automation | `automation/` (код), README §Automation, CASE_STUDY §7, E17–E18, E26 |
| Release Decision | RELEASE_DECISION.md |
| QA Conclusion | RELEASE_DECISION.md §QA Conclusion |
