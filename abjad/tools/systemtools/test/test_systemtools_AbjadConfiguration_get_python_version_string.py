# -*- coding: utf-8 -*-
import abjad
from abjad.tools import systemtools


def test_systemtools_AbjadConfiguration_get_python_version_string_01():
    python_version_string = \
        systemtools.AbjadConfiguration.get_python_version_string()
    assert isinstance(python_version_string, str)
    assert python_version_string.count('.') == 2
