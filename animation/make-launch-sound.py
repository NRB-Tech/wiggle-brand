#!/usr/bin/env python3
"""Make the sound for the launch animation: animation/wiggle-logo-animation.wav.

The sound follows the default motion of wiggle-logo-animation.html:

- a soft, low swell while the line rolls;
- a quiet tone that rises and falls with the sun while the sun is in the air;
- a warm note when the sun lands in the trough;
- six short notes, one for each letter of the name;
- a fade while the overlay goes away.

Run: python3 animation/make-launch-sound.py
The script uses only the standard library and always writes the same file.
"""

import math
import random
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

# G major pentatonic.
G3, G4, A4, B4, D5, E5, G5 = 196.0, 392.0, 440.0, 493.88, 587.33, 659.25, 783.99

count = int(DURATION * RATE)
samples = [0.0] * count


def add_note(start, frequency, level, decay, overtone=0.25):
    """A soft mallet note: the fundamental, a quiet fourth harmonic and a quick attack."""
    first = int(start * RATE)
    for i in range(first, count):
        t = (i - first) / RATE
        attack = min(1.0, t / 0.004)
        body = math.sin(2 * math.pi * frequency * t) * math.exp(-t / decay)
        ring = overtone * math.sin(2 * math.pi * frequency * 4 * t) * math.exp(-t / (decay * 0.25))
        samples[i] += level * attack * (body + ring)


# 1. The roll: a low tone and soft noise. They follow the speed and the sine quantity of the line.
noise = random.Random(7)
low_pass = 0.0
phase = 0.0
for i in range(int(TRAVEL_TIME * RATE)):
    t = i / RATE
    swell = math.sin(math.pi * progress_at(t)) ** 2
    phase += 2 * math.pi * (98.0 + 49.0 * swell) / RATE
    low_pass += 0.05 * (noise.uniform(-1, 1) - low_pass)
    samples[i] += 0.16 * swell * math.sin(phase) + 0.45 * swell * low_pass

# 2. The flick, then the flight of the sun: the pitch follows the height of the sun.
add_note(SUN_LAUNCH, D5, 0.10, 0.05, overtone=0.0)
phase = 0.0
flight = SUN_LAND - SUN_LAUNCH
for i in range(int(SUN_LAUNCH * RATE), int(SUN_LAND * RATE)):
    u = (i / RATE - SUN_LAUNCH) / flight
    height = 4 * u * (1 - u)
    phase += 2 * math.pi * G4 * 2 ** (height * 7 / 12) / RATE
    samples[i] += 0.07 * max(0.0, math.sin(math.pi * u)) ** 0.8 * math.sin(phase)

# 3. The sun lands in the trough.
add_note(SUN_LAND, G3, 0.34, 0.45, overtone=0.1)
add_note(SUN_LAND, G4, 0.22, 0.60)

# 4. One note for each letter, when the letter is almost in its position.
for index, frequency in enumerate([G4, A4, B4, D5, E5, G5]):
    add_note(WORD_START + LETTER_STAGGER * index + 0.12, frequency, 0.15, 0.55)

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
