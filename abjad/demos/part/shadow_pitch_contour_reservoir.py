# -*- coding: utf-8 -*-
from abjad.tools import pitchtools


def shadow_pitch_contour_reservoir(pitch_contour_reservoir):
    r'''Shadows pitch contour reservoir.
    '''

    shadow_pitch_lookup = {
        pitchtools.NamedPitchClass('a'): -5, # add a P4 below
        pitchtools.NamedPitchClass('g'): -3, # add a m3 below
        pitchtools.NamedPitchClass('f'): -1, # add a m2 below
        pitchtools.NamedPitchClass('e'): -4, # add a M3 below
        pitchtools.NamedPitchClass('d'): -2, # add a M2 below
        pitchtools.NamedPitchClass('c'): -3, # add a m3 below
        pitchtools.NamedPitchClass('b'): -2, # add a M2 below
    }

    shadowed_reservoir = {}

    for instrument_name, pitch_contours in pitch_contour_reservoir.items():
        # The viola does not receive any diads
        if instrument_name == 'Viola':
            shadowed_reservoir['Viola'] = pitch_contours
            continue

        shadowed_pitch_contours = []

        for pitch_contour in pitch_contours[:-1]:
            shadowed_pitch_contour = []
            for pitch in pitch_contour:
                pitch_class = pitch.named_pitch_class
                shadow_pitch = pitch + shadow_pitch_lookup[pitch_class]
                diad = (shadow_pitch, pitch)
                shadowed_pitch_contour.append(diad)
            shadowed_pitch_contours.append(tuple(shadowed_pitch_contour))

        # treat the final contour differently: the last note does not become a diad
        final_shadowed_pitch_contour = []
        for pitch in pitch_contours[-1][:-1]:
            pitch_class = pitch.named_pitch_class
            shadow_pitch = pitch + shadow_pitch_lookup[pitch_class]
            diad = (shadow_pitch, pitch)
            final_shadowed_pitch_contour.append(diad)
        final_shadowed_pitch_contour.append(pitch_contours[-1][-1])
        shadowed_pitch_contours.append(tuple(final_shadowed_pitch_contour))

        shadowed_reservoir[instrument_name] = tuple(shadowed_pitch_contours)

    return shadowed_reservoir
