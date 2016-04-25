# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_MultipartBeam___init___01():
    r'''Initialize empty multipart beam spanner.
    '''

    beam = spannertools.MultipartBeam()
    assert isinstance(beam, spannertools.MultipartBeam)
