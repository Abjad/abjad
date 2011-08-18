from abjad import *
from abjad.tools import iotools


def test_iotools_get_last_output_file_name_01():

    last_output_file_name = iotools.get_last_output_file_name()

    assert isinstance(last_output_file_name, str)
    assert len(last_output_file_name) == 7
    assert last_output_file_name.endswith('.ly')
