from experimental import *


def test_rhythm_01():
    '''Sixteenths.
    '''

    leaf_lists = library.sixteenths([(4, 8), (3, 8)])
    containers = [Container(x) for x in leaf_lists]
    staff = Staff(containers)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                c'16
                c'16
                c'16
                c'16
                c'16
                c'16
                c'16
                c'16
            }
            {
                c'16
                c'16
                c'16
                c'16
                c'16
                c'16
            }
        }
        '''
        )


def test_rhythm_02():
    '''Eighths.
    '''

    leaf_lists = library.eighths([(4, 8), (3, 8)])
    containers = [Container(x) for x in leaf_lists]
    staff = Staff(containers)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                c'8
                c'8
                c'8
                c'8
            }
            {
                c'8
                c'8
                c'8
            }
        }
        '''
        )


def test_rhythm_03():
    '''Quarters.
    '''

    leaf_lists = library.quarters([(4, 8), (3, 8)])
    containers = [Container(x) for x in leaf_lists]
    staff = Staff(containers)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                c'4
                c'4
            }
            {
                c'4
                c'8
            }
        }
        '''
        )


def test_rhythm_04():
    '''Thirty-seconds.
    '''

    leaf_lists = library.thirty_seconds([(4, 8), (3, 8)])
    containers = [Container(x) for x in leaf_lists]
    staff = Staff(containers)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
            }
            {
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
                c'32
            }
        }
        '''
        )
