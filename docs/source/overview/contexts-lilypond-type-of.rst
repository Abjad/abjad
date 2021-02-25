Contexts, LilyPond type of
==========================

Working with LilyPond means understanding LilyPond contexts. Abjad implements only four
concrete contexts: voice, staff, staff group, score. But LilyPond comes preloaded with 20
contexts: 9 voice contexts, 6 staff contexts, 4 staff group contexts and a score context:

http://lilypond.org/doc/v2.20/Documentation/notation/contexts-explained

Use Abjad's concept of "LilyPond type" to work with any of LilyPond's 20 predefined
contexts.

----

Setting LilyPond type at initialization
---------------------------------------

If you know the LilyPond type of a context you want to work with, you can set it at
initialization:

::

    >>> voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
    >>> staff = abjad.Staff([voice], lilypond_type="RhythmicStaff", name="Woodblock_Staff")
    >>> abjad.show(staff)

----

Setting LilyPond type after initialization
------------------------------------------

You can change the LilyPond type of a context after initialization, too:

::

    >>> voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
    >>> staff = abjad.Staff([voice], name="Woodblock_Staff")
    >>> abjad.show(staff)

    >>> staff.lilypond_type = "RhythmicStaff"
    >>> abjad.show(staff)
