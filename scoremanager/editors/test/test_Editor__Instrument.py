# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Editor__Instrument_01():
    r'''While editing instrument: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist horn q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (12,)

    input_ = 'red~example~score setup instrumentation hornist horn b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (8, 12))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (0, 12))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn s q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (2, 12))

    input_ = 'red~example~score setup instrumentation hornist horn foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (10, 12))


def test_Editor__Instrument_02():
    r'''While editing short instrument name markup: quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist horn sm q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13,)

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn sm b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (10, 13))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn sm h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (0, 13))


def test_Editor__Instrument_03():
    r'''While editing short instrument name: quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist horn sn q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13,)

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn sn b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (10, 13))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn sn h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (0, 13))


def test_Editor__Instrument_04():
    r'''Short instrument name: number is rejected.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn sn -99 q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15,)


def test_Editor__Instrument_05():
    r'''Short instrument name does not change short instrument name markup.
    Unless short instrument name markup is set explicitly.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Accordion()
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = "sn 'foo' q"
    editor._run(pending_user_input=input_)
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Accordion()
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = "sm 'bar' sn 'foo' q"
    editor._run(pending_user_input=input_)
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == Markup('bar')


def test_Editor__Instrument_06():
    r'''Edits instrument range.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Marimba()
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = 'q'
    editor._run(pending_user_input=input_)
    assert editor.target.pitch_range == pitchtools.PitchRange(-19, 36)

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Marimba()
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = 'rg [C2, C7] q'
    editor._run(pending_user_input=input_)
    assert editor.target.pitch_range == pitchtools.PitchRange(-24, 36)


def test_Editor__Instrument_07():
    r'''While editing instrument name markup: quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist horn im q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13,)

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn im b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (10, 13))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn im h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (0, 13))


def test_Editor__Instrument_08():
    r'''While editing instrument name: quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist horn in q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13,)

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn in b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (10, 13))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn in h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (0, 13))


def test_Editor__Instrument_09():
    r'''While editing instrument name: integer is rejected.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn in -99 q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15,)


def test_Editor__Instrument_10():
    r'''While editing instrument name: instrument name does not 
    change instrument name markup.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Accordion()
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = "in 'foo' q"
    editor._run(pending_user_input=input_)
    instrument = editor.target
    assert instrument.instrument_name == 'foo'

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Accordion()
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = "im 'bar' in 'foo' q"
    editor._run(pending_user_input=input_)
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == Markup('bar')


def test_Editor__Instrument_11():
    r'''While editing instrument: main screen.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Accordion()
    editor = scoremanager.editors.Editor(
        session=session,
        target=target
        )
    input_ = 'q'
    editor._run(pending_user_input=input_)

    lines = [
        'Accordion',
        '',
        '    1: clefs (cf): treble, bass',
        "    2: instrument name (in): accordion",
        "    3: instrument name markup (im): \markup { Accordion }",
        '    4: range (rg): [E1, C8]',
        "    5: short instrument name (sn): acc.",
        "    6: short instrument name markup (sm): \markup { Acc. }",
        "    7: sounding pitch of written middle C (sp): c'",
        '',
        '    done (done)',
        '',
        ]
    assert editor._transcript.last_menu_lines == lines


def test_Editor__Instrument_12():
    r'''Edits sounding pitch of written middle C.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.FrenchHorn()
    assert target.sounding_pitch_of_written_middle_c == NamedPitch('f')
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = 'sp bf done'
    editor._run(pending_user_input=input_)
    instrument = editor.target
    horn = instrumenttools.FrenchHorn(
        sounding_pitch_of_written_middle_c=NamedPitch('bf')
        )
    assert instrument == horn