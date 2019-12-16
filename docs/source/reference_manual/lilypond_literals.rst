LilyPond literals
=================

LilyPond literals allow you to attach arbitrary LilyPond literals
to Abjad score components.


Creating LilyPond literals
--------------------------

Use ``LilyPondLiteral`` to create a LilyPond literal:

::

    >>> literal = abjad.LilyPondLiteral(r'\bar "||"', 'after')


Understanding the interpreter representation of LilyPond literals
-----------------------------------------------------------------

::

    >>> literal

``LilyPondLiteral`` tells you the literal's class.

``r'\bar "||"'`` tells you the LilyPond literal to be formatted.

``'after'`` tells you where the literal will be formatted relative to the leaf
to which it is attached.


Attaching LilyPond literals to Abjad components
-----------------------------------------------

Use ``attach()`` to attach a LilyPond literal to any Abjad leaf:

::

    >>> staff = abjad.Staff()
    >>> staff.extend("{ d''16 ( c''16 fs''16 g''16 ) }")
    >>> staff.extend("{ f''16 ( e''16 d''16 c''16 ) }")
    >>> staff.extend("{ cs''16 ( d''16 f''16 d''16 ) }")
    >>> staff.extend("{ a'8 b'8 }")
    >>> staff.extend("{ d''16 ( c''16 fs''16 g''16 )} ")
    >>> staff.extend("{ f''16 ( e''16 d''16 c''16 ) }")
    >>> staff.extend("{ cs''16 ( d''16 f''16 d''16 ) }")
    >>> staff.extend("{ a'8 b'8 c''2 }")
    >>> key_signature = abjad.KeySignature('f', 'major')
    >>> leaf = abjad.inspect(staff).leaf(0)
    >>> abjad.attach(key_signature, leaf)

::

    >>> abjad.attach(literal, staff[-2])

::

    >>> abjad.show(staff)


Inspecting the LilyPond literals attached to a leaf
---------------------------------------------------

Use ``abjad.inspect()`` to get the LilyPond literals attached to a leaf:

::

    >>> abjad.inspect(staff[-2]).indicators(abjad.LilyPondLiteral)


Detaching LilyPond literals
---------------------------

Use ``abjad.detach()`` to detach LilyPond literals:

::

    >>> abjad.detach(literal, staff[-2])

::

    >>> abjad.show(staff)


Getting the argument of a LilyPond literal
------------------------------------------

Use ``argument`` to get the argument of a LilyPond literal:

::

    >>> literal.argument


Comparing LilyPond literals
---------------------------

LilyPond literals compare equal with equal names. Otherwise LilyPond literals
do not compare equal:

::

    >>> literal_1 = abjad.LilyPondLiteral(r'\bar "||"', 'after')
    >>> literal_2 = abjad.LilyPondLiteral(r'\bar "||"', 'before')
    >>> literal_3 = abjad.LilyPondLiteral(r'\slurUp')

::

    >>> literal_1 == literal_1
    >>> literal_1 == literal_2
    >>> literal_1 == literal_3

::

    >>> literal_2 == literal_1
    >>> literal_2 == literal_2
    >>> literal_2 == literal_3

::

    >>> literal_3 == literal_1
    >>> literal_3 == literal_2
    >>> literal_3 == literal_3
