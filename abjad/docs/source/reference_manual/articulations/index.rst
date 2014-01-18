Articulations
=============

Articulations model staccato dots, marcato wedges and other symbols.

Articulations attach to notes, rests or chords.


Creating articulations
----------------------

Create articulations like this:

::

   >>> articulation = Articulation('turn')



Understanding the interpreter representation of an articulation
---------------------------------------------------------------

The interpreter representation of an articulation looks like this:

::

   >>> articulation
   Articulation('turn')


``Articulation`` tells you the articulation's class.

``'staccato'`` tells you the articulation's name.


Attaching articulations to a leaf
---------------------------------

Use ``attach()`` to attach articulations to a leaf:

::

   >>> staff = Staff()
   >>> key_signature = KeySignature('g', 'major')
   >>> attach(key_signature, staff)
   >>> time_signature = TimeSignature((2, 4), partial=Duration(1, 8))
   >>> attach(time_signature, staff)
   >>> staff.extend("d'8 f'8 a'8 d''8 f''8 gs'4 r8 e'8 gs'8 b'8 e''8 gs''8 a'4")
   >>> attach(articulation, staff[5])


::

   >>> show(staff)

.. image:: images/index-1.png



Attaching articulations to many leaves
--------------------------------------

Write a loop to attach articulations to many leaves:


::

   >>> for leaf in staff[:6]:
   ...     staccato = Articulation('staccato')
   ...     attach(staccato, leaf)
   ... 


::

   >>> show(staff)

.. image:: images/index-2.png



Getting the articulations attached to a leaf
--------------------------------------------

Use the inspector to get the articulations attached to a leaf:

::

   >>> inspect_(staff[5]).get_indicators(Articulation)
   (Articulation('turn'), Articulation('staccato'))



Detaching articulations from a leaf
-----------------------------------

Detach articulations with ``detach()``:

::

   >>> detach(articulation, staff[5])
   (Articulation('turn'),)


::

   >>> show(staff)

.. image:: images/index-3.png



Understanding the string representation of an articulation
----------------------------------------------------------

The string representation of an articulation comprises two parts:

::

   >>> print str(articulation)
   -\turn


``-`` tells you the articulation's direction.

``\staccato`` tells you the articulation's LilyPond command.


Understanding the LilyPond format of an articulation
----------------------------------------------------

The LilyPond format of an articulation is the same as the articulation's string
representation:

::

   >>> print format(articulation, 'lilypond')
   -\turn



Controlling whether an articulation appears above or below the staff
--------------------------------------------------------------------

Use ``Up`` to force an articulation to appear above the staff:

::

   >>> articulation = Articulation('turn', Up)
   >>> attach(articulation, staff[5])


::

   >>> show(staff)

.. image:: images/index-4.png


Use ``Down`` to force an articulation to appear below the staff:

::

   >>> detach(articulation, staff[5])
   (Articulation('turn', Up),)


::

   >>> articulation = Articulation('turn', Down)
   >>> attach(articulation, staff[5])


::

   >>> show(staff)

.. image:: images/index-5.png



Comparing articulations
-----------------------

Articulations compare equal when name and direction strings compare equal:

::

   >>> Articulation('staccato', Up) == Articulation('staccato', Up)
   True


Otherwise articulations do not compare equal:

::

   >>> Articulation('staccato', Up) == Articulation('turn', Up)
   False


(This chapter's musical examples are based on Haydn's piano sonata number 42, 
Hob. XVI/27.)
