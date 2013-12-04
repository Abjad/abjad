# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentEditor_base_states_01():
    r'''Start-up, select instrument, main menu.
    '''

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input='1 q')
    assert editor.session.io_transcript.signature == (4,)
    assert editor.session.io_transcript[-2][1] == \
    ['Accordion',
      '',
      "     1: instrument name (in): accordion",
      "     2: instrument name markup (im): \markup { Accordion }",
      "     3: short instrument name (sn): acc.",
      "     4: short instrument name markup (sm): \markup { Acc. }",
      '     5: range (rg): [E1, C8]',
      '     6: clefs (cf): treble, bass',
      '']


def test_InstrumentEditor_base_states_02():
    r'''Start-up values without target.
    '''

    editor = scoremanagertools.editors.InstrumentEditor()
    assert isinstance(editor.session, scoremanagertools.scoremanager.Session)
    assert editor.target is None


def test_InstrumentEditor_base_states_03():
    r'''Start-up values with target.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'
    editor = scoremanagertools.editors.InstrumentEditor(target=accordion)
    assert isinstance(editor.session, scoremanagertools.scoremanager.Session)
    assert editor.target is accordion
