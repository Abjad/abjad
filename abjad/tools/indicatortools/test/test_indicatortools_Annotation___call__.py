# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Annotation___call___01():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation = indicatortools.Annotation('foo')
    attach(annotation, staff[0])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
