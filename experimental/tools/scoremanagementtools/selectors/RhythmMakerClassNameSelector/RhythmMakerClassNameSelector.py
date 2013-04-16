from experimental.tools.scoremanagementtools.selectors.HandlerClassNameSelector import HandlerClassNameSelector
import os


class RhythmMakerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_importable_names = ['abjad.tools.rhythmmakertools']
    asset_container_path_names = [os.path.join(os.environ.get('ABJAD'), 'tools', 'rhythmmakertools')]
    target_human_readable_name = 'time-token maker class name'
