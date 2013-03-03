from abjad.tools import componenttools
from abjad.tools import pitchtools


def add_artificial_harmonic_to_note(note, melodic_diatonic_interval=None):
    r'''Add artifical harmonic to `note` at `melodic_diatonic_interval`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(staff[:])
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }


    ::

        >>> notetools.add_artificial_harmonic_to_note(staff[0])
        Chord("<c' f'>8")

    ::

        >>> f(staff)
        \new Staff {
            <
                c'
                \tweak #'style #'harmonic
                f'
            >8 [
            d'8
            e'8
            f'8 ]
        }


    When ``melodic_diatonic_interval=None`` set to a perfect fourth.

    Create new artificial harmonic chord from `note`.

    Move parentage and spanners from `note` to artificial harmonic chord.

    Return artificial harmonic chord.
    '''
    from abjad.tools import chordtools

    if melodic_diatonic_interval is None:
        melodic_diatonic_interval = pitchtools.MelodicDiatonicInterval('perfect', 4)

    chord = chordtools.Chord(note)
    chord.append(chord[0].written_pitch.numbered_chromatic_pitch._chromatic_pitch_number)
    chord[1].written_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(
        chord[1].written_pitch, melodic_diatonic_interval)
    chord[1].tweak.style = 'harmonic'
    componenttools.move_parentage_and_spanners_from_components_to_components([note], [chord])
    return chord
