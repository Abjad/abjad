from abjad.tools import instrumenttools
from experimental import *


def test_InstrumentCreationWizard_run_01():

    wizard = scoremanagertools.wizards.InstrumentCreationWizard()
    wizard._run(pending_user_input='violin')
    assert wizard.target == instrumenttools.Violin()


def test_InstrumentCreationWizard_run_02():

    wizard = scoremanagertools.wizards.InstrumentCreationWizard()
    wizard._run(pending_user_input='untuned vibraslap')
    vibraslap = instrumenttools.UntunedPercussion(
        instrument_name='vibraslap',
        short_instrument_name='vibraslap')
    assert wizard.target == vibraslap


def test_InstrumentCreationWizard_run_03():

    wizard = scoremanagertools.wizards.InstrumentCreationWizard(is_ranged=True)
    wizard._run(pending_user_input='violin, viola')
    instruments = [instrumenttools.Violin(), instrumenttools.Viola()]
    assert wizard.target == instruments


def test_InstrumentCreationWizard_run_04():

    wizard = scoremanagertools.wizards.InstrumentCreationWizard(is_ranged=True)
    wizard._run(pending_user_input='violin, viola, untuned vibraslap')
    instruments = [
        instrumenttools.Violin(),
        instrumenttools.Viola(),
        instrumenttools.UntunedPercussion(
            instrument_name='vibraslap',
            short_instrument_name='vibraslap'),
        ]
    assert wizard.target == instruments
