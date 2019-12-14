Rests
=====


Making rests from strings
-------------------------

You can make rests from a LilyPond input string:

::

    >>> rest = abjad.Rest('r8')
    >>> abjad.show(rest)


Making rests from durations
---------------------------

You can make rests from durations:

::

    >>> rest = abjad.Rest(abjad.Duration(1, 4))
    >>> abjad.show(rest)


Making rests from other Abjad leaves
------------------------------------

You can also make rests from other Abjad leaves:

::

    >>> note = abjad.Note("d'4..")
    >>> rest = abjad.Rest(note)
    >>> abjad.show(rest)


Understanding the interpreter representation of a rest
------------------------------------------------------

::

    >>> rest

``Rest`` tells you the rest's class.

``4..`` tells you that the rest's duration is equal to that of a doubly dotted
quarter note.


Making multimeasure rests
-------------------------

Create multimeasure rests like this:

::

    >>> multimeasure_rest = abjad.MultimeasureRest('R1')
    >>> abjad.show(multimeasure_rest)

Multiply the duration of multimeasure rests like this:

::

    >>> multimeasure_rest = abjad.MultimeasureRest('R1', multiplier=4)
    >>> staff = abjad.Staff([multimeasure_rest])
    >>> abjad.show(staff)

Use a LilyPond literal to compress full-bar rests:

::

    >>> command = abjad.LilyPondLiteral(r'\compressFullBarRests')
    >>> abjad.attach(command, staff)
    >>> show(staff)


Getting and setting the written duration of rests
-------------------------------------------------

Get the written duration of rests like this:

::

    >>> rest.written_duration

Set the written duration of rests like this:

::

    >>> rest.written_duration = abjad.Duration(3, 16)
    >>> abjad.show(rest)
