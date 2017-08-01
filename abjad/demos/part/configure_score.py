# -*- coding: utf-8 -*-
import abjad


def configure_score(score):
    r'''Configures score.
    '''

    # configure bell staff
    bell_staff = score['Bell Staff']
    leaf = abjad.inspect(bell_staff).get_leaf(0)
    clef = abjad.Clef('treble')
    abjad.attach(clef, leaf)
    bells = abjad.instrumenttools.Instrument(
        instrument_name='Campana in La',
        short_instrument_name='Camp.',
        pitch_range='[C4, C6]',
        )
    abjad.attach(bells, leaf)
    mark = abjad.MetronomeMark((1, 4), (112, 120))
    abjad.attach(mark, leaf)
    time_signature = abjad.TimeSignature((6, 4))
    abjad.attach(time_signature, leaf)

    # configure first violin staff
    first_violin_staff = score['First Violin Staff']
    leaf = abjad.inspect(first_violin_staff).get_leaf(0)
    clef = abjad.Clef('treble')
    abjad.attach(clef, leaf)
    violin = abjad.instrumenttools.Violin(
        instrument_name_markup=abjad.Markup('Violin I'),
        short_instrument_name_markup=abjad.Markup('Vl. I'),
        )
    abjad.attach(violin, leaf)

    # configure second violin staff
    second_violin_staff = score['Second Violin Staff']
    leaf = abjad.inspect(second_violin_staff).get_leaf(0)
    clef = abjad.Clef('treble')
    abjad.attach(clef, leaf)
    violin = abjad.instrumenttools.Violin(
        instrument_name_markup=abjad.Markup('Violin II'),
        short_instrument_name_markup=abjad.Markup('Vl. II'),
        )
    abjad.attach(violin, leaf)

    # configure viola staff
    leaf = abjad.inspect(score['Viola Staff']).get_leaf(0)
    clef = abjad.Clef('alto')
    abjad.attach(clef, leaf)
    viola = abjad.instrumenttools.Viola()
    abjad.attach(viola, leaf)

    # configure cello staff
    leaf = abjad.inspect(score['Cello Staff']).get_leaf(0)
    clef = abjad.Clef('bass')
    abjad.attach(clef, leaf)
    cello = abjad.instrumenttools.Cello()
    abjad.attach(cello, leaf)

    # configure bass staff
    leaf = abjad.inspect(score['Bass Staff']).get_leaf(0)
    clef = abjad.Clef('bass')
    abjad.attach(clef, leaf)
    contrabass = abjad.instrumenttools.Contrabass(
        short_instrument_name_markup=abjad.Markup('Cb.'),
        )
    abjad.attach(contrabass, leaf)

    # configure score
    vector = abjad.SpacingVector(0, 0, 8, 0)
    abjad.override(score).vertical_axis_group.staff_staff_spacing = vector
    abjad.override(score).staff_grouper.staff_staff_spacing = vector
    abjad.override(score).staff_symbol.thickness = 0.5
    scheme = abjad.Scheme('format-mark-box-numbers')
    abjad.setting(score).mark_formatter = scheme
