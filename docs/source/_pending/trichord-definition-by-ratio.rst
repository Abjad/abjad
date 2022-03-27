:orphan:

Trichord definition, by ratio
=============================

Triadic sequences in Catherine Lamb's `String Quartet`.

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
    ...     bass=False,
    ...     quarter_tones=False,
    ... ):
    ...     ratio = fractions.Fraction(ratio)
    ...     log_ratio = fractions.Fraction(math.log10(ratio))
    ...     log_2 = fractions.Fraction(1200 / math.log10(2))
    ...     ji_cents = fractions.Fraction(log_ratio * log_2)
    ...     semitones = ji_cents / 100
    ...     parts = math.modf(semitones)
    ...     pitch = abjad.NumberedPitch(note_head.written_pitch) + parts[1]
    ...     if bass is False or pitch <= -8:
    ...         direction = abjad.DOWN
    ...     else:
    ...         direction = abjad.UP
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
    ...     string = rf"\markup {cent_string}"
    ...     markup = abjad.Markup(string)
    ...     abjad.tweak(markup, r"- \tweak parent-alignment-X 0") 
    ...     abjad.tweak(markup, r"- \tweak self-alignment-X 0.25") 
    ...     if pitch <= -8:
    ...         abjad.tweak(markup, r"- \tweak padding 1")
    ...     else:
    ...         abjad.tweak(markup, r"- \tweak padding 2.5")
    ...     return markup, direction
    ...

::

    >>> def illustrate_trichords(trichords, fundamental):
    ...     staff_1 = abjad.Staff(name="Staff_1")
    ...     staff_2 = abjad.Staff(name="Staff_2")
    ...     staff_3 = abjad.Staff(name="Staff_3")
    ...     group = abjad.StaffGroup([staff_1, staff_2, staff_3], name="Staff_Group")
    ...     score = abjad.Score([group], name="Score")
    ...     for triad in trichords:
    ...         for i, ratio in enumerate(triad):
    ...             staff = group[i]
    ...             note = abjad.Note(fundamental, (1, 1))
    ...             tune_to_ratio(note.note_head, ratio)
    ...             bass = False
    ...             if i == 2:
    ...                 bass = True
    ...             markup, direction = return_cent_markup(note.note_head, ratio, bass=bass)
    ...             abjad.attach(markup, note, direction=direction)
    ...             staff.append(note)
    ...     for measure_number in (1, 11, 21, 31):
    ...         note = abjad.select.note(staff_1, measure_number - 1)
    ...         markup = abjad.Markup(r"\markup A")
    ...         abjad.tweak(markup, r"- \tweak staff-padding 8")
    ...         abjad.tweak(markup, r"- \tweak transparent ##t")
    ...         abjad.attach(markup, note, direction=abjad.UP)
    ...     interface = abjad.override(staff_1).vertical_axis_group
    ...     interface.staff_staff_spacing__minimum_distance = 12
    ...     interface = abjad.override(staff_2).vertical_axis_group
    ...     interface.staff_staff_spacing__minimum_distance = 14
    ...     note = abjad.select.note(staff_3, 0)
    ...     abjad.attach(abjad.Clef("bass"), note)
    ...     abjad.override(score).BarLine.stencil = False
    ...     abjad.override(score).BarNumber.stencil = False
    ...     abjad.override(score).SpanBar.stencil = False
    ...     abjad.override(score).Rest.stencil = False
    ...     abjad.override(score).SpacingSpanner.strict_note_spacing = True
    ...     abjad.override(score).TimeSignature.stencil = False
    ...     abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 5)"
    ...     items = [score, abjad.Block(name="layout"), abjad.Block(name="paper")]
    ...     string = "#(set-global-staff-size 16)"
    ...     items.insert(0, string)
    ...     lilypond_file = abjad.LilyPondFile(items)
    ...     lilypond_file["layout"].items.append("indent = #0")
    ...     space = "system-system-spacing = #'((basic-distance . 13)"
    ...     space += " (minimum-distance . 13) (padding . 4))"
    ...     lilypond_file["paper"].items.append(space)
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
    ... )
    ...
    >>> abjad.show(file)

:author:`[Evans (3.2)]`
