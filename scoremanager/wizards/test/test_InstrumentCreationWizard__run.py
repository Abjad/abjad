# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentCreationWizard__run_01():

    wizard = scoremanager.wizards.InstrumentCreationWizard()
    input_ = 'violin'
    wizard._run(pending_user_input=input_, is_test=True)
    assert wizard.target == instrumenttools.Violin()


def test_InstrumentCreationWizard__run_02():

    wizard = scoremanager.wizards.InstrumentCreationWizard()
    input_ = 'untuned vibraslap'
    wizard._run(pending_user_input=input_, is_test=True)
    vibraslap = instrumenttools.UntunedPercussion(
        instrument_name='vibraslap',
        short_instrument_name='vibraslap',
        )
    assert wizard.target == vibraslap


def test_InstrumentCreationWizard__run_03():

    wizard = scoremanager.wizards.InstrumentCreationWizard(is_ranged=True)
    input_ = 'violin, viola'
    wizard._run(pending_user_input=input_, is_test=True)
    instruments = [instrumenttools.Violin(), instrumenttools.Viola()]
    assert wizard.target == instruments


def test_InstrumentCreationWizard__run_04():

    wizard = scoremanager.wizards.InstrumentCreationWizard(is_ranged=True)
    input_ = 'violin, viola, untuned vibraslap'
    wizard._run(pending_user_input=input_, is_test=True)
    instruments = [
        instrumenttools.Violin(),
        instrumenttools.Viola(),
        instrumenttools.UntunedPercussion(
            instrument_name='vibraslap',
            short_instrument_name='vibraslap',
            ),
        ]
    assert wizard.target == instruments
