Tuplets
=======


Making a tuplet from a LilyPond input string
--------------------------------------------

You can make an Abjad tuplet from a multiplier and a LilyPond input string:

::

   >>> tuplet = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
   >>> show(tuplet)

.. image:: images/index-1.png



Making a tuplet from a list of other Abjad components
-----------------------------------------------------

You can also make a tuplet from a multiplier and a list of other Abjad
components:

::

   >>> leaves = [Note("fs'8"), Note("g'8"), Rest('r8')]
   >>> tuplet = Tuplet(Fraction(2, 3), leaves)
   >>> show(tuplet)

.. image:: images/index-2.png



Understanding the interpreter representation of a tuplet
--------------------------------------------------------

The interprer representation of an tuplet contains three parts:

::

   >>> tuplet
   Tuplet(2/3, [fs'8, g'8, r8])


``Tuplet`` tells you the tuplet's class.

``2/3`` tells you the tuplet's multiplier.

The list ``[fs'8, g'8, r8]`` shows the top-level components the tuplet
contains.


Understanding the string representation of a tuplet
---------------------------------------------------

The string representation of a tuplet contains four parts:

::

   >>> print tuplet
   {* 3:2 fs'8, g'8, r8 *}


Curly braces ``{`` and ``}`` indicate that the tuplet's music is interpreted
sequentially instead of simultaneously.

The asterisks ``*`` denote a fixed-multiplier tuplet.

``3:2`` tells you the tuplet's ratio.

The remaining arguments show the top-level components of tuplet.


Inspecting the LilyPond format of a tuplet
------------------------------------------

Get the LilyPond input format of any Abjad object with ``lilypond_format``:

::

   >>> tuplet.lilypond_format
   "\\times 2/3 {\n\tfs'8\n\tg'8\n\tr8\n}"


Use ``f()`` as a short-cut to print the LilyPond format of any Abjad object:

::

   >>> f(tuplet)
   \times 2/3 {
       fs'8
       g'8
       r8
   }



Selecting the music in a tuplet
-------------------------------

Slice a tuplet to select its components:

::

   >>> tuplet[:]
   SliceSelection(Note("fs'8"), Note("g'8"), Rest('r8'))



Inspecting a tuplet's leaves
----------------------------

Get the leaves in a tuplet with ``select_leaves()``:

::

   >>> tuplet.select_leaves()
   ContiguousSelection(Note("fs'8"), Note("g'8"), Rest('r8'))



Getting the length of a tuplet
------------------------------

The length of a tuplet is defined equal to the number of top-level components
the tuplet contains.

Get the length of a tuplet with ``len()``:

::

   >>> len(tuplet)
   3



Inspecting duration
-------------------

Use the inspector to get the duration of a voice:

::

   >>> inspect(tuplet).get_duration()
   Duration(1, 4)



Understanding rhythmic augmentation and diminution
--------------------------------------------------

A tuplet with a multiplier less than ``1`` constitutes a type of rhythmic
diminution:

::

   >>> tuplet.multiplier
   Multiplier(2, 3)


::

   >>> tuplet.is_diminution
   True


A tuplet with a multiplier greater than ``1`` is a type of rhythmic
augmentation:

::

   >>> tuplet.is_augmentation
   False



Changing the multiplier of a tuplet
-----------------------------------

You can change the multiplier of a tuplet with ``multiplier``:

::

   >>> tuplet.multiplier = Multiplier(4, 5)
   >>> show(tuplet)

.. image:: images/index-3.png



Adding one component to the end of a tuplet
--------------------------------------------

Add one component to the end of a tuplet with ``append``:

::

   >>> tuplet.append(Note("e'4."))
   >>> show(tuplet)

.. image:: images/index-4.png


You can also use a LilyPond input string:

::

   >>> tuplet.append("bf8")
   >>> show(tuplet)

.. image:: images/index-5.png



Adding many components to the end of a tuplet
---------------------------------------------

Add many components to the end of a tuplet with ``extend``:

::

   >>> notes = [Note("fs'32"), Note("e'32"), Note("d'32"), Rest((1, 32))]
   >>> tuplet.extend(notes)
   >>> show(tuplet)

.. image:: images/index-6.png


You can also use a LilyPond input string:

::

   >>> tuplet.extend("gs'8 a8") 
   >>> show(tuplet)

.. image:: images/index-7.png



Finding the index of a component in a tuplet
--------------------------------------------

Find the index of a component in a tuplet with ``index()``:

::

   >>> notes[1]
   Note("e'32")


::

   >>> tuplet.index(notes[1])
   6



Removing a tuplet component by index
------------------------------------

Use ``pop()`` to remove the last component of a tuplet:

::

   >>> tuplet.pop()
   Note('a8')
   >>> show(tuplet)

.. image:: images/index-8.png



Removing a tuplet component by reference
----------------------------------------

Remove tuplet components by reference with ``remove()``:

::

   >>> tuplet.remove(tuplet[3])
   >>> show(tuplet)

.. image:: images/index-9.png



Overriding attributes of the LilyPond tuplet number grob
--------------------------------------------------------

Override attributes of the LilyPond tuplet number grob like this:

::

   >>> string = 'tuplet-number::calc-fraction-text'
   >>> tuplet.override.tuplet_number.text = schemetools.Scheme(string)
   >>> tuplet.override.tuplet_number.color = 'red'


We'll place the tuplet into a Staff object, so that LilyPond does not complain
about the overrides we've applied, which lexically cannot appear in a
``\score`` block.

::

   >>> staff = Staff([tuplet])
   >>> show(staff)

.. image:: images/index-10.png


See LilyPond's documentation for lists of grob attributes available.


Overriding attributes of the LilyPond tuplet bracket grob
---------------------------------------------------------

Override attributes of the LilyPond tuplet bracket grob like this:

::

   >>> tuplet.override.tuplet_bracket.color = 'red'
   >>> show(staff)

.. image:: images/index-11.png


See LilyPond's documentation for lists of grob attributes available.
