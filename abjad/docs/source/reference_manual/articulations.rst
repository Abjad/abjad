Articulations
=============

..  abjad::

    import abjad

Articulations model staccato dots, marcato wedges and other symbols.

Articulations attach to notes, rests or chords.


Creating articulations
----------------------

Create articulations like this:

..  abjad::

    articulation = abjad.Articulation('turn')


Understanding the interpreter representation of an articulation
---------------------------------------------------------------

The interpreter representation of an articulation looks like this:

..  abjad::

    articulation

``Articulation`` tells you the articulation's class.

``'staccato'`` tells you the articulation's name.


Attaching articulations to a leaf
---------------------------------

Use ``attach()`` to attach articulations to a leaf:

..  abjad::

    staff = abjad.Staff()
    staff.extend("d'8 f'8 a'8 d''8 f''8 gs'4 r8 e'8 gs'8 b'8 e''8 gs''8 a'4")
    key_signature = abjad.KeySignature('g', 'major')
    abjad.attach(key_signature, staff[0])
    time_signature = abjad.TimeSignature((2, 4), partial=(1, 8))
    abjad.attach(time_signature, staff[0])
    abjad.attach(articulation, staff[5])

..  abjad::

    show(staff)


Attaching articulations to many leaves
--------------------------------------

Write a loop to attach articulations to many leaves:


..  abjad::

    for leaf in staff[:6]:
        staccato = abjad.Staccato()
        abjad.attach(staccato, leaf)

..  abjad::

    show(staff)


Getting the articulations attached to a leaf
--------------------------------------------

Use the inspector to get the articulations attached to a leaf:

..  abjad::

    abjad.inspect(staff[5]).get_indicators(abjad.Staccato)


Detaching articulations from a leaf
-----------------------------------

Detach articulations with ``detach()``:

..  abjad::

    abjad.detach(abjad.Staccato, staff[5])

..  abjad::

    show(staff)


Understanding the string representation of an articulation
----------------------------------------------------------

The string representation of an articulation comprises two parts:

..  abjad::

    print(str(articulation))

``-`` tells you the articulation's direction.

``\staccato`` tells you the articulation's LilyPond command.


Understanding the LilyPond format of an articulation
----------------------------------------------------

The LilyPond format of an articulation is the same as the articulation's string
representation:

..  abjad::

    print(format(articulation, 'lilypond'))


Controlling whether an articulation appears above or below the staff
--------------------------------------------------------------------

Use ``Up`` to force an articulation to appear above the staff:

..  abjad::

    articulation = abjad.Articulation('turn', Up)
    abjad.attach(articulation, staff[5])

..  abjad::

    show(staff)

Use ``Down`` to force an articulation to appear below the staff:

..  abjad::

    abjad.detach(articulation, staff[5])

..  abjad::

    articulation = abjad.Articulation('turn', Down)
    abjad.attach(articulation, staff[5])

..  abjad::

    show(staff)


Comparing articulations
-----------------------

Articulations compare equal when name and direction strings compare equal:

..  abjad::

    abjad.Articulation('staccato', Up) == abjad.Articulation('staccato', Up)

Otherwise articulations do not compare equal:

..  abjad::

    abjad.Articulation('staccato', Up) == abjad.Articulation('turn', Up)

(This chapter's musical examples are based on Haydn's piano sonata number 42, 
Hob. XVI/27.)
