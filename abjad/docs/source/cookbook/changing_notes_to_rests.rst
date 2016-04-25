Changing notes to rests
=======================


Making a repeating pattern of notes
-----------------------------------

It is easy to make a repeating pattern of notes.

Multiplying the list ``[0, 2, 4, 9, 7]`` by ``4`` creates a new list of twenty
pitch numbers.

The call to ``scoretools.make_notes()`` creates our notes:

..  abjad::

    pitch_numbers = 4 * [0, 2, 4, 9, 7]
    duration = Duration(1, 8)
    notes = scoretools.make_notes(pitch_numbers, duration)
    staff = Staff(notes)
    show(staff)


Iterating the notes in a staff
------------------------------

Use ``iterate()`` to iterate the notes in any expression:

..  abjad::

    for note in iterate(staff).by_class(Note):
        note


Enumerating the notes in a staff
--------------------------------

Use Python's built-in ``enumerate()``
function to enumerate the elements in any iterable:

..  abjad::

    generator = iterate(staff).by_class(Note)
    for i, note in enumerate(generator):
        i, note


Changing notes to rests by index
--------------------------------

We can change every sixth note in a our score to a rest like this:

..  abjad::

    generator = iterate(staff).by_class(Note)
    for i, note in enumerate(generator):
        if i % 6 == 5:
            rest = Rest('r8')
            staff[i] = rest

..  abjad::

    show(staff)


Changing notes to rests by pitch
--------------------------------

Let's make a new staff:

..  abjad::

    pitch_numbers = 4 * [0, 2, 4, 9, 7]
    duration = Duration(1, 8)
    notes = scoretools.make_notes(pitch_numbers, duration)
    staff = Staff(notes)
    show(staff)

Now we can change every D4 to a rest like this:

..  abjad::

    generator = iterate(staff).by_class(Note)
    for i, note in enumerate(generator):
        if inspect_(note).get_sounding_pitch == "d'":
            rest = Rest('r8')
            staff[i] = rest

..  abjad::

    show(staff)
