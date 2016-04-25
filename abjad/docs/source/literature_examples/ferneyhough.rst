Ferneyhough: *Unsichtbare Farben*
=================================

..  note::

    Explore the ``abjad/demos/ferneyhough/`` directory for the complete code to
    this example, or import it into your Python session directly with ``from
    abjad.demos import ferneyhough``.

Mikhïal Malt analyzes the rhythmic materials of Ferneyhough's `Unsichtbare
Farben` in `The OM Composer's Book 2`.

Malt explains that Ferneyhough used OpenMusic to create an "exhaustive
catalogue of rhythmic cells" such that:

    1.  They are subdivided into two pulses, with proportions from ``1/1`` to
        ``1/11``.

    2.  The second pulse is subdivided successively by ``1``, ``2``, ``3``,
        ``4``, ``5`` and ``6``.

Let's recreate Malt's results in Abjad.


The proportions
---------------

First we define proportions:

..  abjad::

    proportions = [(1, n) for n in range(1, 11 + 1)]

..  abjad::

    proportions

The transforms
--------------

Next we'll show how to divide a quarter note into various ratios, and then
divide the final `logical tie` of the resulting tuplet into yet another ratio:

..  import:: abjad.demos.ferneyhough.make_nested_tuplet:make_nested_tuplet

..  abjad::

    tuplet = make_nested_tuplet(Duration(1, 4), (1, 1), 5)
    staff = scoretools.Staff([tuplet], context_name='RhythmicStaff')
    show(staff)

..  abjad::

    tuplet = make_nested_tuplet(Duration(1, 4), (2, 1), 5)
    staff = scoretools.Staff([tuplet], context_name='RhythmicStaff')
    show(staff)

..  abjad::

    tuplet = make_nested_tuplet(Duration(1, 4), (3, 1), 5)
    staff = scoretools.Staff([tuplet], context_name='RhythmicStaff')
    show(staff)

A `logical tie` is a selection of notes or chords connected by ties. It lets us
talk about a notated rhythm of ``5/16``, for example, which can not be expressed
with only a single leaf.

Note how we can divide a tuplet whose outer proportions are ``3/5``, where
the second `logical tie` requires two notes to express the ``5/16`` duration:

..  abjad::

    normal_tuplet = Tuplet.from_duration_and_ratio(Duration(1, 4), (3, 5))
    staff = scoretools.Staff([normal_tuplet], context_name='RhythmicStaff')
    show(staff)

..  abjad::

    subdivided_tuplet = make_nested_tuplet(Duration(1, 4), (3, 5), 3)
    staff = scoretools.Staff([subdivided_tuplet], context_name='RhythmicStaff')
    show(staff)

The rhythms
-----------

Now that we know how to make the basic building block, let's make a lot of
tuplets all at once.

We'll set the duration of each tuplet equal to a quarter note:

..  abjad::

    duration = Fraction(1, 4)

And then we make one row of rhythms, with the last `logical tie` increasingly
subdivided:

..  import:: abjad.demos.ferneyhough.make_row_of_nested_tuplets:make_row_of_nested_tuplets

..  abjad::

    tuplets = make_row_of_nested_tuplets(duration, (2, 1), 6)
    staff = scoretools.Staff(tuplets, context_name='RhythmicStaff')
    show(staff)

If we can make one single row of rhythms, we can make many rows of rhythms.
Let's try:

..  import:: abjad.demos.ferneyhough.make_rows_of_nested_tuplets:make_rows_of_nested_tuplets

..  abjad::

    score = Score()
    for tuplet_row in make_rows_of_nested_tuplets(duration, 4, 6):
        score.append(scoretools.Staff(tuplet_row, context_name='RhythmicStaff'))

    show(score)

That's getting close to what we want, but the typography isn't as good as it
could be.

The score
---------

First we'll package up the logic for making the un-styled score into a single
function:

..  import:: abjad.demos.ferneyhough.make_score:make_score

..  abjad::

    score = make_score(Duration(1, 4), 4, 6)
    show(score)

Then we'll apply some formatting overrides to improve its overall appearance:

..  import:: abjad.demos.ferneyhough.configure_score:configure_score

..  abjad::

    configure_score(score)
    show(score)

..  note: Consult LilyPond's documentation on `proportional notation <http://www.lilypond.org/doc/v2.16/Documentation/notation/proportional-notation>`_
    to learn all about what the formatting overrides above do.

The proportional spacing makes the score much easier to read, but now the
notation is much too big.  We'll clean that up next.

The LilyPond file
-----------------

Let's adjust the overall size of our output, and put everything together:

..  import:: abjad.demos.ferneyhough.make_lilypond_file:make_lilypond_file

..  import:: abjad.demos.ferneyhough.configure_lilypond_file:configure_lilypond_file

..  abjad::

    lilypond_file = make_lilypond_file(Duration(1, 4), 11, 6)
    show(lilypond_file)
