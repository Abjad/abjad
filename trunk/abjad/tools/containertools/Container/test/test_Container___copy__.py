from abjad import *
import copy


def test_Container___copy___01():
    '''Containes copy parallel indicator.
    '''

    container_1 = Container([Voice("c'8 d'8"), Voice("c''8 b'8")])
    container_1.is_parallel = True

    container_2 = copy.copy(container_1)


    r'''
    <<
        \new Voice {
            c'8
            d'8
        }
        \new Voice {
            c''8
            b'8
        }
    >>
    '''

    assert container_1 is not container_2
    assert container_2.format == '<<\n>>'
