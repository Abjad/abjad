Tuplets
=======


Making a tuplet from a LilyPond input string
--------------------------------------------

You can create tuplets from a LilyPond input string:

::

    >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    >>> abjad.show(tuplet)


Making a tuplet from a list of other components
-----------------------------------------------

You can also make tuplets from a list of other components:

::

    >>> leaves = [abjad.Note("fs'8"), abjad.Note("g'8"), abjad.Rest('r8')]
    >>> tuplet = abjad.Tuplet((2, 3), leaves)
    >>> abjad.show(tuplet)


Understanding the interpreter representation of a tuplet
--------------------------------------------------------

The interprer representation of an tuplet contains three parts:

::

    >>> tuplet

``Tuplet`` tells you the tuplet's class.

``Multiplier(2, 3)`` tells you the tuplet's multiplier.

``[fs'8, g'8, r8]`` tells you the top-level components the tuplet contains.


Understanding the string representation of a tuplet
---------------------------------------------------

The string representation of a tuplet contains four parts:

::

    >>> print(tuplet)

Curly braces ``{`` and ``}`` indicate that the tuplet's music is interpreted
sequentially instead of simultaneously.

The asterisks ``*`` denote a fixed-multiplier tuplet.

``3:2`` tells you the tuplet's ratio.

The remaining arguments show the top-level components of tuplet.


Formatting tuplets
------------------

Use ``abjad.lilypond()`` to get the LilyPond format a tuplet:

::

    >>> print(abjad.lilypond(tuplet))


Selecting the music in a tuplet
-------------------------------

Select the music in a tuplet like this:

::

    >>> tuplet[:]


Selecting a tuplet's leaves
---------------------------

Use ``select(...).leaves()`` to get the leaves in a tuplet:

::

    >>> abjad.select(tuplet).leaves()


Getting the length of a tuplet
------------------------------

Use ``len()`` to get the length of a tuplet.

The length of a tuplet is defined equal to the number of top-level components
the tuplet contains:

::

    >>> len(tuplet)


Getting tuplet duration
-----------------------

Get the duration of a tuplet:

::

    >>> abjad.get.duration(tuplet)


Understanding rhythmic augmentation and diminution
--------------------------------------------------

A tuplet with a multiplier less than ``1`` constitutes a type of rhythmic
diminution:

::

    >>> tuplet.multiplier

::

    >>> tuplet.diminution()

A tuplet with a multiplier greater than ``1`` is a type of rhythmic
augmentation:

::

    >>> tuplet.augmentation()


Getting and setting the multiplier of a tuplet
----------------------------------------------

Get the multiplier of a tuplet like this:

::

    >>> tuplet.multiplier

Set the multiplier of a tuplet like this:

::

    >>> tuplet.multiplier = (4, 5)
    >>> abjad.show(tuplet)


Appending one component to the end of a tuplet
----------------------------------------------

Use ``append()`` to append one component to the end of a tuplet:

::

    >>> tuplet.append("e'4.")
    >>> abjad.show(tuplet)

You can also use a LilyPond input string:

::

    >>> tuplet.append("bf8")
    >>> abjad.show(tuplet)


Extending a tuplet with multiple components at once
---------------------------------------------------

Use ``extend()`` to extend a tuplet with multiple components at once:

::

    >>> notes = [abjad.Note("fs'32"), abjad.Note("e'32")]
    >>> notes.extend([abjad.Note("d'32"), abjad.Rest((1, 32))])
    >>> tuplet.extend(notes)
    >>> abjad.show(tuplet)

You can also use a LilyPond input string:

::

    >>> tuplet.extend("gs'8 a8") 
    >>> abjad.show(tuplet)


Finding the index of a component in a tuplet
--------------------------------------------

Use ``index()`` to find the index of any component in a tuplet:

::

    >>> notes[1]

::

    >>> tuplet.index(notes[1])


Popping a tuplet component by index
-----------------------------------

Use ``pop()`` to remove the last component of a tuplet:

::

    >>> tuplet.pop()
    >>> abjad.show(tuplet)


Removing a tuplet component by reference
----------------------------------------

Use ``remove()`` to remove any component from a tuplet by reference:

::

    >>> tuplet.remove(tuplet[3])
    >>> abjad.show(tuplet)


Overriding attributes of the LilyPond tuplet number grob
--------------------------------------------------------

Override attributes of the LilyPond tuplet number grob like this:

::

    >>> string = "tuplet-number::calc-fraction-text"
    >>> scheme = abjad.Scheme(string)
    >>> abjad.override(tuplet).tuplet_number.text = scheme
    >>> abjad.override(tuplet).tuplet_number.color = "red"
    >>> staff = abjad.Staff([tuplet])
    >>> abjad.show(staff)

See LilyPond's documentation for lists of grob attributes available.


Overriding attributes of the LilyPond tuplet bracket grob
---------------------------------------------------------

Override attributes of the LilyPond tuplet bracket grob like this:

::

    >>> abjad.override(tuplet).tuplet_bracket.color = "red"
    >>> abjad.show(staff)

See LilyPond's documentation for lists of grob attributes available.
