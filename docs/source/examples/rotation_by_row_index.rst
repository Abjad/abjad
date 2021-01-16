:orphan:

Rotation, by row index
======================

..

----

::

    >>> def make_rotation_chart(permutation, label):
    ...     rotations = [0, -1, -2, -3, -4, -5]
    ...     score = abjad.Score(name="Score")
    ...     group = abjad.StaffGroup(name="Staff_Group")
    ...     left, right = permutation[:6], permutation[6:]
    ...     numerals = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
    ...     greek = {0: "α", 1: "β", 2: "γ", 3: "δ"}
    ...     for i, r in enumerate(rotations):
    ...         name = numerals.get(i, label)
    ...         string = fr"\markup \hcenter-in #8 {{ {name} }}"
    ...         start_markup = abjad.StartMarkup(markup=string)
    ...         voice = abjad.Voice(name=f"Voice_{abs(r)}")
    ...         staff = abjad.Staff([voice], name=f"Staff_{abs(r)}")
    ...         segments = [
    ...             left.rotate(r),
    ...             right.rotate(r),
    ...             left.rotate(r).transpose(left[0].number - left.rotate(r)[0].number),
    ...             right.rotate(r).transpose(right[0].number - right.rotate(r)[0].number),
    ...         ]
    ...         for i, segment in enumerate(segments):
    ...             notes = [abjad.Note(_, (1, 16)) for _ in segment]
    ...             voice.extend(notes)
    ...             string = fr"\markup \box {greek[i]}"
    ...             name = abjad.Markup(string, direction=abjad.Up, literal=True)
    ...             abjad.attach(name, notes[0])
    ...         leaf = abjad.select(staff).leaf(0)
    ...         abjad.attach(start_markup, leaf)
    ...         group.append(staff)
    ...     score.append(group)
    ...     time_signature = abjad.TimeSignature((6, 16))
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

Examples 1a-d are based on the following row:

::

    >>> source = abjad.TwelveToneRow([5, 6, 4, 2, 3, 11, 9, 7, 8, 10, 0, 1])
    >>> abjad.show(source)

----

**Example 1a.** A chart based on the prime form of the row. How should this be described?

::

    >>> score = make_rotation_chart(source, "P")
    >>> lilypond_file = abjad.LilyPondFile(items=[preamble, score])
    >>> abjad.show(lilypond_file)

----

**Example 1b.** A chart based on the inversion of the row. How should this be described?

::

    >>> score = make_rotation_chart(source.invert(), r"I(P)")
    >>> lilypond_file = abjad.LilyPondFile(items=[preamble, score])
    >>> abjad.show(lilypond_file)

----

**Example 1c.** A chart based on the retrograde of the row. How should this be described?

::

    >>> score = make_rotation_chart(source.retrograde(), "R(P)")
    >>> lilypond_file = abjad.LilyPondFile(items=[preamble, score])
    >>> abjad.show(lilypond_file)

----

**Example 1d.** A chart based on the inversion of the retrograde of the row. What is
this?

::

    >>> score = make_rotation_chart(source.retrograde().invert(), "IR(P)")
    >>> lilypond_file = abjad.LilyPondFile(items=[preamble, score])
    >>> abjad.show(lilypond_file)

:author:`[Evans (3.2). From Stravinsky's Abraham and Isaac (1962--63).]`
