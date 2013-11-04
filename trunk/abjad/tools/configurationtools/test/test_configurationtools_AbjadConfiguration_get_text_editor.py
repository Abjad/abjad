# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import configurationtools


def test_systemtools_AbjadConfiguration_get_text_editor_01():
    assert isinstance(
        systemtools.AbjadConfiguration.get_text_editor(),
        str,
        )
