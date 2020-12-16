Pitch Recipes
=============

Carter Example
--------------

Elliott Carter's parallel-inverted all-interval collections:


Define appropriately invertible hexachords:

::

    >>> import abjad
    ...
    >>> score = abjad.Score()
    >>> group = abjad.StaffGroup()
    >>> source_hexachords = [
    ...     abjad.PitchClassSegment([0, 4, 9, 10, 8, 5]),
    ...     abjad.PitchClassSegment([0, 8, 3, 2, 4, 7]),
    ...     abjad.PitchClassSegment([0, 3, 5, 4, 11, 7]),
    ...     abjad.PitchClassSegment([0, 9, 7, 8, 1, 5]),
    ... ]
    ...

Iterate over hexachords, combining with hexachord inversion transposed six semitones above the final hexachord pitch, stacking each pitch as an interval above the previous pitch:

::

    >>> for hexachord in source_hexachords:
    ...     s1 = hexachord
    ...     s2 = s1.invert().transpose(s1[-1].number + 6)
    ...     full_sequence = abjad.PitchSegment(s1 + s2)
    ...     transposed_sequence = full_sequence.transpose(-24)
    ...     vertical_sequence = [-24]
    ...     for pitch in transposed_sequence[1:]:
    ...         pitch_number = pitch.number
    ...         while pitch_number < vertical_sequence[-1]:
    ...             pitch_number += 12
    ...         vertical_sequence.append(pitch_number)
    ...     staff = abjad.Staff([abjad.Note(_, (1, 16)) for _ in vertical_sequence])
    ...     abjad.attach(abjad.Clef("bass"), staff[0])
    ...     abjad.attach(abjad.Clef("treble"), staff[4])
    ...     abjad.ottava(staff[8:])
    ...     abjad.label(staff).with_intervals(prototype=abjad.NumberedIntervalClass)
    ...     abjad.override(staff).text_script.staff_padding = 7
    ...     group.append(staff)
    ...

Add staff group to score and override settings:

::

    >>> score.append(group)
    >>> abjad.override(score).Beam.stencil = "##f"
    >>> abjad.override(score).Flag.stencil = "##f"
    >>> abjad.override(score).Stem.stencil = "##f"
    >>> abjad.override(score).TimeSignature.stencil = "##f"
    >>> abjad.override(score).StaffGrouper.staff_staff_spacing = "#'((basic-distance . 20) (minimum-distance . 20) (padding . 2))"
    >>> abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment((1, 45))

Show score:

::

    >>> abjad.show(score)


Stravinsky Example
------------------

Stravinskian tone row rotation in `Abraham and Isaac`:


Define tone row and row permutations:

::

    >>> import abjad
    ...
    >>> file = abjad.LilyPondFile()
    >>> source = abjad.TwelveToneRow([5, 6, 4, 2, 3, 11, 9, 7, 8, 10, 0, 1])
    >>> perms = [
    ...     source,
    ...     source.invert(),
    ...     source.retrograde(),
    ...     abjad.TwelveToneRow(source.retrograde()).invert(),
    ... ]
    ...
    >>> labels = [
    ...     abjad.Markup(
    ...         "P",
    ...         direction=abjad.Up,
    ...     ),
    ...     abjad.Markup(
    ...         "I",
    ...         direction=abjad.Up,
    ...     ),
    ...     abjad.Markup(
    ...         "R",
    ...         direction=abjad.Up,
    ...     ),
    ...     abjad.Markup(
    ...         "IR",
    ...         direction=abjad.Up,
    ...     ),
    ... ]
    ...

Define rotation distances and iterate through permutations, creating charts:

::

    >>> rotations = [0, -1, -2, -3, -4, -5]
    >>> for perm, label in zip(perms, labels):
    ...     source_staff = abjad.Staff([abjad.Note(_, (1, 16)) for _ in perm])
    ...     abjad.attach(label, source_staff[0])
    ...     score = abjad.Score([source_staff])
    ...     group = abjad.StaffGroup()
    ...     hexachords = [
    ...         [_.number for _ in perm[:6]],
    ...         [_.number for _ in perm[6:]],
    ...     ]
    ...     margin_markups = [
    ...         abjad.StartMarkup(markup=label.box()),
    ...         abjad.StartMarkup(markup="I"),
    ...         abjad.StartMarkup(markup="II"),
    ...         abjad.StartMarkup(markup="III"),
    ...         abjad.StartMarkup(markup="IV"),
    ...         abjad.StartMarkup(markup="V"),
    ...     ]
    ...     for r, m in zip(rotations, margin_markups):
    ...         staff = abjad.Staff()
    ...         sets = [
    ...             abjad.PitchClassSegment(hexachords[0]).rotate(r),
    ...             abjad.PitchClassSegment(hexachords[1]).rotate(r),
    ...             abjad.PitchClassSegment(hexachords[0])
    ...             .rotate(r, stravinsky=True)
    ...             .transpose(hexachords[0][0]),
    ...             abjad.PitchClassSegment(hexachords[1])
    ...             .rotate(r, stravinsky=True)
    ...             .transpose(hexachords[1][0]),
    ...         ]
    ...         names = [
    ...             abjad.Markup("α", direction=abjad.Up).box(),
    ...             abjad.Markup("β", direction=abjad.Up).box(),
    ...             abjad.Markup("γ", direction=abjad.Up).box(),
    ...             abjad.Markup("δ", direction=abjad.Up).box(),
    ...         ]
    ...         for set, name in zip(sets, names):
    ...             voice = abjad.Voice([abjad.Note(_, (1, 16)) for _ in set])
    ...             for leaf in abjad.iterate(voice).leaves():
    ...                 mark = abjad.Markup(
    ...                     abjad.NumberedPitchClass(leaf.written_pitch),
    ...                     direction=abjad.Up,
    ...                 )
    ...                 abjad.tweak(mark).staff_padding = "3"
    ...                 abjad.attach(mark, leaf)
    ...             abjad.tweak(name).staff_padding = "3"
    ...             abjad.attach(name, voice[0])
    ...             abjad.attach(abjad.TimeSignature((6, 16)), voice[0])
    ...             staff.append(voice)
    ...         abjad.attach(m, abjad.select(staff).leaf(0))
    ...         group.append(staff)
    ...     score.append(group)
    ...     abjad.override(score).Beam.stencil = "##f"
    ...     abjad.override(score).Flag.stencil = "##f"
    ...     abjad.override(score).Stem.stencil = "##f"
    ...     abjad.override(score).TimeSignature.stencil = "##f"
    ...     abjad.override(score).StaffGrouper.staff_staff_spacing = "#'((basic-distance . 10) (minimum-distance . 10) (padding . 2))"
    ...     abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment((1, 25))
    ...     file.items.append(score)

Show file of chart scores:

::

    >>> abjad.show(file)


Webern Example
--------------

Creation of derived tone rows in Webern's `Concerto for Nine Instruments, Op.24`:

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

Attach extra lables and override score settings:

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


Xenakis Example
---------------

Creation of Xenakisian pitch sieve in `Jonchaies`:

Initialize periodic patterns and create union:

::

    >>> import abjad
    >>> x17_0 = abjad.Pattern(indices=[0], period=17)
    >>> x17_1 = abjad.Pattern(indices=[1], period=17)
    >>> x17_4 = abjad.Pattern(indices=[4], period=17)
    >>> x17_5 = abjad.Pattern(indices=[5], period=17)
    >>> x17_7 = abjad.Pattern(indices=[7], period=17)
    >>> x17_11 = abjad.Pattern(indices=[11], period=17)
    >>> x17_12 = abjad.Pattern(indices=[12], period=17)
    >>> x17_16 = abjad.Pattern(indices=[16], period=17)
    >>> sieve = x17_0 | x17_1 | x17_4 | x17_5 | x17_7 | x17_11 | x17_12 | x17_16

Iterate through boolean vector to create pitch list:

::

    >>> pitches = []
    >>> length = 56
    >>> indices = [_ for _ in range(length)]
    >>> vector = sieve.get_boolean_vector(total_length=length)
    >>> for index, boolean_value in zip(indices, vector):
    ...     if boolean_value:
    ...         pitches.append(abjad.NumberedPitch(index))
    ...

Initialize note objects from pitch list:

::

    >>> staff = abjad.Staff([abjad.Note(_ - 15, (1, 16)) for _ in pitches])
    >>> abjad.attach(abjad.Clef("bass"), staff[0])
    >>> abjad.attach(abjad.Clef("treble"), staff[7])
    >>> abjad.ottava(staff[21:])
    >>> abjad.override(staff).BarLine.stencil = "##f"
    >>> abjad.override(staff).Beam.stencil = "##f"
    >>> abjad.override(staff).Flag.stencil = "##f"
    >>> abjad.override(staff).Stem.stencil = "##f"
    >>> abjad.override(staff).TimeSignature.stencil = "##f"
    >>> abjad.setting(staff).proportional_notation_duration = abjad.SchemeMoment((1, 25))

Show score:

::

    >>> abjad.show(staff)
