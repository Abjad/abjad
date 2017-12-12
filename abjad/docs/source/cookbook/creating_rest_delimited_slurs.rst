Creating rest-delimited slurs
=============================

..  abjad::

    import abjad


Take a look at the slurs in the following example and notice that
there is a pattern to how they arranged.

..  abjad::
    :hide:

    string = r"""
        \times 2/3 { c'4 d' r } 
        r8 e'4 <fs' a' c''>8 ~ q4 
        \times 4/5 { r16 g' r b' d'' } 
        df'4 c' ~ c'1
        """
    staff = abjad.Staff(string)
    leaves = abjad.select(staff).leaves(pitched=True)
    for run in abjad.select(leaves).runs():
        if 1 < len(run):
            selection = abjad.select(run)
            attach(abjad.Slur(), run)

    show(staff)

The pattern?  Slurs in the example span groups of notes and chords separated by
rests. 

Abjad makes it easy to create rest-delimited slurs in a structured way.


Entering input
--------------

Let's start with the note input like this:

..  abjad::

    string = r"""
        \times 2/3 { c'4 d' r } 
        r8 e'4 <fs' a' c''>8 ~ q4 
        \times 4/5 { r16 g' r b' d'' } 
        df'4 c' ~ c'1
        """
    staff = abjad.Staff(string)
    show(staff)


Grouping notes and chords
-------------------------

Next we'll group notes and chords together.

We add slur spanners inside our loop:

..  abjad::

    leaves = abjad.select(staff).leaves(pitched=True)
    for run in abjad.select(leaves).runs():
        if 1 < len(run):
            attach(abjad.Slur(), run)

Here's the result:

..  abjad::

    show(staff)

But there's a problem.

Four slur spanners were generated but only three slurs are shown.

Why? Because LilyPond ignores one-note slurs.


Skipping one-note slurs
-----------------------

Let's rewrite our example to prevent that from happening:

..  abjad::

    staff = abjad.Staff(string)
    leaves = abjad.select(staff).leaves(pitched=True)
    for run in abjad.select(leaves).runs():
        if 1 < len(run):
            attach(abjad.Slur(), run)

And here's the corrected result:

..  abjad::

    show(staff)
