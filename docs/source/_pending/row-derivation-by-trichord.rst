:orphan:

Row derivation, by trichord
===========================

Derived tone rows in Anton Webern's `Concerto for Nine Instruments, Op.24`.

----

First we define functions to illustrate the examples that follow:

::

    >>> def illustrate_row(row):
    ...     notes = [abjad.Note(_, (1, 8)) for _ in row]
    ...     score = abjad.illustrators.make_piano_score(notes)
    ...     treble_staff = score["Treble_Staff"]
    ...     abjad.override(treble_staff).BarLine.stencil = False
    ...     abjad.override(treble_staff).BarNumber.stencil = False
    ...     abjad.override(treble_staff).Beam.stencil = False
    ...     abjad.override(treble_staff).Flag.stencil = False
    ...     abjad.override(treble_staff).Rest.stencil = False
    ...     abjad.override(treble_staff).SpacingSpanner.strict_note_spacing = True
    ...     abjad.override(treble_staff).SpanBar.stencil = False
    ...     abjad.override(treble_staff).Stem.stencil = False
    ...     abjad.override(treble_staff).TimeSignature.stencil = False
    ...     string = r"\musicLength 1*1/25"
    ...     abjad.setting(treble_staff).proportionalNotationDuration = string
    ...     string = "#(set-global-staff-size 16)"
    ...     lilypond_file = abjad.LilyPondFile([string, treble_staff])
    ...     return lilypond_file

----

Define trichord source and tone-row-forming transformations:

::

    >>> source_trichord = abjad.PitchClassSegment([0, 1, 4])
    >>> webern_source = source_trichord.invert().rotate(1).transpose(-8)
    >>> first_part = webern_source.transpose(7)
    >>> second_part = webern_source.invert().retrograde().transpose(6)
    >>> third_part = webern_source.retrograde().transpose(1)
    >>> fourth_part = webern_source.invert()
    >>> row = abjad.TwelveToneRow(first_part + second_part + third_part + fourth_part)

Show prime form:

::

    >>> file = illustrate_row(row)
    >>> abjad.show(file)

Show retrograde:

::

    >>> file = illustrate_row(row.retrograde())
    >>> abjad.show(file)

Show inversion:

::

    >>> file = illustrate_row(row.invert())
    >>> abjad.show(file)

Show retrograde inversion:

::

    >>> file = illustrate_row(row.invert().retrograde())
    >>> abjad.show(file)

:author:`[Evans (3.2), Bača (3.7)]`
