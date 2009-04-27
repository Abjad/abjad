Pitch conventions
=================

Abjad follows the following conventions regarding pitch.



Names
-----

Abjad names pitches according to the LilyPond `english.ly` module.

Abjad names accidentals according to the table below.
quarter sharp 'qs' quarter flat 'qf' sharp 's' flat 'f' three-quarters
sharp 'tqs' three-quarters flat 'tqf' double sharp 'ss' double flat
'ff'


Numbers
-------

Abjad sets middle C equal to 0. This follows the presentation of
American pitch-class theory in, for example, Morris [1978].

IRCAM / MIDI pitch numbers equal Abjad pitch numbers plus 60.



Octaves
-------

Abjad represents octaves with both numbers and ticks.
C7 c'''' C6 c''' C5 c'' C4 c' C3 c C2 c, C1 c,,
Abjad sets the octave of middle C equal to 4. This follows American
usage.

Abjad uses ticks in LilyPond output only.



Accidentals
-----------

Abjad chooses between enharmonic spellings at pitch-initialization
time according to the following table.
0 → C 1 → C♯ 2 → D 3 → E♭ 4 → E 5 → F 6 → F♯ 7 →
G 8 → G♭ 9 → A 10 → B♭ 11 → B

