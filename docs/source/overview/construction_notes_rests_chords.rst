Construction: making notes, rests, chords
=========================================

Newcomers to Abjad usually find it easiest to get started making musical objects by
passing a string of LilyPond input to an Abjad container:

::

    >>> string = "d'8 f'8 a'8 d''8 f''8 gs'4 r8 e'8 gs'8 b'8 e''8 gs''8 a'4"
    >>> voice = abjad.Voice(string)
    >>> abjad.show(voice)

This works because Abjad knows how to parse a basic form of LilyPond's input language.
You can simplify durational input, for example, just like you would in a normal LilyPond
file:

::

    >>> string = "d'8 f' a' d'' f'' gs'4 r8 e' gs' b' e'' gs'' a'4"
    >>> voice = abjad.Voice(string)
    >>> abjad.show(voice)


More text:

::

    >>> voice.extend("d'8 f'8 a'8 d''8 f''8 gs'4 r8 e'8 gs'8 b'8 e''8 gs''8 a'4")
    >>> key_signature = abjad.KeySignature("g", "major")
    >>> abjad.attach(key_signature, voice[0])
    >>> time_signature = abjad.TimeSignature((2, 4), partial=(1, 8))
    >>> abjad.attach(time_signature, voice[0])
    >>> articulation = abjad.Articulation("turn")
    >>> abjad.attach(articulation, voice[5])

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
