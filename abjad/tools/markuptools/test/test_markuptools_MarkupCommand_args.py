# -*- encoding: utf-8 -*-
from abjad import *


def test_markuptools_MarkupCommand_args_01():
    mc = markuptools.MarkupCommand('draw-circle', 1, 0.1, False)
    assert mc.args == (1, 0.1, False)