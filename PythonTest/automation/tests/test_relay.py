def test_led_on_off(device):
    assert device.command("SET LED ON")["led"] is True
    assert device.command("SET LED OFF")["led"] is False

