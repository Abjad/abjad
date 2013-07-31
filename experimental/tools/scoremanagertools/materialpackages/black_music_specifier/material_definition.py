# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools.scoremanagertools import specifiers
output_material_module_import_statements = [
    'from abjad import *',
    'from experimental.tools.scoremanagertools import specifiers',
    ]


black_music_specifier = specifiers.MusicSpecifier([
    specifiers.MusicContributionSpecifier(
        [specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())],
        name='black violin pizzicati',
        description='lower register violin pizzicati'
        ),
    specifiers.MusicContributionSpecifier(
        [specifiers.InstrumentSpecifier(instrument=instrumenttools.Cello())],
        name='black cello pizzicati',
        description='midrange cello pizzicati',
        )
    ],
    name='black music'
    )
