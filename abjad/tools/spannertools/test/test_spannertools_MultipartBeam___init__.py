# -*- coding: utf-8 -*-
import abjad


def test_spannertools_MultipartBeam___init___01():
    r'''Initialize empty multipart beam spanner.
    '''

    beam = abjad.MultipartBeam()
    assert isinstance(beam, abjad.MultipartBeam)
