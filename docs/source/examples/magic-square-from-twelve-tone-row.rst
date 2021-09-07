Magic square, from twelve-tone row
==================================

..

----

The first function below accumulates the twelve transpositions of a twelve-tone row,
ordered by the pitch-classes of the row's inversion. The second function (and LilyPond
preamble) notate the result. Three rows used in compositions of the 1950s conclude the
example:

::

    >>> def make_transpositions(row):
    ...     transpositions = []
    ...     for pitch_class in row.invert():
    ...         n = pitch_class.number - row[0].number
    ...         transposition = row.transpose(n) 
    ...         transpositions.append(transposition)
    ...     return transpositions

::

    >>> def make_score(row):
    ...     score = abjad.Score(name="Score")
    ...     transpositions = make_transpositions(row)
    ...     for i, transposition in enumerate(transpositions):
    ...         notes = [abjad.Note(_, (1, 4)) for _ in transposition] 
    ...         voice = abjad.Voice(notes, name=f"Voice_{i}")
    ...         staff = abjad.Staff([voice], name=f"Staff_{i}")
    ...         score.append(staff)
    ...         number = notes[0].written_pitch.number
    ...         string = r"\markup \larger \with-color #blue"
    ...         string = string + r" { T \hspace #-0.75 \sub" + str(number) + "}"
    ...         markup = abjad.Markup(string, literal=True)
    ...         start_markup = abjad.StartMarkup(markup)
    ...         abjad.attach(start_markup, notes[0])
    ...     for note in score["Voice_0"]:
    ...         number = note.written_pitch.number
    ...         string = r"\markup \larger { IT \hspace #-0.75 \sub "
    ...         string += str(number)
    ...         string += " }"
    ...         markup = abjad.Markup(string, direction=abjad.Up, literal=True)
    ...         abjad.attach(markup, note)
    ...     note = abjad.select(score).note(0)
    ...     time_signature = abjad.TimeSignature((12, 4))
    ...     abjad.attach(time_signature, note)
    ...     return score

::

    >>> preamble = r"""#(set-global-staff-size 14)
    ...
    ... \layout {
    ...     \context {
    ...         \Staff
    ...         \override VerticalAxisGroup.staff-staff-spacing.minimum-distance = 11
    ...     }
    ...     \context {
    ...         \Score
    ...         \override BarLine.stencil = ##f
    ...         \override Clef.stencil = ##f
    ...         \override SpacingSpanner.strict-spacing = ##t
    ...         \override SystemStartBar.stencil = ##f
    ...         \override Stem.stencil = ##f
    ...         \override TextScript.color = #blue
    ...         \override TextScript.staff-padding = 5
    ...         \override TimeSignature.transparent = ##t
    ...         proportionalNotationDuration = #(ly:make-moment 1 16)
    ...     }
    ... }
    ... """

----

**Example 1.** Here are the 48 row forms of ``[7, 3, 8, 5, 4, 6, 0, 10, 11, 2, 9, 1]``:

    >>> row = abjad.TwelveToneRow([7, 3, 8, 5, 4, 6, 0, 10, 11, 2, 9, 1])
    >>> score = make_score(row)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

From the opening measure of Karlheinz Stockhausen's `Grüppen` (1955-57) for three
orchestras.

----

**Example 2.** Here are the 48 row forms of ``[3, 5, 2, 1, 10, 11, 9, 0, 8, 4, 7, 6]``:

    >>> row = abjad.TwelveToneRow([3, 5, 2, 1, 10, 11, 9, 0, 8, 4, 7, 6])
    >>> score = make_score(row)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

From Koblyakov's analysis of Pierre Boulez's `Marteau sans maître` (1955).

----

**Example 3.** Here are the 48 row forms of ``[9, 2, 11, 4, 1, 6, 8, 3, 5, 10, 7, 0]``:

    >>> row = abjad.TwelveToneRow([9, 2, 11, 4, 1, 6, 8, 3, 5, 10, 7, 0])
    >>> score = make_score(row)
    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file)

From Benjamin Britten's `The Turn of the Screw` (1954).

:author:`[Bača (3.3).]`
