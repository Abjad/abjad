:orphan:

Tone-clock tesselation
======================

Tone-clock tesselation in Jenny McLeod's `Tone Clock Piece I`.

----

::

    >>> def illustrate_trichords(trichords):
    ...     group = abjad.StaffGroup([abjad.Staff(), abjad.Staff(), abjad.Staff()])
    ...     score = abjad.Score([group])
    ...     for triad in trichords:
    ...         for i, pitch in enumerate(triad):
    ...             staff = group[i]
    ...             note = abjad.Note(pitch, (1, 1))
    ...             staff.append(note)
    ...     abjad.override(score).Rest.stencil = False
    ...     abjad.override(score).SpacingSpanner.strict_note_spacing = True
    ...     abjad.override(score).TimeSignature.stencil = False
    ...     abjad.override(score).BarLine.stencil = False
    ...     abjad.override(score).BarNumber.stencil = False
    ...     abjad.override(score).SpanBar.stencil = False
    ...     abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 5)"
    ...     string = "#(set-global-staff-size 16)"
    ...     lilypond_file = abjad.LilyPondFile([string, score])
    ...     return lilypond_file
    ...

::

    >>> def tesselate_segment(segment, steering, inversions):
    ...     field = []
    ...     for bool, i in zip(inversions, steering):
    ...         transposition = ipf
    ...         if bool:
    ...             transposition = transposition.invert().retrograde()
    ...             val = transposition[0].number
    ...             transposition = transposition.transpose((0 - val))
    ...             transposition = transposition.transpose(i)
    ...         else:
    ...             transposition = transposition.transpose(i)
    ...         field.append(transposition)
    ...     return field
    ...

----


Trichord reservoir in Jenny McLeod's **Tone Clock Piece I**:

::

    >>> ipf = abjad.PitchSegment([0, 2, 7])
    >>> steering = [abjad.NumberedInterval(_) for _ in [0, 1, 3, 4]]
    >>> tesselation = tesselate_segment(
    ...     ipf,
    ...     steering,
    ...     [False, True, False, True],
    ... )
    ...
    >>> lilypond_file = illustrate_trichords(tesselation)
    >>> abjad.show(lilypond_file)

Alternate reservoir:

::

    >>> ipf = abjad.PitchSegment([0, 1, 6])
    >>> steering = [abjad.NumberedInterval(_) for _ in [0, 1, 4, 6]]
    >>> tesselation = tesselate_segment(
    ...     ipf,
    ...     steering,
    ...     [False, False, True, True],
    ... )
    ...
    >>> lilypond_file = illustrate_trichords(tesselation)
    >>> abjad.show(lilypond_file)

:author:`[Evans (3.2), Bača (3.7)]`
