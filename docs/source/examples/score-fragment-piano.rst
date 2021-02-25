Score fragment, piano
=====================

..

----

Here's one way of modeling piano music with a bit of polyphony in the left hand.

Make an empty score:

::

    >>> rh_voice = abjad.Voice(name="RH_Voice")
    >>> rh_staff = abjad.Staff([rh_voice], name="RH_Staff")
    >>> lh_voice_1 = abjad.Voice(name="LH_Voice_1")
    >>> lh_voice_2 = abjad.Voice(name="LH_Voice_2")
    >>> lh_staff = abjad.Staff(name="LH_Staff", simultaneous=True)
    >>> lh_staff.extend([lh_voice_1, lh_voice_2])
    >>> piano_staff = abjad.StaffGroup(lilypond_type="PianoStaff", name="Piano_Staff")
    >>> piano_staff.extend([rh_staff, lh_staff])
    >>> score = abjad.Score([piano_staff], name="Score")

Type LilyPond input:

::

    >>> rh = r"""
    ...     a'8 \pp [ ( g' f' e' ] d'4 )
    ...     g'8 \mp [ ( f' e' d' ] c'8 \< d'16 e' f'8 e' \! d'2 \> ~ d' \! )
    ... """
    >>> lh_1 = r"s1 * 2/4 s1 * 3/4 s1 * 2/4 \voiceOne b2 ~ b"
    >>> lh_2 = r"""
    ...     b4 d'8 \pp [ ( c' b a ] af4 )
    ...     c'8 \mp [ ( bf a g ] fs g16 a16 \voiceTwo b4 a g2 )
    ... """

Extend the voices:

::

    >>> rh_voice.extend(rh)
    >>> lh_voice_1.extend(lh_1)
    >>> lh_voice_2.extend(lh_2)

Attach time signatures:

::

    >>> time_signature = abjad.TimeSignature((2, 4))
    >>> note = abjad.select(rh_voice).note(0)
    >>> abjad.attach(time_signature, note)
    >>> time_signature = abjad.TimeSignature((3, 4))
    >>> note = abjad.select(rh_voice).note(4)
    >>> abjad.attach(time_signature, note)
    >>> time_signature = abjad.TimeSignature((2, 4))
    >>> note = abjad.select(rh_voice).note(9)
    >>> abjad.attach(time_signature, note)

Attach a clef and final bar line:

::

    >>> clef = abjad.Clef("bass")
    >>> note = abjad.select(lh_voice_2).note(0)
    >>> abjad.attach(clef, note)
    >>> bar_line = abjad.BarLine("|.")
    >>> note = abjad.select(lh_voice_2).note(-1)
    >>> abjad.attach(bar_line, note)

Override LilyPond's hairpin formatting:

::

    >>> note = abjad.select(rh_voice).note(-2)
    >>> abjad.override(note).hairpin.to_barline = False
    >>> abjad.show(score)

:author:`[Adán (1.1), Bača (3.2); ex. Béla Bartók, "Wandering," Mikrokosmos, vol. III]`
