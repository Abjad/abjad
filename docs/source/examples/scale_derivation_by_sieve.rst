Scale derivation, by sieve
--------------------------

The derivation of nonoctave scales by sieve is a 20th-century technique due to Xenakis.

----

First we define a function to illustrate the examples that follow:

::

    >>> def illustrate_scale(pattern, length, transposition, moment_denominator):
    ...     pitches = abjad.sequence(range(length))
    ...     pitches = pitches.retain_pattern(pattern)
    ...     notes = [abjad.Note(_ + transposition, (1, 16)) for _ in pitches]
    ...     containers = abjad.illustrators.make_piano_score(notes)
    ...     score, treble_staff, bass_staff = containers
    ...     abjad.override(score).BarLine.stencil = False
    ...     abjad.override(score).BarNumber.stencil = False
    ...     abjad.override(score).Beam.stencil = False
    ...     abjad.override(score).Flag.stencil = False
    ...     abjad.override(score).Rest.stencil = False
    ...     abjad.override(score).SpacingSpanner.strict_note_spacing = True
    ...     abjad.override(score).SpanBar.stencil = False
    ...     abjad.override(score).Stem.stencil = False
    ...     abjad.override(score).TimeSignature.stencil = False
    ...     moment = abjad.SchemeMoment((1, moment_denominator))
    ...     abjad.setting(score).proportional_notation_duration = moment
    ...     lilypond_file = abjad.LilyPondFile(
    ...         items=[
    ...             score,
    ...             abjad.Block(name="layout"),
    ...         ],
    ...         global_staff_size=16,
    ...     )
    ...     lilypond_file.layout_block.items.append("indent = 0")
    ...     return lilypond_file

----

**Jonchaies.** The sieve underlying Xenakis's orchestra piece *Jonchaies*
(1977) structures a series of 8 consecutive intervals that repeat every 17 semitones.

First three elements of sieve:

::

    >>> first_half = abjad.Pattern(indices=[0, 1, 4], period=17)
    >>> lilypond_file = illustrate_scale(first_half, 56, -15, 25)
    >>> abjad.show(lilypond_file)

Remainder of sieve:

::

    >>> second_half = abjad.Pattern(indices=[5, 7, 11, 12, 16], period=17)
    >>> lilypond_file = illustrate_scale(second_half, 56, -15, 25)
    >>> abjad.show(lilypond_file)

Complete sieve:

::

    >>> sieve = first_half | second_half
    >>> lilypond_file = illustrate_scale(sieve, 56, -15, 25)
    >>> abjad.show(lilypond_file)

Non-octave scale in Joel Hoffman's **Piano Concerto**:

::

    >>> scale = abjad.Pattern(indices=[0, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13], period=14)
    >>> lilypond_file = illustrate_scale(scale, 84, -37, 25)
    >>> abjad.show(lilypond_file)

:author:`[Authored: Bača/Evans (3.2).]`
