Changing notes to rests
=======================

..  abjad::

    import abjad

Making a repeating pattern of notes
-----------------------------------

It is easy to make a repeating pattern of notes.

Multiplying the list ``[0, 2, 4, 9, 7]`` by ``4`` creates a new list of twenty
pitch numbers.

The call to ``NoteMaker`` creates our notes:

..  abjad::

    pitch_numbers = 4 * [0, 2, 4, 9, 7]
    duration = abjad.Duration(1, 8)
    maker = abjad.NoteMaker()
    notes = maker(pitch_numbers, duration)
    staff = abjad.Staff(notes)
    show(staff)


Iterating the notes in a staff
------------------------------

Use ``iterate()`` to iterate the notes in any expression:

..  abjad::

    for note in abjad.iterate(staff).by_leaf():
        note


Enumerating the notes in a staff
--------------------------------

Use Python's built-in ``enumerate()`` function to enumerate the elements in any
iterable:

..  abjad::

    generator = abjad.iterate(staff).by_leaf()
    for i, note in enumerate(generator):
        i, note


Changing notes to rests by index
--------------------------------

We can change every sixth note in a our score to a rest like this:

..  abjad::

    generator = abjad.iterate(staff).by_leaf()
    for i, note in enumerate(generator):
        if i % 6 == 5:
            rest = abjad.Rest('r8')
            staff[i] = rest

..  abjad::

    show(staff)


Changing notes to rests by pitch
--------------------------------

Let's make a new staff:

..  abjad::

    pitch_numbers = 4 * [0, 2, 4, 9, 7]
    duration = abjad.Duration(1, 8)
    maker = abjad.NoteMaker()
    notes = maker(pitch_numbers, duration)
    staff = abjad.Staff(notes)
    show(staff)

Now we can change every D4 to a rest like this:

..  abjad::

    generator = abjad.iterate(staff).by_leaf()
    for i, note in enumerate(generator):
        if abjad.inspect(note).get_sounding_pitch == "d'":
            rest = abjad.Rest('r8')
            staff[i] = rest

..  abjad::

    show(staff)
