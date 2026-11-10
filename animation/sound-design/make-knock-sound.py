#!/usr/bin/env python3
"""Make an audition sound for the launch animation: wiggle-logo-knock.wav.

The sound follows the default motion of ../wiggle-logo-animation.html and has
only three parts. The roll of the line is silent.

- The flick: one gentle pop when the line flicks the sun up. Its pitch goes up
  from G4 to E5, as the sun does.
- The landing: a soft, low thump with a warm C4 and G4 mallet tone, when the
  sun lands in the trough. A much quieter thump follows for the bounce.
- The name: six wooden knocks, one for each letter, that go up the C major
  pentatonic scale from C5 to C6 and move a little from left to right.

All pitches come from one scale, so the parts agree, and the last knock is the
octave of the first, so the sound ends at rest.

Run: python3 animation/sound-design/make-knock-sound.py
The script uses only the standard library and a fixed noise seed, so it always
writes the same file.
"""

import math
import random
import struct
import wave
from pathlib import Path

RATE = 48000

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

# A letter makes its knock when it is almost in its position.
LETTER_KNOCK = 0.15

C4, G4, C5, D5, E5, G5, A5, C6 = 261.63, 392.00, 523.25, 587.33, 659.25, 783.99, 880.00, 1046.50
LETTER_PITCHES = [C5, D5, E5, G5, A5, C6]


def travel_ease(u):
    return u * u * u * (u * (6 * u - 15) + 10)


def sun_launch_time():
    lo, hi = 0.0, TRAVEL_TIME
    for _ in range(40):
        mid = (lo + hi) / 2
        if PERIOD * travel_ease(mid / TRAVEL_TIME) < SUN_RIDE:
            lo = mid
        else:
            hi = mid
    return lo


SUN_LAUNCH = sun_launch_time()

count = int(DURATION * RATE)
left = [0.0] * count
right = [0.0] * count
noise = random.Random(20261110)


def write(start, length, pan, voice):
    """Add voice(t) from `start` for `length` seconds. Pan is from -1 (left) to 1 (right)."""
    first = int(start * RATE)
    angle = (pan + 1) * math.pi / 4
    gain_left, gain_right = math.cos(angle), math.sin(angle)
    for i in range(first, min(count, first + int(length * RATE))):
        value = voice((i - first) / RATE)
        left[i] += gain_left * value
        right[i] += gain_right * value


def fade_in(t, time):
    return math.sin(0.5 * math.pi * min(1.0, t / time)) ** 2


def soft_noise(cutoff):
    """Noise through a one-pole low-pass filter, so it has no hiss."""
    keep = math.exp(-2 * math.pi * cutoff / RATE)
    state = [0.0]

    def sample():
        state[0] = keep * state[0] + (1 - keep) * noise.uniform(-1, 1)
        return state[0]
    return sample


def glide_voice(start_pitch, end_pitch, glide_time, level, fade, decay, octave=0.0):
    """A sine tone whose pitch moves from start_pitch to end_pitch."""
    phase = [0.0]

    def voice(t):
        pitch = end_pitch + (start_pitch - end_pitch) * math.exp(-t / glide_time)
        phase[0] += 2 * math.pi * pitch / RATE
        tone = math.sin(phase[0]) + octave * math.sin(2 * phase[0])
        return level * fade_in(t, fade) * math.exp(-t / decay) * tone
    return voice


def knock_voice(pitch, level):
    """A small wooden knock, as a marimba bar makes.

    The fundamental stops quickly. A partial two octaves above it and a 3 ms tick of
    soft noise give the strike. The level comes in during 2 ms, so there is no click.
    """
    phase = [0.0]
    tick = soft_noise(5000)

    def voice(t):
        phase[0] += 2 * math.pi * pitch * (1 + 0.06 * math.exp(-t / 0.006)) / RATE
        body = math.sin(phase[0]) * math.exp(-t / 0.060)
        bar = 0.22 * math.sin(4 * phase[0]) * math.exp(-t / 0.014)
        strike = 0.5 * tick() * math.exp(-t / 0.003)
        return level * fade_in(t, 0.002) * (body + bar + strike)
    return voice


def landing_voice(level):
    """A soft thump: a low tone that goes down, a puff of soft noise and a warm mallet tone."""
    thump = glide_voice(170.0, 95.0, 0.030, 1.0, 0.004, 0.090)
    puff = soft_noise(700)
    phase = [0.0]

    def voice(t):
        phase[0] += 2 * math.pi * C4 / RATE
        mallet = (0.50 * math.sin(phase[0]) + 0.22 * math.sin(1.5 * phase[0])) * math.exp(-t / 0.200)
        return level * (thump(t) + fade_in(t, 0.005) * (mallet + 1.6 * puff() * math.exp(-t / 0.030)))
    return voice


# 1. The line flicks the sun up: one gentle pop. Its pitch goes up quickly.
write(SUN_LAUNCH, 0.40, -0.10, glide_voice(G4, E5, 0.022, 0.42, 0.006, 0.050, octave=0.12))

# 2. The sun lands in the trough, then makes one small bounce.
write(SUN_LAND, 1.20, 0.0, landing_voice(0.50))
write(BOUNCE_END, 0.60, 0.0, glide_voice(150.0, 100.0, 0.030, 0.10, 0.005, 0.070))

# 3. One knock for each letter. The knocks go up the scale and become a little louder.
for index, pitch in enumerate(LETTER_PITCHES):
    start = WORD_START + LETTER_STAGGER * index + LETTER_KNOCK
    write(start, 0.50, -0.30 + 0.12 * index, knock_voice(pitch, 0.26 + 0.02 * index))

# 4. A small room: a few quiet, early echoes, different for each ear.
def with_room(dry, other, taps):
    wet = list(dry)
    for delay, level in taps:
        shift = int(delay * RATE)
        for i in range(shift, count):
            wet[i] += level * 0.5 * (dry[i - shift] + other[i - shift])
    return wet


left, right = (
    with_room(left, right, [(0.019, 0.16), (0.043, 0.10), (0.071, 0.06)]),
    with_room(right, left, [(0.023, 0.16), (0.037, 0.10), (0.079, 0.06)]),
)

# 5. The overlay goes away: fade to silence. Then set the peak to -6 dBFS.
for i in range(int(AWAY_START * RATE), count):
    remain = max(0.0, 1 - (i / RATE - AWAY_START) / AWAY_TIME) ** 2
    left[i] *= remain
    right[i] *= remain
peak = max(max(abs(value) for value in left), max(abs(value) for value in right))
gain = 10 ** (-6 / 20) / peak

target = Path(__file__).with_name("wiggle-logo-knock.wav")
with wave.open(str(target), "wb") as out:
    out.setnchannels(2)
    out.setsampwidth(2)
    out.setframerate(RATE)
    out.writeframes(b"".join(
        struct.pack("<hh", round(a * gain * 32767), round(b * gain * 32767)) for a, b in zip(left, right)
    ))
print(f"{target.name}: {DURATION:.2f} s, sun launch {SUN_LAUNCH:.2f} s, sun land {SUN_LAND:.2f} s, "
      f"knocks {WORD_START + LETTER_KNOCK:.2f} to {WORD_START + LETTER_STAGGER * 5 + LETTER_KNOCK:.2f} s")
