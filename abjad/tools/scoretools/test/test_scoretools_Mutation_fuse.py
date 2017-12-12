import abjad
import pytest


def test_scoretools_Mutation_fuse_01():
    r'''Works with list of leaves.
    '''

    notes = 8 * abjad.Note("c'4")
    fused = abjad.mutate(notes).fuse()

    assert len(fused) == 1
    assert fused[0].written_duration == abjad.Duration(2)


def test_scoretools_Mutation_fuse_02():
    r'''Works with Leaf component.
    '''

    fused = abjad.mutate(abjad.Note("c'4")).fuse()
    assert len(fused) == 1
    assert fused[0].written_duration == abjad.Duration(1, 4)


def test_scoretools_Mutation_fuse_03():
    r'''Works with containers.
    '''

    voice = abjad.Voice(8 * abjad.Note("c'4"))
    fused = abjad.mutate(voice[:]).fuse()
    assert len(fused) == 1
    assert fused[0].written_duration == 2
    assert voice[0] is fused[0]


def test_scoretools_Mutation_fuse_04():
    r'''Fusion results in tied notes.
    '''

    voice = abjad.Voice([abjad.Note(0, (2, 16)), abjad.Note(9, (3, 16))])
    fused = abjad.mutate(voice[:]).fuse()

    assert len(fused) == 2
    assert fused[0].written_duration == abjad.Duration(1, 4)
    assert fused[1].written_duration == abjad.Duration(1, 16)

    tie_1 = abjad.inspect(fused[0]).get_spanner(abjad.Tie)
    tie_2 = abjad.inspect(fused[1]).get_spanner(abjad.Tie)

    assert tie_1 is tie_2
    assert voice[0] is fused[0]
    assert voice[1] is fused[1]
    assert voice[0].written_pitch == voice[1].written_pitch


def test_scoretools_Mutation_fuse_05():
    r'''Fuses leaves with differing LilyPond multipliers.
    '''

    staff = abjad.Staff([abjad.Skip((1, 1)), abjad.Skip((1, 1))])
    abjad.attach(abjad.Multiplier(1, 16), staff[0])
    abjad.attach(abjad.Multiplier(5, 16), staff[1])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            s1 * 1/16
            s1 * 5/16
        }
        '''
        )

    assert abjad.inspect(staff).get_duration() == abjad.Duration(3, 8)

    abjad.mutate(staff[:]).fuse()

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            s1 * 3/8
        }
        '''
        )

    assert abjad.inspect(staff).get_duration() == abjad.Duration(3, 8)
    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Mutation_fuse_06():
    r'''Fuses two unincorporated tuplets with same multiplier.
    '''

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    beam = abjad.Beam()
    abjad.attach(beam, tuplet_1[:])
    tuplet_2 = abjad.Tuplet((2, 3), "c'16 d'16 e'16")
    slur = abjad.Slur()
    abjad.attach(slur, tuplet_2[:])

    assert format(tuplet_1) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    assert format(tuplet_2) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'16 (
            d'16
            e'16 )
        }
        '''
        )

    tuplets = abjad.select([tuplet_1, tuplet_2])
    new = abjad.mutate(tuplets).fuse()

    assert format(new) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'8 [
            d'8
            e'8 ]
            c'16 (
            d'16
            e'16 )
        }
        '''
        )

    assert len(tuplet_1) == 0
    assert len(tuplet_2) == 0
    assert new is not tuplet_1 and new is not tuplet_2
    assert abjad.inspect(new).is_well_formed()


def test_scoretools_Mutation_fuse_07():
    r'''Fuses tuplets with same multiplier in score.
    '''

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    beam = abjad.Beam()
    abjad.attach(beam, tuplet_1[:])
    tuplet_2 = abjad.Tuplet((2, 3), "c'16 d'16 e'16")
    slur = abjad.Slur()
    abjad.attach(slur, tuplet_2[:])
    voice = abjad.Voice([tuplet_1, tuplet_2])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \times 2/3 {
                c'16 (
                d'16
                e'16 )
            }
        }
        '''
        )

    tuplets = voice[:]
    abjad.mutate(tuplets).fuse()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
                c'16 (
                d'16
                e'16 )
            }
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Mutation_fuse_08():
    r'''Fuses fixed-multiplier tuplets with same multiplier in score.
    '''

    tuplet_1 = abjad.Tuplet(abjad.Multiplier(2, 3), "c'8 d'8 e'8")
    beam = abjad.Beam()
    abjad.attach(beam, tuplet_1[:])
    tuplet_2 = abjad.Tuplet(abjad.Multiplier(2, 3), "c'8 d'8 e'8 f'8 g'8")
    slur = abjad.Slur()
    abjad.attach(slur, tuplet_2[:])
    voice = abjad.Voice([tuplet_1, tuplet_2])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8 (
                d'8
                e'8
                f'8
                g'8 )
            }
        }
        '''
        )

    tuplets = voice[:]
    abjad.mutate(tuplets).fuse()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
                c'8 (
                d'8
                e'8
                f'8
                g'8 )
            }
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Mutation_fuse_09():
    r'''Tuplets must carry same multiplier.
    '''

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    tuplet_2 = abjad.Tuplet ((4, 5), "c'8 d'8 e'8 f'8 g'8")
    tuplets = abjad.select([tuplet_1, tuplet_2])

    assert pytest.raises(Exception, 'abjad.mutate(tuplets).fuse()')


def test_scoretools_Mutation_fuse_10():
    r'''Dominant spanners on contents are preserved.
    '''

    tuplet_1 = abjad.Tuplet((2, 3), "c'8")
    tuplet_2 = abjad.Tuplet((2, 3), "c'4")
    voice = abjad.Voice([tuplet_1, tuplet_2, abjad.Note("c'4")])
    leaves = abjad.select(voice).leaves()
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8 (
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'4
            }
            c'4 )
        }
        '''
        )

    tuplets = voice[:2]
    abjad.mutate(tuplets).fuse()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8 (
                c'4
            }
            c'4 )
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Mutation_fuse_11():
    r'''Fuses unicorporated measures carrying
    time signatures with power-of-two denominators.
    '''

    measure_1 = abjad.Measure((1, 8), "c'16 d'16")
    beam = abjad.Beam()
    abjad.attach(beam, measure_1[:])
    measure_2 = abjad.Measure((2, 16), "c'16 d'16")
    slur = abjad.Slur()
    abjad.attach(slur, measure_2[:])
    staff = abjad.Staff([measure_1, measure_2])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/8
                c'16 [
                d'16 ]
            } % measure
            { % measure
                \time 2/16
                c'16 (
                d'16 )
            } % measure
        }
        '''
        )

    new = abjad.mutate(staff[:]).fuse()

    assert new is not measure_1 and new is not measure_2
    assert len(measure_1) == 0
    assert len(measure_2) == 0

    assert format(new) == abjad.String.normalize(
        r'''
        { % measure
            \time 2/8
            c'16 [
            d'16 ]
            c'16 (
            d'16 )
        } % measure
        '''
        )

    assert abjad.inspect(new).is_well_formed()


def test_scoretools_Mutation_fuse_12():
    r'''Fuses measures carrying time signatures with differing
    power-of-two denominators. Helpers abjad.selects minimum of two denominators.
    Beams are OK because they abjad.attach to leaves rather than containers.
    '''

    voice = abjad.Voice("abj: | 1/8 c'16 d'16 || 2/16 e'16 f'16 |")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            { % measure
                \time 1/8
                c'16 [
                d'16
            } % measure
            { % measure
                \time 2/16
                e'16
                f'16 ]
            } % measure
        }
        '''
        )

    abjad.mutate(voice[:]).fuse()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            { % measure
                \time 2/8
                c'16 [
                d'16
                e'16
                f'16 ]
            } % measure
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Mutation_fuse_13():
    r'''Fuses measures with differing power-of-two denominators.
    Helpers abjad.selects minimum of two denominators.
    Beam abjad.attaches to container rather than leaves.
    '''

    voice = abjad.Voice("abj: | 1/8 c'16 d'16 || 2/16 e'16 f'16 |")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            { % measure
                \time 1/8
                c'16 [
                d'16 ]
            } % measure
            { % measure
                \time 2/16
                e'16
                f'16
            } % measure
        }
        '''
        )

    abjad.mutate(voice[:]).fuse()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            { % measure
                \time 2/8
                c'16 [
                d'16 ]
                e'16
                f'16
            } % measure
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Mutation_fuse_14():
    r'''Fuses measures with power-of-two-denominators together with measures
    without power-of-two denominators.
    Helpers abjad.selects least common multiple of denominators.
    Beams are OK because they abjad.attach to leaves rather than containers.
    '''

    measure_1 = abjad.Measure((1, 8), "c'8")
    measure_1.implicit_scaling = True
    measure_2 = abjad.Measure((1, 12), "d'8")
    measure_2.implicit_scaling = True
    voice = abjad.Voice([measure_1, measure_2])
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            { % measure
                \time 1/8
                c'8 [
            } % measure
            { % measure
                \time 1/12
                \scaleDurations #'(2 . 3) {
                    d'8 ]
                }
            } % measure
        }
        '''
        )

    abjad.mutate(voice[:]).fuse()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            { % measure
                \time 5/24
                \scaleDurations #'(2 . 3) {
                    c'8. [
                    d'8 ]
                }
            } % measure
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Mutation_fuse_15():
    r'''Fusing empty selection returns none.
    '''

    staff = abjad.Staff()
    result = abjad.mutate(staff[:]).fuse()
    assert result == abjad.Selection()


def test_scoretools_Mutation_fuse_16():
    r'''Fusing selection of only one measure returns measure unaltered.
    '''

    measure = abjad.Measure((3, 8), "c'8 d'8 e'8")
    staff = abjad.Staff([measure])
    new = abjad.mutate(staff[:]).fuse()

    assert new is measure


def test_scoretools_Mutation_fuse_17():
    r'''Fuses three measures.
    '''

    voice = abjad.Voice("abj: | 1/8 c'16 d'16 || 1/8 e'16 f'16 || 1/8 g'16 a'16 |")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            { % measure
                \time 1/8
                c'16 [
                d'16
            } % measure
            { % measure
                e'16
                f'16
            } % measure
            { % measure
                g'16
                a'16 ]
            } % measure
        }
        '''
        )

    abjad.mutate(voice[:]).fuse()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            { % measure
                \time 3/8
                c'16 [
                d'16
                e'16
                f'16
                g'16
                a'16 ]
            } % measure
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Mutation_fuse_18():
    r'''Fusing measures with power-of-two denominators
    to measures without power-of-two denominators.
    With change in number of note-heads because of non-power-of-two multiplier.
    '''

    measure_1 = abjad.Measure((9, 80), [])
    measure_1.implicit_scaling = True
    measure_1.extend(9 * abjad.Note("c'64"))
    measure_2 = abjad.Measure((2, 16), [])
    measure_2.implicit_scaling = True
    measure_2.extend(2 * abjad.Note("c'16"))
    staff = abjad.Staff([measure_1, measure_2])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 9/80
                \scaleDurations #'(4 . 5) {
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                }
            } % measure
            { % measure
                \time 2/16
                c'16
                c'16
            } % measure
        }
        '''
        )

    new = abjad.mutate(staff[:]).fuse()

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 19/80
                \scaleDurations #'(4 . 5) {
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'16 ~
                    c'64
                    c'16 ~
                    c'64
                }
            } % measure
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
