# -*- encoding: utf-8 -*-
import os
from abjad.tools.systemtools.Configuration import Configuration
from abjad.tools.systemtools.AbjadConfiguration \
    import AbjadConfiguration


class ScoreManagerConfiguration(Configuration):
    r'''Score manager configuration.

        >>> configuration = \
        ...     scoremanagertools.scoremanager.ScoreManagerConfiguration()
        >>> configuration
        ScoreManagerConfiguration()

    '''

    ### CLASS VARIABLES ###

    abjad_configuration = AbjadConfiguration()

    ### INITIALIZER ###

    def __init__(self):
        Configuration.__init__(self)

        # score manager tools

        self._score_manager_tools_directory_path = os.path.join(
            self.abjad_configuration.abjad_experimental_directory_path,
            'tools',
            'scoremanagertools',
            )
        self._score_manager_tools_package_path = '.'.join([
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
        self.user_asset_library_editors_directory_path = os.path.join(
            self.user_asset_library_directory_path,
            'editors',
            )
        self.user_asset_library_material_package_makers_directory_path = \
            os.path.join(
            self.user_asset_library_directory_path,
            'material_package_makers',
            )
        self.user_asset_library_material_packages_directory_path = \
            os.path.join(
            self.user_asset_library_directory_path,
            'material_packages',
            )
        self.user_asset_library_specifiers_directory_path = os.path.join(
            self.user_asset_library_directory_path,
            'specifiers',
            )
        self.user_asset_library_stylesheets_directory_path = os.path.join(
            self.user_asset_library_directory_path,
            'stylesheets',
            )

        # user asset library package paths

        self.user_asset_library_package_path = 'score_manager_asset_library'
        self.user_asset_library_editors_package_path = '.'.join([
            self.user_asset_library_package_path,
            'editors',
            ])
        self.user_asset_library_material_package_makers_package_path = \
            '.'.join([
            self.user_asset_library_package_path,
            'material_package_makers',
            ])
        self.user_asset_library_material_packages_package_path = '.'.join([
            self.user_asset_library_package_path,
            'material_packages',
            ])
        self.user_asset_library_specifiers_package_path = '.'.join([
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
            self.user_asset_library_editors_directory_path,
            self.user_asset_library_material_package_makers_directory_path,
            self.user_asset_library_material_packages_directory_path,
            self.user_asset_library_specifiers_directory_path,
            ):
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                file_path = os.path.join(directory_path, '__init__.py')
                file(file_path, 'w').write('')

        # make missing directories

        if not os.path.exists(self.user_score_packages_directory_path):
            os.makedirs(self.user_score_packages_directory_path)
        if not os.path.exists(
            self.user_asset_library_stylesheets_directory_path):
            os.makedirs(self.user_asset_library_stylesheets_directory_path)
        if not os.path.exists(self.transcripts_directory_path):
            os.makedirs(self.transcripts_directory_path)

        # other directory paths

        self._handler_tools_directory_path = os.path.join(
            self.abjad_configuration.abjad_experimental_directory_path,
            'tools',
            'handlertools',
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        return [
            '-*- coding: utf-8 -*-',
            '',
            'Score manager tools configuration file created on {}.'.format(
                self._current_time),
            'This file is interpreted by ConfigObj'
            ' and should follow ini syntax.',
        ]

    @property
    def _option_definitions(self):
        options = {
            'user_asset_library_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you'
                    ' house your user-specific assets.',
                    'Defaults to $HOME/score_manager_asset_library/.',
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.home_directory_path,
                        'score_manager_asset_library',
                        )
                    ),
            },
            'user_score_packages_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your scores.',
                    'Defaults to $HOME/score_packages/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.home_directory_path, 
                        'score_packages',
                        )
                    )
            },
        }
        return options

    ### PUBLIC PROPERTIES ###

    @property
    def configuration_directory_path(self):
        r'''Configuration directory path.

        ::

            >>> configuration.configuration_directory_path
            '.../.score_manager'

        Returns string.
        '''
        return os.path.join(self.home_directory_path, '.score_manager')

    @property
    def configuration_file_name(self):
        r'''Configuration file name.

        ::

            >>> configuration.configuration_file_name
            'score_manager.cfg'

        Returns string.
        '''
        return 'score_manager.cfg'

    @property
    def configuration_file_path(self):
        r'''Configuration file path.

        ::

            >>> configuration.configuration_file_path
            '.../.score_manager/score_manager.cfg'

        Returns string.
        '''
        superclass = super(ScoreManagerConfiguration, self)
        return superclass.configuration_file_path

    @property
    def handler_tools_directory_path(self):
        r'''Handler tools directory path.

        ::

            >>> configuration.handler_tools_directory_path
            '.../experimental/tools/handlertools'

        Returns string.
        '''
        return self._handler_tools_directory_path  
        
    @property
    def home_directory_path(self):
        r'''Home directory path.

        ::

            >>> configuration.home_directory_path # doctest: +SKIP
            '/Users/...'

        Returns string.
        '''
        superclass = super(ScoreManagerConfiguration, self)
        return superclass.home_directory_path

    @property
    def score_manager_tools_directory_path(self):
        r'''Score manager tools directory path.

        ::

            >>> configuration.score_manager_tools_directory_path
            '.../experimental/tools/scoremanagertools'

        Returns string.
        '''
        return self._score_manager_tools_directory_path

    @property
    def score_manager_tools_package_path(self):
        r'''Score manager tools package path.

        ::

            >>> configuration.score_manager_tools_package_path
            'experimental.tools.scoremanagertools'

        Returns string.
        '''
        return self._score_manager_tools_package_path

    ### PUBLIC METHODS ###

    def filesystem_path_to_packagesystem_path(self, filesystem_path):
        r'''Changes `filesystem_path` to package path.

        Returns string.
        '''
        if filesystem_path is None:
            return
        assert isinstance(filesystem_path, str), repr(filesystem_path)
        filesystem_path = os.path.normpath(filesystem_path)
        if filesystem_path.endswith('.py'):
            filesystem_path = filesystem_path[:-3]
        if filesystem_path.startswith(
            self.built_in_score_packages_directory_path):
            prefix_length = \
                len(self.abjad_configuration.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(
            self.user_asset_library_material_packages_directory_path):
            prefix_length = \
                len(self.user_asset_library_material_packages_directory_path) + 1
            remainder = filesystem_path[prefix_length:]
            if remainder:
                remainder = remainder.replace(os.path.sep, '.')
                result = '{}.{}'.format(
                    self.user_asset_library_material_packages_package_path, 
                    remainder)
            else:
                result = self.user_asset_library_material_packages_package_path
            return result
        elif filesystem_path.startswith(
            self.user_asset_library_material_package_makers_directory_path):
            return '.'.join([
                self.user_asset_library_material_package_makers_package_path,
                os.path.basename(filesystem_path)])
        elif filesystem_path.startswith(
            self.built_in_material_package_makers_directory_path):
            prefix_length = \
                len(self.abjad_configuration.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(
            self.built_in_material_packages_directory_path):
            prefix_length = \
                len(self.abjad_configuration.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(
            self.score_manager_tools_directory_path):
            prefix_length = \
                len(os.path.dirname(self.score_manager_tools_directory_path)) + 1
        elif filesystem_path.startswith(
            self.user_score_packages_directory_path):
            prefix_length = len(self.user_score_packages_directory_path) + 1
        elif filesystem_path.startswith(
            self.user_asset_library_stylesheets_directory_path):
            prefix_length = \
                len(os.path.dirname(
                self.user_asset_library_stylesheets_directory_path)) + 1
        else:
            message = 'can not change filesystem path {!r}'
            message += ' to packagesystem path.'
            raise Exception(message.format(filesystem_path))
        packagesystem_path = filesystem_path[prefix_length:]
        packagesystem_path = packagesystem_path.replace(os.path.sep, '.')
        return packagesystem_path

    def list_score_directory_paths(
        self, 
        built_in=False, 
        user=False, 
        head=None,
        ):
        r'''Lists score directory paths.

        Example. List built-in score directory paths:

        ::

            >>> for x in configuration.list_score_directory_paths(
            ...     built_in=True):
            ...     x
            '.../tools/scoremanagertools/scorepackages/blue_example_score'
            '.../tools/scoremanagertools/scorepackages/green_example_score'
            '.../tools/scoremanagertools/scorepackages/red_example_score'

        Returns list.
        '''
        result = []
        if built_in:
            for directory_entry in \
                sorted(os.listdir(
                    self.built_in_score_packages_directory_path)):
                if directory_entry[0].isalpha():
                    package_path = '.'.join([
                        self.built_in_score_packages_package_path,
                        directory_entry])
                    if head is None or package_path.startswith(head):
                        filesystem_path = os.path.join(
                            self.built_in_score_packages_directory_path,
                            directory_entry)
                        result.append(filesystem_path)
        if user:
            for directory_entry in \
                sorted(os.listdir(self.user_score_packages_directory_path)):
                if directory_entry[0].isalpha():
                    package_path = '.'.join([
                        self.user_score_packages_package_path,
                        directory_entry])
                    if head is None or package_path.startswith(head):
                        filesystem_path = os.path.join(
                            self.user_score_packages_directory_path,
                            directory_entry)
                        result.append(filesystem_path)
        return result

    def packagesystem_path_exists(self, packagesystem_path):
        r'''True whens `packagesystem_path` exists. Otherwise false.

        ::

            >>> packagesystem_path = 'scoremanagertools.materialpackages'
            >>> configuration.packagesystem_path_exists(packagesystem_path)
            True

        Returns boolean.
        '''
        assert os.path.sep not in packagesystem_path
        filesystem_path = \
            self.packagesystem_path_to_filesystem_path(packagesystem_path)
        return os.path.exists(filesystem_path)

    def packagesystem_path_to_filesystem_path(
        self, packagesystem_path, is_module=False):
        r'''Changes `packagesystem_path` to filesystem path.

        Returns string.
        '''
        if packagesystem_path is None:
            return
        assert isinstance(packagesystem_path, str), repr(packagesystem_path)
        packagesystem_path_parts = packagesystem_path.split('.')
        if packagesystem_path_parts[0] == 'scoremanagertools':
            directory_parts = [self.score_manager_tools_directory_path] + \
                packagesystem_path_parts[1:]
        elif packagesystem_path_parts[:3] == \
            ['experimental', 'tools', 'scoremanagertools']:
            directory_parts = [self.score_manager_tools_directory_path] + \
                packagesystem_path_parts[3:]
        elif packagesystem_path_parts[0] == \
            self.built_in_material_packages_package_path:
            directory_parts = \
                [self.built_in_material_packages_filesystem_path] + \
                packagesystem_path_parts[1:]
        elif packagesystem_path.startswith(
            self.user_asset_library_package_path):
            prefix_length = len(self.user_asset_library_package_path)
            trimmed_packagesystem_path = packagesystem_path[prefix_length:]
            directory_parts = []
            directory_parts.append(self.user_asset_library_directory_path)
            directory_parts.extend(trimmed_packagesystem_path.split('.'))
        else:
            directory_parts = \
                [self.user_score_packages_directory_path] + \
                packagesystem_path_parts[:]
        filesystem_path = os.path.join(*directory_parts)
        filesystem_path = os.path.normpath(filesystem_path)
        if is_module:
            filesystem_path += '.py'
        return filesystem_path
