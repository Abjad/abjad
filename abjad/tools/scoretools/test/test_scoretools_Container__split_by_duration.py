import abjad


def test_scoretools_Container__split_by_duration_01():

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/32
                c'32 [ (
            } % measure
            { % measure
                \time 7/32
                c'16.
                d'8 ]
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_02():
    '''Split staff. Resulting halves are not well-formed.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(halves[0][0]) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/32
                c'32 [ (
            } % measure
        }
        '''
        ), format(halves[0][0])

    assert format(halves[1][0]) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 7/32
                c'16.
                d'8 ]
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(halves[1][0])

    assert not abjad.inspect(halves[0][0]).is_well_formed()
    assert not abjad.inspect(halves[1][0]).is_well_formed()


def test_scoretools_Container__split_by_duration_03():
    r'''Split one measure in score.
    Do not fracture spanners. But do add tie after split.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/32
                c'32 ~ [ (
            } % measure
            { % measure
                \time 7/32
                c'16.
                d'8 ]
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_04():
    r'''Split in-score measure with power-of-two time signature denominator
    at split offset without power-of-two denominator.
    Do not fracture spanners and do not tie leaves after split.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 5),
        fracture_spanners=False,
        )

    # TODO: The tie at the split locus here is a (small) bug.
    #       Eventually should fix.
    #       The tie after the d'16. is the incorrect one.
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 4/20
                \scaleDurations #'(4 . 5) {
                    c'8 ~ [ (
                    c'32
                    d'16. ~
                }
            } % measure
            { % measure
                \time 1/20
                \scaleDurations #'(4 . 5) {
                    d'16 ]
                }
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_05():
    r'''Split in-score measure with power-of-two time signature denominator
    at split offset without power-of-two denominator.
    Do fracture spanners and do tie leaves after split.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 5),
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 4/20
                \scaleDurations #'(4 . 5) {
                    c'8 ~ [ (
                    c'32
                    d'16. ~
                }
            } % measure
            { % measure
                \time 1/20
                \scaleDurations #'(4 . 5) {
                    d'16 ]
                }
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_06():
    r'''Split measure in score and fracture spanners.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/32
                c'32 [ ]
            } % measure
            { % measure
                \time 7/32
                c'16. [ (
                d'8 ]
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_07():
    r'''Split staff outside of score and fracture spanners.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(halves[0][0]) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/32
                c'32 [ ]
            } % measure
        }
        '''
        ), format(halves[0][0])

    assert format(halves[1][0]) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 7/32
                c'16. [ (
                d'8 ]
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(halves[1][0])


def test_scoretools_Container__split_by_duration_08():
    r'''Split container over leaf at nonzero index.
    Fracture spanners.
    Test results from bug fix.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(7, 32),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 7/32
                c'8 [ (
                d'16. ] )
            } % measure
            { % measure
                \time 1/32
                d'32 [ ] (
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_09():
    r'''Split container between leaves and fracture spanners.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 8),
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/8
                c'8 [ ]
            } % measure
            { % measure
                d'8 [ ] (
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_10():
    r'''Split measure in score and fracture spanners.
    Tie leaves after split.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/32
                c'32 ~ [ ]
            } % measure
            { % measure
                \time 7/32
                c'16. [ (
                d'8 ]
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_11():
    r'''Split in-score measure with power-of-two time signature denominator
    at split offset without power-of-two denominator.
    Do fracture spanners but do not tie leaves after split.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 5),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 4/20
                \scaleDurations #'(4 . 5) {
                    c'8 ~ [ (
                    c'32
                    d'16. ] )
                }
            } % measure
            { % measure
                \time 1/20
                \scaleDurations #'(4 . 5) {
                    d'16 [ ] (
                }
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_12():
    r'''Split in-score measure with power-of-two time signature denominator at
    split offset without power-of-two denominator.
    Do fracture spanners and do tie leaves after split.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 8), "c'8 d'8"))
    staff.append(abjad.Measure((2, 8), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/8
                c'8 [ (
                d'8 ]
            } % measure
            { % measure
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 5),
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 4/20
                \scaleDurations #'(4 . 5) {
                    c'8 ~ [ (
                    c'32
                    d'16. ~ ] )
                }
            } % measure
            { % measure
                \time 1/20
                \scaleDurations #'(4 . 5) {
                    d'16 [ ] (
                }
            } % measure
            { % measure
                \time 2/8
                e'8 [
                f'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_13():
    r'''Split measure with power-of-two time signature denominator at
    split offset without power-of-two denominator.
    Do fracture spanners but do not tie across split locus.
    This test results from a fix.
    What's being tested here is contents rederivation.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((3, 8), "c'8 d'8 e'8"))
    staff.append(abjad.Measure((3, 8), "c'8 d'8 e'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:3])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-3:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 3/8
                c'8 [ (
                d'8
                e'8 ]
            } % measure
            { % measure
                c'8 [
                d'8
                e'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(7, 20),
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 14/40
                \scaleDurations #'(4 . 5) {
                    c'8 ~ [ (
                    c'32
                    d'8 ~
                    d'32
                    e'8 ] )
                }
            } % measure
            { % measure
                \time 1/40
                \scaleDurations #'(4 . 5) {
                    e'32 [ ] (
                }
            } % measure
            { % measure
                \time 3/8
                c'8 [
                d'8
                e'8 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_14():
    r'''Split measure with power-of-two time signature denominator
    with multiplied leaes. Split at between-leaf offset with
    power-of-two denominator. Leaves remain unaltered.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 16), "c'8 d'8"))
    staff.append(abjad.Measure((2, 16), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    for leaf in leaves:
        abjad.attach(abjad.Multiplier(1, 2), leaf)
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/16
                c'8 * 1/2 [ (
                d'8 * 1/2 ]
            } % measure
            { % measure
                e'8 * 1/2 [
                f'8 * 1/2 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 16),
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 1/16
                c'8 * 1/2 [ ]
            } % measure
            { % measure
                d'8 * 1/2 [ ] (
            } % measure
            { % measure
                \time 2/16
                e'8 * 1/2 [
                f'8 * 1/2 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_15():
    r'''Split measure with power-of-two time signature denominator
    with multiplied leaves. Split at through-leaf offset with
    power-of-two denominator. Leaf written durations stay the same
    but multipliers change.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 16), "c'8 d'8"))
    staff.append(abjad.Measure((2, 16), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    for leaf in leaves:
        abjad.attach(abjad.Multiplier(1, 2), leaf)
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/16
                c'8 * 1/2 [ (
                d'8 * 1/2 ]
            } % measure
            { % measure
                e'8 * 1/2 [
                f'8 * 1/2 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(3, 32),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 3/32
                c'8 * 1/2 [ (
                d'8 * 1/4 ] )
            } % measure
            { % measure
                \time 1/32
                d'8 * 1/4 [ ] (
            } % measure
            { % measure
                \time 2/16
                e'8 * 1/2 [
                f'8 * 1/2 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_16():
    r'''Split measure with power-of-two time signature denominator
    with multiplied leaves. Split at through-leaf offset without
    power-of-two denominator. Leaf written durations adjust for change
    from power-of-two denominator to non-power-of-two denominator.
    Leaf multipliers also change.
    '''

    staff = abjad.Staff()
    staff.append(abjad.Measure((2, 16), "c'8 d'8"))
    staff.append(abjad.Measure((2, 16), "e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    for leaf in leaves:
        abjad.attach(abjad.Multiplier(1, 2), leaf)
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/16
                c'8 * 1/2 [ (
                d'8 * 1/2 ]
            } % measure
            { % measure
                e'8 * 1/2 [
                f'8 * 1/2 ] )
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(2, 24),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 2/24
                \scaleDurations #'(2 . 3) {
                    c'8. * 1/2 [ (
                    d'8. * 1/6 ] )
                }
            } % measure
            { % measure
                \time 1/24
                \scaleDurations #'(2 . 3) {
                    d'8. * 1/3 [ ] (
                }
            } % measure
            { % measure
                \time 2/16
                e'8 * 1/2 [
                f'8 * 1/2 ] )
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_17():
    r'''Split measure with power-of-two time signature denominator
    with multiplied leaves. Time signature carries numerator that
    necessitates ties. Split at through-leaf offset without
    power-of-two denominator.
    '''

    staff = abjad.Staff([abjad.Measure((5, 16), "s1 * 5/16")])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 5/16
                s1 * 5/16
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(16, 80),
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 16/80
                \scaleDurations #'(4 . 5) {
                    s1 * 1/4
                }
            } % measure
            { % measure
                \time 9/80
                \scaleDurations #'(4 . 5) {
                    s1 * 1/16
                    s4 * 5/16
                }
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_18():
    r'''Split measure without power-of-two time signature denominator
    at split offset without power-of-two denominator.
    abjad.Measure multiplier and split offset multiplier match.
    Split between leaves but do fracture spanners.
    '''

    measure = abjad.Measure((15, 80), "c'32 d' e' f' g' a' b' c''64")
    measure.implicit_scaling = True
    staff = abjad.Staff([measure])
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 15/80
                \scaleDurations #'(4 . 5) {
                    c'32 [ (
                    d'32
                    e'32
                    f'32
                    g'32
                    a'32
                    b'32
                    c''64 ] )
                }
            } % measure
        }
        '''
        ), format(staff)

    halves = staff[0]._split_by_duration(
        abjad.Duration(14, 80),
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            { % measure
                \time 14/80
                \scaleDurations #'(4 . 5) {
                    c'32 [ (
                    d'32
                    e'32
                    f'32
                    g'32
                    a'32
                    b'32 ] )
                }
            } % measure
            { % measure
                \time 1/80
                \scaleDurations #'(4 . 5) {
                    c''64 [ ]
                }
            } % measure
        }
        '''
        ), format(staff)

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Container__split_by_duration_19():
    r'''Make sure tie (re)application happens only where sensible.
    '''

    halves = abjad.Container("c'4")._split_by_duration(
        abjad.Duration(3, 16),
        fracture_spanners=True,
        )

    assert format(halves[0][0]) == abjad.String.normalize(
        r'''
        {
            c'8.
        }
        '''
        ), format(halves[0][0])

    assert format(halves[-1][0]) == abjad.String.normalize(
        r'''
        {
            c'16
        }
        '''
        ), format(halves[-1][0])

    assert abjad.inspect(halves[0][0]).is_well_formed()
    assert abjad.inspect(halves[-1][0]).is_well_formed()
