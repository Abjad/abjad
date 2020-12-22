Staves
======


Making a staff from a LilyPond input string
-------------------------------------------

You can make a staff from a LilyPond input string:

::

    >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'4 c''1")
    >>> abjad.show(staff)


Making a staff from a list of Abjad components
----------------------------------------------

You can also make a staff from a list of other Abjad components:

::

    >>> tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), "c'4 d'4 e'4")
    >>> components = [tuplet, abjad.Note("f'2"), abjad.Note("g'1")]
    >>> staff = abjad.Staff(components)
    >>> abjad.show(staff)


Understanding the interpreter representation of a staff
-------------------------------------------------------

The interpreter representation of a staff contains three parts:

::

    >>> staff

``Staff`` tells you the staff's class.

``3`` tells you the staff's length (which is the number of top-level components
the staff contains).

Curly braces ``{`` and ``}`` tell you that the music inside the staff is
interpreted sequentially rather than simultaneously.


Getting the LilyPond format of a staff
--------------------------------------

Use ``abjad.lilypond()`` to get the LilyPond format of a staff:

::

    >>> string = abjad.lilypond(staff)
    >>> print(string)


Selecting the music in a staff
------------------------------

Slice a staff to select its components:

::

    >>> staff[:]


Selecting a staff's leaves
--------------------------

Use ``abjad.select(...).leaves()`` to select in the leaves in a staff:

::

    >>> abjad.select(staff).leaves()


Getting the length of a staff
-----------------------------

Use ``len()`` to get the length of a staff.

The length of a staff is defined equal to the number of top-level components
the staff contains:

::

    >>> len(staff)


Getting duration
----------------

Get the duration of a staff:

::

    >>> abjad.get.duration(staff)


Appending one component to the end of a staff
---------------------------------------------

Use ``append()`` to append one component to the end of a staff:

::

    >>> staff.append("d''2")
    >>> abjad.show(staff)

You can also use a LilyPond input string:

::

    >>> staff.append("cs''2")
    >>> abjad.show(staff)


Extending a staff with multiple components at once
--------------------------------------------------

Use ``extend()`` to extend a staff with multiple components at once:

::

    >>> notes = [abjad.Note("e''8"), abjad.Note("d''8"), abjad.Note("c''4")]
    >>> staff.extend(notes)
    >>> abjad.show(staff)

You can also use a LilyPond input string:

::

    >>> staff.extend("b'8 a'8 g'4")
    >>> abjad.show(staff)


Finding the index of a component in a staff
-------------------------------------------

Use ``index()`` to find the index of any component in a staff:

::

    >>> notes[0]

::

    >>> staff.index(notes[0])


Popping a staff component by index
----------------------------------

Use ``pop()`` to pop the last component of a staff:

::

    >>> staff[8]

::

    >>> staff.pop()
    >>> abjad.show(staff)


Removing a staff component by reference
---------------------------------------

Use ``remove()`` to remove any component in a staff by reference:

::

    >>> staff.remove(staff[-1])
    >>> abjad.show(staff)


Naming staves
-------------

You can name Abjad staves:

::

    >>> staff.name = "Example Staff"

Staff names appear in LilyPond input but not in notational output:

::

    >>> string = abjad.lilypond(staff)
    >>> print(string)

::

    >>> abjad.show(staff)


Changing the context of a voice
-------------------------------

The context of a staff is set to ``abjad.Staff`` by default:

::

    >>> staff.lilypond_type

But you can change the context of a staff if you want.

Change the context of a voice when you have defined a new LilyPond context
based on a LilyPond staff:

::

    >>> staff.lilypond_type = "CustomUserStaff"

::

    >>> staff.lilypond_type

::

    >>> string = abjad.lilypond(staff)
    >>> print(string)


Making parallel voices in a staff
---------------------------------

You can make a staff treat its contents as simultaneous with ``simultaneous``:

::

    >>> soprano_voice = abjad.Voice(r"b'4 a'8 g'8 a'4 d''4 b'4 g'4 a'2 \fermata")
    >>> alto_voice = abjad.Voice(r"d'4 d'4 d'4 fs'4 d'4 d'8 e'8 fs'2") 
    >>> abjad.override(soprano_voice).stem.direction = abjad.Up
    >>> abjad.override(alto_voice).stem.direction = abjad.Down
    >>> staff = abjad.Staff([soprano_voice, alto_voice])
    >>> staff.simultaneous = True
    >>> abjad.show(staff)
