# -*- encoding: utf-8 -*-
import os
from abjad import *
from abjad.tools import handlertools
import scoremanager


def test_Performer_autoedit_01():
    r'''Adds instruments to performer instrument inventory.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Performer()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'nm flutist i add flute add piccolo done done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    instruments = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Piccolo(),
        ])
    performer = instrumenttools.Performer(
        name='flutist',
        instruments=instruments,
        )

    assert autoeditor.target == performer


def test_Performer_autoedit_02():
    r'''Removes instruments from performer instrument inventory.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Performer()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'nm flutist i add flute add piccolo rm piccolo done done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    instruments = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        ])
    performer = instrumenttools.Performer(
        name='flutist',
        instruments=instruments,
        )

    assert autoeditor.target == performer


def test_Performer_autoedit_03():
    r'''Moves instruments in performer instrument inventory.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = instrumenttools.Performer()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'nm flutist i add flute add piccolo mv 1 2 done done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    instruments = instrumenttools.InstrumentInventory([
        instrumenttools.Piccolo(),
        instrumenttools.Flute(),
        ])
    performer = instrumenttools.Performer(
        name='flutist',
        instruments=instruments,
        )

    assert autoeditor.target == performer