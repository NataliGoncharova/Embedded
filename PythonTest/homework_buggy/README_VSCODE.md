# PlatformIO / VS Code project

## Build and upload
1. Install Visual Studio Code and the PlatformIO IDE extension.
2. Open this folder (the one containing `platformio.ini`) in VS Code.
3. Connect an ESP32 DevKit board over USB and select its COM port if needed.
4. In the PlatformIO sidebar, run **Build**. For a physical board, run **Upload**.
5. Open **Monitor** at 115200 baud. Close Serial Monitor before running Python tests against the same COM port.

## Wokwi
The project includes `diagram.json` and `wokwi.toml` for use with the Wokwi VS Code extension. Build the project first, then start the Wokwi simulation. The DHT22 is connected to GPIO15 (`esp:D15`); the LED is connected to GPIO2 (`esp:D2`).

## Python automation
The Python tests in the parent `automation/` folder use `DEVICE_PORT` and PySerial. With Wokwi, the running simulation exposes its serial port at `rfc2217://localhost:4000` (see `wokwi.toml`): set `DEVICE_PORT=rfc2217://localhost:4000` and run the tests while the simulation is running. With a physical ESP32, set `DEVICE_PORT` to its COM port.
