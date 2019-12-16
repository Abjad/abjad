Articulations
=============

Articulations model staccato dots, marcato wedges and other symbols.

Articulations attach to notes, rests or chords.


Creating articulations
----------------------

Create articulations like this:

::

    >>> articulation = abjad.Articulation('turn')


Understanding the interpreter representation of an articulation
---------------------------------------------------------------

The interpreter representation of an articulation looks like this:

::

    articulation

``Articulation`` tells you the articulation's class.

``'staccato'`` tells you the articulation's name.


Attaching articulations to a leaf
---------------------------------

Use ``attach()`` to attach articulations to a leaf:

::

    >>> staff = abjad.Staff()
    >>> staff.extend("d'8 f'8 a'8 d''8 f''8 gs'4 r8 e'8 gs'8 b'8 e''8 gs''8 a'4")
    >>> key_signature = abjad.KeySignature('g', 'major')
    >>> abjad.attach(key_signature, staff[0])
    >>> time_signature = abjad.TimeSignature((2, 4), partial=(1, 8))
    >>> abjad.attach(time_signature, staff[0])
    >>> abjad.attach(articulation, staff[5])

::

    >>> show(staff)


Attaching articulations to many leaves
--------------------------------------

Write a loop to attach articulations to many leaves:


::

    >>> for leaf in staff[:6]:
    ...     staccato = abjad.Staccato()
    ...     abjad.attach(staccato, leaf)
    ...

::

    >>> show(staff)


Getting the articulations attached to a leaf
--------------------------------------------

Use the inspector to get the articulations attached to a leaf:

::

    >>> abjad.inspect(staff[5]).indicators(abjad.Staccato)


Detaching articulations from a leaf
-----------------------------------

Detach articulations with ``detach()``:

::

    >>> abjad.detach(abjad.Staccato, staff[5])

::

    >>> show(staff)


Understanding the string representation of an articulation
----------------------------------------------------------

The string representation of an articulation comprises two parts:

::

    >>> print(str(articulation))

``-`` tells you the articulation's direction.

``\staccato`` tells you the articulation's LilyPond command.


Understanding the LilyPond format of an articulation
----------------------------------------------------

The LilyPond format of an articulation is the same as the articulation's string
representation:

::

    >>> print(format(articulation, 'lilypond'))


Controlling whether an articulation appears above or below the staff
--------------------------------------------------------------------

Use ``Up`` to force an articulation to appear above the staff:

::

    >>> articulation = abjad.Articulation('turn', direction=abjad.Up)
    >>> abjad.attach(articulation, staff[5])

::

    >>> show(staff)

Use ``Down`` to force an articulation to appear below the staff:

::

    >>> abjad.detach(articulation, staff[5])

::

    >>> articulation = abjad.Articulation('turn', direction=Down)
    >>> abjad.attach(articulation, staff[5])

::

    >>> show(staff)


Comparing articulations
-----------------------

Articulations compare equal when name and direction strings compare equal:

::

    >>> abjad.Articulation('staccato', direction=Up) == abjad.Articulation('staccato', direction=abjad.Up)

Otherwise articulations do not compare equal:

::

    >>> abjad.Articulation('staccato', direction=abjad.Up) == abjad.Articulation('turn', direction=abjad.Up)

(This chapter's musical examples are based on Haydn's piano sonata number 42, 
Hob. XVI/27.)
