#!/usr/bin/env python3
"""
Periodically press a key through Linux uinput.
Works on Wayland
Tested OS:
    - CachyOS (COSMIC)
    - Arch (UNKNOWN)
"""

import argparse
import time

from evdev import UInput, ecodes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--key",
        default="KEY_SPACE",
        help="Linux key name, such as KEY_SPACE or KEY_A (default: KEY_SPACE)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.01,
        help="Seconds between presses (default: 0.05)",
    )
    parser.add_argument(
        "--countdown",
        type=int,
        default=5,
        help="Seconds to wait before starting (default: 5)",
    )
    args = parser.parse_args()

    key_name = args.key.upper()
    keycode = ecodes.ecodes.get(key_name)
    if keycode is None:
        parser.error(f"unknown key name: {key_name}")
    if args.interval <= 0:
        parser.error("--interval must be greater than zero")

    for remaining in range(args.countdown, 0, -1):
        print(f"Switch to the game — starting in {remaining}…", flush=True)
        time.sleep(1)

    try:
        with UInput(
            events={ecodes.EV_KEY: [keycode]},
            name="Periodic key presser",
        ) as keyboard:
            print(f"Pressing {key_name} every {args.interval}s. Press Ctrl+C to stop.")
            next_press = time.monotonic()

            while True:
                keyboard.write(ecodes.EV_KEY, keycode, 1)
                keyboard.syn()
                keyboard.write(ecodes.EV_KEY, keycode, 0)
                keyboard.syn()

                next_press += args.interval
                time.sleep(max(0, next_press - time.monotonic()))
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
