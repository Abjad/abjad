Tone-clock tesselation
-----------------------

Tone-clock tesselation in Jenny McLeod's `Tone Clock Piece I`:

Define interval prime form and steering vector:

::

    >>> ipf = abjad.PitchSegment([0, 2, 7])
    >>> steering = abjad.PitchSegment([0, 1, 3, 4])

Transpose IPF by steering pitches, inverting as necessary:

::

    >>> field = abjad.PitchSegment()
    >>> inversions = [False, True, False, True]
    >>> for bool, i in zip(inversions, steering):
    ...     transposition = ipf
    ...     if bool:
    ...         transposition = transposition.invert().retrograde()
    ...         val = transposition[0].number
    ...         transposition = transposition.transpose((0 - val))
    ...         transposition = transposition.transpose(i)
    ...     else:
    ...         transposition = transposition.transpose(i)
    ...     field += transposition
    ...

Confirm that pitch field is 12-note-complete:

::

    >>> row = abjad.TwelveToneRow(field)

Populate and override staff:

::

    >>> staff = abjad.Staff([abjad.Note(_, (1, 8)) for _ in row])
    >>> abjad.override(staff).BarLine.stencil = "##f"
    >>> abjad.override(staff).Beam.stencil = "##f"
    >>> abjad.override(staff).Flag.stencil = "##f"
    >>> abjad.override(staff).Stem.stencil = "##f"
    >>> abjad.override(staff).text_script.staff_padding = 4
    >>> abjad.override(staff).TimeSignature.stencil = "##f"
    >>> score = abjad.Score([staff])

Show score:

::

    >>> abjad.show(score)
