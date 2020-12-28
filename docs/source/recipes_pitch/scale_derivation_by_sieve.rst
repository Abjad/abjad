Scale derivation, by sieve
--------------------------

The derivation of nonoctave scales by sieve is a 20th-century technique due to Xenakis.

----

First we define a function to illustrate the examples that follow:

::

    >>> def illustrate_sieve(sieve, length):
    ...     pitches = abjad.sequence(range(length))
    ...     pitches = pitches.retain_pattern(sieve)
    ...     notes = [abjad.Note(_ - 15, (1, 16)) for _ in pitches]
    ...     containers = abjad.illustrators.make_piano_score(notes)
    ...     score, treble_staff, bass_staff = containers
    ...     abjad.override(score).BarLine.stencil = False
    ...     abjad.override(score).Beam.stencil = False
    ...     abjad.override(score).Flag.stencil = False
    ...     abjad.override(score).Rest.stencil = False
    ...     abjad.override(score).SpacingSpanner.strict_note_spacing = True
    ...     abjad.override(score).SpanBar.stencil = False
    ...     abjad.override(score).Stem.stencil = False
    ...     abjad.override(score).TimeSignature.stencil = False
    ...     moment = abjad.SchemeMoment((1, 25))
    ...     abjad.setting(score).proportional_notation_duration = moment
    ...     lilypond_file = abjad.LilyPondFile(items=[score], global_staff_size=16)
    ...     return lilypond_file

----

**Jonchaies.** The sieve underlying Xenakis's orchestra piece *Jonchaies*
(1977) structures a series of 8 consecutive intervals that repeat every 17 semitones.

First three elements of sieve:

::

    >>> first_half = abjad.Pattern(indices=[0, 1, 4], period=17)
    >>> lilypond_file = illustrate_sieve(first_half, 56)
    >>> abjad.show(lilypond_file)

Remainder of sieve:

::

    >>> second_half = abjad.Pattern(indices=[5, 7, 11, 12, 16], period=17)
    >>> lilypond_file = illustrate_sieve(second_half, 56)
    >>> abjad.show(lilypond_file)

Complete sieve:

::

    >>> sieve = first_half | second_half
    >>> lilypond_file = illustrate_sieve(sieve, 56)
    >>> abjad.show(lilypond_file)
