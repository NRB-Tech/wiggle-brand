# Logo sound auditions

Original, synthesised backing sounds for the default 2.9-second logo
animation. All start at animation time zero.

- `wiggle-logo-playful.wav`: a soft air sweep under the roll, rounded pops
  for the flick and landing, small letter pops and a quiet exit sweep.
- `wiggle-logo-minimal.wav`: quieter air under the roll, a brief brush at
  the flick, one subdued landing and a faint breath under the name and exit.

Nick chose a third sound on 10 November 2026: a gentle pop for the flick, a
soft thump for the landing and six wooden knocks that go up a scale, one for
each letter. It is now the reference sound, `../wiggle-logo-animation.wav`,
made by `../make-launch-sound.py`, and the apps play it (US-XPLAT-010). The
two files here stay as auditions.

To hear an audition with the motion, open the reference page with its path:
`wiggle-logo-animation.html?sound=sound-design/wiggle-logo-playful.wav`.

Both files are stereo 48 kHz, 16-bit PCM WAV. The minimal version is
deliberately quieter; compare them at the same playback volume. Their timings
match the reference page's defaults, not arbitrary changes to its sliders.

Regenerate with `python3 animation/sound-design/make-backing-sounds.py`.
The generator uses the Python standard library and fixed noise seeds; it
contains no third-party recordings. These are audition assets.
