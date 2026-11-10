#!/usr/bin/env python3
"""Render two original sound-design auditions; standard library only.

Run from any directory. Writes 48 kHz stereo 16-bit WAVs beside this source.
Timing follows the default wiggle-logo-animation.html. No sampled recordings.
"""

import math
import random
import struct
import wave
from pathlib import Path

RATE = 48000
DURATION = 2.9
COUNT = round(RATE * DURATION)
LAND = 1.4
BOUNCE = 1.62


def ease(u):
    return u**3 * (u * (6 * u - 15) + 10)


lo, hi = 0.0, 1.5
for _ in range(48):
    mid = (lo + hi) / 2
    if 856 * ease(mid / 1.5) < 130:
        lo = mid
    else:
        hi = mid
LAUNCH = (lo + hi) / 2


def pan_add(bus, index, value, pan=0.0):
    angle = (pan + 1) * math.pi / 4
    bus[0][index] += value * math.cos(angle)
    bus[1][index] += value * math.sin(angle)


def pop(bus, start, frequency, level, length=0.18, pan=0.0):
    """Rounded pitch bend with a smooth attack and no sharp click."""
    phase = 0.0
    size = round(length * RATE)
    first = round(start * RATE)
    for k in range(min(size, COUNT - first)):
        t = k / RATE
        u = k / (size - 1)
        hz = frequency * (1 + 0.35 * math.exp(-t / 0.032))
        phase += 2 * math.pi * hz / RATE
        attack = math.sin(min(1, t / 0.009) * math.pi / 2) ** 2
        envelope = attack * math.exp(-t / (length / 5)) * (1 - u**4) ** 2
        value = math.sin(phase) + 0.06 * math.sin(2 * phase)
        pan_add(bus, first + k, value * envelope * level, pan)


def air(bus, start, length, level, seed, moving=True):
    """Soft band-limited air; seeded noise, broad envelope, restrained stereo."""
    rng = random.Random(seed)
    low = slow = 0.0
    size = round(length * RATE)
    first = round(start * RATE)
    for k in range(min(size, COUNT - first)):
        u = k / (size - 1)
        cutoff = 420 + 650 * math.sin(math.pi * u) ** 2
        alpha = 1 - math.exp(-2 * math.pi * cutoff / RATE)
        low += alpha * (rng.uniform(-1, 1) - low)
        slow += (1 - math.exp(-2 * math.pi * 160 / RATE)) * (low - slow)
        envelope = math.sin(math.pi * u) ** 2
        pan = 0.24 * math.cos(math.pi * u) if moving else 0.0
        pan_add(bus, first + k, (low - slow) * level * envelope, pan)


def roll(bus, level):
    phase = 0.0
    for i in range(round(1.5 * RATE)):
        progress = ease(i / RATE / 1.5)
        envelope = math.sin(math.pi * progress) ** 2
        phase += 2 * math.pi * (145 + 52 * envelope) / RATE
        pan_add(bus, i, level * envelope * math.sin(phase), 0.12 * (1 - 2 * progress))


def render(style):
    bus = [[0.0] * COUNT for _ in range(2)]
    if style == "playful":
        air(bus, 0.06, 1.42, 0.36, 41)
        roll(bus, 0.032)
        pop(bus, LAUNCH, 490, 0.42, 0.19, -0.17)
        pop(bus, LAND, 340, 0.30, 0.22, 0.05)
        pop(bus, BOUNCE, 430, 0.095, 0.13, 0.05)
        for index, hz in enumerate([460, 575, 510, 640, 550, 690]):
            pop(bus, 1.52 + index * 0.05, hz, 0.10, 0.12, -0.20 + index * 0.08)
        air(bus, 2.48, 0.42, 0.13, 42, moving=False)
    else:
        air(bus, 0.08, 1.44, 0.22, 41)
        roll(bus, 0.019)
        air(bus, LAUNCH - 0.045, 0.23, 0.26, 43)
        pop(bus, LAND, 240, 0.14, 0.20)
        air(bus, 1.49, 0.51, 0.095, 44, moving=False)
        air(bus, 2.48, 0.42, 0.07, 42, moving=False)

    # Short room reflections add softness without a long musical tail.
    dry = [channel[:] for channel in bus]
    for delay, gain in [(0.029, 0.10), (0.047, 0.07), (0.071, 0.035)]:
        offset = round(delay * RATE)
        for channel in range(2):
            for i in range(offset, COUNT):
                bus[channel][i] += dry[1 - channel][i - offset] * gain

    # Equal master gain preserves the intentional level difference between variants.
    for i in range(COUNT):
        fade = min(1.0, max(0.0, (DURATION - i / RATE) / 0.07)) ** 2
        for channel in bus:
            channel[i] *= 1.65 * fade
    peak = max(abs(value) for channel in bus for value in channel)
    assert peak < 0.9, "Leave headroom; never silently clip."
    target = Path(__file__).with_name(f"wiggle-logo-{style}.wav")
    frames = bytearray()
    for left, right in zip(*bus):
        frames.extend(struct.pack("<hh", round(left * 32767), round(right * 32767)))
    with wave.open(str(target), "wb") as out:
        out.setparams((2, 2, RATE, COUNT, "NONE", "not compressed"))
        out.writeframes(frames)
    rms = math.sqrt(sum(v * v for channel in bus for v in channel) / (2 * COUNT))
    print(f"{target.name}: {DURATION:.2f}s, peak {20 * math.log10(peak):.1f} dBFS, RMS {20 * math.log10(rms):.1f} dBFS")


if __name__ == "__main__":
    print(f"Flick {LAUNCH:.3f}s; landing {LAND:.3f}s; bounce {BOUNCE:.3f}s")
    for style in ("playful", "minimal"):
        render(style)
