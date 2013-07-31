# -*- encoding: utf-8 -*-
import os
from abjad import abjad_configuration
from experimental.tools.scoremanagertools.selectors.HandlerClassNameSelector \
    import HandlerClassNameSelector


class RhythmMakerClassNameSelector(HandlerClassNameSelector):

    ### CLASS VARIABLES ###

    storehouse_package_paths = ['abjad.tools.rhythmmakertools']

    storehouse_filesystem_paths = [
        os.path.join(
            abjad_configuration.abjad_directory_path, 
            'tools', 
            'rhythmmakertools',
            )]

    space_delimited_lowercase_target_name = 'time-menu_entry maker class name'
