# -*- coding: utf-8 -*-
import abjad


def test_schemetools_SchemeMoment_duration_01():

    scheme_moment = abjad.SchemeMoment((1, 68))

    assert scheme_moment.duration == abjad.Duration((1, 68))
