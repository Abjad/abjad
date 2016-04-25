Mozart: *Musikalisches Würfelspiel*
===================================

..  note::

    Explore the ``abjad/demos/mozart/`` directory for the complete code to this
    example, or import it into your Python session directly with ``from
    abjad.demos import mozart``.

..  abjad::
    :hide:

    import random
    random.seed(0)

Mozart's dice game is a method for aleatorically generating
sixteen-measure-long minuets.  For each measure, two six-sided dice are rolled,
and the sum of the dice used to look up a measure number in one of two tables
(one for each half of the minuet).  The measure number then locates a single
measure from a collection of musical fragments.  The fragments are concatenated
together, and "music" results.

Implementing the dice game in a composition environment is somewhat akin to
(although also somewhat more complicated than) the ubiquitous `hello world
program <http://en.wikipedia.org/wiki/Hello_world_program>`_ which every
programming language uses to demonstrate its basic syntax.

..  figure:: images/mozart-tables.png
    :align: center
    :width: 640px

    *Part of a pen-and-paper implementation from the 20th century.*

..  note::

    The musical dice game in question (*k516f*) has long been attributed to
    Mozart, albeit inconclusively.  Its actual provenance is a musicological
    problem with which we are unconcerned here.

The materials
-------------

At the heart of the dice game is a large collection, *or corpus*, of musical
fragments.  Each fragment is a single 3/8 measure, consisting of a treble voice
and a bass voice.  Traditionally, these fragments are stored in a "score", or
"table of measures", and located via two tables of measure numbers, which act
as lookups, indexing into that collection.

Duplicate measures in the original corpus are common.  Notably, the 8th measure
- actually a pair of measures represent the first and second alternate ending
of the first half of the minuet - are always identical.  The last measure of
the piece is similarly limited - there are only two possibilities rather than
the usual eleven (for the numbers 2 to 12, being all the possible sums of two
6-sided dice).

How might we store this corpus compactly?

Some basic musical information in Abjad can be stored as strings, rather than
actual collections of class instances.  Abjad can parse simple LilyPond strings
via :py:func:`p <abjad.tools.systemtools.p>`, which interprets a subset of LilyPond
syntax, and understands basic concepts like notes, chords, rests and skips, as
well as beams, slurs, ties, and articulations.

..  abjad::

    staff = Staff("""
        c'4 ( d'4 <cs' e'>8 ) -. r8 
        <g' b' d''>4 ^ \marcato ~ <g' b' d''>1
        """)
    print(format(staff))

..  abjad::
    :stylesheet: non-proportional.ly

    show(staff)

So, instead of storing our musical information as Abjad components, we'll
represent each fragment in the corpus as a pair of strings: one representing
the bass voice contents, and the other representing the treble.  This pair of
strings can be packaged together into a collection.  For this implementation,
we'll package them into a dictionary.  Python dictionaries are cheap, and often
provide more clarity than lists; the composer does not have to rely on
remembering a convention for what data should appear in which position in a
list - they can simply label that data semantically.  In our musical
dictionary, the treble voice will use the key 't' and the bass voice will use
the key 'b'.

..  abjad::

    fragment = {'t': "g''8 ( e''8 c''8 )", 'b': '<c e>4 r8'}

Instead of relying on measure number tables to find our fragments - as in the
original implementation, we'll package our fragment dictionaries into a list of
lists of fragment dictionaries.  That is to say, each of the sixteen measures
in the piece will be represented by a list of fragment dictionaries.
Furthermore, the 8th measure, which breaks the pattern, will simply be a list
of two fragment dictionaries.  Structuring our information in this way lets us
avoid using measure number tables entirely; Python's list-indexing affordances
will take care of that for us.  The complete corpus looks like this:

..  import:: abjad.demos.mozart.make_mozart_measure_corpus:make_mozart_measure_corpus

We can then use the :py:func:`~abjad.tools.systemtools.p` function we saw earlier
to "build" the treble and bass components of a measure like this:

..  import:: abjad.demos.mozart.make_mozart_measure:make_mozart_measure

Let's try with a measure-definition of our own:

..  abjad::

    my_measure_dict = {'b': r'c4 ^\trill r8', 't': "e''8 ( c''8 g'8 )"}
    treble, bass = make_mozart_measure(my_measure_dict)

..  abjad::

    print(format(treble))

..  abjad::

    print(format(bass))

Now with one from the Mozart measure collection defined earlier.
We'll grab the very last choice for the very last measure:

..  abjad::

    my_measure_dict = make_mozart_measure_corpus()[-1][-1]
    treble, bass = make_mozart_measure(my_measure_dict)

..  abjad::

    print(format(treble))

..  abjad::

    print(format(bass))

The structure
-------------

After storing all of the musical fragments into a corpus, concatenating those
elements into a musical structure is relatively trivial.  We'll use the
:py:func:`~random.choice` function from Python's `random` module.
:py:func:`random.choice` randomly selects one element from an input list.

..  abjad::

    import random
    my_list = [1, 'b', 3]
    my_result = [random.choice(my_list) for i in range(20)]
    my_result

Our corpus is a list comprising sixteen sublists, one for each measure in the
minuet.  To build our musical structure, we can simply iterate through the
corpus and call `choice` on each sublist, appending the chosen results to
another list.  The only catch is that the *eighth* measure of our minuet is
actually the first-and-second-ending for the repeat of the first phrase.  The
sublist of the corpus for measure eight contains *only* the first and second
ending definitions, and both of those measures should appear in the final
piece, always in the same order.  We'll have to intercept that sublist while we
iterate through the corpus and apply some different logic.

The easist way to intercept measure eight is to use the Python builtin
`enumerate`, which allows you to iterate through a collection while also
getting the index of each element in that collection:

..  import:: abjad.demos.mozart.choose_mozart_measures:choose_mozart_measures

..  note::

    In `choose_mozart_measures` we test for index *7*, rather then *8*, because
    list indices count from *0* instead of *1*.

The result will be a *seventeen*-item-long list of measure definitions:

..  abjad::

    choices = choose_mozart_measures()
    for i, measure in enumerate(choices):
        print(i, measure)

The score
---------

Now that we have our raw materials, and a way to organize them, we can start
building our score.  The tricky part here is figuring out how to implement
LilyPond's repeat structure in Abjad.  LilyPond structures its repeats
something like this:

::

    \repeat volta n {
        music to be repeated
    }

    \alternative {
        { ending 1 }
        { ending 2 }
        { ending n }
    }

    ...music after the repeat...

What you see above is really just two containers, each with a little text
("\repeat volta n" and "alternative") prepended to their opening curly brace.
To create that structure in Abjad, we'll need to use the
:py:class:`~abjad.tools.indicatortools.LilyPondCommand` class, which allows you
to place LilyPond commands like "\break" relative to any score component:

..  abjad::

    container = Container("c'4 d'4 e'4 f'4")
    command = indicatortools.LilyPondCommand('before-the-container', 'before')
    attach(command, container)
    command = indicatortools.LilyPondCommand('after-the-container', 'after')
    attach(command, container)
    command = indicatortools.LilyPondCommand('opening-of-the-container', 'opening')
    attach(command, container)
    command = indicatortools.LilyPondCommand('closing-of-the-container', 'closing')
    attach(command, container)
    command = indicatortools.LilyPondCommand('to-the-right-of-a-note', 'right')
    attach(command, container[2])
    print(format(container))

Notice the second argument to each
:py:class:`~abjad.tools.indicatortools.LilyPondCommand` above, like `before`
and `closing`.  These are format slot indications, which control where the
command is placed in the LilyPond code relative to the score element it is
attached to.  To mimic LilyPond's repeat syntax, we'll have to create two
:py:class:`~abjad.tools.indicatortools.LilyPondCommand` instances, both using
the "before" format slot, insuring that their command is placed before their
container's opening curly brace.

Now let's take a look at the code that puts our score together:

..  import:: abjad.demos.mozart.make_mozart_score:make_mozart_score

..  abjad::
    :stylesheet: non-proportional.ly

    score = make_mozart_score()
    show(score)

..  note::

    Our instrument name got cut off!  Looks like we need to do a little
    formatting.  Keep reading...

The document
------------

As you can see above, we've now got our randomized minuet.  However, we can
still go a bit further.  LilyPond provides a wide variety of settings for
controlling the overall *look* of a musical document, often through its
`\header`, `\layout` and `\paper` blocks.  Abjad, in turn, gives us
object-oriented access to these settings through the its `lilypondfiletools`
module.

We'll use :py:func:`abjad.tools.lilypondfiletools.make_basic_lilypond_file` to
wrap our :py:class:`~abjad.tools.scoretools.Score` inside a
:py:class:`~abjad.tools.lilypondfiletools.LilyPondFile` instance.  From there
we can access the other "blocks" of our document to add a title, a composer's
name, change the global staff size, paper size, staff spacing and so forth.

..  import:: abjad.demos.mozart.make_mozart_lilypond_file:make_mozart_lilypond_file

..  abjad::

    lilypond_file = make_mozart_lilypond_file()
    print(lilypond_file)

..  abjad::

    print(format(lilypond_file.header_block))

..  abjad::

    print(format(lilypond_file.header_block))

..  abjad::

    print(format(lilypond_file.layout_block))

..  abjad::

    print(format(lilypond_file.layout_block))

..  abjad::

    print(format(lilypond_file.paper_block))

..  abjad::

    print(format(lilypond_file.paper_block))

And now the final result:

..  abjad::
    :stylesheet: non-proportional.ly

    show(lilypond_file)
