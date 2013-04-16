from abjad import *
from experimental.tools import handlertools
from experimental import *


def test_TerracedDynamicsHandlerEditor_run_01():

    editor = scoremanagementtools.editors.TerracedDynamicsHandlerEditor()
    editor.run(user_input="1 ['p', 'f', 'f'] Duration(1, 8) q", is_autoadvancing=True)

    handler = handlertools.TerracedDynamicsHandler(
        dynamics=['p', 'f', 'f'],
        minimum_duration=Duration(1, 8),
        )

    assert editor.target == handler
