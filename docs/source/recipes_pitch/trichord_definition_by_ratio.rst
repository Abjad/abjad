Trichord definition, by ratio
-----------------------------

Triadic sequences in Catherine Lamb's `String Quartet`:

Define helper function to transpose notehead based on calculated cent value of ratio:

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

Define helper function to create markup of cent deviation from equal temperament:

::

    >>> def return_cent_markup(
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
    ...     if 50 < abs(remainder):
    ...         if 0 < remainder:
    ...             pitch += 1
    ...             remainder = -100 + remainder
    ...         else:
    ...             pitch -= 1
    ...             remainder = 100 + remainder
    ...     if remainder < 0:
    ...         cent_string = f"{remainder}"
    ...     else:
    ...         cent_string = f"+{remainder}"
    ...     mark = abjad.Markup(cent_string, direction=abjad.Up).center_align()
    ...     return mark
    ...

Create list of triad sequences written as ratios:

::

    >>> triadic_sequences = [
    ...     [1, 1, 1],
    ...     [1, 1, "120/121"],
    ...     [1, "121/120", "80/81"],
    ...     [1, "121/120", "48/49"],
    ...     [1, "49/48", "35/36"],
    ...     [1, "49/48", "20/21"],
    ...     [1, "28/27", "14/15"],
    ...     [1, "36/35", "9/10"],
    ...     [1, "49/48", "7/8"],
    ...     [1, "36/35", "6/7"],
    ... ]
    ...

Populate staff and call functions on leaves:

::

    >>> group = abjad.StaffGroup()
    >>> score = abjad.Score([group])
    >>> for triad in triadic_sequences:
    ...     staff = abjad.Staff()
    ...     for ratio in triad:
    ...         note = abjad.Note()
    ...         tune_to_ratio(note.note_head, ratio)
    ...         markup = return_cent_markup(note.note_head, ratio)
    ...         abjad.attach(markup, note)
    ...         staff.append(note)
    ...     group.append(staff)
    ...

Override score settings:

::

    >>> abjad.override(score).BarLine.stencil = "##f"
    >>> abjad.override(score).Beam.stencil = "##f"
    >>> abjad.override(score).Flag.stencil = "##f"
    >>> abjad.override(score).Stem.stencil = "##f"
    >>> abjad.override(score).text_script.staff_padding = 4
    >>> abjad.override(score).TimeSignature.stencil = "##f"

Show score:

::

    >>> abjad.show(score)
