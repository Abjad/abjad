Rests
=====


Making rests from strings
-------------------------

You can make rests from a LilyPond input string:

::

   >>> rest = Rest('r8')
   >>> show(rest)

.. image:: images/index-1.png



Making rests from durations
---------------------------

You can make rests from durations:

::

   >>> rest = Rest(Duration(1, 4))
   >>> show(rest)

.. image:: images/index-2.png



Making rests from other Abjad leaves
------------------------------------

You can also make rests from other Abjad leaves:

::

   >>> note = Note("d'4..")
   >>> rest = Rest(note)
   >>> show(rest)

.. image:: images/index-3.png



Understanding the interpreter representation of a rest
------------------------------------------------------

::

   >>> rest
   Rest('r4..')


``Rest`` tells you the rest's class.

``4..`` tells you that the rest's duration is equal to that of a doubly dotted
quarter note.


Making multimeasure rests
-------------------------

Create multimeasure rests like this:

::

   >>> multimeasure_rest = scoretools.MultimeasureRest('R1')
   >>> show(multimeasure_rest)

.. image:: images/index-4.png


Multiply the duration of multimeasure rests like this:

::

   >>> attach(Multiplier(4), multimeasure_rest)
   >>> staff = Staff([multimeasure_rest])
   >>> show(staff)

.. image:: images/index-5.png


Use a LilyPond command to compress full-bar rests:

::

   >>> command = indicatortools.LilyPondCommand('compressFullBarRests')
   >>> attach(command, staff)
   >>> show(staff)

.. image:: images/index-6.png



Getting and setting the written duration of rests
-------------------------------------------------

Get the written duration of rests like this:

::

   >>> rest.written_duration
   Duration(7, 16)


Set the written duration of rests like this:

::

   >>> rest.written_duration = Duration(3, 16)
   >>> show(rest)

.. image:: images/index-7.png
