# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_Autoeditor_set_attributes_to_none_01():

    material_package_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'test_rhythm_maker',
        )

    with systemtools.FilesystemState(remove=[material_package_path]):
        input_ = 'red~example~score m new test~rhythm~maker y'
        input_ += ' oaes TaleaRhythmMaker'
        input_ += ' oae t c (1, 2, 3, 4) done bs done done y'
        input_ += ' m test~rhythm~maker q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        lines = [
            '* talea: Talea(counts=(1, 2, 3, 4), denominator=16)',
            '* split divisions by counts: None',
            '* extra counts per division: None',
            '* beam specifier: BeamSpecifier(beam_each_division=True, beam_divisions_together=False)',
            '* burnish specifier: None',
            '* duration spelling specifier: None',
            '* tie specifier: None',
            ]
        for line in lines:
            assert line in contents
        input_ = 'red~example~score m test~rhythm~maker'
        input_ += ' oae none bs done y'
        input_ += ' m test~rhythm~maker q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        lines = [
            '* talea: Talea(counts=(1, 2, 3, 4), denominator=16)',
            '* split divisions by counts: None',
            '* extra counts per division: None',
            '* beam specifier: None',
            '* burnish specifier: None',
            '* duration spelling specifier: None',
            '* tie specifier: None',
            ]
        for line in lines:
            assert line in contents