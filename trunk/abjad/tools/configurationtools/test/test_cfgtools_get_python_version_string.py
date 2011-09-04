from abjad import *
from abjad.tools import configurationtools


def test_configurationtools_get_python_version_string_01():


    python_version_string = configurationtools.get_python_version_string()

    assert isinstance(python_version_string, str)
    assert python_version_string.count('.') == 2
