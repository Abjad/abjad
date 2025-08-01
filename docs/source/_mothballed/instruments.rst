:orphan:

Instruments
===========

Creating instruments
--------------------

Initialize instruments like this:

::

    >>> violin = abjad.Violin()

Understanding the interpreter representation of an instrument
-------------------------------------------------------------

The interpreter representation of an instrument tells you the instrument's class:

::

    >>> violin

Attaching instruments to a component
------------------------------------

Use ``abjad.attach()`` to attach an instrument to a leaf:

::

    >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
    >>> abjad.attach(violin, staff[0])
    >>> abjad.show(staff)

Getting the instrument attached to a component
----------------------------------------------

Get the instrument attached to a leaf:

::

    >>> abjad.get.indicator(staff[0], abjad.Instrument)

Getting a component's effective instrument
------------------------------------------

Get the instrument currently in effect for a component:

::

    >>> for note in staff:
    ...     abjad.get.effective_indicator(note, abjad.Instrument)
    ...

Detaching instruments from a component
--------------------------------------

Use ``abjad.detach()`` to detach an instrument from a component:

::

    >>> abjad.detach(violin, staff[0])
    >>> abjad.show(staff)

Getting an instrument's range
-----------------------------

Use ``pitch_range`` to get the range of any instrument:

::

    >>> violin.pitch_range

::

    >>> lilypond_file = abjad.illustrate(violin.pitch_range)
    >>> abjad.show(lilypond_file)

Getting an instrument's level of transposition
----------------------------------------------

Use ``middle_c_sounding_pitch`` to get an instrument's level of transposition:

::

    >>> violin.middle_c_sounding_pitch

::

    >>> note = abjad.Note(violin.middle_c_sounding_pitch, 4)
    >>> abjad.show(note)

Getting an instrument's clefs
-----------------------------

Use ``clefs`` to get clefs on which an instrument is conventionally notated:

::

    >>> violin.clefs

Customizing instrument properties
---------------------------------

You can change the properties of any instrument at initialization:

::

    >>> viola = abjad.Viola(
    ...     clefs=("alto", "treble"),
    ...     pitch_range=abjad.PitchRange("[C3, C6]"),
    ... )

::

    >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
    >>> abjad.attach(viola, staff[0])
    >>> clef = abjad.Clef("alto")
    >>> abjad.attach(clef, staff[0])
    >>> abjad.show(staff)
