Row derivation, by trichord
---------------------------

Derived tone rows in Anton Webern's `Concerto for Nine Instruments, Op.24`:

Define trichord source and tone-row-forming transformations:

::

    >>> import abjad
    ...
    >>> score = abjad.Score()
    >>> group = abjad.StaffGroup()
    >>> source_trichord = abjad.PitchClassSegment([0, 1, 4])
    >>> webern_source = source_trichord.invert().rotate(1).transpose(-8)
    >>> first_part = webern_source.transpose(7)
    >>> second_part = webern_source.invert().retrograde().transpose(6)
    >>> third_part = webern_source.retrograde().transpose(1)
    >>> fourth_part = webern_source.invert()
    >>> row = abjad.TwelveToneRow(first_part + second_part + third_part + fourth_part)
    >>> perms = [
    ...     (
    ...         row,
    ...         abjad.StartMarkup(abjad.Markup("P").box()),
    ...     ),
    ...     (
    ...         row.retrograde(),
    ...         abjad.StartMarkup(abjad.Markup("R").box()),
    ...     ),
    ...     (
    ...         row.invert(),
    ...         abjad.StartMarkup(abjad.Markup("I").box()),
    ...     ),
    ...     (
    ...         row.invert().retrograde(),
    ...         abjad.StartMarkup(abjad.Markup("RI").box()),
    ...     ),
    ... ]
    ...

Iterate through permutations, creating staves and labeling trichords:

::

    >>> counter = 0
    >>> for perm in perms:
    ...     cyc_tuple = abjad.CyclicTuple(["red", "blue"])
    ...     staff = abjad.Staff([abjad.Note(_, (1, 16)) for _ in perm[0]])
    ...     abjad.attach(perm[1], staff[0])
    ...     for trichord in (
    ...         abjad.select(staff)
    ...         .leaves()
    ...         .partition_by_counts(
    ...             [3],
    ...             cyclic=True,
    ...             overhang=True,
    ...         )
    ...     ):
    ...         pc_set = abjad.PitchClassSet([_.written_pitch for _ in trichord])
    ...         set_class = abjad.SetClass.from_pitch_class_set(pc_set)
    ...         abjad.attach(abjad.Markup(set_class), trichord[0])
    ...         abjad.label(trichord).color_leaves(cyc_tuple[counter])
    ...         counter += 1
    ...         abjad.override(staff).text_script.staff_padding = 4
    ...     group.append(staff)
    ...

Attach extra labels and override score settings:

::

    >>> abjad.attach(
    ...     abjad.Markup.concat(
    ...         [abjad.Markup("P"), abjad.Markup("7").sub()], direction=abjad.Up
    ...     ).parenthesize(),
    ...     abjad.select(group[0]).leaf(0),
    ... )
    ...
    >>> abjad.attach(
    ...     abjad.Markup.concat(
    ...         [abjad.Markup("RI"), abjad.Markup("6").sub()], direction=abjad.Up
    ...     ).parenthesize(),
    ...     abjad.select(group[0]).leaf(3),
    ... )
    ...
    >>> abjad.attach(
    ...     abjad.Markup.concat(
    ...         [abjad.Markup("R"), abjad.Markup("1").sub()], direction=abjad.Up
    ...     ).parenthesize(),
    ...     abjad.select(group[0]).leaf(6),
    ... )
    ...
    >>> abjad.attach(
    ...     abjad.Markup.concat(
    ...         [abjad.Markup("I"), abjad.Markup("0").sub()], direction=abjad.Up
    ...     ).parenthesize(),
    ...     abjad.select(group[0]).leaf(9),
    ... )
    ...
    >>> score.append(group)
    >>> abjad.override(score).Beam.stencil = "##f"
    >>> abjad.override(score).Flag.stencil = "##f"
    >>> abjad.override(score).Stem.stencil = "##f"
    >>> abjad.override(score).TimeSignature.stencil = "##f"
    >>> abjad.override(
    ...     score
    ... ).StaffGrouper.staff_staff_spacing = (
    ...     "#'((basic-distance . 20) (minimum-distance . 20) (padding . 2))"
    ... )
    >>> abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment((1, 45))
    >>> file = abjad.LilyPondFile.new(
    ...     score, includes=["abjad.ily"]
    ... )
    ...

Show file:

::

    >>> abjad.show(file)


