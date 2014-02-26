# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_base_states_01():
    r'''Start-up, select instrument, main menu.
    '''

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='1 q')
    assert editor._transcript.signature == (4,)
    assert editor._transcript.last_menu_lines == \
    ['Accordion',
      '',
      "     1: instrument name (in): accordion",
      "     2: instrument name markup (im): \markup { Accordion }",
      "     3: short instrument name (sn): acc.",
      "     4: short instrument name markup (sm): \markup { Acc. }",
      '     5: range (rg): [E1, C8]',
      '     6: clefs (cf): treble, bass',
      '',
      '     done (done)',
      '']


def test_InstrumentEditor_base_states_02():
    r'''Start-up values without target.
    '''

    editor = scoremanager.editors.InstrumentEditor()
    assert isinstance(editor._session, scoremanager.core.Session)
    assert editor.target is None


def test_InstrumentEditor_base_states_03():
    r'''Start-up values with target.
    '''

    accordion = instrumenttools.Accordion(
        instrument_name='accordion I',
        short_instrument_name='acc. I',
        )
    editor = scoremanager.editors.InstrumentEditor(target=accordion)
    assert isinstance(editor._session, scoremanager.core.Session)
    assert editor.target is accordion
