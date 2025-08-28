:orphan:

Superimposition of partials
===========================

Initial harmony in Kaija Saariaho's `Du Cristal`.

----

First we define functions to illustrate the examples that follow:

::

    >>> import fractions
    >>> import math
    >>> def tune_to_ratio(
    ...     note_head,
    ...     ratio,
    ...     quarter_tones=False,
    ... ):
    ...     ratio = fractions.Fraction(ratio)
    ...     log_ratio = fractions.Fraction(math.log10(ratio))
    ...     log_2 = fractions.Fraction(1200 / math.log10(2))
    ...     ji_cents = fractions.Fraction(log_ratio * log_2)
    ...     semitones = ji_cents / 100
    ...     parts = math.modf(semitones)
    ...     numbered_pitch = abjad.NumberedPitch(note_head.written_pitch()) + parts[1]
    ...     remainder = round(parts[0] * 100)
    ...     if 50 < abs(remainder):
    ...         if 0 < remainder:
    ...             numbered_pitch += 1
    ...             remainder = -100 + remainder
    ...         else:
    ...             numbered_pitch -= 1
    ...             remainder = 100 + remainder
    ...     if quarter_tones:
    ...         if 25 < abs(remainder):
    ...             if 0 < remainder:
    ...                 numbered_pitch += 0.5
    ...                 remainder = -50 + remainder
    ...             else:
    ...                 numbered_pitch -= 0.5
    ...                 remainder = 50 + remainder
    ...     pitch = abjad.NamedPitch(numbered_pitch)
    ...     note_head.set_written_pitch(pitch)
    ...
    >>> def illustrate_partials(
    ...     fundamental,
    ...     ratio_sequence,
    ...     with_quarter_tones=False,
    ... ):
    ...     pitch = abjad.NamedPitch(fundamental)
    ...     notes = []
    ...     duration = abjad.Duration(1, 16)
    ...     for ratio in sequence:
    ...         note = abjad.Note.from_duration_and_pitch(duration, pitch)
    ...         tune_to_ratio(note.note_head(), ratio, quarter_tones=with_quarter_tones)
    ...         notes.append(note)
    ...     score = abjad.illustrators.make_piano_score(notes)
    ...     treble_staff = score["Treble_Staff"]
    ...     abjad.override(score).BarLine.stencil = False
    ...     abjad.override(score).BarNumber.stencil = False
    ...     abjad.override(score).Beam.stencil = False
    ...     abjad.override(score).Flag.stencil = False
    ...     abjad.override(score).Rest.stencil = False
    ...     abjad.override(score).SpacingSpanner.strict_note_spacing = True
    ...     abjad.override(score).SpanBar.stencil = False
    ...     abjad.override(score).Stem.stencil = False
    ...     abjad.override(score).TimeSignature.stencil = False
    ...     abjad.setting(score).proportionalNotationDuration = "#1/25"
    ...     string = "#(set-global-staff-size 16)"
    ...     lilypond_file = abjad.LilyPondFile([string, score])
    ...     return lilypond_file

----

Illustrate harmonic series approximated to semitones:

::

    >>> sequence = [_ + 1 for _ in range(31)]
    >>> file = illustrate_partials("a,,", sequence)
    >>> abjad.show(file)

Illustrate harmonic series approximated to quarter tones:

::

    >>> sequence = [_ + 1 for _ in range(31)]
    >>> file = illustrate_partials("a,,", sequence, with_quarter_tones=True)
    >>> abjad.show(file)

Illustrate re-octavated harmonics:

::

    >>> sequence = [
    ...     "11/8",
    ...     "7/4",
    ...     "5/2",
    ... ]
    ...
    >>> file = illustrate_partials("a'", sequence, with_quarter_tones=True)
    >>> abjad.show(file)

Illustrate sonority of Du Cristal:

::

    >>> sequence = [
    ...     1,
    ...     "15/8",
    ...     "7/2",
    ...     "17/4",
    ...     "21/4",
    ...     6,
    ...     9,
    ...     10,
    ...     "21/2",
    ...     12,
    ...     18,
    ...     20,
    ... ]
    ...
    >>> file = illustrate_partials("df,", sequence)
    >>> abjad.show(file)

:author:`[Evans (3.2); Bača (3.29)]`
