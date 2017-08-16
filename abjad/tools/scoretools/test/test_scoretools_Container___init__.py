import abjad


def test_scoretools_Container___init___01():
    r'''Initialize empty container.
    '''

    container = abjad.Container([])

    r'''
    {
    }
    '''

    assert isinstance(container, abjad.Container)
    assert format(container) == abjad.String.normalize(
        r'''
        {
        }
        '''
        )


def test_scoretools_Container___init___02():
    r'''Initialize container with LilyPond note-entry string.
    '''

    container = abjad.Container("c'8 d'8 e'8")

    r'''
    {
        c'8
        d'8
        e'8
    }
    '''

    assert isinstance(container, abjad.Container)
    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            d'8
            e'8
        }
        '''
        )


def test_scoretools_Container___init___03():
    r'''Initialize container with RTM-syntax string.
    '''

    container = abjad.Container('rtm: (1 (1 1 1)) (2 (2 (1 (1 1 1)) 2))')

    r'''
    {
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        \times 4/5 {
            c'4
            \times 2/3 {
                c'16
                c'16
                c'16
            }
            c'4
        }
    }
    '''

    assert isinstance(container, abjad.Container)
    assert format(container) == abjad.String.normalize(
        r'''
        {
            \times 2/3 {
                c'8
                c'8
                c'8
            }
            \times 4/5 {
                c'4
                \times 2/3 {
                    c'16
                    c'16
                    c'16
                }
                c'4
            }
        }
        '''
        )

def test_scoretools_Container___init___04():
    r'''Initialize container with "reduced ly" syntax string.
    '''

    container = abjad.Container('abj: 2/3 { 8 8 8 }')

    r'''
    \times 2/3 {
        c'8
        c'8
        c'8
    }
    '''

    assert isinstance(container, abjad.Container)
    assert format(container) == abjad.String.normalize(
        r'''
        {
            \times 2/3 {
                c'8
                c'8
                c'8
            }
        }
        '''
        )
