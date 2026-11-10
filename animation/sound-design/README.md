# Logo sound auditions

Original, synthesised backing sounds for the default 2.9-second logo
animation. All start at animation time zero.

- `wiggle-logo-playful.wav`: a soft air sweep under the roll, rounded pops
  for the flick and landing, small letter pops and a quiet exit sweep.
- `wiggle-logo-minimal.wav`: quieter air under the roll, a brief brush at
  the flick, one subdued landing and a faint breath under the name and exit.

A third audition, `wiggle-logo-knock.wav`, has no sound for the roll or the
exit: a gentle pop that goes up for the flick, a soft thump with a warm mallet
tone for the landing, and six wooden knocks that go up the C major pentatonic
scale, one for each letter. Regenerate it with
`python3 animation/sound-design/make-knock-sound.py`.

To hear an audition with the motion, open the reference page with its path:
`wiggle-logo-animation.html?sound=sound-design/wiggle-logo-knock.wav`.

All files are stereo 48 kHz, 16-bit PCM WAV. The minimal version is
deliberately quieter; compare them at the same playback volume. Their timings
match the reference page's defaults, not arbitrary changes to its sliders.

Regenerate with `python3 animation/sound-design/make-backing-sounds.py`.
The generator uses the Python standard library and fixed noise seeds; it
contains no third-party recordings. These are audition assets. The existing
reference soundtrack and app playback are unchanged.
