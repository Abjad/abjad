Mapping lists to rhythms
========================

..  abjad::

    import abjad


Let's say you have a list of numbers that you want to convert into rhythmic
notation.  This is very easy to do. There are a number of related topics
that are presented separately as other tutorials.

Simple example
--------------

First create a list of integer representing numerators.  Then turn that list
into a list of Durations instances:

..  abjad::

    integers = [4, 2, 2, 4, 3, 1, 5]
    denominator = 8
    durations = [abjad.Duration(i, denominator) for i in integers]

Now we notate them using a single pitch with ``abjad.NoteMaker``:

..  abjad::

    maker = abjad.NoteMaker()
    notes = maker(["c'"], durations)
    staff = abjad.Staff(notes)
    show(staff)

There we have it. Durations notated based on a simple list of numbers.
Read the tutorials on splitting rhythms based on beats or bars in order to
notate more complex duration patterns. Also, consider how changing the
denominator in the Fraction above would change the series of durations.
