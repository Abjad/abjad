# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.selectors.MaterialPackageSelector \
    import MaterialPackageSelector


class PitchClassReservoirSelector(MaterialPackageSelector):

    ### CLASS VARIABLES ###

    generic_output_name = 'pitch class reservoir'

    tags_to_match = ('is_numeric_sequence', )

    space_delimited_lowercase_target_name = 'pitch class reservoir'
