Containers
==========


Creating containers
-------------------

Create a container with components:

::

    >>> notes = [abjad.Note("ds'16"), abjad.Note("cs'16"), abjad.Note("e'16"), abjad.Note("c'16")]
    >>> container = abjad.Container(notes)
    >>> abjad.show(container)

Or with a LilyPond input string:

.. Xenakis: Jalons (1986): Contrabass: m58

::

    >>> container = abjad.Container("ds'16 cs'16 e'16 c'16 d'2 ~ d'8")
    >>> abjad.show(container)


Selecting music
---------------

Slice a container to select its components:

::

    >>> container[:]


Inspecting length
-----------------

Get the length of a container with Python's built-in ``len()`` function:

::

    >>> len(container)


Inspecting duration
-------------------

Get the duration of a container:

::

    >>> abjad.get.duration(container)


Adding one component to the end of a container
----------------------------------------------

Add one component to the end of a container with ``append()``:

::

    >>> container.append(abjad.Note("af'32"))
    >>> abjad.show(container)


Adding many components to the end of a container
------------------------------------------------

Add many components to the end of a container with ``extend()``:

::

    >>> container.extend([abjad.Note("c''32"), abjad.Note("a'32")])
    >>> abjad.show(container)


Finding the index of a component
--------------------------------

Find the index of a component with ``index()``:

::

    >>> note = container[7]

::

    >>> container.index(note)


Inserting a component by index
------------------------------

Insert a component by index with ``insert()``:

::

    >>> container.insert(-3, abjad.Note("g'32"))
    >>> abjad.show(container)


Removing a component by index
-----------------------------

Remove a component by index with ``pop()``:

::

    >>> container.pop(-1)
    >>> abjad.show(container)


Removing a component by reference
---------------------------------

Remove a component by reference with ``remove()``:

::

    >>> container.remove(container[-1])
    >>> abjad.show(container)

..  ``__getslice__``, ``__setslice__`` and ``__delslice__`` 
    remain to be documented.


Naming containers
-----------------

You can name Abjad containers:

::

    >>> flute_staff = abjad.Staff("c'8 d'8 e'8 f'8", name='Flute')
    >>> violin_staff = abjad.Staff("c'8 d'8 e'8 f'8", name='Violin')
    >>> staff_group = abjad.StaffGroup([flute_staff, violin_staff])
    >>> score = abjad.Score([staff_group])

Container names appear in LilyPond input:

::

    >>> abjad.f(score)

And make it easy to retrieve containers later:

::

    >>> score['Flute']

But container names do not appear in notational output:

::

    >>> abjad.show(score)


Understanding ``{ }`` and ``<< >>`` in LilyPond
-----------------------------------------------

LilyPond uses curly ``{ }`` braces to wrap a stream of musical events
that are to be engraved one after the other::

    \new Voice {
        e''4
        f''4
        g''4
        g''4
        f''4
        e''4
        d''4
        d''4 \fermata
    }

..  book::
    :hide:

    >>> staff = abjad.Staff(r"e''4 f''4 g''4 g''4 f''4 e''4 d''4 d''4 \fermata")
    >>> abjad.show(staff)

LilyPond uses skeleton ``<< >>`` braces to wrap two or more musical
expressions that are to be played at the same time::

    \new Staff <<
        \new Voice {
            \voiceOne
            e''4
            f''4
            g''4
            g''4
            f''4
            e''4
            d''4
            d''4 \fermata
        }
        \new Voice {
            \voiceTwo
            c''4
            c''4
            b'4
            c''4
            c''8
            b'8
            c''4
            b'4
            b'4 \fermata
        }
    >>

::
    :hide:

    >>> voice_1 = abjad.Voice(r"e''4 f''4 g''4 g''4 f''4 e''4 d''4 d''4 \fermata")
    >>> voice_2 = abjad.Voice(r"c''4 c''4 b'4 c''4 c''8 b'8 c''4 b'4 b'4 \fermata")
    >>> staff = abjad.Staff([voice_1, voice_2])
    >>> staff.simultaneous = True
    >>> literal = abjad.LilyPondLiteral(r'\voiceOne')
    >>> abjad.attach(literal, voice_1)
    >>> literal = abjad.LilyPondLiteral(r'\voiceTwo')
    >>> abjad.attach(literal, voice_2)
    >>> abjad.show(staff)

The examples above are both LilyPond input.

The most common use of LilyPond ``{ }`` is to group a 
potentially long stream of notes and rests into a single expression.

The most common use of LilyPond ``<< >>`` is to group a relatively smaller
number of note lists together polyphonically.


Understanding sequential and simultaneous containers
----------------------------------------------------

Abjad implements LilyPond ``{ }`` and ``<< >>`` in the container 
``simultaneous`` attribute.

Some containers set ``simultaneous`` to false at initialization:

::

    >>> staff = abjad.Staff()
    >>> staff.simultaneous

Other containers set ``simultaneous`` to true:

::

    >>> score = abjad.Score()
    >>> score.simultaneous


Changing sequential and simultaneous containers
-----------------------------------------------

Set ``simultaneous`` by hand as necessary:

::

    >>> voice_1 = abjad.Voice(r"e''4 f''4 g''4 g''4 f''4 e''4 d''4 d''4 \fermata")
    >>> voice_2 = abjad.Voice(r"c''4 c''4 b'4 c''4 c''8 b'8 c''4 b'4 b'4 \fermata")
    >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
    >>> literal = abjad.LilyPondLiteral(r'\voiceOne')
    >>> abjad.attach(literal, voice_1)
    >>> literal = abjad.LilyPondLiteral(r'\voiceTwo')
    >>> abjad.attach(literal, voice_2)
    >>> abjad.show(staff)

The staff in the example above is set to simultaneous after initialization 
to create a type of polyphonic staff.
