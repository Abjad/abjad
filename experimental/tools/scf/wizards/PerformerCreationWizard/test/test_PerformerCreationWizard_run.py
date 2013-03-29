from abjad import *
import scf


def test_PerformerCreationWizard_run_01():

    wizard = scf.wizards.PerformerCreationWizard()
    assert wizard.run(user_input='q') is None

    wizard = scf.wizards.PerformerCreationWizard()
    assert wizard.run(user_input='b') is None

    wizard = scf.wizards.PerformerCreationWizard()
    assert wizard.run(user_input='studio') is None


def test_PerformerCreationWizard_run_02():

    wizard = scf.wizards.PerformerCreationWizard()
    assert wizard.run(user_input='vn default') == scoretools.Performer(
        name='violinist', instruments=[instrumenttools.Violin()])


def test_PerformerCreationWizard_run_03():
    '''Ranged.
    '''

    wizard = scf.wizards.PerformerCreationWizard(is_ranged=True)
    assert wizard.run(user_input='vn, va default default') == [
        scoretools.Performer(name='violinist', instruments=[instrumenttools.Violin()]),
        scoretools.Performer(name='violist', instruments=[instrumenttools.Viola()])]


def test_PerformerCreationWizard_run_04():
    '''Skipping instruments.
    '''

    wizard = scf.wizards.PerformerCreationWizard(is_ranged=True)
    assert wizard.run(user_input='vn, va skip skip') == [
        scoretools.Performer(name='violinist'),
        scoretools.Performer(name='violist')]


def test_PerformerCreationWizard_run_05():
    '''More instruments.
    '''

    wizard = scf.wizards.PerformerCreationWizard(is_ranged=True)
    assert wizard.run(user_input='vn, va skip more xyl') == [
        scoretools.Performer(name='violinist'),
        scoretools.Performer(name='violist', instruments=[instrumenttools.Xylophone()])]


def test_PerformerCreationWizard_run_06():
    '''Auxiliary percussion.
    '''

    wizard = scf.wizards.PerformerCreationWizard(is_ranged=True)
    caxixi = instrumenttools.UntunedPercussion(instrument_name='caxixi', short_instrument_name='caxixi')
    wizard.run(user_input='vn more untuned cax')
    assert wizard.target == [scoretools.Performer(name='violinist', instruments=[caxixi])]
