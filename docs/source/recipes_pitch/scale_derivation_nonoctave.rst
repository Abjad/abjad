Scale derivation, nonoctave
---------------------------

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
