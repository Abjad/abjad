Rests
=====


Making rests from strings
-------------------------

You can make rests from a LilyPond input string:

..  abjad::

    rest = abjad.Rest('r8')
    abjad.show(rest)


Making rests from durations
---------------------------

You can make rests from durations:

..  abjad::

    rest = abjad.Rest(abjad.Duration(1, 4))
    abjad.show(rest)


Making rests from other Abjad leaves
------------------------------------

You can also make rests from other Abjad leaves:

..  abjad::

    note = abjad.Note("d'4..")
    rest = abjad.Rest(note)
    abjad.show(rest)


Understanding the interpreter representation of a rest
------------------------------------------------------

..  abjad::

    rest

``Rest`` tells you the rest's class.

``4..`` tells you that the rest's duration is equal to that of a doubly dotted
quarter note.


Making multimeasure rests
-------------------------

Create multimeasure rests like this:

..  abjad::

    multimeasure_rest = abjad.MultimeasureRest('R1')
    abjad.show(multimeasure_rest)

Multiply the duration of multimeasure rests like this:

..  abjad::

    abjad.attach(abjad.Multiplier(4), multimeasure_rest)
    staff = abjad.Staff([multimeasure_rest])
    abjad.show(staff)

Use a LilyPond literal to compress full-bar rests:

..  abjad::

    command = abjad.LilyPondLiteral(r'\compressFullBarRests')
    abjad.attach(command, staff)
    show(staff)


Getting and setting the written duration of rests
-------------------------------------------------

Get the written duration of rests like this:

..  abjad::

    rest.written_duration

Set the written duration of rests like this:

..  abjad::

    rest.written_duration = abjad.Duration(3, 16)
    abjad.show(rest)
