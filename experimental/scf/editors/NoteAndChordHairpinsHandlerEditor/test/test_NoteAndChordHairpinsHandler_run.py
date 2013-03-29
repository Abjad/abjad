from abjad import *
from experimental.tools import handlertools
import scf


def test_NoteAndChordHairpinsHandler_run_01():

    editor = scf.editors.NoteAndChordHairpinsHandlerEditor()
    editor.run(user_input="1 [('p', '<', 'f')] Duration(1, 8) q", is_autoadvancing=True)

    handler = handlertools.NoteAndChordHairpinsHandler(
        hairpin_tokens=[('p', '<', 'f')],
        minimum_duration=Duration(1, 8),
        )

    assert editor.target == handler
