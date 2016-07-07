Staves
======


Making a staff from a LilyPond input string
-------------------------------------------

You can make a staff from a LilyPond input string:

..  abjad::

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'4 c''1")
    show(staff)


Making a staff from a list of Abjad components
----------------------------------------------

You can also make a staff from a list of other Abjad components:

..  abjad::

    components = [Tuplet(Multiplier(2, 3), "c'4 d'4 e'4"), Note("f'2"), Note("g'1")]
    staff = Staff(components)
    show(staff)


Understanding the interpreter representation of a staff
-------------------------------------------------------

The interpreter representation of a staff contains three parts:

..  abjad::

    staff

``Staff`` tells you the staff's class.

``3`` tells you the staff's length (which is the number of top-level components
the staff contains).

Curly braces ``{`` and ``}`` tell you that the music inside the staff is
interpreted sequentially rather than simultaneously.


Inspecting the LilyPond format of a staff
-----------------------------------------

Use ``format()`` to get the LilyPond format of a staff:

..  abjad::

    print(format(staff, 'lilypond'))


Selecting the music in a staff
------------------------------

Slice a staff to select its components:

..  abjad::

    staff[:]


Selecting a staff's leaves
--------------------------

Use ``select(...).by_leaf()`` to select in the leaves in a staff:

..  abjad::

    select(staff).by_leaf()


Getting the length of a staff
-----------------------------

Use ``len()`` to get the length of a staff.

The length of a staff is defined equal to the number of top-level components
the staff contains:

..  abjad::

    len(staff)


Inspecting duration
-------------------

Use the inspector to get the duration of a staff:

..  abjad::

    inspect_(staff).get_duration()


Appending one component to the end of a staff
---------------------------------------------

Use ``append()`` to append one component to the end of a staff:

..  abjad::

    staff.append(Note("d''2"))
    show(staff)

You can also use a LilyPond input string:

..  abjad::

    staff.append("cs''2")
    show(staff)


Extending a staff with multiple components at once
--------------------------------------------------

Use ``extend()`` to extend a staff with multiple components at once:

..  abjad::

    notes = [Note("e''8"), Note("d''8"), Note("c''4")]
    staff.extend(notes)
    show(staff)

You can also use a LilyPond input string:

..  abjad::

    staff.extend("b'8 a'8 g'4")
    show(staff)


Finding the index of a component in a staff
-------------------------------------------

Use ``index()`` to find the index of any component in a staff:

..  abjad::

    notes[0]

..  abjad::

    staff.index(notes[0])


Popping a staff component by index
----------------------------------

Use ``pop()`` to pop the last component of a staff:

..  abjad::

    staff[8]

..  abjad::

    staff.pop()
    show(staff)


Removing a staff component by reference
---------------------------------------

Use ``remove()`` to remove any component in a staff by reference:

..  abjad::

    staff.remove(staff[-1])
    show(staff)


Naming staves
-------------

You can name Abjad staves:

..  abjad::

    staff.name = 'Example Staff'

Staff names appear in LilyPond input but not in notational output:

..  abjad::

    print(format(staff))

..  abjad::

    show(staff)


Changing the context of a voice
-------------------------------

The context of a staff is set to ``Staff`` by default:

..  abjad::

    staff.context_name

But you can change the context of a staff if you want.

Change the context of a voice when you have defined a new LilyPond context
based on a LilyPond staff:

..  abjad::

    staff.context_name = 'CustomUserStaff'

..  abjad::

    staff.context_name

..  abjad::

    print(format(staff))


Making parallel voices in a staff
---------------------------------

You can make a staff treat its contents as simultaneous with
``is_simultaneous``:

..  abjad::

    soprano_voice = Voice(r"b'4 a'8 g'8 a'4 d''4 b'4 g'4 a'2 \fermata")
    alto_voice = Voice(r"d'4 d'4 d'4 fs'4 d'4 d'8 e'8 fs'2") 
    override(soprano_voice).stem.direction = Up
    override(alto_voice).stem.direction = Down
    staff = Staff([soprano_voice, alto_voice])
    staff.is_simultaneous = True
    show(staff)
