:orphan:

Rotation, by row index
======================

..

----

::

    >>> def make_rotation_chart(segment, label):
    ...     score = abjad.Score(name="Score")
    ...     group = abjad.StaffGroup(name="Staff_Group")
    ...     length = len(segment)
    ...     assert length % 2 == 0
    ...     center = length // 2
    ...     left, right = segment[:center], segment[center:]
    ...     greek = {0: "α", 1: "β", 2: "γ", 3: "δ"}
    ...     for i in range(center):
    ...         name = i or label
    ...         string = fr"\markup \hcenter-in #8 {{ {name} }}"
    ...         start_markup = abjad.StartMarkup(markup=string)
    ...         voice = abjad.Voice(name=f"Voice_{i}")
    ...         staff = abjad.Staff([voice], name=f"Staff_{i}")
    ...         transforms = [
    ...             left.rotate(-i),
    ...             right.rotate(-i),
    ...             left.rotate(-i).transpose(left[0].number - left.rotate(-i)[0].number),
    ...             right.rotate(-i).transpose(right[0].number - right.rotate(-i)[0].number),
    ...         ]
    ...         for i, transform in enumerate(transforms):
    ...             notes = [abjad.Note(_, (1, 16)) for _ in transform]
    ...             voice.extend(notes)
    ...             string = fr"\markup \box {greek[i]}"
    ...             name = abjad.Markup(string, direction=abjad.Up, literal=True)
    ...             abjad.attach(name, notes[0])
    ...         leaf = abjad.select(staff).leaf(0)
    ...         abjad.attach(start_markup, leaf)
    ...         group.append(staff)
    ...     score.append(group)
    ...     time_signature = abjad.TimeSignature((center, 16))
    ...     leaf = abjad.select(score).leaf(0)
    ...     abjad.attach(time_signature, leaf)
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
    ...         \override Stem.stencil = ##f
    ...         \override TextScript.staff-padding = 2.3
    ...         \override TimeSignature.stencil = ##f
    ...         proportionalNotationDuration = #(ly:make-moment 1 25)
    ...     }
    ... }"""

----

Examples
--------

Example 1 is based on the following row:

::

    >>> source = abjad.TwelveToneRow([5, 6, 4, 2, 3, 11, 9, 7, 8, 10, 0, 1])
    >>> abjad.show(source)

**Example 1.** A chart based on the prime form of the row. How should this be described?

::

    >>> score = make_rotation_chart(source, "X")
    >>> lilypond_file = abjad.LilyPondFile(items=[preamble, score])
    >>> abjad.show(lilypond_file)

----

Example 2 is based on the following segment:

::

    >>> source = abjad.PitchClassSegment([-1, 7, -1, 12, 1, 3, 5, 6])
    >>> abjad.show(source)

** Example 2.**

::

    >>> score = make_rotation_chart(source, "Y")
    >>> lilypond_file = abjad.LilyPondFile(items=[preamble, score])
    >>> abjad.show(lilypond_file)

:author:`[Evans (3.2). From Stravinsky's Abraham and Isaac (1962--63).]`
