Notes
=====


Making notes from a LilyPond input string
-----------------------------------------

You can make notes from a LilyPond input string:

::

    >>> note = abjad.Note("c'4")
    >>> abjad.show(note)


Making notes from numbers
-------------------------

You can also make notes from numbers:

::

    >>> note = abjad.Note(0, abjad.Duration(1, 4))
    >>> abjad.show(note)


Understanding the interpreter representation of a note
------------------------------------------------------

::

    >>> note

``Note`` tells you the note's class.

``c'`` tells you that the note's pitch is equal to middle C.

``4`` tells you that the note's duration is equal to a quarter note.


Getting and setting the written pitch of notes
----------------------------------------------

Get the written pitch of notes like this:

::

    >>> note.written_pitch

Set the written pitch of notes like this:

::

    >>> note.written_pitch = abjad.NamedPitch("cs'")
    >>> abjad.show(note)

Or this:

::

    >>> note.written_pitch = "d'"
    >>> abjad.show(note)

Or this:

::

    >>> note.written_pitch = 3
    >>> abjad.show(note)


Getting and setting the written duration of notes
-------------------------------------------------

Get the written duration of notes like this:

::

    >>> note.written_duration

Set the written duration of notes like this:

::

    >>> note.written_duration = abjad.Duration(3, 16)
    >>> abjad.show(note)
