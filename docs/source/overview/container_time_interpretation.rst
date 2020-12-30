Time interpretation of containers
=================================

..

----

Time interpretation defaults
----------------------------

The time interpretation of Abjad containers initializes to either sequential or
simultaneous. Defaults correspond to the most common use of each type of container.
Abjad's vanilla containers, voices and staves all default to sequential time
interpretation:

::

    >>> abjad.Container(name="Example_Container").simultaneous is None

    >>> abjad.Voice(name="Example_Voice").simultaneous is None

    >>> abjad.Staff(name="Example_Staff").simultaneous is None

Abjad's staff groups and scores default to simultaneous time interpretation:

::

    >>> abjad.StaffGroup(name="Example_Staff_Group").simultaneous

    >>> abjad.Score(name="Example_Score").simultaneous

----

Setting time interpretation at initialization
---------------------------------------------

You can set the time interpretation of any container at initialization. If you know how
you will use a container, go ahead and set the container's time interpretation when you
create it. The staff below initializes as simultaneous to allow two-voice polyphony:

::

    >>> voice_1 = abjad.Voice(r"e''4 f''4 g''4 g''4 f''4 e''4 d''4 d''4 \fermata")
    >>> voice_2 = abjad.Voice(r"c''4 c''4 b'4 c''4 c''8 b'8 c''4 b'4 b'4 \fermata")
    >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
    >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
    >>> abjad.attach(literal, voice_1)
    >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
    >>> abjad.attach(literal, voice_2)
    >>> abjad.show(staff)

----

Changing time interpretation after initialization
-------------------------------------------------

You can also set the time interpretation of containers after you create them. The staff
below initializes as sequential. But you can change the staff's time interpretation after
you initialization:

::

    >>> voice_1 = abjad.Voice(r"e''4 f''4 g''4 g''4 f''4 e''4 d''4 d''4 \fermata")
    >>> voice_2 = abjad.Voice(r"c''4 c''4 b'4 c''4 c''8 b'8 c''4 b'4 b'4 \fermata")
    >>> staff = abjad.Staff([voice_1, voice_2])
    >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
    >>> abjad.attach(literal, voice_1)
    >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
    >>> abjad.attach(literal, voice_2)
    >>> abjad.show(staff)

    >>> staff.simultaneous = True
    >>> abjad.show(staff)
