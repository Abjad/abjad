Rotation, by row index
======================

Tone row rotation in Igor Stravinsky's `Abraham and Isaac`.


Define helper functions:

----

::

    >>> def permute_row(source):
    ...     perms = [
    ...         source,
    ...         source.invert(),
    ...         source.retrograde(),
    ...         abjad.TwelveToneRow(source.retrograde()).invert(),
    ...     ]
    ...     return perms
    ...

::

    >>> def make_rotation_chart(perm, label):
    ...     file = abjad.LilyPondFile()
    ...     rotations = [0, -1, -2, -3, -4, -5]
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
    ...     abjad.override(score).BarNumber.stencil = False
    ...     abjad.override(score).Beam.stencil = "##f"
    ...     abjad.override(score).Flag.stencil = "##f"
    ...     abjad.override(score).Stem.stencil = "##f"
    ...     abjad.override(score).TimeSignature.stencil = "##f"
    ...     abjad.override(score).StaffGrouper.staff_staff_spacing = "#'((basic-distance . 10) (minimum-distance . 10) (padding . 2))"
    ...     abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment((1, 25))
    ...     file.items.append(score)
    ...     return file

----

Show file of chart scores:

::

    >>> source = abjad.TwelveToneRow([5, 6, 4, 2, 3, 11, 9, 7, 8, 10, 0, 1])
    >>> perms = permute_row(source)
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

::

    >>> file = make_rotation_chart(perms[0], labels[0])
    >>> abjad.show(file)

::

    >>> file = make_rotation_chart(perms[1], labels[1])
    >>> abjad.show(file)

::

    >>> file = make_rotation_chart(perms[2], labels[2])
    >>> abjad.show(file)

::

    >>> file = make_rotation_chart(perms[3], labels[3])
    >>> abjad.show(file)

:author:`[Evans (3.2)]`
