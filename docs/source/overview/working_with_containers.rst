Working with containers
=======================

Creating containers
-------------------

Create a container with a LilyPond input string:

.. Xenakis: Jalons (1986): Contrabass: m58

::

    >>> container = abjad.Container("ds'16 cs'16 e'16 c'16 d'2 ~ d'8")
    >>> abjad.show(container)

Selecting music
---------------

Slice a container to select its components:

::

    >>> container[:]

Getting length
--------------

Get the length of a container with Python's built-in ``len()`` function:

::

    >>> len(container)

Getting duration
----------------

Get the duration of a container:

::

    >>> abjad.get.duration(container)

Appending one component to the end of a container
-------------------------------------------------

Append one component to the end of a container like this:

::

    >>> container.append(abjad.Note("af'32"))
    >>> abjad.show(container)

Extending a container with many components
------------------------------------------

Extend a container like this:

::

    >>> container.extend([abjad.Note("c''32"), abjad.Note("a'32")])
    >>> abjad.show(container)

Finding the index of a component inside a container
---------------------------------------------------

Index the components in an Abjad container just like you index items in Python's built-in
lists:

::

    >>> note = container[7]
    >>> abjad.show(note)

::

    >>> container.index(note)

Inserting a component by index
------------------------------

Insert a component into a container at an index like this:

::

    >>> note = abjad.Note("g'32")
    >>> container.insert(-3, note)
    >>> abjad.show(container)

Popping a component at a container index
----------------------------------------

Pop a component at any index like this:

::

    >>> container.pop(-1)
    >>> abjad.show(container)

Removing components from a container
------------------------------------

First get a reference to a component. Then remove the component from its container like
this:

::

    >>> note = container[-1]
    >>> container.remove(note)
    >>> abjad.show(container)

..  ``__getslice__``, ``__setslice__`` and ``__delslice__`` 
    remain to be documented.

Naming containers
-----------------

You can name Abjad containers:

::

    >>> flute_staff = abjad.Staff("c'8 d'8 e'8 f'8", name="Flute_Staff")
    >>> violin_staff = abjad.Staff("c'8 d'8 e'8 f'8", name="Violin_Staff")
    >>> staff_group = abjad.StaffGroup([flute_staff, violin_staff])
    >>> score = abjad.Score([staff_group])

Container names appear in LilyPond input:

::

    >>> string = abjad.lilypond(score)
    >>> print(string)

Containers can be retrieved by name like this:

::

    >>> score["Flute_Staff"]

Note that container names do not appear in notational output:

::

    >>> abjad.show(score)

Understanding ``{ }`` and ``<< >>`` in LilyPond
-----------------------------------------------

LilyPond uses curly ``{ }`` braces to wrap a stream of musical events that are to be
engraved one after the other::

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

LilyPond uses skeleton ``<< >>`` braces to wrap two or more musical expressions that are
to be played at the same time::

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

The most common use of LilyPond ``{ }`` is to group a potentially long stream of notes
and rests into a single expression.

The most common use of LilyPond ``<< >>`` is to group a relatively smaller number of note
lists together polyphonically.

Understanding the time interpretation defaults of Abjad containers
------------------------------------------------------------------

Abjad containers are set to either sequential or simultaneous when you initialize them.
Defaults correspond to the most common use of each type of container. Abjad's vanilla
containers, voices and staves all default to sequential time structure:

::

    >>> abjad.Container(name="Example_Container").simultaneous

    >>> abjad.Voice(name="Example_Voice").simultaneous

    >>> abjad.Staff(name="Example_Staff").simultaneous

Abjad's staff groups and scores default to simultaneous time structure:

::

    >>> abjad.StaffGroup(name="Example_Staff_Group").simultaneous

    >>> abjad.Score(name="Example_Score").simultaneous

Changing the time interpretation of containers
----------------------------------------------

You can set the time structure of any container at initialization. If you know how you
will use a container, go ahead and set the container's time structure when you create it.
The staff below initializes as simultaneous to allow two-voice polyphony:

::

    >>> voice_1 = abjad.Voice(r"e''4 f''4 g''4 g''4 f''4 e''4 d''4 d''4 \fermata")
    >>> voice_2 = abjad.Voice(r"c''4 c''4 b'4 c''4 c''8 b'8 c''4 b'4 b'4 \fermata")
    >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
    >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
    >>> abjad.attach(literal, voice_1)
    >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
    >>> abjad.attach(literal, voice_2)
    >>> abjad.show(staff)

You can also set the time structure of containers after you create them. The staff below
initializes as sequential:

::

    >>> voice_1 = abjad.Voice(r"e''4 f''4 g''4 g''4 f''4 e''4 d''4 d''4 \fermata")
    >>> voice_2 = abjad.Voice(r"c''4 c''4 b'4 c''4 c''8 b'8 c''4 b'4 b'4 \fermata")
    >>> staff = abjad.Staff([voice_1, voice_2])
    >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
    >>> abjad.attach(literal, voice_1)
    >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
    >>> abjad.attach(literal, voice_2)
    >>> abjad.show(staff)

Then change the staff's time structure like this:

::

    >>> staff.simultaneous = True
    >>> abjad.show(staff)

Voices
------


Changing the context of a voice
-------------------------------

The context of a voice is set to ``'Voice'`` by default:

::

    >>> voice = abjad.Voice("c'8 d'8 e'8 f'8 g'8 a'8 b'4 c''1")
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

Making simultaneous voices in a staff
-------------------------------------

You can make a staff treat its contents as simultaneous with ``simultaneous``:

::

    >>> soprano_voice = abjad.Voice(r"b'4 a'8 g'8 a'4 d''4 b'4 g'4 a'2 \fermata")
    >>> alto_voice = abjad.Voice(r"d'4 d'4 d'4 fs'4 d'4 d'8 e'8 fs'2") 
    >>> abjad.override(soprano_voice).stem.direction = abjad.Up
    >>> abjad.override(alto_voice).stem.direction = abjad.Down
    >>> staff = abjad.Staff([soprano_voice, alto_voice])
    >>> staff.simultaneous = True
    >>> abjad.show(staff)

Checking containment
--------------------

Use ``in`` to find out whether a score contains a given component:
