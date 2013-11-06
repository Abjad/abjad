# -*- encoding: utf-8 -*-
from abjad.tools import iotools
import os


def test_iotools_IOManager_save_last_ly_as_01():

    iotools.IOManager.save_last_ly_as('tmp_foo.ly')
    assert os.path.exists('tmp_foo.ly')

    os.remove('tmp_foo.ly')
    assert not os.path.exists('tmp_foo.ly')
