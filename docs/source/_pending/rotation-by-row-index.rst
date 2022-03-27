:orphan:

Rotation, by row index
======================

..

----

::

    >>> def make_rotation_chart(permutation, label):
    ...     rotations = [0, -1, -2, -3, -4, -5]
    ...     source_staff = abjad.Staff([abjad.Note(_, (1, 16)) for _ in permutation])
    ...     markup = abjad.Markup(rf'\markup "{label}"')
    ...     abjad.attach(markup, source_staff[0], direction=abjad.UP)
    ...     score = abjad.Score([source_staff], name="Score")
    ...     group = abjad.StaffGroup(name="Staff_Group")
    ...     hexachords = [
    ...         [_.number for _ in permutation[:6]],
    ...         [_.number for _ in permutation[6:]],
    ...     ]
    ...     markup = abjad.Markup(rf'\markup \box "{label}"')
    ...     margin_markups = [
    ...         abjad.StartMarkup(markup=markup),
    ...         abjad.StartMarkup(markup="I"),
    ...         abjad.StartMarkup(markup="II"),
    ...         abjad.StartMarkup(markup="III"),
    ...         abjad.StartMarkup(markup="IV"),
    ...         abjad.StartMarkup(markup="V"),
    ...     ]
    ...     for r, margin_markup in zip(rotations, margin_markups):
    ...         staff = abjad.Staff()
    ...         sets = [
    ...             abjad.PitchClassSegment(hexachords[0]).rotate(r),
    ...             abjad.PitchClassSegment(hexachords[1]).rotate(r),
    ...             abjad.PitchClassSegment(hexachords[0]).rotate(r)
    ...             .transpose(-int(hexachords[0][0]))
    ...             .transpose(hexachords[0][0]),
    ...             abjad.PitchClassSegment(hexachords[1]).rotate(r)
    ...             .transpose(-int(hexachords[1][0]))
    ...             .transpose(hexachords[1][0]),
    ...         ]
    ...         names = [
    ...             abjad.Markup(r"\markup \box α"),
    ...             abjad.Markup(r"\markup \box β"),
    ...             abjad.Markup(r"\markup \box γ"),
    ...             abjad.Markup(r"\markup \box δ"),
    ...         ]
    ...         for set, name in zip(sets, names):
    ...             voice = abjad.Voice([abjad.Note(_, (1, 16)) for _ in set])
    ...             for leaf in abjad.select.leaves(voice):
    ...                 markup = abjad.Markup(
    ...                     rf"\markup {abjad.NumberedPitchClass(leaf.written_pitch)}",
    ...                 )
    ...                 bundle = abjad.bundle(markup, r"- \tweak staff-padding 3")
    ...                 abjad.attach(bundle, leaf, direction=abjad.UP)
    ...             bundle = abjad.bundle(name, r"- \tweak staff-padding 3")
    ...             abjad.attach(bundle, voice[0])
    ...             time_signature = abjad.TimeSignature((6, 16))
    ...             abjad.attach(time_signature, voice[0])
    ...             staff.append(voice)
    ...         leaf = abjad.select.leaf(staff, 0)
    ...         abjad.attach(margin_markup, leaf)
    ...         group.append(staff)
    ...     score.append(group)
    ...     return score

::

    >>> preamble = r"""#(set-global-staff-size 16)
    ...
    ... \layout {
    ...     \context {
    ...         \Staff
    ...         \override VerticalAxisGroup.staff-staff-spacing.minimum-distance = 16
    ...     }
    ...     \context {
    ...         \Score
    ...         \override BarNumber.stencil = ##f
    ...         \override Beam.stencil = ##f
    ...         \override Flag.stencil = ##f
    ...         \override StaffGrouper.staff-staff-spacing = #'(
    ...             (basic-distance . 10) (minimum-distance . 10) (padding . 2))
    ...         \override Stem.stencil = ##f
    ...         \override TimeSignature.stencil = ##f
    ...         proportionalNotationDuration = #(ly:make-moment 1 25)
    ...     }
    ... }"""

----

Examples
--------

Examples 1a-d are based on the following row:

::

    >>> source = abjad.TwelveToneRow([5, 6, 4, 2, 3, 11, 9, 7, 8, 10, 0, 1])
    >>> abjad.show(source)

----

**Example 1a.** A chart based on the prime form of the row. How should this be described?

::

    >>> score = make_rotation_chart(source, "P")
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

----

**Example 1b.** A chart based on the inversion of the row. How should this be described?

::

    >>> score = make_rotation_chart(source.invert(), "I")
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

----

**Example 1c.** A chart based on the retrograde of the row. How should this be described?

::

    >>> score = make_rotation_chart(source.retrograde(), "R")
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

----

**Example 1d.** A chart based on the inversion of the retrograde of the row. What is
this?

::

    >>> score = make_rotation_chart(source.retrograde().invert(), "IR")
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

:author:`[Evans (3.2); ex. Igor Stravinsky, Abraham and Isaac (1962--63).]`
