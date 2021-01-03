Trichord definition, by ratio
-----------------------------

Triadic sequences in Catherine Lamb's `String Quartet`:

----

Define helper functions:

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
    ...     pitch = abjad.NumberedPitch(note_head.written_pitch) + parts[1]
    ...     remainder = round(parts[0] * 100)
    ...     if 50 < abs(remainder):
    ...         if 0 < remainder:
    ...             pitch += 1
    ...             remainder = -100 + remainder
    ...         else:
    ...             pitch -= 1
    ...             remainder = 100 + remainder
    ...     if quarter_tones:
    ...         if 25 < abs(remainder):
    ...             if 0 < remainder:
    ...                 pitch += 0.5
    ...                 remainder = -50 + remainder
    ...             else:
    ...                 pitch -= 0.5
    ...                 remainder = 50 + remainder
    ...     note_head.written_pitch = pitch
    ...

::

    >>> def return_cent_markup(
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
    ...     pitch = abjad.NumberedPitch(note_head.written_pitch) + parts[1]
    ...     remainder = round(parts[0] * 100)
    ...     if 50 < abs(remainder):
    ...         if 0 < remainder:
    ...             pitch += 1
    ...             remainder = -100 + remainder
    ...         else:
    ...             pitch -= 1
    ...             remainder = 100 + remainder
    ...     if quarter_tones:
    ...         if 25 < abs(remainder):
    ...             if 0 < remainder:
    ...                 pitch += 0.5
    ...                 remainder = -50 + remainder
    ...             else:
    ...                 pitch -= 0.5
    ...                 remainder = 50 + remainder
    ...     if remainder < 0:
    ...         cent_string = f"{remainder}"
    ...     else:
    ...         cent_string = f"+{remainder}"
    ...     mark = abjad.Markup(cent_string, direction=abjad.Down)
    ...     return mark
    ...

::

    >>> def illustrate_trichords(trichords, fundamental, moment_denominator):
    ...     group = abjad.StaffGroup([abjad.Staff(), abjad.Staff(), abjad.Staff()])
    ...     score = abjad.Score([group])
    ...     for triad in trichords:
    ...         for i, ratio in enumerate(triad):
    ...             staff = group[i]
    ...             note = abjad.Note(fundamental, (1, 1))
    ...             tune_to_ratio(note.note_head, ratio)
    ...             markup = return_cent_markup(note.note_head, ratio)
    ...             abjad.attach(markup, note)
    ...             staff.append(note)
    ...     abjad.override(score).Rest.stencil = False
    ...     abjad.override(score).SpacingSpanner.strict_note_spacing = True
    ...     abjad.override(score).TimeSignature.stencil = False
    ...     moment = abjad.SchemeMoment((1, moment_denominator))
    ...     abjad.setting(score).proportional_notation_duration = moment
    ...     lilypond_file = abjad.LilyPondFile(items=[score], global_staff_size=16)
    ...     return lilypond_file
    ...

----

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
    ...     [1, "126/121", "5/6"],
    ...     [1, "36/35", "4/5"],
    ...     [1, "28/27", "7/9"],
    ...     [1, "121/120", 1],
    ...     [1, "21/20", "3/4"],
    ...     [1, "81/80", "120/121"],
    ...     [1, "49/48", "120/121"],
    ...     [1, "15/14", "5/7"],
    ...     [1, "36/35", "48/49"],
    ...     [1, "126/121", "35/36"],
    ...     [1, "16/15", "2/3"],
    ...     [1, "16/15", "121/126"],
    ...     [1, "16/15", "14/15"],
    ...     [1, "35/32", "5/8"],
    ...     [1, "35/32", "15/16"],
    ...     [1, "10/9", "112/121"],
    ...     [1, "8/7", "4/7"],
    ...     [1, "9/8", "9/10"],
    ...     [1, "8/7", "8/9"],
    ...     [1, "7/6", "1/2"],
    ...     [1, "7/6", "7/8"],
    ...     [1, "6/5", "6/7"],
    ...     [1, "5/4", "5/6"],
    ...     [1, "9/7", "3/7"],
    ...     [1, "9/7", "4/5"],
    ...     [1, "4/3", "7/9"],
    ...     [1, "4/3", "1/3"],
    ...     [1, "7/5", "3/4"],
    ...     [1, "3/2", "1/4"],
    ...     [1, "3/2", "3/4"],
    ... ]
    ...
    >>> file = illustrate_trichords(
    ...     triadic_sequences,
    ...     0,
    ...     5,
    ... )
    ...
    >>> abjad.show(file)
