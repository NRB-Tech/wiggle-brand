#!/usr/bin/env python3
"""Make the sound for the launch animation: animation/wiggle-logo-animation.wav.

The sound follows the default motion of wiggle-logo-animation.html:

- a very quiet, low swell while the line rolls;
- a soft bubble pop when the line flicks the sun up;
- a lower, rounder pop when the sun lands in the trough;
- six small bubble pops, one for each letter of the name;
- a fade while the overlay goes away.

The pops are not notes of a scale, so the sound does not become a tune.

Run: python3 animation/make-launch-sound.py
The script uses only the standard library and always writes the same file.
"""

import math
import struct
import wave
from pathlib import Path

RATE = 44100

# The default values of the controls in wiggle-logo-animation.html.
TRAVEL_TIME = 1.5
SUN_RIDE = 130
WORD_START = 1.4
PAUSE = 0.6
LETTER_TIME, LETTER_STAGGER, AWAY_TIME = 0.35, 0.05, 0.3
PERIOD = (870 - 154) + 140

SUN_LAND = TRAVEL_TIME - 0.1
BOUNCE_END = SUN_LAND + 0.22
WORD_END = WORD_START + LETTER_STAGGER * 5 + LETTER_TIME
AWAY_START = max(BOUNCE_END + 0.3, WORD_END) + PAUSE
DURATION = AWAY_START + AWAY_TIME


def travel_ease(u):
    return u * u * u * (u * (6 * u - 15) + 10)


def progress_at(t):
    return travel_ease(min(1.0, max(0.0, t / TRAVEL_TIME)))


def sun_launch_time():
    lo, hi = 0.0, TRAVEL_TIME
    for _ in range(40):
        mid = (lo + hi) / 2
        if PERIOD * progress_at(mid) < SUN_RIDE:
            lo = mid
        else:
            hi = mid
    return lo


SUN_LAUNCH = sun_launch_time()

count = int(DURATION * RATE)
samples = [0.0] * count


def add_pop(start, frequency, level, rise=0.8, length=0.045):
    """A soft bubble pop: a short sine tone. Its pitch goes up while its level goes down."""
    first = int(start * RATE)
    phase = 0.0
    for i in range(first, min(count, first + int(length * 6 * RATE))):
        t = (i - first) / RATE
        phase += 2 * math.pi * frequency * (1 + rise * min(1.0, t / length)) / RATE
        attack = min(1.0, t / 0.006)
        samples[i] += level * attack * math.exp(-t / (length * 0.6)) * math.sin(phase)


# 1. The roll: a very quiet, low tone that follows the sine quantity of the line.
phase = 0.0
for i in range(int(TRAVEL_TIME * RATE)):
    swell = math.sin(math.pi * progress_at(i / RATE)) ** 2
    phase += 2 * math.pi * (98.0 + 30.0 * swell) / RATE
    samples[i] += 0.07 * swell * math.sin(phase)

# 2. The line flicks the sun up: one bubble pop. The sun makes no sound in the air.
add_pop(SUN_LAUNCH, 520.0, 0.46, rise=1.0, length=0.05)

# 3. The sun lands in the trough: a lower, rounder pop, then a small one for the bounce.
add_pop(SUN_LAND, 210.0, 0.50, rise=0.5, length=0.09)
add_pop(BOUNCE_END, 300.0, 0.12, rise=0.5, length=0.05)

# 4. One small pop for each letter, when the letter is almost in its position.
# The pitches go up and down irregularly, as bubbles do.
for index, frequency in enumerate([640.0, 820.0, 710.0, 930.0, 780.0, 1010.0]):
    add_pop(WORD_START + LETTER_STAGGER * index + 0.12, frequency, 0.20, rise=0.9, length=0.035)

# 5. The overlay goes away: fade to silence. Then set the peak to -3 dBFS.
for i in range(int(AWAY_START * RATE), count):
    left = 1 - (i / RATE - AWAY_START) / AWAY_TIME
    samples[i] *= max(0.0, left) ** 2
peak = max(abs(value) for value in samples)
gain = 10 ** (-3 / 20) / peak

target = Path(__file__).with_name("wiggle-logo-animation.wav")
with wave.open(str(target), "wb") as out:
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(RATE)
    out.writeframes(b"".join(struct.pack("<h", round(value * gain * 32767)) for value in samples))
print(f"{target.name}: {DURATION:.2f} s, sun launch {SUN_LAUNCH:.2f} s, sun land {SUN_LAND:.2f} s")
