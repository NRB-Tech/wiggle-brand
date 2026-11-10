# Logo sound auditions

Two original, synthesised backing sounds for the default 2.9-second logo
animation. Both start at animation time zero.

- `wiggle-logo-playful.wav`: a soft air sweep under the roll, rounded pops
  for the flick and landing, small letter pops and a quiet exit sweep.
- `wiggle-logo-minimal.wav`: quieter air under the roll, a brief brush at
  the flick, one subdued landing and a faint breath under the name and exit.

Both files are stereo 48 kHz, 16-bit PCM WAV. The minimal version is
deliberately quieter; compare them at the same playback volume. Their timings
match the reference page's defaults, not arbitrary changes to its sliders.

Regenerate with `python3 animation/sound-design/make-backing-sounds.py`.
The generator uses the Python standard library and fixed noise seeds; it
contains no third-party recordings. These are audition assets. The existing
reference soundtrack and app playback are unchanged.
