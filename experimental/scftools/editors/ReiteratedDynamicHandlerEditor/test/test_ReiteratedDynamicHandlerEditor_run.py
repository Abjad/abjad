from abjad import *
from experimental.tools import handlertools
import scftools


def test_ReiteratedDynamicHandlerEditor_run_01():

    editor = scftools.editors.ReiteratedDynamicHandlerEditor()
    editor.run(user_input="1 f Duration(1, 8) q", is_autoadvancing=True)

    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 8),
        )

    assert editor.target == handler
