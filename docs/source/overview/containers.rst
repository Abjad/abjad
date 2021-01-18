Containers
==========

..  

----

Abjad models voices, staves, scores as types of container. Newcomers usually find it easy
to get started working with Abjad by typing LilyPond input into a container. This works
because Abjad understands the basics of LilyPond's input language:

::

    >>> string = "d'8 f' a' d'' f'' gs'4 r8 e' gs' b' e'' gs'' a'4"
    >>> voice = abjad.Voice(string, name="RH_Voice")
    >>> staff = abjad.Staff([voice], name="RH_Staff")
    >>> score = abjad.Score([staff], name="Score")
    >>> abjad.show(score)

Abjad displays pitch information in English. But LilyPond's other input languages are
available, too:

::

    >>> string = "re'8 fa' la' re'' fa'' sold'4 r8 mi' sold' si' mi'' sold'' la'4"
    >>> voice = abjad.Voice(string, language="français", name="RH_Voice")
    >>> staff = abjad.Staff([voice], name="RH_Staff")
    >>> score = abjad.Score([staff], name="Score")
    >>> abjad.show(score)
