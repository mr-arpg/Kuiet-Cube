#!/usr/bin/env python3
"""
Lê linhas PLOT do firmware (radar_test) na porta serial e mostra distâncias em tempo real.

Uso (Windows):  python plot_radar_serial.py COM7
Linux/Mac:      python plot_radar_serial.py /dev/ttyUSB0

Antes: pip install -r scripts/requirements-plot.txt
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import deque

try:
    import serial
except ImportError:
    print("Instala: pip install -r scripts/requirements-plot.txt", file=sys.stderr)
    raise

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
except ImportError:
    print("Instala: pip install -r scripts/requirements-plot.txt", file=sys.stderr)
    raise

PLOT_RE = re.compile(
    r"^PLOT,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*([01])\s*,\s*([01])\s*$"
)
BAUD_DEFAULT = 115200
MAX_POINTS = 250


def open_serial(port: str, baud: int) -> serial.Serial:
    return serial.Serial(port, baud, timeout=0.05)


def main() -> None:
    p = argparse.ArgumentParser(description="Gráfico em tempo real do LD2410 via serial.")
    p.add_argument("port", help="Porta serial, ex. COM7 ou /dev/ttyUSB0")
    p.add_argument("-b", "--baud", type=int, default=BAUD_DEFAULT)
    p.add_argument(
        "-n",
        "--points",
        type=int,
        default=MAX_POINTS,
        help="Amostras no eixo X (janela deslizante).",
    )
    args = p.parse_args()

    ser = open_serial(args.port, args.baud)

    t = deque(maxlen=args.points)
    y_m = deque(maxlen=args.points)
    y_s = deque(maxlen=args.points)
    y_inactive = deque(maxlen=args.points)
    pres = deque(maxlen=args.points)
    conn = deque(maxlen=args.points)
    idx = 0

    fig, ax = plt.subplots(figsize=(10, 5))
    (line_m,) = ax.plot([], [], label="Movimento (cm)", color="tab:blue", linewidth=1.5)
    (line_s,) = ax.plot([], [], label="Estático (cm)", color="tab:orange", linewidth=1.5)

    # Terceiro estado (firmware): radar ligado mas presenceDetected()==false → distâncias -1.
    ax2 = ax.twinx()
    (line_i,) = ax2.plot(
        [],
        [],
        label="Inativo (sem presença)",
        color="tab:purple",
        linewidth=1.8,
        drawstyle="steps-post",
        alpha=0.85,
    )
    ax2.set_ylabel("Inativo (1 = sem alvo, radar OK)")
    ax2.set_ylim(-0.05, 1.05)
    ax2.set_yticks([0, 1])

    ax.set_xlabel("Amostra")
    ax.set_ylabel("Distância (cm)")
    ax.set_title("LD2410 — Serial (linhas PLOT)")
    ax.legend(handles=[line_m, line_s, line_i], loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 600)

    def on_frame(_frame: int):
        nonlocal idx
        while ser.in_waiting:
            raw = ser.readline()
            try:
                line = raw.decode("utf-8", errors="ignore").strip()
            except Exception:
                continue
            m = PLOT_RE.match(line)
            if not m:
                continue
            mv, st, pr, co = m.groups()
            imv, ist = int(mv), int(st)
            ipr, ico = int(pr), int(co)

            t.append(idx)
            y_m.append(imv if imv >= 0 else float("nan"))
            y_s.append(ist if ist >= 0 else float("nan"))
            # Inativo: ligado ao radar mas sem presença (ver radar_test.cpp: presence==0 com conn==1).
            y_inactive.append(1.0 if (ico == 1 and ipr == 0) else 0.0)
            pres.append(ipr)
            conn.append(ico)
            idx += 1

        if len(t) == 0:
            return line_m, line_s, line_i

        xs = list(range(len(y_m)))
        line_m.set_data(xs, list(y_m))
        line_s.set_data(xs, list(y_s))
        line_i.set_data(xs, list(y_inactive))
        ax.set_xlim(0, max(len(y_m) - 1, 1))
        ymax = 50
        for v in list(y_m) + list(y_s):
            if v == v and v >= 0:
                ymax = max(ymax, min(600, v + 20))
        ax.set_ylim(0, ymax)

        if conn and conn[-1] == 0:
            ax.set_facecolor("#fff0f0")
        elif pres and pres[-1] == 1:
            ax.set_facecolor("#f0fff4")
        else:
            ax.set_facecolor("white")

        return line_m, line_s, line_i

    ani = animation.FuncAnimation(
        fig, on_frame, interval=50, blit=False, cache_frame_data=False
    )
    plt.tight_layout()

    def on_close(_event):
        ser.close()

    fig.canvas.mpl_connect("close_event", on_close)

    print(
        "À espera de linhas PLOT na serial… Fecha a janela para sair.",
        file=sys.stderr,
    )
    plt.show()


if __name__ == "__main__":
    main()
