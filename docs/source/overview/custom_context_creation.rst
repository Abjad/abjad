Custom context creation
=======================

What if you define a custom LilyPond context in an external stylesheet? Just set the
LilyPond type of an Abjad context the same way. The name of the custom context will
appear in the LilyPond output you create with Abjad. Make sure to include the name of
your external stylesheet and LilyPond will style your output accordingly:

::

    >>> voice = abjad.Voice(name="Flute_Voice", lilypond_type="Custom_Flute_Voice")
    >>> voice.extend("c'8 d' e' f' g' a' b' c''")
    >>> string = abjad.lilypond(voice)
    >>> print(string)
