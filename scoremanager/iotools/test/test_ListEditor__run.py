# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ListEditor__run_01():
    r'''Edits built-in list.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.iotools.ListEditor(session=session)
    input_ = "17 99 'foo' done q"
    editor._is_autoadding = True
    editor._run(pending_user_input=input_)

    assert editor.target == [17, 99, 'foo']


def test_ListEditor__run_02():
    r'''Edits empty clef inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.ClefInventory()
    editor = scoremanager.iotools.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add nm treble done add nm bass done done'
    editor._run(pending_user_input=input_)

    inventory = indicatortools.ClefInventory(['treble', 'bass'])
    assert editor.target == inventory


def test_ListEditor__run_03():
    r'''Edits nonempty clef inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.ClefInventory(['treble', 'bass'])
    editor = scoremanager.iotools.ListEditor(
        session=session,
        target=target,
        )
    input_ = '2 nm alto done done'
    editor._run(pending_user_input=input_)

    new_inventory = indicatortools.ClefInventory(['treble', 'alto'])
    assert editor.target == new_inventory


def test_ListEditor__run_04():
    r'''Edits empty markup inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = markuptools.MarkupInventory()
    editor = scoremanager.iotools.ListEditor(
        session=session,
        target=target,
        )
    input_ = r'add arg \italic~{~serenamente~possibile~} done done'
    editor._run(pending_user_input=input_)

    inventory = markuptools.MarkupInventory([
        markuptools.Markup(
            '\\italic { serenamente possibile }',
            )
        ])

    assert editor.target == inventory


def test_ListEditor__run_05():
    r'''Edits nonempty markup inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = markuptools.MarkupInventory()
    editor = scoremanager.iotools.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add'
    input_ += r' arg \italic~{~serenamente~possibile~}'
    input_ += ' direction up done'
    input_ += r' add arg \italic~{~presto~} done done'
    editor._run(pending_user_input=input_)

    inventory = markuptools.MarkupInventory([
        markuptools.Markup(
            '\\italic { serenamente possibile }',
            direction='^',
            ),
        markuptools.Markup(
            '\\italic { presto }',
            )
        ],
        )

    assert editor.target == inventory


def test_ListEditor__run_06():
    r'''Edits empty tempo inventory.

    Works with duration pairs.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.TempoInventory()
    editor = scoremanager.iotools.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add d (1, 4) units 60 done'
    input_ +=  ' add d (1, 4) units 72 done'
    input_ += ' add d (1, 4) units 84 done done'
    editor._run(pending_user_input=input_)
    inventory = indicatortools.TempoInventory([
        Tempo(Duration(1, 4), 60),
        Tempo(Duration(1, 4), 72),
        Tempo(Duration(1, 4), 84),
        ])
    assert editor.target == inventory


def test_ListEditor__run_07():
    r'''Edits empty tempo inventory.

    Works with durations.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.TempoInventory()
    editor = scoremanager.iotools.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add d Duration(1, 4) units 60 done'
    input_ += ' add d Duration(1, 4) units 72 done'
    input_ += ' add d Duration(1, 4) units 84 done done'
    editor._run(pending_user_input=input_)
    inventory = indicatortools.TempoInventory([
        Tempo(Duration(1, 4), 60),
        Tempo(Duration(1, 4), 72),
        Tempo(Duration(1, 4), 84),
        ])
    assert editor.target == inventory


def test_ListEditor__run_08():
    r'''Edits empty pitch range inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = pitchtools.PitchRangeInventory()
    editor = scoremanager.iotools.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add range [C0, C6] done'
    input_ += ' add range [C1, C7] done'
    input_ += ' add range [C2, C8] done'
    input_ += ' rm 1 mv 1 2 q'
    editor._run(pending_user_input=input_)
    assert editor.target == pitchtools.PitchRangeInventory([
        pitchtools.PitchRange('[C2, C8]'),
        pitchtools.PitchRange('[C1, C7]'),
        ])


def test_ListEditor__run_09():
    r'''Edits empty octave transposition mapping.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = pitchtools.OctaveTranspositionMapping()
    editor = scoremanager.iotools.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add source [A0, F#4] target 22 done'
    input_ += ' add source (F#4, C8] target 26 done done done'
    editor._run(pending_user_input=input_)

    mapping = pitchtools.OctaveTranspositionMapping([
        ('[A0, F#4]', 22),
        ('(F#4, C8]', 26),
        ])
    assert editor.target == mapping


def test_ListEditor__run_10():
    r'''Edits empty octave transposition mapping.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = pitchtools.OctaveTranspositionMapping()
    editor = scoremanager.iotools.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add source [A0, F#4] target 22 done'
    input_ +=  ' add source (F#4, C8] target 26 done done done'
    editor._run(pending_user_input=input_)

    mapping = pitchtools.OctaveTranspositionMapping(
            [('[A0, F#4]', 22), ('(F#4, C8]', 26)],
            )

    assert editor.target == mapping


def test_ListEditor__run_11():
    r'''Edits instrument inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.InstrumentInventory()
    editor = scoremanager.iotools.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add flute add piccolo done'
    editor._run(pending_user_input=input_)

    inventory = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Piccolo(),
        ])

    assert editor.target == inventory