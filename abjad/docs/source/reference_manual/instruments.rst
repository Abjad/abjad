Instruments
===========

..  abjad::

    import abjad


Creating instruments
--------------------

Initialize instruments like this:

..  abjad::

    violin = abjad.Violin()


Understanding the interpreter representation of an instrument
-------------------------------------------------------------

The interpreter representation of an instrument tells you the instrument's
class:

..  abjad::

    violin


Attaching instruments to a component
------------------------------------

Use ``abjad.attach()`` to attach an instrument to a leaf:

..  abjad::

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    abjad.attach(violin, staff[0])
    abjad.show(staff)


Inspecting the instrument attached to a component
-------------------------------------------------

Use ``abjad.inspect()`` to get the instrument attached to a leaf:

..  abjad::

    abjad.inspect(staff[0]).get_indicator(abjad.Instrument)


Inspecting a component's effective instrument
---------------------------------------------

Use ``abjad.inspect()`` to get the instrument currently in effect for a
component:

..  abjad::

    for note in staff:
        abjad.inspect(note).get_effective(abjad.Instrument)


Detaching instruments from a component
--------------------------------------

Use ``abjad.detach()`` to detach an instrument from a component:

..  abjad::

    abjad.detach(violin, staff[0])
    abjad.show(staff)


Getting the name of an instrument
---------------------------------

Use ``name`` to get the name of any instrument:

..  abjad::

    violin.name

Use ``name_markup`` to get the instrument name markup of any instrument:

..  abjad::

    violin.name_markup

..  abjad::

    abjad.show(violin.name_markup)


Getting the short name of an instrument
---------------------------------------

Use ``short_name`` to get the short name of any instrument:

..  abjad::

    violin.short_name

Use ``short_name_markup`` to get the short instrument name markup of any
instrument:

..  abjad::

    violin.short_name_markup

..  abjad::

    abjad.show(violin.short_name_markup)


Getting an instrument's range
-----------------------------

Use ``pitch_range`` to get the range of any instrument:

..  abjad::

    violin.pitch_range

..  abjad::

    abjad.show(violin.pitch_range)


Getting an instrument's level of transposition
----------------------------------------------

Use ``middle_c_sounding_pitch`` to get an instrument's level of
transposition:

..  abjad::

    violin.middle_c_sounding_pitch

..  abjad::

    abjad.show(violin.middle_c_sounding_pitch)


Getting an instrument's allowable clefs
---------------------------------------

Use ``allowable_clefs`` to get clefs on which an instrument is conventionally
notated:

..  abjad::

    violin.allowable_clefs


Customizing instrument properties
---------------------------------

You can change the properties of any instrument at initialization:

..  abjad::

    viola = abjad.Viola(
        name='Bratsche',
        short_name='Br.',
        allowable_clefs=['alto', 'treble'],
        pitch_range='[C3, C6]',
        )

..  abjad::

    staff = abjad.Staff("c'4 d'4 e'4 fs'4")
    abjad.attach(viola, staff[0])
    clef = abjad.Clef('alto')
    abjad.attach(clef, staff[0])
    abjad.show(staff)
