# -*- coding: utf-8 -*-
from abjad import *


#named_pitches = []
#diatonic_pitch_names = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
#accidental_names = ['ff', 'tqf', 'f', 'qf', '', 'qs', 's', 'tqs', 'ss']
#octave_ticks = ['', "'"]
#iterator = sequencetools.yield_outer_product_of_sequences(
#    [
#        diatonic_pitch_names,
#        accidental_names,
#        octave_ticks,
#        ],
#    )
#for diatonic_pitch_name, accidental_name, octave_tick in iterator:
#    joined = '{}{}{}'.format(diatonic_pitch_name, accidental_name, octave_tick)
#    named_pitch = pitchtools.NamedPitch(joined)
#    named_pitches.append(named_pitch)
#named_pitch_pairs = tuple(
#    sequencetools.yield_all_unordered_pairs_of_sequence(named_pitches)
#    )


def test_pitchtools_NamedInterval_from_pitch_carriers_01():

    pitch = NamedPitch(12)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        pitch,
        NamedPitch(12),
        )
    assert interval == pitchtools.NamedInterval('perfect', 1)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        pitch,
        NamedPitch('b', 4),
        )
    assert interval == pitchtools.NamedInterval('minor', -2)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        pitch,
        NamedPitch('bf', 4),
        )
    assert interval == pitchtools.NamedInterval('major', -2)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        NamedPitch(12),
        NamedPitch('as', 4),
        )
    assert interval == pitchtools.NamedInterval('diminished', -3)


def test_pitchtools_NamedInterval_from_pitch_carriers_02():

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        NamedPitch(12),
        NamedPitch('a', 4),
        )
    assert interval == pitchtools.NamedInterval('minor', -3)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        NamedPitch(12),
        NamedPitch('af', 4),
        )
    assert interval == pitchtools.NamedInterval('major', -3)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        NamedPitch(12),
        NamedPitch('gs', 4),
        )
    assert interval == pitchtools.NamedInterval('diminished', -4)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        NamedPitch(12),
        NamedPitch('g', 4),
        )
    assert interval == pitchtools.NamedInterval('perfect', -4)


#@pytest.mark.parametrize('pair', named_pitch_pairs)
#def test_pitchtools_NamedInterval_from_pitch_carriers_03(pair):
#    named_pitch_one, named_pitch_two = pair
#    staff_position_one = named_pitch_one.to_staff_position()
#    staff_position_two = named_pitch_two.to_staff_position()
#    staff_spaces = staff_position_two.number - staff_position_one.number
#    named_interval = pitchtools.NamedInterval.from_pitch_carriers(
#        named_pitch_one,
#        named_pitch_two,
#        )
#    assert named_interval.staff_spaces == staff_spaces
#    semitones = named_interval.semitones
#    assert float(named_pitch_two) - float(named_pitch_one) == semitones
