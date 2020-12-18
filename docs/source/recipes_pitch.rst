Pitch Recipes
=============

Babbitt Example
---------------

Derived tone rows from inversionally related interval cycles in Milton Babbitt's `Partitions for Piano`:

Define helper function for creating interval cycles:

::

    >>> import abjad
    >>> def perle_cyclic_set(starting_pitch, interval):
    ...     returned_list = [starting_pitch]
    ...     for _ in range(10):
    ...         val = returned_list[-1] + interval
    ...         val %= 12
    ...         returned_list.append(val)
    ...     return returned_list

Define helper function to intersect cycles:

::

    >>> def intersect_sequences(seq_1, seq_2, pattern_1, pattern_2, length):
    ...     returned_list = []
    ...     for index in range(length):
    ...         match_1 = pattern_1.matches_index(index, length)
    ...         match_2 = pattern_2.matches_index(index, length)
    ...         if match_1:
    ...             value = seq_1.pop(0)
    ...             returned_list.append(value)
    ...         elif match_2:
    ...             value = seq_2.pop(0)
    ...             returned_list.append(value)
    ...         else:
    ...             returned_list.append(None)
    ...     return returned_list

Create first intersection:

::

    >>> ic1_p5 = perle_cyclic_set(starting_pitch=5, interval=1)
    >>> ic1_p2 = perle_cyclic_set(starting_pitch=2, interval=1)
    >>> ic1_p5_pattern = abjad.Pattern(
    ...     indices=[0, 2, 4],
    ...     period=6,
    ... )
    >>> ic1_p2_pattern = abjad.Pattern(
    ...     indices=[1, 3, 5],
    ...     period=6,
    ... )
    >>> intersection_1 = intersect_sequences(ic1_p5, ic1_p2, ic1_p5_pattern, ic1_p2_pattern, 6)

Create second intersection:

::

    >>> ic11_p10 = perle_cyclic_set(starting_pitch=10, interval=11)
    >>> ic11_p1 = perle_cyclic_set(starting_pitch=1, interval=11)
    >>> ic11_p10_pattern = abjad.Pattern(
    ...     indices=[0, 2, 4],
    ...     period=6,
    ... )
    >>> ic11_p1_pattern = abjad.Pattern(
    ...     indices=[1, 3, 5],
    ...     period=6,
    ... )
    >>> intersection_2 = intersect_sequences(ic11_p10, ic11_p1, ic11_p10_pattern, ic11_p1_pattern, 6)

Create and override staff:

::

    >>> row = abjad.TwelveToneRow(intersection_1 + intersection_2)
    >>> staff = abjad.Staff([abjad.Note(_, (1, 8)) for _ in row])
    >>> abjad.attach(abjad.TimeSignature((6, 8)), staff[0])
    >>> abjad.label(staff).with_intervals(prototype=abjad.NumberedIntervalClass)
    >>> abjad.override(staff).Beam.stencil = "##f"
    >>> abjad.override(staff).Flag.stencil = "##f"
    >>> abjad.override(staff).Stem.stencil = "##f"
    >>> abjad.override(staff).text_script.staff_padding = 4
    >>> abjad.override(staff).TimeSignature.stencil = "##f"
    >>> score = abjad.Score([staff])
    >>> abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment(
    ...     (1, 20)
    ... )

Show score:

::

    >>> abjad.show(score)


Carter Example
--------------

Elliott Carter's parallel-inverted all-interval collections:

Define appropriately invertible hexachords:

::

    >>> import abjad
    ...
    >>> score = abjad.Score()
    >>> group = abjad.StaffGroup()
    >>> source_hex = abjad.PitchClassSegment([0, 4, 9, 10, 8, 5])
    >>> source_hexachords = [
    ...     source_hex,
    ...     source_hex.invert(),
    ...     source_hex.retrograde().transpose((0 - source_hex[-1].number)),
    ...     source_hex.retrograde().transpose((0 - source_hex[-1].number)).invert(),
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
    >>> abjad.label(group[0][:6]).color_leaves("red")
    >>> abjad.label(group[0][6:]).color_leaves("blue")
    >>> abjad.label(group[1][:6]).color_leaves("blue")
    >>> abjad.label(group[1][6:]).color_leaves("red")
    >>> abjad.label(group[2][:6]).color_leaves("blue")
    >>> abjad.label(group[2][6:]).color_leaves("red")
    >>> abjad.label(group[3][:6]).color_leaves("red")
    >>> abjad.label(group[3][6:]).color_leaves("blue")
    >>> file = abjad.LilyPondFile.new(
    ...     score,
    ...     includes=["abjad.ily"],
    ... )
    ...

Show file:

::

    >>> abjad.show(file)


Hoffman Example
---------------

Non-octave-iterating scale in Joel Hoffman's `Piano Concerto`:

Define source scale and interval of replication:

::

    >>> import abjad
    >>> interval_down = abjad.NamedInterval("-M9")
    >>> cell = abjad.PitchSegment(
    ...     [
    ...         "bf''''",
    ...         "af''''",
    ...         "g''''",
    ...         "fs''''",
    ...         "f''''",
    ...         "ef''''",
    ...         "d''''",
    ...         "cs''''",
    ...         "c''''",
    ...         "b'''",
    ...         "a'''",
    ...     ]
    ... )
    ...

Collect transpositions of scales:

::

    >>> cells = [cell]
    >>> for _ in range(5):
    ...     new_cell = cells[-1].transpose(interval_down)
    ...     cells.append(new_cell)
    ...
    >>> full_scale = []
    >>> for cell in cells:
    ...     full_scale.extend(cell)
    ...
    >>> full_scale.sort()
    >>> final_set = abjad.PitchSegment([_ for _ in full_scale])

Create notes from pitch segment:

::

    >>> staff = abjad.Staff([abjad.Note(abjad.NumberedPitch(_), (1, 16)) for _ in final_set])

Attach extra attachments and override score settings:

::

    >>> abjad.attach(abjad.Clef("bass"), staff[0])
    >>> for note in abjad.select(staff).leaves():
    ...     if note.written_pitch == "c'":
    ...         abjad.attach(abjad.Clef("treble"), note)
    ...
    >>> abjad.ottava(staff[:11], start_ottava=abjad.Ottava(n=-1))
    >>> abjad.ottava(staff[44:])
    >>> abjad.override(staff).BarLine.stencil = "##f"
    >>> abjad.override(staff).Beam.stencil = "##f"
    >>> abjad.override(staff).Flag.stencil = "##f"
    >>> abjad.override(staff).Stem.stencil = "##f"
    >>> abjad.override(staff).TimeSignature.stencil = "##f"
    >>> abjad.setting(staff).proportional_notation_duration = abjad.SchemeMoment(
    ...     (1, 25)
    ... )
    ...
    >>> colors = [
    ...     "red",
    ...     "blue",
    ...     "red",
    ...     "blue",
    ...     "red",
    ...     "blue",
    ... ]
    ...
    >>> leaf_group = abjad.select(staff).leaves().partition_by_counts([11], cyclic=True, overhang=True,)
    >>> for color, leaves in zip(colors, leaf_group):
    ...     abjad.label(leaves).color_leaves(color)
    ...
    >>> file = abjad.LilyPondFile.new(
    ...     staff,
    ...     includes=["abjad.ily"]
    ... )
    ...
    >>> file.paper_block.items.append("indent = 0")

Show file:

::

    >>> abjad.show(file)


Lamb Example
------------

Triadic sequences in Catherine Lamb's `String Quartet`:

Define helper function to transpose notehead based on calculated cent value of ratio:

::

    >>> import abjad
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


McLeod Example
--------------

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


Nono Example
------------

Double-stop creation from hexachord pairs in Luigi Nono's `Fragmente -- Stille, an Diotima`:

Define tone row and divide into hexachords:

::

    >>> import abjad
    >>> scale = abjad.PitchSegment(["cs''", "d''", "ef''", "e''", "f''", "fs''", "g''", "gs''", "a''", "bf''", "b''", "c'''"])
    >>> hexachord_1 = [_ for _ in scale[:6]]
    >>> hexachord_2 = [_ for _ in scale[6:]]

Isolate diads from paired hexachords:

::

    >>> diads = [list(_) for _ in zip(hexachord_1, hexachord_2)]
    >>> reversed_indices = [1, 2, 4, 5]
    >>> for index in reversed_indices:
    ...     diads[index] = (diads[index][1], diads[index][0])
    ...
    >>> staff = abjad.Staff()
    >>> for diad in diads:
    ...     lower = diad[0]
    ...     higher = diad[1]
    ...     while higher < lower:
    ...         higher = abjad.NamedInterval("+P8").transpose(higher)
    ...     chord = abjad.Chord([lower, higher], (1, 8))
    ...     staff.append(chord)
    ...

Change octaves:

::

    >>> staff[2].written_pitches = abjad.NamedInterval("+P8").transpose(staff[2].written_pitches)
    >>> staff[3].written_pitches = abjad.NamedInterval("+P8").transpose(staff[3].written_pitches)
    >>> staff[4].written_pitches = abjad.NamedInterval("-P8").transpose(staff[4].written_pitches)
    >>> staff[5].written_pitches = abjad.NumberedInterval("-24").transpose(staff[5].written_pitches)

Override staff settings:

::

    >>> abjad.override(staff).Beam.stencil = "##f"
    >>> abjad.override(staff).Flag.stencil = "##f"
    >>> abjad.override(staff).Stem.stencil = "##f"
    >>> abjad.override(staff).text_script.staff_padding = 4
    >>> abjad.override(staff).TimeSignature.stencil = "##f"
    >>> score = abjad.Score([staff])
    >>> abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment(
    ...     (1, 20)
    ... )

Show score:

::

    >>> abjad.show(score)


Saariaho Example
----------------

Initial harmony in Kaija Saariaho's `Du Cristal`:

Define helper function to transpose notehead by ratio:

::

    >>> import abjad
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


Stravinsky Example
------------------

Tone row rotation in Igor Stravinsky's `Abraham and Isaac`:


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


Xenakis Example
---------------

Pitch sieve in Iannis Xenakis's `Jonchaies`:

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
