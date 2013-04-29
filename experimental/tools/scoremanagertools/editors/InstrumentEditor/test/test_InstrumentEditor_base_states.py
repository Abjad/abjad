from abjad import *
from experimental import *


def test_InstrumentEditor_base_states_01():
    '''Start-up, select instrument, main menu.
    '''

    editor = scoremanagertools.editors.InstrumentEditor()
    editor.run(user_input='1 q')
    assert editor.transcript_signature == (4,)
    assert editor.transcript[-2] == \
    ['Accordion',
      '',
      "     (1) instrument name (in): accordion",
      "     (2) instrument name markup (im): Markup(('Accordion',))",
      "     (3) short instrument name (sn): acc.",
      "     (4) short instrument name markup (sm): Markup(('Acc.',))",
      '     (5) range (rg): [E1, C8]',
      '     (6) clefs (cf): treble, bass',
      '']


def test_InstrumentEditor_base_states_02():
    '''Start-up values without target.
    '''

    editor = scoremanagertools.editors.InstrumentEditor()
    assert isinstance(editor.session, scoremanagertools.core.Session)
    assert editor.target is None


def test_InstrumentEditor_base_states_03():
    '''Start-up values with target.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'
    editor = scoremanagertools.editors.InstrumentEditor(target=accordion)
    assert isinstance(editor.session, scoremanagertools.core.Session)
    assert editor.target is accordion
