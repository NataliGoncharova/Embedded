# Evidence Package Index

Усі файли лежать у папці [`evidence/`](evidence/) — це копії артефактів домашніх робіт W1–W7 (без змін), плюс скріншоти, витягнуті з Word-звітів, щоб їх можна було відкрити напряму.

Правило: evidence має дозволяти іншій людині перевірити висновок QA.

| Evidence ID | Related Risk / Test | Type | Description (що саме доводить) | File / Link |
|---|---|---|---|---|
| E01 | R09, R12 · W1 TC-01…10 | Test cases + serial log | 10 тест-кейсів Smart Gate: 5 PASS, 4 FAIL, 1 BLOCKED; логи `STATE: X -> Y` для FAIL | [Smart_Gate_Test_Cases_Honcharova.xlsm](evidence/W1_SmartGate/Smart_Gate_Test_Cases_Honcharova.xlsm) |
| E02 | R09, R12 · W1 BR-01…04 | Bug reports + serial log | LIMIT_OPEN не переводить в OPEN (`OPEN LIMIT DETECTED` повторюється, OPEN relay ON); OPEN LED світиться у STOPPED | [Bug_Report_Template_Honcharova.xlsx](evidence/W1_SmartGate/Bug_Report_Template_Honcharova.xlsx) |
| E03 | R01 · W2 TC-01…07 | Logger counters + logic analyzer | RAW / LOGICAL / ACTIONS для кожного сценарію (напр. TC-05: RAW 1 → LOGICAL 1 → ACTION 1; TC-06: RAW 173, LOGICAL 2, ACTIONS 2) | [Test_Case_Honcahrova.xlsm](evidence/W2_Debounce/Test_Case_Honcahrova.xlsm) (аркуші TestCaseLog, LoggerEvidence) |
| E04 | R01 · W2 BR-01, BR-02 | Bug reports + serial log | шумовий імпульс і шум під час critical operation створюють logical event та action | [Bug_Report_Honcharova.xlsx](evidence/W2_Debounce/Bug_Report_Honcharova.xlsx) |
| E05 | R01 · W2 | QA Conclusion | висновок FAIL: система не відокремлює натискання від завад | [QA_Conclusion_Honcharova.docx](evidence/W2_Debounce/QA_Conclusion_Honcharova.docx) |
| E06 | R02 · W3 TC-01…22, BUG-01…05 | Test report + serial log | 22 кейси (17 PASS / 5 FAIL), boundary/length analysis, лог reboot `rst:0xc (SW_CPU_RESET)` на 41 символ | [Homework_Test_Report_Honcharova.docx](evidence/W3_UART_CLI/Homework_Test_Report_Honcharova.docx) · [TestCases_and_BugReports_Honcharova.xlsx](evidence/W3_UART_CLI/TestCases_and_BugReports_Honcharova.xlsx) |
| E07 | R03 · W4 транзакції 1–6 | Logic trace (VCD / PulseView) + firmware log | останній ACK (+8950 ns), перший NACK на адресу 0x69 (+11425 ns), `Wire.cpp:499 ... Error -1`, далі main loop мовчить | [Protocol_Analysis_Sheet_Test_Honharova.docx](evidence/W4_I2C/Protocol_Analysis_Sheet_Test_Honharova.docx) · [i2c_last_ack.png](evidence/W4_I2C/i2c_last_ack.png) · [i2c_first_nack.png](evidence/W4_I2C/i2c_first_nack.png) · [firmware_log_fault_on.png](evidence/W4_I2C/firmware_log_fault_on.png) |
| E08 | R03 · W4 bug report | Trace + firmware log | evidence до bug report «System freezes indefinitely after I2C bus error» (Critical, 5/5) | [bug_trace.png](evidence/W4_I2C/bug_trace.png) · [bug_firmware_log.png](evidence/W4_I2C/bug_firmware_log.png) |
| E09 | R10 · W5 T01 | Screenshot (Wokwi + terminal) | після від'єднання DHT22: `"sensor_ok":false`; `[SENSOR] temp=0.0C humidity=0.0%` | [DHT_disconnect.png](evidence/W5_Recovery/DHT_disconnect.png) |
| E10 | R04 · W5 T04 | Reset log | 3 цикли `hang` → `task_wdt` → `rst:0x8 (TG1WDT_SYS_RESET)` → `reset_reason=INT_WDT`; 5.514–5.515 s від `PRE_HANG` до `POST_BOOT` | [hang.txt](evidence/W5_Recovery/hang.txt) |
| E11 | R04 · W5 T07 | Reset log | 15 циклів hang/recovery, усі `INT_WDT`, STATUS `"state":"ACTIVE"` | [boot_loop.txt](evidence/W5_Recovery/boot_loop.txt) (оригінал — формат macOS clipboard) · [boot_loop_extracted.txt](evidence/W5_Recovery/boot_loop_extracted.txt) (той самий текст, витягнутий для читання) |
| E12 | R01 · W5 T02 | Video | 20 натискань кнопки | [ButtonBounce2026-10-29.mov](evidence/W5_Recovery/ButtonBounce2026-10-29.mov) |
| E13 | R01 · W5 BUG-01 | Before/after STATUS | `"counter":0` → `"counter":24` після 20 натискань | [bug01_button_counter.png](evidence/W5_Recovery/bug01_button_counter.png) |
| E14 | R11 · W5 BUG-02 | Timestamped log | `[TIMESTAMP_PRE_SLEEP] 17.247 s` → `[TIMESTAMP_POST_SLEEP] 18.615 s` (1.368 s при `sleep 5`) | [bug02_sleep_timing.png](evidence/W5_Recovery/bug02_sleep_timing.png) |
| E15 | R04 · W5 BUG-03 | Reset log + STATUS | `relay on` → `hang` → `reset_reason=INT_WDT`, `"relay":true` | [bug03_relay_after_wdt_1.png](evidence/W5_Recovery/bug03_relay_after_wdt_1.png) · [bug03_relay_after_wdt_2.png](evidence/W5_Recovery/bug03_relay_after_wdt_2.png) |
| E16 | R05 · W5 BUG-04, T06 | Before/after STATUS | `[FAULT] power loss DURING save`; `counter` 0 → 100, 101 → 201 | [Recovery_Fault_Injection_Test_Sheet_Honcharova.docx](evidence/W5_Recovery/Recovery_Fault_Injection_Test_Sheet_Honcharova.docx) (Bug Report 04, а також Test Matrix і Release Decision W5) |
| E17 | R02, R04, R10 · W6 T-01…20 | Pytest execution log | 20 тестів: 13 PASS / 7 FAIL, класифікація FAIL (6 Firmware, 1 Test) | [Python_Automation_Honcharova.docx](evidence/W6_Pytest/Python_Automation_Honcharova.docx) |
| E18 | R02, R04, R10 · W6 BUG-01…04 | Pytest output + raw serial | `assert 'ERROR' == 'OK'` (PWM 100); `assert 2 == 1`, `assert 252 == 99`; `assert True is False` (RESET LED); `assert 12 == 0` (RESET PWM); `Invalid JSON from device` | [pytest_pwm_valid_100.png](evidence/W6_Pytest/pytest_pwm_valid_100.png) · [pytest_pwm_saved_1.png](evidence/W6_Pytest/pytest_pwm_saved_1.png) · [pytest_pwm_saved_99.png](evidence/W6_Pytest/pytest_pwm_saved_99.png) · [pytest_reset_led.png](evidence/W6_Pytest/pytest_reset_led.png) · [pytest_reset_pwm.png](evidence/W6_Pytest/pytest_reset_pwm.png) · [pytest_temp_json.png](evidence/W6_Pytest/pytest_temp_json.png) |
| E19 | R06 · W7 Scenario A | Network log | NET DOWN 10:02:55.356 → 188 retry (`backoff_ms=500`, далі 50) → `network restored` 10:03:16.350 → CONNECTED 10:03:16.358; heap 350868 без змін | [RECOVERY.log](evidence/W7_Network/RECOVERY.log) |
| E20 | R06, R07 · W7 Scenario B, E | Message IDs + STATUS | `queued id=1…5`; після NET UP кожен id опубліковано двічі; STATUS `sent=10, duplicates=5` | [BUFFER.log](evidence/W7_Network/BUFFER.log) |
| E21 | R07 · W7 Scenario C (контроль) | Message IDs + STATUS | 8 SEND: count 8/8, dropped=0; flush — кожен id двічі, `sent=16, duplicates=8` | [SEND_BUFFER_8.log](evidence/W7_Network/SEND_BUFFER_8.log) |
| E22 | R07 · W7 Scenario C | Message IDs + STATUS | 9 SEND: `count=9/8`, `overflow ... dropped_total=0`; id=1 зник; `sent=18, dropped=0, duplicates=9` | [SEND_BUFFER_9.log](evidence/W7_Network/SEND_BUFFER_9.log) |
| E23 | R07 · W7 Scenario C | Message IDs + STATUS | 12 SEND: count до 12/8; id=1–4 зникли; `sent=24, dropped=0, duplicates=12` | [SEND_BUFFER_12.log](evidence/W7_Network/SEND_BUFFER_12.log) |
| E24 | R08 · W7 Scenario D | Metrics (heap trend) | 13 × `STRESS 100`: heap 350868 → 246600 (≈ −8000 Б/ітерація), `sent=1300, duplicates=0` | [STRESS.log](evidence/W7_Network/STRESS.log) |
| E25 | R06–R08 · W7 аналіз | Risk register, bug reports, state model, QA conclusion | реєстр RISK-01…07 (3 Pass / 4 Fail), 4 bug reports, таблиця переходів станів, R1–R8 (4 PASS / 4 FAIL), перевірки на залізі | [risk_register.xlsx](evidence/W7_Network/risk_register.xlsx) · [bug_reports.xlsx](evidence/W7_Network/bug_reports.xlsx) · [network_state_model.xlsx](evidence/W7_Network/network_state_model.xlsx) · [QA_conclusion.xlsx](evidence/W7_Network/QA_conclusion.xlsx) |
| E26 | R02, R04, R10 · W6 | Test code | pytest-фреймворк: `device.py` (timeout → `TimeoutError`, невалідний JSON → `AssertionError`), `conftest.py` (RESET до/після тесту), 6 тест-файлів; дозволяє повторно відтворити E17–E18 | [`automation/`](automation/) · [automation/README.md](automation/README.md) · [GitHub: NataliGoncharova/Embedded](https://github.com/NataliGoncharova/Embedded) |

## Найсильніші evidence (для захисту)

| # | Claim | Evidence | Чому достатньо |
|---|---|---|---|
| 1 | Після аварійного WDT reset relay лишається ввімкненим | E15 | у лозі одночасно видно `reset_reason=INT_WDT` і `"relay":true` — причина й наслідок в одному STATUS |
| 2 | Free heap систематично падає | E24 | 13 точок з однаковим кроком ≈ −8000 Б і контроль: без повідомлень heap сталий (E19) |
| 3 | Буфер мовчки губить і дублює повідомлення | E20–E23 | message ID в `queued` / `publish` можна порахувати вручну і звірити зі STATUS |
| 4 | Втрата I²C заморожує MCU | E07 | трейс показує точний момент першого NACK, firmware log — помилку, після якої лог припиняється |
| 5 | RESET не повертає безпечний стан | E18 | pytest assert + сирі відповіді пристрою, відтворюється автоматично |
