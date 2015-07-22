Instruments
===========


Creating instruments
--------------------

Use ``instrumenttools`` to create an instrument:

<abjad>
violin = instrumenttools.Violin()
</abjad>


Understanding the interpreter representation of an instrument
-------------------------------------------------------------

The interpreter representation of an instrument tells you the instrument's
class:

<abjad>
violin
</abjad>


Attaching instruments to a component
------------------------------------

Use ``attach()`` to attach an instrument to a component:

<abjad>
staff = Staff("c'4 d'4 e'4 f'4")
attach(violin, staff)
show(staff)
</abjad>


Inspecting the instrument attached to a component
-------------------------------------------------

Use the inspector to get the instrument attached to a component:

<abjad>
inspect_(staff).get_indicator(instrumenttools.Instrument)
</abjad>


Inspecting a component's effective instrument
---------------------------------------------

Use the inspector to get the instrument currently in effect for a component:

<abjad>
for note in staff:
    inspect_(note).get_effective(instrumenttools.Instrument)
</abjad>


Detaching instruments from a component
--------------------------------------

Use ``detach()`` to detach an instrument from a component:

<abjad>
detach(violin, staff)
show(staff)
</abjad>


Getting the name of an instrument
---------------------------------

Use ``instrument_name`` to get the name of any instrument:

<abjad>
violin.instrument_name
</abjad>

Use ``instrument_name_markup`` to get the instrument name markup of
any instrument:

<abjad>
violin.instrument_name_markup
</abjad>

<abjad>
show(violin.instrument_name_markup)
</abjad>


Getting the short name of an instrument
---------------------------------------

Use ``short_instrument_name`` to get the short name of any instrument:

<abjad>
violin.short_instrument_name
</abjad>

Use ``short_instrument_name_markup`` to get the short instrument name
markup of any instrument:

<abjad>
violin.short_instrument_name_markup
</abjad>

<abjad>
show(violin.short_instrument_name_markup)
</abjad>


Getting an instrument's range
-----------------------------

Use ``pitch_range`` to get the range of any instrument:

<abjad>
violin.pitch_range
</abjad>

<abjad>
show(violin.pitch_range)
</abjad>


Getting an instrument's level of transposition
----------------------------------------------

Use ``sounding_pitch_of_written_middle_c`` to get an instrument's level of
transposition:

<abjad>
violin.sounding_pitch_of_written_middle_c
</abjad>

<abjad>
show(violin.sounding_pitch_of_written_middle_c)
</abjad>


Getting an instrument's allowable clefs
---------------------------------------

Use ``allowable_clefs`` to get clefs on which an instrument is conventionally
notated:

<abjad>
violin.allowable_clefs
</abjad>

<abjad>
show(violin.allowable_clefs)
</abjad>


Customizing instrument properties
---------------------------------

You can change the properties of any instrument at initialization:

<abjad>
viola = instrumenttools.Viola(
    instrument_name='Bratsche',
    short_instrument_name='Br.',
    allowable_clefs=['alto', 'treble'],
    pitch_range='[C3, C6]',
    )
</abjad>

<abjad>
staff = Staff("c'4 d'4 e'4 fs'4")
attach(viola, staff)
clef = Clef('alto')
attach(clef, staff)
show(staff)
</abjad>
