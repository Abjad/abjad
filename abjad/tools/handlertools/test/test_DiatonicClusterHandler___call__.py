# -*- encoding: utf-8 -*-
from abjad import *


def test_DiatonicClusterHandler___call___01():

    diatonic_cluster_handler = handlertools.DiatonicClusterHandler([4, 6])

    staff = Staff("c' d' e' f'")
    diatonic_cluster_handler(staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            <c' d' e' f'>4
            <d' e' f' g' a' b'>4
            <e' f' g' a'>4
            <f' g' a' b' c'' d''>4
        }
        ''',
        )