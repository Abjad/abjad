# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_CollectionAutoeditor__run_01():
    r'''Edits built-in list.
    '''

    session = scoremanager.core.Session(is_test=True)
    autoeditor = scoremanager.iotools.CollectionAutoeditor(session=session)
    input_ = "17 99 'foo' done q"
    autoeditor._is_autoadding = True
    autoeditor._run(input_=input_)

    assert autoeditor.target == [17, 99, 'foo']


def test_CollectionAutoeditor__run_02():
    r'''Edits empty clef inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.ClefInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add nm treble done add nm bass done done'
    autoeditor._run(input_=input_)

    inventory = indicatortools.ClefInventory(['treble', 'bass'])
    assert autoeditor.target == inventory


def test_CollectionAutoeditor__run_03():
    r'''Edits nonempty clef inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.ClefInventory(['treble', 'bass'])
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = '2 nm alto done done'
    autoeditor._run(input_=input_)

    new_inventory = indicatortools.ClefInventory(['treble', 'alto'])
    assert autoeditor.target == new_inventory


def test_CollectionAutoeditor__run_04():
    r'''Edits empty markup inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = markuptools.MarkupInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = r'add arg \italic~{~serenamente~possibile~} done done'
    autoeditor._run(input_=input_)

    inventory = markuptools.MarkupInventory([
        markuptools.Markup(
            '\\italic { serenamente possibile }',
            )
        ])

    assert autoeditor.target == inventory


def test_CollectionAutoeditor__run_05():
    r'''Edits nonempty markup inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = markuptools.MarkupInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add'
    input_ += r' arg \italic~{~serenamente~possibile~}'
    input_ += ' direction up done'
    input_ += r' add arg \italic~{~presto~} done done'
    autoeditor._run(input_=input_)

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

    assert autoeditor.target == inventory


def test_CollectionAutoeditor__run_06():
    r'''Edits empty tempo inventory.

    Works with duration pairs.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.TempoInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add ((1, 4), 60)'
    input_ +=  ' add (Duration(1, 4), 72)'
    input_ += ' add ((1, 4), 84) done'
    autoeditor._run(input_=input_)
    inventory = indicatortools.TempoInventory([
        Tempo(Duration(1, 4), 60),
        Tempo(Duration(1, 4), 72),
        Tempo(Duration(1, 4), 84),
        ])
    assert autoeditor.target == inventory


def test_CollectionAutoeditor__run_07():
    r'''Edits empty tempo inventory.

    Works with durations.
    '''
    pytest.skip('make me work again.')

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.TempoInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add (Duration(1, 4), 60)'
    input_ += ' add (Duration(1, 4), 72)'
    input_ += ' add (Duration(1, 4), 84) done'
    autoeditor._run(input_=input_)
    inventory = indicatortools.TempoInventory([
        Tempo(Duration(1, 4), 60),
        Tempo(Duration(1, 4), 72),
        Tempo(Duration(1, 4), 84),
        ])
    assert autoeditor.target == inventory


def test_CollectionAutoeditor__run_08():
    r'''Edits empty pitch range inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = pitchtools.PitchRangeInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add [C0, C6]'
    input_ += ' add [C1, C7]'
    input_ += ' add [C2, C8]'
    input_ += ' rm 1 mv 1 2 q'
    autoeditor._run(input_=input_)
    assert autoeditor.target == pitchtools.PitchRangeInventory([
        pitchtools.PitchRange('[C2, C8]'),
        pitchtools.PitchRange('[C1, C7]'),
        ])


def test_CollectionAutoeditor__run_09():
    r'''Edits empty octave transposition mapping.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = pitchtools.OctaveTranspositionMapping()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = "add ('[A0, F#4]', 22)"
    input_ += " add ('(F#4, C8]', 26) done"
    autoeditor._run(input_=input_)

    mapping = pitchtools.OctaveTranspositionMapping([
        ('[A0, F#4]', 22),
        ('(F#4, C8]', 26),
        ])
    assert autoeditor.target == mapping


def test_CollectionAutoeditor__run_10():
    r'''Edits empty octave transposition mapping.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = pitchtools.OctaveTranspositionMapping()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = "add ('[A0, F#4]', 22)"
    input_ +=  " add ('(F#4, C8]', 26) done"
    autoeditor._run(input_=input_)

    mapping = pitchtools.OctaveTranspositionMapping(
            [('[A0, F#4]', 22), ('(F#4, C8]', 26)],
            )

    assert autoeditor.target == mapping


def test_CollectionAutoeditor__run_11():
    r'''Edits instrument inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.InstrumentInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add flute add piccolo done'
    autoeditor._run(input_=input_)

    inventory = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Piccolo(),
        ])

    assert autoeditor.target == inventory


def test_CollectionAutoeditor__run_12():
    r'''Edits view.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = scoremanager.iotools.View()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'add first~pattern <return> add second~pattern <return> done'
    autoeditor._run(input_=input_)

    view = scoremanager.iotools.View([
        'first pattern',
        'second pattern',
        ])

    assert autoeditor.target == view


def test_CollectionAutoeditor__run_13():

    input_ = 'red~example~score m instrumentation ae q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - instrumentation (AE)',
        'Red Example Score (2013) - materials - instrumentation (EDIT)',
        ]
    assert score_manager._transcript.titles == titles