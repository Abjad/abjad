:orphan:

Tuplets
=======

Making a tuplet from a LilyPond input string
--------------------------------------------

You can create tuplets from a LilyPond input string:

::

    >>> tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8")
    >>> abjad.show(tuplet)


Making a tuplet from a list of other components
-----------------------------------------------

You can also make tuplets from a list of other components:

::

    >>> leaves = [abjad.Note("fs'8"), abjad.Note("g'8"), abjad.Rest('r8')]
    >>> tuplet = abjad.Tuplet("3:2", leaves)
    >>> abjad.show(tuplet)

Understanding the interpreter representation of a tuplet
--------------------------------------------------------

The interprer representation of an tuplet contains three parts:

::

    >>> tuplet

``Tuplet`` tells you the tuplet's class.

``"3:2"`` tells you the tuplet's ratio.

``"fs'8, g'8, r8"`` tells you the top-level components the tuplet contains.

Understanding the string representation of a tuplet
---------------------------------------------------

The string representation of a tuplet is the same as the interpreter representation:

::

    >>> print(tuplet)

Formatting tuplets
------------------

Use ``abjad.lilypond()`` to get the LilyPond format a tuplet:

::

    >>> string = abjad.lilypond(tuplet)
    >>> print(string)

Selecting the music in a tuplet
-------------------------------

Select the music in a tuplet like this:

::

    >>> tuplet[:]

Selecting a tuplet's leaves
---------------------------

Use ``abjad.select.leaves()`` to get the leaves in a tuplet:

::

    >>> abjad.select.leaves(tuplet)

Getting the length of a tuplet
------------------------------

Use ``len()`` to get the length of a tuplet.

The length of a tuplet is defined equal to the number of top-level components the tuplet
contains:

::

    >>> len(tuplet)

Getting tuplet duration
-----------------------

Get the duration of a tuplet:

::

    >>> abjad.get.duration(tuplet)

Understanding rhythmic augmentation and diminution
--------------------------------------------------

A tuplet with a ratio greather than ``1:1`` constitutes a type of rhythmic diminution:

::

    >>> tuplet.ratio

::

    >>> tuplet.ratio.is_diminished()

A tuplet with a ratio less than ``1:1`` is a type of rhythmic augmentation:

::

    >>> tuplet.ratio.is_augmented()

Getting and setting the ratio of a tuplet
-----------------------------------------

Get the ratio of a tuplet like this:

::

    >>> tuplet.ratio

Set the ratio of a tuplet like this:

::

    >>> tuplet.ratio = abjad.Ratio(5, 4)
    >>> abjad.show(tuplet)

Appending one component to the end of a tuplet
----------------------------------------------

Use ``append()`` to append one component to the end of a tuplet:

::

    >>> note = abjad.Note("e'4.")
    >>> tuplet.append(note)
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

    >>> abjad.override(tuplet).TupletNumber.text = "#tuplet-number::calc-fraction-text"
    >>> abjad.override(tuplet).TupletNumber.color = "#red"
    >>> staff = abjad.Staff([tuplet])
    >>> abjad.show(staff)

See LilyPond's documentation for lists of grob attributes available.

Overriding attributes of the LilyPond tuplet bracket grob
---------------------------------------------------------

Override attributes of the LilyPond tuplet bracket grob like this:

::

    >>> abjad.override(tuplet).TupletBracket.color = "#red"
    >>> abjad.show(staff)

See LilyPond's documentation for lists of grob attributes available.
