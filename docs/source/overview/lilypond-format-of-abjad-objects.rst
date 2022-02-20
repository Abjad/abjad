LilyPond format, of Abjad objects
=================================

..

----

Many Abjad objects can be transformed into LilyPond input:

::

    >>> string = r"\tuplet 3/2 { gs''32 \sfp ( b'' cs''' } b''4.. \trill )"
    >>> voice_1 = abjad.Voice(4 * string, name="Voice_1")
    >>> note = abjad.select.note(voice_1, 0)
    >>> key_signature = abjad.KeySignature("e", "major")
    >>> abjad.attach(key_signature, note)
    >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
    >>> abjad.attach(literal, note)
    >>> literal = abjad.LilyPondLiteral(r"\dynamicUp")
    >>> abjad.attach(literal, note)
    >>> string = r"""
    ...     r4 \tuplet 3/2 { b'32 \sfp ( e'' fs'' } e''4.. \trill )
    ...     \tuplet 3/2 { b'32 \sfp ( e'' fs'' } e''8. ~ \trill )
    ...     e''4 \tuplet 3/2 { b'32 \sfp ( fs'' gs'' } fs''4.. \trill )
    ...    \tuplet 3/2 { b'32 \sfp ( fs'' gs'' } fs''8. \trill )"""
    >>> voice_2 = abjad.Voice(string, name="Voice_2")
    >>> abjad.override(voice_2).script.direction = "#down"
    >>> abjad.override(voice_2).slur.direction = "#down"
    >>> abjad.override(voice_2).tie.direction = "#down"
    >>> abjad.override(voice_2).tuplet_bracket.stencil = "##f"
    >>> staff = abjad.Staff([voice_1, voice_2], name="Example_Staff", simultaneous=True)
    >>> score = abjad.Score([staff], name="Example_Score")
    >>> abjad.show(score)

Here's LilyPond input for the score above:

::

    >>> string = abjad.lilypond(score)
    >>> print(string)

Here's LilyPond input for just voice 1:

::

    >>> string = abjad.lilypond(voice_1)
    >>> print(string)

Here's LilyPond input for the very first note:

::

    >>> note = abjad.select.note(score, 0)
    >>> string = abjad.lilypond(note)
    >>> print(string)

----

**Discussion.**

* The output of :func:`abjad.lilypond` is a string.

* Indentation (4 spaces per level) shows container nesting.

:author:`[Bača (3.2); ex. Gustav Mahler, Symphony 6, movt III, 3 after 94.]`
