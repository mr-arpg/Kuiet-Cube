# Kuiet Cube

A collaborative project between **NOVA SBE** and **KPMG** to design and build a dedicated space for **meditation and deep focus** on campus.

The Kuiet Cube is a quiet room where lighting and ambience respond to presence — helping people step out of distraction and into a calmer, more focused state. This repository contains the embedded firmware, 3D-printable hardware, and project media for the presence-sensing lighting system used inside the cube.

## Overview

The room uses **contactless presence detection** instead of switches or motion buttons. When someone enters the cube, ambient lighting turns on automatically; when the space is empty, lights fade off to save energy and preserve a restful atmosphere.

| Component | Role |
|-----------|------|
| **ESP32** | Main controller |
| **HLK-LD2410** | 24 GHz mmWave radar for presence detection |
| **WS2811 LED strip** | Ambient lighting (13 LEDs) |
| **3D-printed enclosure** | Desk-mounted sensor housing |

## Project structure

```
├── src/                    # Firmware (PlatformIO / Arduino)
├── scripts/                # Serial plotting & development tools
├── hardware/stl/           # 3D-printable parts for the sensor enclosure
├── docs/media/photos/      # Installation and hardware photos
└── docs/media/videos/      # Room demo footage
```

## Hardware — 3D models

Print files are in [`hardware/stl/`](hardware/stl/):

| File | Description |
|------|-------------|
| `esp32-box-top.stl` | Top half of the ESP32 enclosure |
| `esp32-boxbottom.stl` | Bottom half of the ESP32 enclosure |
| `suporte.stl` | Mount / bracket for desk installation |
| `tampa.stl` | Lid / cover |

See [`docs/media/photos/sensor_enclosure_3Dmodel.png`](docs/media/photos/sensor_enclosure_3Dmodel.png) for a render of the assembled enclosure.

## Firmware

Built with [PlatformIO](https://platformio.org/) for **ESP32**.

### Build environments

| Environment | Source | Purpose |
|-------------|--------|---------|
| `app` | `src/main.cpp` | Production firmware — presence → LED on/off |
| `radar_test` | `src/radar_test.cpp` | Radar diagnostics & serial plotting |
| `led_test` | `src/led_test.cpp` | LED strip verification |

### Quick start

```bash
# Install PlatformIO, then from the repo root:
pio run -e app
pio run -e app -t upload
pio device monitor
```

### Wiring (default)

| Signal | ESP32 pin |
|--------|-----------|
| Radar TX → ESP RX | GPIO 16 |
| Radar RX → ESP TX | GPIO 17 |
| LED data | GPIO 5 |

Radar UART: **256000 baud**. Monitor/debug serial: **115200 baud**.

### Live radar plot (development)

```bash
pip install -r scripts/requirements-plot.txt
pio run -e radar_test -t upload
python scripts/plot_radar_serial.py COM7   # adjust port
```

## Media

- **Photos** — [`docs/media/photos/`](docs/media/photos/)
- **Videos** — [`docs/media/videos/demo_room.mp4`](docs/media/videos/demo_room.mp4)

## Partners

- [NOVA SBE](https://www.novasbe.unl.pt/) — Business school partner & project host
- [KPMG](https://home.kpmg/) — Collaboration on the Kuiet Cube initiative

## License

Unless otherwise noted, project materials are shared for reference and educational use. Contact the maintainers before commercial reuse.
