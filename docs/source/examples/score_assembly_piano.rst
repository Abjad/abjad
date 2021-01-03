Score assembly, piano
=====================

This example reconstructs the last five measures of Bartók's "Wandering" from
*Mikrokosmos*, volume III. The example covers the basics of modeling a preexisting
fragment of music in Abjad.

First let's create an empty score:

::

    >>> score = abjad.Score(name="Score")
    >>> piano_staff = abjad.StaffGroup(lilypond_type="PianoStaff", name="Piano_Staff")
    >>> upper_staff = abjad.Staff(name="Upper_Staff")
    >>> lower_staff = abjad.Staff(name="Lower_Staff")
    >>> upper_staff_voice = abjad.Voice(name="Upper_Staff_Voice")
    >>> lower_staff_voice_2 = abjad.Voice(name="Lower_Staff_Voice_2")
    >>> upper_staff.append(upper_staff_voice)
    >>> lower_staff.append(lower_staff_voice_2)
    >>> piano_staff.extend([upper_staff, lower_staff])
    >>> score.append(piano_staff)

Now let's add notes to the upper staff:

::

    >>> upper_staff_voice.extend(r"\time 2/4 a'8 g'8 f'8 e'8")
    >>> upper_staff_voice.extend(r"\time 3/4 d'4 g'8 f'8 e'8 d'8")
    >>> upper_staff_voice.extend(r"\time 2/4 c'8 d'16 e'16 f'8 e'8")
    >>> upper_staff_voice.extend("d'2 d'2")
    >>> abjad.show(score)

Then to the monophonic part of the lower staff:

::

    >>> lower_staff_voice_2.extend("b4 d'8 c'8")
    >>> lower_staff_voice_2.extend("b8 a8 af4 c'8 bf8")
    >>> lower_staff_voice_2.extend("a8 g8 fs8 g16 a16")
    >>> abjad.show(score)

The polyphony in the final measures requires a simultaneous container:

::

    >>> voice_1 = abjad.Voice("b2 b2", name="Lower_Staff_Voice_1")
    >>> voice_2 = abjad.Voice("b4 a4 g2", name="Lower_Staff_Voice_2")
    >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
    >>> abjad.attach(literal, voice_1[0])
    >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
    >>> abjad.attach(literal, voice_2[0])
    >>> container = abjad.Container([voice_1, voice_2], simultaneous=True)
    >>> lower_staff.append(container)
    >>> abjad.show(score)

It will help to store the contents of each voice is a list before adding details to the
score. This effectively flattens out the polyphonic structure of the excerpt and makes
our score easier to work with. Notice that the only voice in the upper staff runs the
full length of the excerpt. So does voice 2 in the lower staff. But voice 1 in the lower
staff is only two measures long:

::

    >>> upper_staff_notes = abjad.select(upper_staff).notes()

::

    >>> lower_staff_voice_2_notes = []
    >>> for note in abjad.select(lower_staff).notes():
    ...     voice = abjad.get.parentage(note).get(abjad.Voice)
    ...     if voice.name == "Lower_Staff_Voice_2":
    ...         lower_staff_voice_2_notes.append(note)
    ...

::

    >>> lower_staff_voice_1_notes = []
    >>> for note in abjad.select(lower_staff).notes():
    ...     voice = abjad.get.parentage(note).get(abjad.Voice)
    ...     if voice.name == "Lower_Staff_Voice_1":
    ...         lower_staff_voice_1_notes.append(note)
    ...

The bottom staff has a treble clef just like the top staff. Let's change that, and add a
double bar to the end of the score:

::

    >>> clef = abjad.Clef("bass")
    >>> note = lower_staff_voice_2_notes[0]
    >>> abjad.attach(clef, note)
    >>> note = lower_staff_voice_2_notes[-1]
    >>> bar_line = abjad.BarLine("|.")
    >>> abjad.attach(bar_line, note)
    >>> abjad.show(score)

Now let's attach dynamics:

::

    >>> abjad.attach(abjad.Dynamic("pp"), upper_staff_notes[0])
    >>> abjad.attach(abjad.Dynamic("mp"), upper_staff_notes[5])
    >>> abjad.attach(abjad.Dynamic("pp"), lower_staff_voice_2_notes[1])
    >>> abjad.attach(abjad.Dynamic("mp"), lower_staff_voice_2_notes[6])
    >>> abjad.override(upper_staff).dynamic_line_spanner.staff_padding = 2
    >>> abjad.override(lower_staff).dynamic_line_spanner.staff_padding = 3
    >>> abjad.show(score)

Notice that the beams of the eighth and sixteenth notes appear as you would usually
expect: grouped by beat. We get this for free thanks to LilyPond's default beaming
algorithm. But this is not the way Bartók notated the beams. Let's set the beams as
Bartók did with some crossing the bar lines:

::

    >>> abjad.beam(upper_staff_notes[:4])
    >>> abjad.beam(lower_staff_voice_2_notes[1:5])
    >>> abjad.beam(lower_staff_voice_2_notes[6:10])
    >>> abjad.show(score)

Now we add slurs:

::

    >>> abjad.slur(upper_staff_notes[:5])
    >>> abjad.slur(upper_staff_notes[5:])
    >>> abjad.slur(lower_staff_voice_2_notes[1:6])
    >>> abjad.slur(lower_staff_voice_2_notes[-10:])
    >>> note = lower_staff_voice_2_notes[-10]
    >>> abjad.override(note).slur.direction = abjad.Down
    >>> abjad.show(score)

And hairpins:

::

    >>> abjad.hairpin("< !", upper_staff_notes[-7:-2])
    >>> abjad.hairpin("> !", upper_staff_notes[-2:])
    >>> note = upper_staff_notes[-7]
    >>> abjad.override(note).dynamic_line_spanner.staff_padding = 4.5
    >>> note = upper_staff_notes[-2]
    >>> abjad.override(note).dynamic_line_spanner.staff_padding = 4.5
    >>> abjad.override(note).hairpin.to_barline = False
    >>> abjad.show(score)

And a text spanner for the ritardando:

::

    >>> markup = abjad.Markup("ritard.")
    >>> start_text_span = abjad.StartTextSpan(left_text=markup)
    >>> abjad.text_spanner(
    ...     upper_staff_notes[-7:],
    ...     start_text_span=start_text_span
    >>> )
    >>> abjad.override(upper_staff_notes[-7]).text_spanner.staff_padding = 2
    >>> abjad.show(score)

Finally, we tie the last two notes in each staff:

::

    >>> abjad.tie(upper_staff_notes[-2:])
    >>> abjad.tie(lower_staff_voice_1_notes)
    >>> abjad.show(score)
