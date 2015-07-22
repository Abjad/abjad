Rests
=====


Making rests from strings
-------------------------

You can make rests from a LilyPond input string:

<abjad>
rest = Rest('r8')
show(rest)
</abjad>


Making rests from durations
---------------------------

You can make rests from durations:

<abjad>
rest = Rest(Duration(1, 4))
show(rest)
</abjad>


Making rests from other Abjad leaves
------------------------------------

You can also make rests from other Abjad leaves:

<abjad>
note = Note("d'4..")
rest = Rest(note)
show(rest)
</abjad>


Understanding the interpreter representation of a rest
------------------------------------------------------

<abjad>
rest
</abjad>

``Rest`` tells you the rest's class.

``4..`` tells you that the rest's duration is equal to that of a doubly dotted
quarter note.


Making multimeasure rests
-------------------------

Create multimeasure rests like this:

<abjad>
multimeasure_rest = scoretools.MultimeasureRest('R1')
show(multimeasure_rest)
</abjad>

Multiply the duration of multimeasure rests like this:

<abjad>
attach(Multiplier(4), multimeasure_rest)
staff = Staff([multimeasure_rest])
show(staff)
</abjad>

Use a LilyPond command to compress full-bar rests:

<abjad>
command = indicatortools.LilyPondCommand('compressFullBarRests')
attach(command, staff)
show(staff)
</abjad>


Getting and setting the written duration of rests
-------------------------------------------------

Get the written duration of rests like this:

<abjad>
rest.written_duration
</abjad>

Set the written duration of rests like this:

<abjad>
rest.written_duration = Duration(3, 16)
show(rest)
</abjad>
