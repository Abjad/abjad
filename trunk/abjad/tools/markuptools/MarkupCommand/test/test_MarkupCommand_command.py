from abjad import *


def test_MarkupCommand_command_01():
    mc = markuptools.MarkupCommand('draw-circle', ['#1', '#0.1', '##f'], None)
    assert mc.command == 'draw-circle'
