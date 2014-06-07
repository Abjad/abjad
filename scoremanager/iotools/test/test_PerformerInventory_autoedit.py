# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools import handlertools
import scoremanager


def test_PerformerInventory_autoedit_01():
    r'''Adds three performers to instrumentation specifier.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.PerformerInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'ps add accordionist <return> add bassoonist <return>'
    input_ += ' add cellist <return> done done'
    autoeditor._run(input_=input_)

    specifier = instrumenttools.PerformerInventory([
        instrumenttools.Performer(
            name='accordionist',
            instruments=[instrumenttools.Accordion()],
            ),
        instrumenttools.Performer(
            name='bassoonist',
            instruments=[instrumenttools.Bassoon()],
            ),
        instrumenttools.Performer(
            name='cellist',
            instruments=[instrumenttools.Cello()],
            )])

    assert autoeditor.target == specifier


def test_PerformerInventory_autoedit_02():
    r'''Adds three performers to instrumentation specifier.

    Tests range handling.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.PerformerInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'ps add 1-3 <return> <return> <return> done done'
    autoeditor._run(input_=input_)

    specifier = instrumenttools.PerformerInventory([
        instrumenttools.Performer(
            name='accordionist',
            instruments=[instrumenttools.Accordion()]),
        instrumenttools.Performer(
            name='alto',
            instruments=[instrumenttools.AltoVoice()]),
        instrumenttools.Performer(
            name='baritone',
            instruments=[instrumenttools.BaritoneVoice()]),
            ])

    assert autoeditor.target == specifier


def test_PerformerInventory_autoedit_03():
    r'''Edits instrumentation specifier. Adds three performers. Removes two.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.PerformerInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'ps add acc <return> add bass <return> add bassoon <return>'
    input_ += ' rm 3 rm 2 done done'
    autoeditor._run(input_=input_)

    specifier = instrumenttools.PerformerInventory(
        [
            instrumenttools.Performer(
                'accordionist',
                instruments=[instrumenttools.Accordion()],
                ),
            ]
        )

    assert autoeditor.target == specifier


def test_PerformerInventory_autoedit_04():
    r'''Edits instrumentation specifier. Adds and removes.

    Tests range handling.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.PerformerInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'ps add 1-3 <return> <return> <return> rm 3-2 done done'
    autoeditor._run(input_=input_)

    specifier = instrumenttools.PerformerInventory(
        [
            instrumenttools.Performer(
                'accordionist',
                instruments=[instrumenttools.Accordion()],
                )
            ]
        )

    assert autoeditor.target == specifier


def test_PerformerInventory_autoedit_05():
    r'''Edits instrumentation specifier. Adds three performers.
    Makes two moves.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = instrumenttools.PerformerInventory()
    autoeditor = scoremanager.iotools.CollectionAutoeditor(
        session=session,
        target=target,
        )
    input_ = 'ps add accordionist <return> add bassist <return>'
    input_ += ' add bassoonist bassoon mv 1 2 mv 2 3 done done'
    autoeditor._run(input_=input_)

    specifier = instrumenttools.PerformerInventory([
        instrumenttools.Performer(
            name='bassist',
            instruments=[instrumenttools.Contrabass()],
            ),
        instrumenttools.Performer(
            name='bassoonist',
            instruments=[instrumenttools.Bassoon()],
            ),
        instrumenttools.Performer(
            name='accordionist',
            instruments=[instrumenttools.Accordion()],
            ),
        ])

    assert autoeditor.target == specifier