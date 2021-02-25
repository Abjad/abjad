:orphan:

Understanding reprs
===================

Python's interpreter will show you a summary of the objects you create. The second and
third examples below work because you can index Abjad voices the same way you index
Python lists:

::

    >>> string = "d'8 f' a' d'' f'' gs'4 r8 e' gs' b' e'' gs'' a'4"
    >>> voice = abjad.Voice(string)
    >>> staff = abjad.Staff([voice])
    >>> abjad.show(staff)

::

    >>> voice

    >>> voice[5]

    >>> voice[6]
