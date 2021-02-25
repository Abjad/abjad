Containers, retrieving by name
==============================

..

----

Assembling a score means nesting containers:

::

    >>> string = "d'8 f' a' d'' f'' gs'4 r8 e' gs' b' e'' gs'' a'4"
    >>> voice = abjad.Voice(string, name="RH_Voice")
    >>> staff = abjad.Staff([voice], name="RH_Staff")
    >>> score = abjad.Score([staff], name="Score")
    >>> abjad.show(score)

Use integer indices to retrieve nested containers:

::

    >>> score[0]

    >>> score[0][0]

Or use container names:

::

    >>> score["RH_Staff"]

    >>> score["RH_Voice"]
