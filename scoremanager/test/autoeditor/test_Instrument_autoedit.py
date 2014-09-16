# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Instrument_autoedit_01():
    r'''Short instrument name does not change short instrument name markup.
    Unless short instrument name markup is set explicitly.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Accordion()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "sn 'foo' q"
    autoeditor._session._pending_input = input_
    autoeditor._run()
    instrument = autoeditor.target
    assert instrument.short_instrument_name == 'foo'

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Accordion()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "sm 'bar' sn 'foo' q"
    autoeditor._session._pending_input = input_
    autoeditor._run()
    instrument = autoeditor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == Markup('bar')


def test_Instrument_autoedit_02():
    r'''Edits instrument range.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Marimba()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'q'
    autoeditor._session._pending_input = input_
    autoeditor._run()
    range_ = pitchtools.PitchRange.from_pitches(-19, 36)
    assert autoeditor.target.pitch_range == range_

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Marimba()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'rg [C2, C7] q'
    autoeditor._session._pending_input = input_
    autoeditor._run()
    range_ = pitchtools.PitchRange.from_pitches(-24, 36)
    assert autoeditor.target.pitch_range == range_


def test_Instrument_autoedit_03():
    r'''While editing instrument name: instrument name does not
    change instrument name markup.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Accordion()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "in 'foo' q"
    autoeditor._session._pending_input = input_
    autoeditor._run()
    instrument = autoeditor.target
    assert instrument.instrument_name == 'foo'

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Accordion()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "im 'bar' in 'foo' q"
    autoeditor._session._pending_input = input_
    autoeditor._run()
    instrument = autoeditor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == Markup('bar')


def test_Instrument_autoedit_04():
    r'''While editing instrument: main screen.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Accordion()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target
        )
    input_ = 'q'
    autoeditor._session._pending_input = input_
    autoeditor._run()
    contents = autoeditor._transcript.contents

    lines = [
        'Accordion',
        '',
        '   1: clefs (cf): treble, bass',
        "   2: instrument name (in): accordion",
        "   3: instrument name markup (im): \markup { Accordion }",
        '   4: range (rg): [E1, C8]',
        "   5: short instrument name (sn): acc.",
        "   6: short instrument name markup (sm): \markup { Acc. }",
        "   7: sounding pitch of written middle C (sp): c'",
        '',
        '      done (done)',
        '',
        ]
    for line in lines:
        assert line in contents


def test_Instrument_autoedit_05():
    r'''Edits sounding pitch of written middle C.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.FrenchHorn()
    assert target.sounding_pitch_of_written_middle_c == NamedPitch('f')
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'sp bf done'
    autoeditor._session._pending_input = input_
    autoeditor._run()
    instrument = autoeditor.target
    horn = instrumenttools.FrenchHorn(
        sounding_pitch_of_written_middle_c=NamedPitch('bf')
        )
    assert instrument == horn