from experimental.tools.scoremanagertools.selectors.HandlerClassNameSelector import HandlerClassNameSelector
import os
from abjad import ABJCFG


class RhythmMakerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_importable_names = ['abjad.tools.rhythmmakertools']
    asset_container_path_names = [os.path.join(ABJCFG.ABJAD_DIRECTORY_PATH, 'tools', 'rhythmmakertools')]
    target_human_readable_name = 'time-token maker class name'
