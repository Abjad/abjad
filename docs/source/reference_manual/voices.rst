Voices
======


Making a voice from a LilyPond input string
-------------------------------------------

You can make a voice from a LilyPond input string:

::

    >>> voice = abjad.Voice("c'8 d'8 e'8 f'8 g'8 a'8 b'4 c''1")
    >>> abjad.show(voice)


Making a voice from a list of other components
----------------------------------------------

You can also make a voice from a list of other components:

::

    >>> tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), "c'4 d'4 e'4")
    >>> components = [tuplet, abjad.Note("f'2"), abjad.Note("g'1")]
    >>> voice = abjad.Voice(components)
    >>> abjad.show(voice)


Understanding the interpreter representation of a voice
-------------------------------------------------------

The interpreter representation of a voice contains three parts:

::

    >>> voice

``Voice`` tells you the voice's class.

``3`` tells you the voice's length (which is the number of
top-level components the voice contains).

Curly braces ``{`` and ``}`` tell you that the music inside the voice is
interpreted sequentially rather than simultaneously.


Formatting voices
-----------------

Use ``abjad.lilypond()`` to get the LilyPond format of a voice:

::

    >>> string = abjad.lilypond(voice)
    >>> print(string)


Selecting the components in a voice
-----------------------------------

Select the components in a voice like this:

::

    >>> voice[:]


Selecting a voice's leaves
--------------------------

Use ``abjad.select(...).leaves()`` to select the leaves in a voice:

::

    >>> abjad.select(voice).leaves()


Getting the length of a voice
-----------------------------

Use ``len()`` to get the length of a voice.

The length of a voice is defined equal to the number of top-level components
the voice contains:

::

    >>> len(voice)


Getting voice duration
-------------------------

Get the duration of a voice:

::

    >>> abjad.get.duration(voice)


Appending one component to the end of a voice
---------------------------------------------

Use ``append()`` to append one component to the end of a voice:

::

    >>> voice.append(abjad.Note("af'2"))
    >>> abjad.show(voice)

You can also use a LilyPond input string:

::

    >>> voice.append("bf'2")
    >>> abjad.show(voice)


Extending a voice with multiple components at once
--------------------------------------------------

Use ``extend()`` to extend a voice with multiple components at once:

::

    >>> notes = [abjad.Note("g'4"), abjad.Note("f'4")]
    >>> voice.extend(notes)
    >>> abjad.show(voice)

You can also use a LilyPond input string:

::

    >>> voice.extend("e'4 ef'4")
    >>> abjad.show(voice)


Finding the index of a component in a voice
-------------------------------------------

Use ``index()`` to find the index of any component in a voice:

::

    >>> notes[0]

::

    >>> voice.index(notes[0])


Popping a voice component by index
----------------------------------

Use ``pop()`` to pop the last component of a voice:

::

    >>> voice.pop()
    >>> abjad.show(voice)


Removing a voice component by reference
---------------------------------------

Use ``remove()`` to remove any component from a voice by reference:

::

    >>> voice.remove(voice[-1])
    >>> abjad.show(voice)


Naming voices
-------------

You can name Abjad voices:

::

    >>> voice.name = "Upper Voice"

Voice names appear in LilyPond input but not in notation output:

::

    >>> string = abjad.lilypond(voice)
    >>> print(string)

::

    >>> abjad.show(voice)


Changing the context of a voice
-------------------------------

The context of a voice is set to ``'Voice'`` by default:

::

    >>> voice.lilypond_type

But you can change the context of a voice if you want.

Change the context of a voice when you have defined a new LilyPond context
based on a LilyPond voice:

::

    >>> voice.lilypond_type = "SpeciallyDefinedVoice"

::

    >>> voice.lilypond_type

::

    >>> string = (voice)
    >>> print(string)
