Enumeration, of rhythmic cells
==============================

Mikhïal Malt analyzes the rhythmic materials of Ferneyhough's `Unsichtbare Farben` in
`The OM Composer's Book 2`. Malt explains that Ferneyhough used OpenMusic to create an
"exhaustive catalogue of rhythmic cells" such that two conditions are met. First,
rhythmic cells are subdivided into two pulses, with proportions from 1/1 to 1/11. Second,
the second pulse of each cell is subdivided into 1, 2, 3, 4, 5, 6 parts. Let's recreate
Malt's results in Abjad.

First we define proportions:

::

    >>> proportions = [(1, n) for n in range(1, 11 + 1)]

::

    >>> proportions

Then we define a function to make the type of outer tuplet Malt describes:

::

    >>> def make_outer_tuplet(duration, ratio):
    ...     duration = abjad.Duration(duration)
    ...     ratio = abjad.Ratio(ratio)
    ...     basic_prolated_duration = duration / abjad.math.weight(ratio.numbers)
    ...     basic_written_duration = basic_prolated_duration.equal_or_greater_assignable
    ...     written_durations = [n * basic_written_duration for n in ratio.numbers]
    ...     denominator = duration.denominator
    ...     durations = [(n, denominator) for n in ratio.numbers]
    ...     maker = abjad.NoteMaker()
    ...     notes = maker([0], durations)
    ...     tuplet = abjad.Tuplet.from_duration(duration, notes)
    ...     tuplet.normalize_multiplier()
    ...     tuplet.force_fraction = True
    ...     tuplet.hide = tuplet.trivial()
    ...     return tuplet

We call the function like this:

::

    >>> duration, ratio = (1, 4), (1, 2)
    >>> make_outer_tuplet(duration, ratio)

To visualize the results, let's define a helper to wrap a single tuplet in a score:

::

    >>> def tuplet_to_score(tuplet):
    ...     staff = abjad.Staff([tuplet], lilypond_type="RhythmicStaff", name="Staff")
    ...     score = abjad.Score([staff], name="Score")
    ...     return score

And let's define another function to make a bunch of LilyPond settings:

::

    >>> def configure_score(score):
    ...     moment = abjad.SchemeMoment((1, 56))
    ...     abjad.setting(score).proportional_notation_duration = moment
    ...     abjad.setting(score).tuplet_full_length = True
    ...     abjad.override(score).bar_line.stencil = False
    ...     abjad.override(score).bar_number.transparent = True
    ...     abjad.override(score).spacing_spanner.uniform_stretching = True
    ...     abjad.override(score).spacing_spanner.strict_note_spacing = True
    ...     abjad.override(score).time_signature.stencil = False
    ...     abjad.override(score).tuplet_bracket.padding = 2
    ...     abjad.override(score).tuplet_bracket.staff_padding = 4
    ...     scheme = abjad.Scheme("tuplet-number::calc-fraction-text")
    ...     abjad.override(score).tuplet_number.text = scheme

Then we can visualize output of the function that makes our outer tuplets:

::

    >>> duration, ratio = (1, 4), (1, 2)
    >>> tuplet = make_outer_tuplet(duration, ratio)
    >>> score = tuplet_to_score(tuplet)
    >>> configure_score(score)
    >>> abjad.show(score)

::

    >>> duration, ratio = (1, 4), (1, 4)
    >>> tuplet = make_outer_tuplet(duration, ratio)
    >>> score = tuplet_to_score(tuplet)
    >>> configure_score(score)
    >>> abjad.show(score)

Then we define a function to make the type of nested tuplet implied in Malt's
description:

::

    >>> def make_nested_tuplet(
    ...     tuplet_duration,
    ...     outer_tuplet_proportions,
    ...     inner_tuplet_subdivision_count,
    ... ):
    ...     outer_tuplet = make_outer_tuplet(tuplet_duration, outer_tuplet_proportions)
    ...     inner_tuplet_proportions = inner_tuplet_subdivision_count * [1]
    ...     selector = abjad.select().leaves()
    ...     last_leaf = selector(outer_tuplet)[-1]
    ...     logical_tie = abjad.get.logical_tie(last_leaf)
    ...     abjad.mutate.logical_tie_to_tuplet(logical_tie, inner_tuplet_proportions)
    ...     inner_tuplet = outer_tuplet[-1]
    ...     inner_tuplet.force_fraction = True
    ...     inner_tuplet.hide = inner_tuplet.trivial()
    ...     return outer_tuplet

Now we'll show how to divide a quarter note into various ratios, and then divide the
final logical tie of the resulting tuplet into yet another ratio:

::

    >>> tuplet = make_nested_tuplet((1, 4), (1, 1), 5)
    >>> score = tuplet_to_score(tuplet)
    >>> configure_score(score)
    >>> abjad.show(score)

::

    >>> tuplet = make_nested_tuplet((1, 4), (2, 1), 5)
    >>> score = tuplet_to_score(tuplet)
    >>> configure_score(score)
    >>> abjad.show(score)

::

    >>> tuplet = make_nested_tuplet((1, 4), (3, 1), 5)
    >>> score = tuplet_to_score(tuplet)
    >>> configure_score(score)
    >>> abjad.show(score)

A logical tie is a selection of notes or chords connected by ties. It lets us talk about
a notated rhythm of ``5/16``, for example, which can not be expressed with only a single
leaf. Note how we can divide a tuplet whose outer proportions are ``3/5``, where the
second logical tie requires two notes to express the ``5/16`` duration:

::

    >>> tuplet = make_outer_tuplet((1, 4), (3, 5))
    >>> score = tuplet_to_score(tuplet)
    >>> configure_score(score)
    >>> abjad.show(score)

Then we can subdivide the logical tie with the duration of ``5/16`` into 3 parts:

::

    >>> tuplet = make_nested_tuplet((1, 4), (3, 5), 3)
    >>> score = tuplet_to_score(tuplet)
    >>> configure_score(score)
    >>> abjad.show(score)

Then we define a function to make one row of nested tuplets:

::

    >>> def make_row_of_nested_tuplets(
    ...     tuplet_duration, outer_tuplet_proportions, column_count
    ... ):
    ...     assert 0 < column_count
    ...     row_of_nested_tuplets = []
    ...     for n in range(column_count):
    ...         inner_tuplet_subdivision_count = n + 1
    ...         nested_tuplet = make_nested_tuplet(
    ...             tuplet_duration,
    ...             outer_tuplet_proportions,
    ...             inner_tuplet_subdivision_count,
    ...         )
    ...         row_of_nested_tuplets.append(nested_tuplet)
    ...     return row_of_nested_tuplets

Now that we know how to make the basic building block, let's make a lot of tuplets all at
once. We'll set the duration of each tuplet equal to a quarter note. Then we make one row
of rhythms, with the last logical tie increasingly subdivided:

::

    >>> tuplet_duration = (1, 4)
    >>> tuplets = make_row_of_nested_tuplets(tuplet_duration, (2, 1), 6)
    >>> staff = abjad.Staff(tuplets, lilypond_type="RhythmicStaff")
    >>> abjad.override(staff).bar_line.stencil = False
    >>> abjad.override(staff).time_signature.stencil = False
    >>> abjad.show(staff)

Then we define a function to accumulate multiple rows:

::

    >>> def make_rows_of_nested_tuplets(tuplet_duration, row_count, column_count):
    ...     assert 0 < row_count
    ...     rows_of_nested_tuplets = []
    ...     for n in range(row_count):
    ...         outer_tuplet_proportions = (1, n + 1)
    ...         row_of_nested_tuplets = make_row_of_nested_tuplets(
    ...             tuplet_duration, outer_tuplet_proportions, column_count
    ...         )
    ...         rows_of_nested_tuplets.append(row_of_nested_tuplets)
    ...     return rows_of_nested_tuplets

We can make 4 rows with 6 columns like this:

::

    >>> score = abjad.Score(name="Score")
    >>> abjad.override(score).bar_line.stencil = False
    >>> abjad.override(score).time_signature.stencil = False
    >>> for tuplet_row in make_rows_of_nested_tuplets(tuplet_duration, 4, 6):
    ...     staff = abjad.Staff(tuplet_row, lilypond_type="RhythmicStaff")
    ...     score.append(staff)
    ...
    >>> abjad.show(score)

Now let's bundle all our score-making logic in one place:

::

    >>> def make_score(tuplet_duration, row_count, column_count):
    ...     score = abjad.Score(name="Score")
    ...     rows = make_rows_of_nested_tuplets(tuplet_duration, row_count, column_count)
    ...     for row in rows:
    ...         staff = abjad.Staff(row, lilypond_type="RhythmicStaff")
    ...         score.append(staff)
    ...     return score

::

    >>> tuplet_duration, row_count, column_count = (1, 4), 4, 6
    >>> score = make_score(tuplet_duration, row_count, column_count)
    >>> abjad.show(score)

And a function to make and configure the layout of a  LilyPond file:

::

    >>> def configure_lilypond_file(lilypond_file):
    ...     lilypond_file._default_paper_size = "11x17", "portrait"
    ...     lilypond_file._global_staff_size = 12
    ...     lilypond_file.layout_block.indent = 0
    ...     lilypond_file.layout_block.ragged_right = True
    ...     lilypond_file.paper_block.ragged_bottom = True
    ...     spacing_vector = abjad.SpacingVector(0, 0, 8, 0)
    ...     lilypond_file.paper_block.system_system_spacing = spacing_vector

::

    >>> def make_lilypond_file(tuplet_duration, row_count, column_count):
    ...     score = make_score(tuplet_duration, row_count, column_count)
    ...     configure_score(score)
    ...     lilypond_file = abjad.LilyPondFile.new(score)
    ...     configure_lilypond_file(lilypond_file)
    ...     return lilypond_file

Then we'll adjust the overall size of our output, and put everything together:

::

    >>> configure_score(score)
    >>> tuplet_duration, row_count, column_count = (1, 4), 11, 6
    >>> lilypond_file = make_lilypond_file(tuplet_duration, row_count, column_count)
    >>> abjad.show(lilypond_file)
