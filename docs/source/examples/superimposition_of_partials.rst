Superimposition of partials
---------------------------

Initial harmony in Kaija Saariaho's `Du Cristal`:

----

First we define functions to illustrate the examples that follow:

::

    >>> import fractions
    >>> import math
    >>> def tune_to_ratio(
    ...     note_head,
    ...     ratio,
    ... ):
    ...     ratio = fractions.Fraction(ratio)
    ...     log_ratio = fractions.Fraction(math.log10(ratio))
    ...     log_2 = fractions.Fraction(1200 / math.log10(2))
    ...     ji_cents = fractions.Fraction(log_ratio * log_2)
    ...     semitones = ji_cents / 100
    ...     parts = math.modf(semitones)
    ...     pitch = abjad.NumberedPitch(note_head.written_pitch) + parts[1]
    ...     remainder = round(parts[0] * 100)
    ...     if 50 < remainder:
    ...         pitch += 1
    ...         remainder = -100 + remainder
    ...     note_head.written_pitch = pitch
    ...
    >>> def illustrate_partials(fundamental, ratio_sequence, moment_denominator):
    ...     notes = []
    ...     for ratio in sequence:
    ...         note = abjad.Note(fundamental, (1, 16))
    ...         tune_to_ratio(note.note_head, ratio)
    ...         notes.append(note)
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
    ...     moment = abjad.SchemeMoment((1, moment_denominator))
    ...     abjad.setting(score).proportional_notation_duration = moment
    ...     lilypond_file = abjad.LilyPondFile(items=[score], global_staff_size=16)
    ...     return lilypond_file

----

Illustrate harmonic series:

::

    >>> sequence = [
    ...     1,
    ...     2,
    ...     3,
    ...     4,
    ...     5,
    ...     6,
    ...     7,
    ...     8,
    ...     9,
    ...     10,
    ...     11,
    ...     12,
    ...     13,
    ...     14,
    ...     15,
    ...     16,
    ...     17,
    ...     18,
    ...     19,
    ...     20,
    ...     21,
    ...     22,
    ...     23,
    ... ]
    ...
    >>> file = illustrate_partials("a,,", sequence, 25)
    >>> abjad.show(file)

Illustrate re-octavated harmonics:

::

    >>> sequence = [
    ...     "11/8",
    ...     "7/4",
    ...     "5/2",
    ... ]
    ...
    >>> file = illustrate_partials("a'", sequence, 25)
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
    >>> file = illustrate_partials("df,", sequence, 25)
    >>> abjad.show(file)
