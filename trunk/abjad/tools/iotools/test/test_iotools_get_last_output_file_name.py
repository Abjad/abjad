from abjad import *
from abjad.tools import iotools


def test_iotools_get_last_output_file_name_01():

    last_output_file_name = iotools.get_last_output_file_name()

    assert isinstance(last_output_file_name, (str, type(None)))
    if isinstance(last_output_file_name, str):
        if last_output_file_name.endswith('.ly'):
            assert len(last_output_file_name) == 7
        elif last_output_file_name.endswith('.pdf'):
            assert len(last_output_file_name) == 8
        elif last_output_file_name.endswith('.mid'):
            assert len(last_output_file_name) == 8
        elif last_output_file_name.endswith('.midi'):
            assert len(last_output_file_name) == 9
        else:
            raise Exception
