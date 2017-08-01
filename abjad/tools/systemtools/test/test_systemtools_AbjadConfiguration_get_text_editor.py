# -*- coding: utf-8 -*-
import abjad
from abjad.tools import systemtools


def test_systemtools_AbjadConfiguration_get_text_editor_01():
    assert isinstance(
        systemtools.AbjadConfiguration.get_text_editor(),
        str,
        )
