# -*- encoding: utf-8 -*-
import pytest
pytest.skip()
from abjad import *


def test_NoteAndChordHairpinsHandler___call___01():

    handler = handlertools.NoteAndChordHairpinsHandler(
        hairpin_tokens=[
            ('p', '<', 'f'),
            ('p', '<', 'f'),
            ('pp', '<', 'p'),
            ],
        minimum_duration=Duration(1, 8),
        )

    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8 a'32 b'32 r8. c''8 d''8" )
    handler(staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 \< \p
            d'8 \f
            r8
            e'8 \< \p
            f'8 \f
            r8
            g'8 \pp
            r8
            a'32 \p
            b'32
            r8.
            c''8 \< \p
            d''8 \f
        }
        '''
        )