Notes
=====


Making notes from a LilyPond input string
-----------------------------------------

You can make notes from a LilyPond input string:

::

   >>> note = Note("c'4")
   >>> show(note)

.. image:: images/index-1.png



Making notes from numbers
-------------------------

You can also make notes from a pitch number and duration:

::

   >>> note = Note(0, Duration(1, 4))
   >>> show(note)

.. image:: images/index-2.png



Getting and setting the written pitch of notes
----------------------------------------------

Get the written pitch of notes like this:

::

   >>> note.written_pitch
   NamedPitch("c'")


Set the written pitch of notes like this:

::

   >>> note.written_pitch = NamedPitch("cs'")
   >>> show(note)

.. image:: images/index-3.png


Or this:

::

   >>> note.written_pitch = "d'"
   >>> show(note)

.. image:: images/index-4.png


Or this:

::

   >>> note.written_pitch = 3
   >>> show(note)

.. image:: images/index-5.png



Getting and setting the written duration of notes
-------------------------------------------------

Get the written duration of notes like this:

::

   >>> note.written_duration
   Duration(1, 4)


Set the written duration of notes like this:

::

   >>> note.written_duration = Duration(3, 16)
   >>> show(note)

.. image:: images/index-6.png

