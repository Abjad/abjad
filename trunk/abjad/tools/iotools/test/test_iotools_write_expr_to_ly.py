from abjad import *
from abjad.tools import iotools
import os


def test_iotools_write_expr_to_ly_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    iotools.write_expr_to_ly(staff, 'tmp_staff.ly')
    assert os.path.exists('tmp_staff.ly')

    os.remove('tmp_staff.ly')
    assert not os.path.exists('tmp_staff.ly')
