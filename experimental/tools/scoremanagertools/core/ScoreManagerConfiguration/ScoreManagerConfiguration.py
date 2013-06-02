import os
from abjad.tools.configurationtools.Configuration import Configuration
from abjad.tools.configurationtools.AbjadConfiguration import AbjadConfiguration


class ScoreManagerConfiguration(Configuration):
    '''Score manager configuration.

        >>> configuration = scoremanagertools.core.ScoreManagerConfiguration()
        >>> configuration
        ScoreManagerConfiguration()

    Return score manager configuration.
    '''

    ### CLASS VARIABLES ###

    abjad_configuration = AbjadConfiguration()

    ### INITIALIZER ###

    def __init__(self):
        Configuration.__init__(self)

        # score manager tools

        self.score_manager_tools_directory_path = os.path.join(
            self.abjad_configuration.abjad_experimental_directory_path,
            'tools',
            'scoremanagertools',
            )
        self.score_manager_tools_package_path = '.'.join([
            'experimental',
            'tools',
            'scoremanagertools',
            ])

        # built-in asset library directory paths

        self.built_in_editors_directory_path = os.path.join(
            self.score_manager_tools_directory_path, 
            'editors',
            )
        self.built_in_material_package_makers_directory_path = os.path.join(
            self.score_manager_tools_directory_path, 
            'materialpackagemakers',
            )
        self.built_in_material_packages_directory_path = os.path.join(
            self.score_manager_tools_directory_path, 
            'materialpackages',
            )
        self.built_in_specifiers_directory_path = os.path.join(
            self.score_manager_tools_directory_path, 
            'specifiers',
            )
        self.built_in_stylesheets_directory_path = os.path.join(
            self.score_manager_tools_directory_path, 
            'stylesheets',
            )

        # built-in asset library package paths

        self.built_in_editors_package_path = '.'.join([
            self.score_manager_tools_package_path,
            'editors',
            ])
        self.built_in_material_package_makers_package_path = '.'.join([
            self.score_manager_tools_package_path, 
            'materialpackagemakers',
            ])
        self.built_in_material_packages_package_path = '.'.join([
            self.score_manager_tools_package_path, 
            'materialpackages',
            ])
        self.built_in_specifiers_package_path = '.'.join([
            self.score_manager_tools_package_path,
            'specifiers',
            ])

        # user asset library directory paths

        self.user_asset_library_directory_path = \
            os.path.normpath(os.path.expanduser(
            self._settings['user_asset_library_directory_path']
            ))
        self.user_external_editors_directory_path = os.path.join(
            self.user_asset_library_directory_path, 
            'editors',
            )
        self.user_external_material_package_makers_directory_path = os.path.join(
            self.user_asset_library_directory_path,
            'material_package_makers',
            )
        self.user_external_material_packages_directory_path = os.path.join(
            self.user_asset_library_directory_path, 
            'material_packages',
            )
        self.user_external_specifiers_directory_path = os.path.join(
            self.user_asset_library_directory_path, 
            'specifiers',
            )
        self.user_external_stylesheets_directory_path = os.path.join(
            self.user_asset_library_directory_path,
            'stylesheets',
            )

        # user asset library package paths

        self.user_asset_library_package_path = 'score_manager_asset_library'
        self.user_external_editors_package_path = '.'.join([
            self.user_asset_library_package_path, 
            'editors',
            ])
        self.user_external_material_package_makers_package_path = '.'.join([
            self.user_asset_library_package_path,
            'material_package_makers',
            ])
        self.user_external_material_packages_package_path = '.'.join([
            self.user_asset_library_package_path, 
            'material_packages',
            ])
        self.user_external_specifiers_package_path = '.'.join([
            self.user_asset_library_package_path, 
            'specifiers',
            ])

        # built-in score packages

        self.built_in_score_packages_directory_path = os.path.join(
            self.score_manager_tools_directory_path, 
            'scorepackages',
            )
        self.built_in_score_packages_package_path = '.'.join([
            self.score_manager_tools_package_path,
            'scorepackages',
            ])

        # user score packages

        self.user_score_packages_directory_path = \
            os.path.normpath(os.path.expanduser(
            self._settings['user_score_packages_directory_path']
            ))
        self.user_score_packages_package_path = ''

        # transcripts directory path

        self.transcripts_directory_path = os.path.join(
            self.configuration_directory_path,
            'transcripts',
            )

        # make missing packages

        for directory_path in (
            self.user_asset_library_directory_path,
            self.user_external_editors_directory_path,
            self.user_external_material_package_makers_directory_path,
            self.user_external_material_packages_directory_path,
            self.user_external_specifiers_directory_path):
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                file_path = os.path.join(directory_path, '__init__.py')
                file(file_path, 'w').write('')

        # make missing directories 

        if not os.path.exists(self.user_external_stylesheets_directory_path):
            os.makedirs(self.user_external_stylesheets_directory_path)
        if not os.path.exists(self.transcripts_directory_path):
            os.makedirs(self.transcripts_directory_path)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        return [
            '-*- coding: utf-8 -*-',
            '',
            'Score manager tools configuration file created on {}.'.format(
                self._current_time),
            'This file is interpreted by ConfigObj and should follow ini syntax.',
        ]

    @property
    def _option_definitions(self):
        options = {
            'user_asset_library_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your user-specific assets.',
                    'Defaults to $HOME/score_manager_asset_library/.',
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.home_directory_path, 'score_manager_asset_library')),
            },
            'user_score_packages_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your scores.',
                    'Defaults to $HOME/score_packages/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.home_directory_path, 'score_packages'))
            },
        }
        return options

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def configuration_directory_path(self):
        return os.path.join(self.home_directory_path, '.score_manager')

    @property
    def configuration_file_name(self):
        return 'score_manager.cfg'

    ### PUBLIC METHODS ###

    def filesystem_path_to_packagesystem_path(self, filesystem_path):
        '''Change `filesystem_path` to package path.

        Return string.
        '''
        if filesystem_path is None:
            return
        assert isinstance(filesystem_path, str), repr(filesystem_path)
        filesystem_path = os.path.normpath(filesystem_path)
        if filesystem_path.endswith('.py'):
            filesystem_path = filesystem_path[:-3]
        if filesystem_path.startswith(self.built_in_score_packages_directory_path):
            prefix_length = len(self.abjad_configuration.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(self.user_external_material_packages_directory_path):
            prefix_length = len(self.user_external_material_packages_directory_path) + 1
            remainder = filesystem_path[prefix_length:]
            if remainder:
                remainder = remainder.replace(os.path.sep, '.')
                result = '{}.{}'.format(self.user_external_material_packages_package_path, remainder)
            else:
                result = self.user_external_material_packages_package_path
            return result
        elif filesystem_path.startswith(self.user_external_material_package_makers_directory_path):
            return '.'.join([
                self.user_external_material_package_makers_package_path,
                os.path.basename(filesystem_path)])
        elif filesystem_path.startswith(self.built_in_material_package_makers_directory_path):
            prefix_length = len(self.abjad_configuration.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(self.built_in_material_packages_directory_path):
            prefix_length = len(self.abjad_configuration.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(self.score_manager_tools_directory_path):
            prefix_length = \
                len(os.path.dirname(self.score_manager_tools_directory_path)) + 1
        elif filesystem_path.startswith(self.user_score_packages_directory_path):
            prefix_length = len(self.user_score_packages_directory_path) + 1
        elif filesystem_path.startswith(self.user_external_stylesheets_directory_path):
            prefix_length = len(os.path.dirname(self.user_external_stylesheets_directory_path)) + 1
        else:
            raise Exception('can not change filesystem path {!r} to packagesystem path.'.format(
                filesystem_path))
        package_path = filesystem_path[prefix_length:]
        package_path = package_path.replace(os.path.sep, '.')
        return package_path

    def list_score_directory_paths(self, built_in=False, user=False, head=None):
        '''List score directory paths.
    
        Example. List built-in score directory paths:

        ::

            >>> for x in configuration.list_score_directory_paths(built_in=True):
            ...     x
            '.../tools/scoremanagertools/scorepackages/blue_example_score'
            '.../tools/scoremanagertools/scorepackages/green_example_score'
            '.../tools/scoremanagertools/scorepackages/red_example_score'

        Return list.
        '''
        result = []
        if built_in:
            for directory_entry in os.listdir(self.built_in_score_packages_directory_path):
                if directory_entry[0].isalpha():
                    package_path = '.'.join([
                        self.built_in_score_packages_package_path, directory_entry])
                    if head is None or package_path.startswith(head):
                        filesystem_path = os.path.join(
                            self.built_in_score_packages_directory_path, directory_entry)
                        result.append(filesystem_path)
        if user:
            for directory_entry in os.listdir(self.user_score_packages_directory_path):
                if directory_entry[0].isalpha():
                    package_path = '.'.join([
                        self.user_score_packages_package_path, directory_entry])
                    if head is None or package_path.startswith(head):
                        filesystem_path = os.path.join(
                            self.user_score_packages_directory_path, directory_entry)
                        result.append(filesystem_path)
        return result

    def packagesystem_path_exists(self, packagesystem_path):
        '''True when `packagesystem_path` exists. Otherwise false.

        Return boolean.
        '''
        assert os.path.sep not in packagesystem_path, repr(packagesystem_path)
        filesystem_path = self.packagesystem_path_to_filesystem_path(packagesystem_path)
        return os.path.exists(filesystem_path)

    def packagesystem_path_to_filesystem_path(self, package_path, is_module=False):
        '''Change `package_path` to directory path.
        
        Return string.
        '''
        if package_path is None:
            return
        assert isinstance(package_path, str), repr(package_path)
        package_path_parts = package_path.split('.')
        if package_path_parts[0] == 'scoremanagertools':
            directory_parts = [self.score_manager_tools_directory_path] + \
                package_path_parts[1:]
        elif package_path_parts[:3] == ['experimental', 'tools', 'scoremanagertools']:
            directory_parts = [self.score_manager_tools_directory_path] + \
                package_path_parts[3:]
        elif package_path_parts[0] == \
            self.built_in_material_packages_package_path:
            directory_parts = \
                [self.built_in_material_packages_directory_path] + \
                package_path_parts[1:]
        elif package_path.startswith(self.user_asset_library_package_path):
            prefix_length = len(self.user_asset_library_package_path)
            trimmed_package_path = package_path[prefix_length:]     
            directory_parts = []
            directory_parts.append(self.user_asset_library_directory_path)
            directory_parts.extend(trimmed_package_path.split('.'))
        else:
            directory_parts = [self.user_score_packages_directory_path] + package_path_parts[:]
        directory_path = os.path.join(*directory_parts)
        directory_path = os.path.normpath(directory_path)
        if is_module:
            directory_path += '.py'
        return directory_path
