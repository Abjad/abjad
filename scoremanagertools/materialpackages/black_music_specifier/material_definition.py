# -*- encoding: utf-8 -*-
from abjad import *
from scoremanagertools import specifiers
output_material_module_import_statements = [
    'from abjad import *',
    'from scoremanagertools import specifiers',
    ]


black_music_specifier = specifiers.MusicSpecifier([
    specifiers.MusicContributionSpecifier(
        [specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())],
        custom_identifier='black violin pizzicati',
        description='lower register violin pizzicati'
        ),
    specifiers.MusicContributionSpecifier(
        [specifiers.InstrumentSpecifier(instrument=instrumenttools.Cello())],
        custom_identifier='black cello pizzicati',
        description='midrange cello pizzicati',
        )
    ],
    custom_identifier='black music'
    )
