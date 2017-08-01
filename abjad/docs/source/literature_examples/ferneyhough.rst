Ferneyhough: *Unsichtbare Farben*
=================================

..  abjad::

    import abjad
    from abjad.demos.ferneyhough import FerneyhoughDemo
    ferneyhough = FerneyhoughDemo()

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

Now we'll show how to divide a quarter note into various ratios, and then
divithe final `logical tie` of the resulting tuplet into yet another ratio:

..  abjad::

    tuplet = ferneyhough.make_nested_tuplet(abjad.Duration(1, 4), (1, 1), 5)
    staff = abjad.Staff([tuplet], context_name='RhythmicStaff')
    show(staff)

..  abjad::

    tuplet = ferneyhough.make_nested_tuplet(abjad.Duration(1, 4), (2, 1), 5)
    staff = abjad.Staff([tuplet], context_name='RhythmicStaff')
    show(staff)

..  abjad::

    tuplet = ferneyhough.make_nested_tuplet(abjad.Duration(1, 4), (3, 1), 5)
    staff = abjad.Staff([tuplet], context_name='RhythmicStaff')
    show(staff)

A `logical tie` is a selection of notes or chords connected by ties. It lets us
talk about a notated rhythm of ``5/16``, for example, which can not be expressed
with only a single leaf.

Note how we can divide a tuplet whose outer proportions are ``3/5``, where
the second `logical tie` requires two notes to express the ``5/16`` duration:

..  abjad::

    normal_tuplet = abjad.Tuplet.from_duration_and_ratio(abjad.Duration(1, 4), (3, 5))
    staff = abjad.Staff([normal_tuplet], context_name='RhythmicStaff')
    show(staff)

..  abjad::

    subdivided_tuplet = ferneyhough.make_nested_tuplet(abjad.Duration(1, 4), (3, 5), 3)
    staff = abjad.Staff([subdivided_tuplet], context_name='RhythmicStaff')
    show(staff)

The rhythms
-----------

Now that we know how to make the basic building block, let's make a lot of
tuplets all at once.

We'll set the duration of each tuplet equal to a quarter note:

..  abjad::

    duration = abjad.Duration(1, 4)

And then we make one row of rhythms, with the last `logical tie` increasingly
subdivided:

..  abjad::

    tuplets = ferneyhough.make_row_of_nested_tuplets(duration, (2, 1), 6)
    staff = abjad.Staff(tuplets, context_name='RhythmicStaff')
    show(staff)

If we can make one single row of rhythms, we can make many rows of rhythms.
Let's try:

..  abjad::

    score = abjad.Score()
    for tuplet_row in ferneyhough.make_rows_of_nested_tuplets(duration, 4, 6):
        staff = abjad.Staff(tuplet_row, context_name='RhythmicStaff')
        score.append(staff)

    show(score)

That's getting close to what we want, but the typography isn't as good as it
could be.

The score
---------

First we'll package up the logic for making the un-styled score into a single
function:

..  abjad::

    score = ferneyhough.make_score(abjad.Duration(1, 4), 4, 6)
    show(score)

Then we'll adjust the overall size of our output, and put everything together:

..  abjad::

    ferneyhough.configure_score(score)
    lilypond_file = ferneyhough.make_lilypond_file(abjad.Duration(1, 4), 11, 6)
    show(lilypond_file)

Explore the ``abjad/demos/ferneyhough/`` directory for the complete code to
this example, or import it into your Python session directly with ``from
abjad.demos import ferneyhough``.
