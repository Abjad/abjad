# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.core.Session()
inventory = instrumenttools.InstrumentInventory()
class_ = inventory._make_wizard()


def test_InstrumentCreationWizard__run_01():

    #wizard = scoremanager.wizards.InstrumentCreationWizard(session=session)
    wizard = class_(session=session)
    input_ = 'violin'
    wizard._run(input_=input_)
    assert wizard.target == instrumenttools.Violin()


def test_InstrumentCreationWizard__run_02():

    #wizard = scoremanager.wizards.InstrumentCreationWizard(session=session)
    wizard = class_(session=session)
    input_ = 'untuned vibraslap'
    wizard._run(input_=input_)
    vibraslap = instrumenttools.UntunedPercussion(
        instrument_name='vibraslap',
        short_instrument_name='vibraslap',
        )
    assert wizard.target == vibraslap


def test_InstrumentCreationWizard__run_03():

    #wizard = scoremanager.wizards.InstrumentCreationWizard(
    #    is_ranged=True,
    #    session=session,
    #    )
    wizard = class_(is_ranged=True, session=session)
    input_ = 'violin, viola'
    wizard._run(input_=input_)
    instruments = [instrumenttools.Violin(), instrumenttools.Viola()]
    assert wizard.target == instruments


def test_InstrumentCreationWizard__run_04():

    #wizard = scoremanager.wizards.InstrumentCreationWizard(
    #    is_ranged=True,
    #    session=session,
    #    )
    wizard = class_(is_ranged=True, session=session)
    input_ = 'violin, viola, untuned vibraslap'
    wizard._run(input_=input_)
    instruments = [
        instrumenttools.Violin(),
        instrumenttools.Viola(),
        instrumenttools.UntunedPercussion(
            instrument_name='vibraslap',
            short_instrument_name='vibraslap',
            ),
        ]
    assert wizard.target == instruments