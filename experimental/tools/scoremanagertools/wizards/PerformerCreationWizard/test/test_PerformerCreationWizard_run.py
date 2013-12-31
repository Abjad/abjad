# -*- encoding: utf-8 -*-
from experimental import *


def test_PerformerCreationWizard_run_01():

    wizard = scoremanagertools.wizards.PerformerCreationWizard()
    assert wizard._run(pending_user_input='q') is None

    wizard = scoremanagertools.wizards.PerformerCreationWizard()
    assert wizard._run(pending_user_input='b') is None

    wizard = scoremanagertools.wizards.PerformerCreationWizard()
    assert wizard._run(pending_user_input='home') is None


def test_PerformerCreationWizard_run_02():

    wizard = scoremanagertools.wizards.PerformerCreationWizard()
    assert wizard._run(pending_user_input='vn default') == \
        instrumenttools.Performer(
            name='violinist', 
            instruments=[instrumenttools.Violin()],
            )


def test_PerformerCreationWizard_run_03():
    r'''Ranged.
    '''

    wizard = scoremanagertools.wizards.PerformerCreationWizard(is_ranged=True)
    assert wizard._run(pending_user_input='vn, va default default') == [
        instrumenttools.Performer(name='violinist', instruments=[instrumenttools.Violin()]),
        instrumenttools.Performer(name='violist', instruments=[instrumenttools.Viola()])]


def test_PerformerCreationWizard_run_04():
    r'''Skipping instruments.
    '''

    wizard = scoremanagertools.wizards.PerformerCreationWizard(is_ranged=True)
    assert wizard._run(pending_user_input='vn, va skip skip') == [
        instrumenttools.Performer(name='violinist'),
        instrumenttools.Performer(name='violist')]


def test_PerformerCreationWizard_run_05():
    r'''More instruments.
    '''

    wizard = scoremanagertools.wizards.PerformerCreationWizard(is_ranged=True)
    assert wizard._run(pending_user_input='vn, va skip more xyl') == [
        instrumenttools.Performer(name='violinist'),
        instrumenttools.Performer(name='violist', instruments=[instrumenttools.Xylophone()])]


def test_PerformerCreationWizard_run_06():
    r'''Auxiliary percussion.
    '''

    wizard = scoremanagertools.wizards.PerformerCreationWizard(is_ranged=True)
    caxixi = instrumenttools.UntunedPercussion(instrument_name='caxixi', short_instrument_name='caxixi')
    wizard._run(pending_user_input='vn more untuned cax')
    assert wizard.target == [instrumenttools.Performer(name='violinist', instruments=[caxixi])]
