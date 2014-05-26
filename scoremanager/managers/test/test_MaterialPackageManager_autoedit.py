# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
from experimental import *
import scoremanager


def test_MaterialPackageManager_autoedit_01():
    '''Edit menu has correct header.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'm example~markup~inventory ae q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Score Manager - materials -'
    string += ' example markup inventory (Abjad) - markup inventory'
    assert string in contents


def test_MaterialPackageManager_autoedit_02():
    r'''Edits tempo inventory.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testtempoinventory',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]
    inventory = indicatortools.TempoInventory([
        ((1, 4), 60),
        ((1, 4), 90),
        ])

    assert not os.path.exists(path)

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new testtempoinventory aes TempoInventory <return>'
        input_ += ' ae add ((1, 4), 60) add ((1, 4), 90) done'
        input_ += ' done y <return> q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == inventory
        input_ = 'm rm testtempoinventory remove q'
        score_manager._run(input_=input_)


def test_MaterialPackageManager_autoedit_03():
    r'''Edits empty pitch range inventory.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testpri',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]
    inventory = pitchtools.PitchRangeInventory()

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new testpri'
        input_ += ' aes PitchRangeInventory <return> done y <return> q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == inventory
        input_ = 'm rm testpri remove q'
        score_manager._run(input_=input_)


def test_MaterialPackageManager_autoedit_04():
    r'''Edits populated pitch range inventory.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testpri',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]
    inventory = pitchtools.PitchRangeInventory([
        pitchtools.PitchRange('[C2, G5]'),
        pitchtools.PitchRange('[C2, F#5]'),
        ])
    input_ = 'm new testpri aes PitchRangeInventory <return>'
    input_ += ' ae add range [A0, C8] done'
    input_ += ' add range [C2, F#5] done'
    input_ += ' add range [C2, G5] done'
    input_ += ' rm 1 mv 1 2 b y <return> q'

    with systemtools.FilesystemState(remove=[path]):
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == inventory
        input_ = 'm rm testpri remove q'
        score_manager._run(input_=input_)


def test_MaterialPackageManager_autoedit_05():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testmarkupinventory',
        )
    inventory = markuptools.MarkupInventory(
        [
            markuptools.Markup(
                '\\italic { serenamente }',
                ),
            markuptools.Markup(
                '\\italic { presto }',
                )
            ],
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = "m new testmarkupinventory aes markup <return>"
        input_ += " ae add arg r'\\italic~{~serenamente~}' done"
        input_ += " add arg r'\\italic~{~presto~}' done done y <return> q"
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == inventory
        input_ = 'm rm testmarkupinventory remove q'
        score_manager._run(input_=input_)


def test_MaterialPackageManager_autoedit_06():
    r'''Edits empty octave transposition mapping inventory.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testoctavetrans',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]
    inventory = pitchtools.OctaveTranspositionMappingInventory()

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new testoctavetrans'
        input_ += ' aes OctaveTranspositionMappingInventory <return>'
        input_ += ' done y <return> q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == inventory
        input_ = 'm rm testoctavetrans remove q'
        score_manager._run(input_=input_)


def test_MaterialPackageManager_autoedit_07():
    r'''Edits populated octave transposition mapping inventory.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testoctavetrans',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]
    mapping_1 = pitchtools.OctaveTranspositionMapping([
        ('[A0, C4)', 15),
        ('[C4, C8)', 27),
        ])
    mapping_2 = pitchtools.OctaveTranspositionMapping([
        ('[A0, C8]', -18),
        ])
    inventory = pitchtools.OctaveTranspositionMappingInventory([
        mapping_1,
        mapping_2
        ])

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new testoctavetrans'
        input_ += ' aes OctaveTranspositionMappingInventory <return>'
        input_ += " ae add add ('[A0, C4)', 15)"
        input_ += " add ('[C4, C8)', 27) done"
        input_ += " add add ('[A0, C8]', -18)"
        input_ += ' done done y <return> q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == inventory
        input_ = 'm rm testoctavetrans remove q'
        score_manager._run(input_=input_)


def test_MaterialPackageManager_autoedit_08():
    pytest.skip('make autoadding work again.')

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testlist',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new testlist aes list <return> ae 17 foo done b <return> q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == [17, 'foo']
        input_ = 'm rm testlist remove q'
        score_manager._run(input_=input_)


def test_MaterialPackageManager_autoedit_09():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testlist',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new testlist aes list <return>'
        input_ += ' ae add 17 add foo done y <return> q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == [17, 'foo']
        input_ = 'm rm testlist remove q'
        score_manager._run(input_=input_)


def test_MaterialPackageManager_autoedit_10():
    r'''Edits talea rhythm-maker.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testrhythmmaker',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]
    talea = rhythmmakertools.Talea(
        counts=(-1, 2, -3, 4),
        denominator=16,
        )
    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        split_divisions_by_counts=(6,),
        extra_counts_per_division=(2, 3),
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new testrhythmmaker aes TaleaRhythmMaker <return>'
        input_ += ' ae talea counts (-1, 2, -3, 4) denominator 16 done'
        input_ += ' split (6,)'
        input_ += ' extra (2, 3)'
        input_ += ' done y <return> q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == maker
        input_ = 'm rm testrhythmmaker remove q'
        score_manager._run(input_=input_)


def test_MaterialPackageManager_autoedit_11():
    r'''Edits retierated articulation handler.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testarticulationhandler',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]
    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['^', '.'],
        minimum_duration=Duration(1, 64),
        maximum_duration=Duration(1, 4),
        minimum_written_pitch=NamedPitch('c'),
        maximum_written_pitch=NamedPitch("c''''"),
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = "m new testarticulationhandler"
        input_ += " aes ReiteratedArticulationHandler <return>"
        input_ += " ae al ['^', '.'] nd (1, 64) xd (1, 4) np c xp c''''"
        input_ += " done y <return> q"
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == handler
        input_ = 'm rm testarticulationhandler remove q'
        score_manager._run(input_=input_)


def test_MaterialPackageManager_autoedit_12():
    r'''Edits dynamic handler.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'testdynamichandler',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        ]
    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 16),
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new testdynamichandler'
        input_ += ' aes ReiteratedDynamicHandler <return>'
        input_ += ' ae dy f md (1, 16) done y <return> q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == handler
        input_ = 'm rm testdynamichandler remove q'
        score_manager._run(input_=input_)