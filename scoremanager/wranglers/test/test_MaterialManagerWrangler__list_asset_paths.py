# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MaterialManagerWrangler__list_asset_paths_01():

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.MaterialManagerWrangler(session=session)

    file_names = [
        'ArticulationHandlerMaterialManager.py',
        'DynamicHandlerMaterialManager.py',
        'ListMaterialManager.py',
        'MarkupInventoryMaterialManager.py',
        'OctaveTranspositionMappingInventoryMaterialManager.py',
        'PitchRangeInventoryMaterialManager.py',
        'RhythmMakerMaterialManager.py',
        'SargassoMeasureMaterialManager.py',
        'TempoInventoryMaterialManager.py',
        ]
    paths = []
    for file_name in file_names:
        path = os.path.join(
            wrangler._configuration.abjad_material_managers_directory_path,
            file_name,
            )
        paths.append(path)

    result = wrangler._list_asset_paths(
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths
