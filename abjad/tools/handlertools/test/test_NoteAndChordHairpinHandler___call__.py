# -*- encoding: utf-8 -*-
import pytest
pytest.skip()
from abjad import *


def test_NoteAndChordHairpinHandler___call___01():

    handler = handlertools.NoteAndChordHairpinHandler(('p', '<', 'f'))
    staff = Staff("r4 c'8 d'8 r4 e'8 r8")
    handler(staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            r4
            c'8 \< \p
            d'8
            r4
            e'8 \f
            r8
        }
        '''
        )