# Device Requirements

1. `PING` → valid JSON with `status=OK`.
2. `STATUS` → valid JSON containing current LED/PWM state and heap.
3. `GET TEMP` → valid JSON; either valid temperature or explicit sensor error.
4. `SET LED ON/OFF` → output state changes accordingly.
5. `SET PWM N` accepts every integer from 0 through 100 inclusive.
6. PWM values outside 0..100 return `INVALID_VALUE`.
7. `RESET` restores safe output state: LED/PWM OFF/0.
8. Unknown commands return structured `UNKNOWN_COMMAND`.
9. Automation must never wait forever: communication uses a finite timeout.
10. A failed autotest is evidence of a mismatch, not automatic proof of a firmware defect.

скачати та розгорнути енваермент для тестового фреймворку.
Підключити Python до Wokwi.
Запустити готовий набір тестів: python -m pytest -v.
Для кожного FAIL визначити причину. Це може бути:
помилка самого тесту;
середовище;
зв'язок (communication);
вимога;
дефект прошивки.
Додати щонайменше 5 власних параметризованих тестів на межові та негативні значення.
Перевірити поведінку при timeout.
Додати контрольований precondition і cleanup, наприклад через fixture з RESET до і після тесту.
Зберегти докази (лог, вивід pytest) для кожного підтвердженого дефекту прошивки.
Оформити короткий Test Summary.
