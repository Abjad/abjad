Notes
=====


Making notes from a LilyPond input string
-----------------------------------------

You can make notes from a LilyPond input string:

<abjad>
note = Note("c'4")
show(note)
</abjad>


Making notes from numbers
-------------------------

You can also make notes from numbers:

<abjad>
note = Note(0, Duration(1, 4))
show(note)
</abjad>


Understanding the interpreter representation of a note
------------------------------------------------------

<abjad>
note
</abjad>

``Note`` tells you the note's class.

``c'`` tells you that the note's pitch is equal to middle C.

``4`` tells you that the note's duration is equal to a quarter note.


Getting and setting the written pitch of notes
----------------------------------------------

Get the written pitch of notes like this:

<abjad>
note.written_pitch
</abjad>

Set the written pitch of notes like this:

<abjad>
note.written_pitch = NamedPitch("cs'")
show(note)
</abjad>

Or this:

<abjad>
note.written_pitch = "d'"
show(note)
</abjad>

Or this:

<abjad>
note.written_pitch = 3
show(note)
</abjad>


Getting and setting the written duration of notes
-------------------------------------------------

Get the written duration of notes like this:

<abjad>
note.written_duration
</abjad>

Set the written duration of notes like this:

<abjad>
note.written_duration = Duration(3, 16)
show(note)
</abjad>
