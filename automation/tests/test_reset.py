def test_reset_restores_set_led_on(device):
    device.command("SET LED ON")
    device.command("RESET")
    status = device.command("STATUS")
    assert status["led"] is False

def test_reset_restores_set_pwm(device):
    device.command("SET PWM 5")
    device.command("RESET")
    status = device.command("STATUS")
    assert status["pwm"] == 0
  