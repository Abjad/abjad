# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools import predicates
from experimental.tools.scoremanagertools.wranglers.PackageWrangler \
    import PackageWrangler


class MaterialPackageWrangler(PackageWrangler):
    r'''Material package wrangler.

    ::

        >>> wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
        >>> wrangler
        MaterialPackageWrangler()

    Wrangler in built-in score:

    ::

        >>> wrangler_in_built_in_score = \
        ...     scoremanagertools.wranglers.MaterialPackageWrangler()
        >>> session = wrangler_in_built_in_score.session
        >>> session.snake_case_current_score_name = \
        ...     'red_example_score'
        >>> wrangler_in_built_in_score
        MaterialPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    score_package_asset_storehouse_path_infix_parts = ('materials',)

    asset_storehouse_packagesystem_path_in_built_in_asset_library = \
        PackageWrangler.configuration.built_in_material_packages_package_path

    asset_storehouse_packagesystem_path_in_user_asset_library = \
        PackageWrangler.configuration.user_asset_library_material_packages_package_path

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        PackageWrangler.__init__(self, session=session)
        self._material_package_maker_wrangler = \
            scoremanagertools.wranglers.MaterialPackageMakerWrangler(
                session=self.session)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'materials'

    ### PRIVATE METHODS ###

    def _get_appropriate_material_package_proxy(
        self,
        material_package_maker_class_name, 
        material_package_path,
        ):
        from experimental.tools import scoremanagertools
        if material_package_maker_class_name is None:
            material_package_proxy = \
                scoremanagertools.proxies.MaterialPackageProxy(
                material_package_path, 
                session=self.session,
                )
        else:
            command = 'material_package_proxy = '
            command += 'scoremanagertools.materialpackagemakers.{}'
            command += '(material_package_path, session=self.session)'
            command = command.format(material_package_maker_class_name)
            try:
                exec(command)
            except AttributeError:
                command = 'from {0}.{1}.{1}'
                command += ' import {1} as material_package_maker_class'
                command = command.format(
                    self.configuration.user_asset_library_material_package_makers_package_path,
                    material_package_maker_class_name,
                    )
                exec(command)
                material_package_proxy = material_package_maker_class(
                    material_package_path, 
                    session=self.session,
                    )
        return material_package_proxy

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            material_package_proxy = self._initialize_asset_proxy(result)
            material_package_proxy._run()

    def _initialize_asset_proxy(self, package_path):
        return self._material_package_maker_wrangler._initialize_asset_proxy(
            package_path)

    def _make_main_menu(self, head=None):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        asset_section = main_menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        asset_section.menu_entries = asset_menu_entries
        command_section = main_menu.make_command_section()
        command_section.append(('data-only', 'd'))
        command_section.append(('handmade', 'h'))
        command_section.append(('maker-made', 'm'))
        hidden_section = main_menu.make_command_section(is_hidden=True)
        hidden_section.append(('create numeric sequence', 's'))
        hidden_section.append(('create missing packages', 'missing'))
        hidden_section.append(('profile packages', 'profile'))
        return main_menu

    ### PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        r'''Asset proxy class of material packge wrangler.

        ::

            >>> wrangler.asset_proxy_class.__name__
            'PackageProxy'

        Returns class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.PackageProxy

    @property
    def storage_format(self):
        r'''Storage format of material package wrangler.

        ::

            >>> wrangler.storage_format
            'wranglers.MaterialPackageWrangler()'

        Returns string.
        '''
        return super(MaterialPackageWrangler, self).storage_format

    ### PUBLIC METHODS ###

    def interactively_make_data_package(
        self, 
        tags=None, 
        pending_user_input=None,
        ):
        r'''Interactively makes data package.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        with self.backtracking:
            material_package_path = \
                self.interactively_get_available_packagesystem_path()
        if self.session.backtrack():
            return
        self.make_data_package(material_package_path, tags=tags)

    def interactively_make_handmade_material_package(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively makes handmade material package.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        with self.backtracking:
            package_path = \
                self.interactively_get_available_packagesystem_path()
        if self.session.backtrack():
            return
        self.make_handmade_material_package(package_path)

    def interactively_make_makermade_material_package(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively makes makermade material package.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        with self.backtracking:
            wrangler = self._material_package_maker_wrangler
            result = wrangler.interactively_select_asset_packagesystem_path(
                cache=True, clear=False)
        if self.session.backtrack():
            return
        material_package_maker_package_path = result
        material_package_maker_class_name = \
            material_package_maker_package_path.split('.')[-1]
        with self.backtracking:
            material_package_path = \
                self.interactively_get_available_packagesystem_path()
        if self.session.backtrack():
            return
        self.make_makermade_material_package(
            material_package_path, material_package_maker_class_name)
        proxy = self._get_appropriate_material_package_proxy(
            material_package_maker_class_name, material_package_path)
        proxy.run_first_time()

    def interactively_make_numeric_sequence_package(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively makes numeric sequence package.

        Returns none.
        '''
        tags = {'is_numeric_sequence': True}
        self.interactively_make_data_package(
            tags=tags, 
            pending_user_input=pending_user_input,
            )

    def list_asset_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Example. List built-in material package filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../scoremanagertools/materialpackages/red_directives'
            '.../scoremanagertools/materialpackages/red_forte'
            '.../scoremanagertools/materialpackages/red_marcati'
            '.../scoremanagertools/materialpackages/red_notes'
            '.../scoremanagertools/materialpackages/red_numbers'
            '.../scoremanagertools/materialpackages/red_sargasso_measures'
            '.../scoremanagertools/materialpackages/sargasso_multipliers'
            '.../scorepackages/red_example_score/materials/tempo_inventory'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_names(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset names.

        Example. List built-in material package names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     in_user_asset_library=False, in_user_score_packages=False):
            ...     x
            'black music specifier'
            'green music specifier'
            'red directives'
            'red forte'
            'red marcati'
            'red notes'
            'red numbers'
            'red sargasso measures'
            'sargasso multipliers'
            'tempo inventory'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_names(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_packagesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset packagesystem paths.

        Example. List built-in material package paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            'experimental.tools.scoremanagertools.materialpackages.black_music_specifier'
            'experimental.tools.scoremanagertools.materialpackages.green_music_specifier'
            'experimental.tools.scoremanagertools.materialpackages.red_directives'
            'experimental.tools.scoremanagertools.materialpackages.red_forte'
            'experimental.tools.scoremanagertools.materialpackages.red_marcati'
            'experimental.tools.scoremanagertools.materialpackages.red_notes'
            'experimental.tools.scoremanagertools.materialpackages.red_numbers'
            'experimental.tools.scoremanagertools.materialpackages.red_sargasso_measures'
            'experimental.tools.scoremanagertools.materialpackages.sargasso_multipliers'
            'experimental.tools.scoremanagertools.scorepackages.red_example_score.materials.tempo_inventory'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_packagesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_proxies(
        self, 
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset proxies.

        Example. List built-in material package proxies:

        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackages/black_music_specifier')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackages/green_music_specifier')
            MarkupInventoryMaterialPackageMaker('.../tools/scoremanagertools/materialpackages/red_directives')
            DynamicHandlerMaterialPackageMaker('.../tools/scoremanagertools/materialpackages/red_forte')
            ArticulationHandlerMaterialPackageMaker('.../tools/scoremanagertools/materialpackages/red_marcati')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackages/red_notes')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackages/red_numbers')
            SargassoMeasureMaterialPackageMaker('.../tools/scoremanagertools/materialpackages/red_sargasso_measures')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackages/sargasso_multipliers')
            TempoMarkInventoryMaterialPackageMaker('.../tools/scoremanagertools/scorepackages/red_example_score/materials/tempo_inventory')

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_proxies(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_storehouse_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Example. List built-in material package storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_asset_storehouse_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/materialpackages'
            '.../tools/scoremanagertools/scorepackages/blue_example_score/materials'
            '.../tools/scoremanagertools/scorepackages/green_example_score/materials'
            '.../tools/scoremanagertools/scorepackages/red_example_score/materials'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            )

    def make_data_package(self, material_package_path, tags=None):
        r'''Makes data package.

        Returns none.
        '''
        tags = tags or {}
        tags['material_package_maker_class_name'] = None
        tags['should_have_illustration'] = False
        tags['should_have_user_input_module'] = False
        self.make_material_package(material_package_path, tags=tags)

    def make_handmade_material_package(self, material_package_path, tags=None):
        r'''Makes handmade material package.

        Returns none.
        '''
        tags = tags or {}
        tags['material_package_maker_class_name'] = None
        tags['should_have_illustration'] = True
        tags['should_have_user_input_module'] = False
        self.make_material_package(material_package_path, tags=tags)

    def make_makermade_material_package(self,
        material_package_path, 
        material_package_maker_class_name, 
        tags=None,
        ):
        r'''Makes makermade material package.

        Returns none.
        '''
        tags = tags or {}
        command = 'from experimental.tools.scoremanagertools.materialpackagemakers '
        command += 'import {} as material_package_maker_class'.format(
            material_package_maker_class_name)
        try:
            exec(command)
        except ImportError:
            command = 'from {} import {} as material_package_maker_class'.format(
                self.configuration.user_asset_library_material_package_makers_package_path,
                material_package_maker_class_name)
            exec(command)
        should_have_user_input_module = getattr(
            material_package_maker_class, 'should_have_user_input_module', True)
        should_have_illustration = hasattr(
            material_package_maker_class, 'illustration_builder')
        tags['material_package_maker_class_name'] = material_package_maker_class_name
        tags['should_have_illustration'] = should_have_illustration
        tags['should_have_user_input_module'] = should_have_user_input_module
        self.make_material_package(material_package_path, tags=tags)

    def make_material_package(
        self, 
        package_path, 
        is_interactive=False, 
        tags=None,
        ):
        r'''Makes material package.

        Returns none.
        '''
        tags = collections.OrderedDict(tags or {})
        tags['is_material_package'] = True
        directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            package_path)
        assert not os.path.exists(directory_path)
        os.mkdir(directory_path)
        material_package_maker_class_name = tags.get(
            'material_package_maker_class_name')
        pair = (material_package_maker_class_name, package_path)
        material_package_proxy = self._get_appropriate_material_package_proxy(
            *pair)
        material_package_proxy.initializer_file_proxy.write_stub_to_disk()
        material_package_proxy.tags_module_proxy.write_stub_to_disk()
        material_package_proxy.tags_module_proxy.write_tags_to_disk(tags)
        material_package_proxy.conditionally_write_stub_material_definition_module_to_disk()
        material_package_proxy.conditionally_write_stub_user_input_module_to_disk()
        line = 'material package {!r} created.'.format(package_path)
        self.session.io_manager.proceed(line, is_interactive=is_interactive)

    def make_numeric_sequence_package(self, package_path):
        r'''Makes numeric sequence package.

        Returns none.
        '''
        tags = {'is_numeric_sequence': True}
        self.make_data_package(package_path, tags=tags)

    ### UI MANIFEST ###

    user_input_to_action = PackageWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'd': interactively_make_data_package,
        's': interactively_make_numeric_sequence_package,
        'h': interactively_make_handmade_material_package,
        'm': interactively_make_makermade_material_package,
        })
