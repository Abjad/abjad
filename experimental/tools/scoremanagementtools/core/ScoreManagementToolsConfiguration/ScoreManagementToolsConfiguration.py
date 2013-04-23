import os
from abjad.tools.configurationtools.Configuration import Configuration


class ScoreManagementToolsConfiguration(Configuration):
    '''Score management tools configuration.
    '''

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        return []

    @property
    def _option_definitions(self):
        return []

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def CONFIG_DIRECTORY_PATH(self):
        return os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH')

    @property
    def CONFIG_FILE_NAME(self):
        return 'config.py'

    @property
    def boilerplate_directory_name(self):
        return os.path.join(self.score_management_tools_package_path_name, 'boilerplate')

    @property
    def score_management_tools_package_path_name(self):
        return os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH')
