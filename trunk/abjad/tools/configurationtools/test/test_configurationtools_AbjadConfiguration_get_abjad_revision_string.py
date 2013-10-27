# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import configurationtools


def test_configurationtools_AbjadConfiguration_get_abjad_revision_string_01():
    assert isinstance(
        configurationtools.AbjadConfiguration.get_abjad_revision_string(), 
        str,
        )
