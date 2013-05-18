from experimental.tools.scoremanagertools.selectors.HandlerClassNameSelector import HandlerClassNameSelector
import os
from abjad import ABJCFG


class RhythmMakerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    storehouse_package_paths = ['abjad.tools.rhythmmakertools']
    storehouse_filesystem_paths = [os.path.join(ABJCFG.abjad_directory_path, 'tools', 'rhythmmakertools')]
    space_delimited_lowercase_target_name = 'time-token maker class name'
