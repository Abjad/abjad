# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import systemtools


def test_systemtools_IOManager_get_last_output_file_name_01():

    last_output_file_name = systemtools.IOManager.get_last_output_file_name()

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
            message = 'can not pasre last output file name: {!r}.'
            message = message.format(last_output_file_name)
            raise Exception(message)
