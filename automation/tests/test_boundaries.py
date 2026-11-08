import pytest

@pytest.mark.parametrize("value", [0, 1, 50, 99, 100])
def test_pwm_valid_boundaries(device, value):
    r = device.command(f"SET PWM {value}")
    assert r["status"] == "OK"
    assert r["pwm"] == value

@pytest.mark.parametrize("value", [1, 99])
def test_pwm_saved_valid_boundaries(device, value):
    device.command(f"SET PWM {value}")
    r = device.command(f"STATUS")
    assert r["status"] == "OK"
    assert r["pwm"] == value

@pytest.mark.parametrize("value", [-1, 101, 999])
def test_pwm_invalid_boundaries(device, value):
    r = device.command(f"SET PWM {value}")
    assert r["status"] == "ERROR"
    assert r["code"] == "INVALID_VALUE"

@pytest.mark.parametrize("value", ["aa", "1.5", "$#@!%^^&"])
def test_pwm_malformed_values(device, value):
    r = device.command(f"SET PWM {value}")
    assert r["status"] == "ERROR"
    assert r["code"] == "INVALID_VALUE"

def test_pwm_empty_values(device):
    r = device.command(f"SET PWM  ")
    assert r["status"] == "ERROR"
    assert r["code"] == "UNKNOWN_COMMAND"
