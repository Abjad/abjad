# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Editor__Instrument_01():
    r'''Short instrument name does not change short instrument name markup.
    Unless short instrument name markup is set explicitly.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Accordion()
    editor = scoremanager.iotools.Editor(
        session=session,
        target=target,
        )
    input_ = "sn 'foo' q"
    editor._run(pending_input=input_)
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Accordion()
    editor = scoremanager.iotools.Editor(
        session=session,
        target=target,
        )
    input_ = "sm 'bar' sn 'foo' q"
    editor._run(pending_input=input_)
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == Markup('bar')


def test_Editor__Instrument_02():
    r'''Edits instrument range.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Marimba()
    editor = scoremanager.iotools.Editor(
        session=session,
        target=target,
        )
    input_ = 'q'
    editor._run(pending_input=input_)
    assert editor.target.pitch_range == pitchtools.PitchRange(-19, 36)

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Marimba()
    editor = scoremanager.iotools.Editor(
        session=session,
        target=target,
        )
    input_ = 'rg [C2, C7] q'
    editor._run(pending_input=input_)
    assert editor.target.pitch_range == pitchtools.PitchRange(-24, 36)


def test_Editor__Instrument_03():
    r'''While editing instrument name: instrument name does not
    change instrument name markup.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Accordion()
    editor = scoremanager.iotools.Editor(
        session=session,
        target=target,
        )
    input_ = "in 'foo' q"
    editor._run(pending_input=input_)
    instrument = editor.target
    assert instrument.instrument_name == 'foo'

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Accordion()
    editor = scoremanager.iotools.Editor(
        session=session,
        target=target,
        )
    input_ = "im 'bar' in 'foo' q"
    editor._run(pending_input=input_)
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == Markup('bar')


def test_Editor__Instrument_04():
    r'''While editing instrument: main screen.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.Accordion()
    editor = scoremanager.iotools.Editor(
        session=session,
        target=target
        )
    input_ = 'q'
    editor._run(pending_input=input_)

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
    assert editor._transcript.last_menu_lines == lines


def test_Editor__Instrument_05():
    r'''Edits sounding pitch of written middle C.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.FrenchHorn()
    assert target.sounding_pitch_of_written_middle_c == NamedPitch('f')
    editor = scoremanager.iotools.Editor(
        session=session,
        target=target,
        )
    input_ = 'sp bf done'
    editor._run(pending_input=input_)
    instrument = editor.target
    horn = instrumenttools.FrenchHorn(
        sounding_pitch_of_written_middle_c=NamedPitch('bf')
        )
    assert instrument == horn