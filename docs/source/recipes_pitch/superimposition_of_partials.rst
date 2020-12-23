Superimposition of partials
---------------------------

Initial harmony in Kaija Saariaho's `Du Cristal`:

Define helper function to transpose notehead by ratio:

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

Create ratio sequence:

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

Populate staff:

::

    >>> staff = abjad.Staff()
    >>> for ratio in sequence:
    ...     note = abjad.Note("df,16")
    ...     tune_to_ratio(note.note_head, ratio)
    ...     staff.append(note)
    ...

Override staff settings:

::

    >>> abjad.attach(abjad.Clef("bass"), staff[0])
    >>> abjad.attach(abjad.Clef("treble"), staff[3])
    >>> abjad.ottava(staff[8:])
    >>> score = abjad.Score([staff])
    >>> abjad.override(score).BarLine.stencil = "##f"
    >>> abjad.override(score).Beam.stencil = "##f"
    >>> abjad.override(score).Flag.stencil = "##f"
    >>> abjad.override(score).Stem.stencil = "##f"
    >>> abjad.override(score).text_script.staff_padding = 4
    >>> abjad.override(score).TimeSignature.stencil = "##f"

Show score:

::

    >>> abjad.show(score)


