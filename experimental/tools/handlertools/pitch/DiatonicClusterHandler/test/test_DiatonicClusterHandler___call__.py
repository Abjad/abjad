from experimental import *


def test_DiatonicClusterHandler___call___01():

    diatonic_cluster_handler = handlertools.pitch.DiatonicClusterHandler([4, 6])

    staff = Staff("c' d' e' f'")
    diatonic_cluster_handler(staff)

    r'''
    \new Staff {
        <c' d' e' f'>4
        <d' e' f' g' a' b'>4
        <e' f' g' a'>4
        <f' g' a' b' c'' d''>4
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t<c' d' e' f'>4\n\t<d' e' f' g' a' b'>4\n\t<e' f' g' a'>4\n\t<f' g' a' b' c'' d''>4\n}"
