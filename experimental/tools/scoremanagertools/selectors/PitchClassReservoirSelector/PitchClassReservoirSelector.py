from experimental.tools.scoremanagertools.selectors.MaterialPackageSelector import MaterialPackageSelector


class PitchClassReservoirSelector(MaterialPackageSelector):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'pitch class reservoir'
    tags_to_match = ('is_numeric_sequence', )
    space_delimited_lowercase_target_name = 'pitch class reservoir'
