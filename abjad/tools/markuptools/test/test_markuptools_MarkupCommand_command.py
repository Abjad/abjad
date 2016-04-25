# -*- coding: utf-8 -*-
from abjad import *


def test_markuptools_MarkupCommand_command_01():
    mc = markuptools.MarkupCommand('draw-circle', 1, 0.1, False)
    assert mc.command == 'draw-circle'
