# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import stringtools
from scoremanager import predicates
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class MaterialPackageWrangler(PackageWrangler):
    r'''Material package wrangler.

    ::

        >>> wrangler = scoremanager.wranglers.MaterialPackageWrangler()
        >>> wrangler
        MaterialPackageWrangler()

    Wrangler in built-in score:

    ::

        >>> wrangler_in_built_in_score = \
        ...     scoremanager.wranglers.MaterialPackageWrangler()
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
        from scoremanager import wranglers
        PackageWrangler.__init__(self, session=session)
        self._material_package_manager_wrangler = \
            wranglers.MaterialPackageManagerWrangler(
                session=self.session)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'materials'

    ### PRIVATE METHODS ###

    def _get_appropriate_material_package_manager(
        self,
        material_package_manager_class_name, 
        material_package_path,
        ):
        import scoremanager
        from scoremanager import managers
        if material_package_manager_class_name is None:
            material_package_manager = \
                managers.MaterialPackageManager(
                material_package_path, 
                session=self.session,
                )
        else:
            command = 'material_package_manager = '
            command += 'scoremanager.materialpackagemanagers.{}'
            command += '(material_package_path, session=self.session)'
            command = command.format(material_package_manager_class_name)
            try:
                exec(command)
            except AttributeError:
                command = 'from {0}.{1}.{1}'
                command += ' import {1} as material_package_manager_class'
                command = command.format(
                    self.configuration.user_asset_library_material_package_managers_package_path,
                    material_package_manager_class_name,
                    )
                exec(command)
                material_package_manager = material_package_manager_class(
                    material_package_path, 
                    session=self.session,
                    )
        return material_package_manager

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            material_package_manager = self._initialize_asset_manager(result)
            material_package_manager._run()

    def _initialize_asset_manager(self, package_path):
        return self._material_package_manager_wrangler._initialize_asset_manager(
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

    ### PUBLIC METHODS ###

    def interactively_make_data_package(
        self, 
        metadata=None, 
        pending_user_input=None,
        ):
        r'''Interactively makes data package.

        Returns none.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        with self.backtracking:
            material_package_path = \
                self.interactively_get_available_packagesystem_path()
        if self.session.backtrack():
            return
        self.make_data_package(material_package_path, metadata=metadata)

    def interactively_make_handmade_material_package(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively makes handmade material package.

        Returns none.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
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
        self.session.io_manager._assign_user_input(pending_user_input)
        with self.backtracking:
            wrangler = self._material_package_manager_wrangler
            result = wrangler.interactively_select_asset_packagesystem_path(
                cache=True, clear=False)
        if self.session.backtrack():
            return
        material_package_manager_package_path = result
        material_package_manager_class_name = \
            material_package_manager_package_path.split('.')[-1]
        with self.backtracking:
            material_package_path = \
                self.interactively_get_available_packagesystem_path()
        if self.session.backtrack():
            return
        self.make_makermade_material_package(
            material_package_path, material_package_manager_class_name)
        manager = self._get_appropriate_material_package_manager(
            material_package_manager_class_name, material_package_path)
        manager.run_first_time()

    def interactively_make_numeric_sequence_package(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively makes numeric sequence package.

        Returns none.
        '''
        metadata = {'is_numeric_sequence': True}
        self.interactively_make_data_package(
            metadata=metadata, 
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
            '.../scoremanager/materialpackages/red_directives'
            '.../scoremanager/materialpackages/red_forte'
            '.../scoremanager/materialpackages/red_marcati'
            '.../scoremanager/materialpackages/red_notes'
            '.../scoremanager/materialpackages/red_numbers'
            '.../scoremanager/materialpackages/red_sargasso_measures'
            '.../scoremanager/materialpackages/sargasso_multipliers'
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

    def list_asset_managers(
        self, 
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        Example. List built-in material package managers:

        ::

            >>> for x in wrangler.list_asset_managers(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            MarkupInventoryMaterialPackageManager('.../scoremanager/materialpackages/red_directives')
            DynamicHandlerMaterialPackageManager('.../scoremanager/materialpackages/red_forte')
            ArticulationHandlerMaterialPackageManager('.../scoremanager/materialpackages/red_marcati')
            MaterialPackageManager('.../scoremanager/materialpackages/red_notes')
            MaterialPackageManager('.../scoremanager/materialpackages/red_numbers')
            SargassoMeasureMaterialPackageManager('.../scoremanager/materialpackages/red_sargasso_measures')
            MaterialPackageManager('.../scoremanager/materialpackages/sargasso_multipliers')
            TempoInventoryMaterialPackageManager('.../scoremanager/scorepackages/red_example_score/materials/tempo_inventory')

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_managers(
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
            'scoremanager.materialpackages.red_directives'
            'scoremanager.materialpackages.red_forte'
            'scoremanager.materialpackages.red_marcati'
            'scoremanager.materialpackages.red_notes'
            'scoremanager.materialpackages.red_numbers'
            'scoremanager.materialpackages.red_sargasso_measures'
            'scoremanager.materialpackages.sargasso_multipliers'
            'scoremanager.scorepackages.red_example_score.materials.tempo_inventory'

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
            '.../scoremanager/materialpackages'
            '.../scoremanager/scorepackages/blue_example_score/materials'
            '.../scoremanager/scorepackages/green_example_score/materials'
            '.../scoremanager/scorepackages/red_example_score/materials'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            )

    def make_data_package(self, material_package_path, metadata=None):
        r'''Makes data package.

        Returns none.
        '''
        metadata = metadata or {}
        metadata['material_package_manager_class_name'] = None
        metadata['should_have_illustration'] = False
        metadata['should_have_user_input_module'] = False
        self.make_material_package(material_package_path, metadata=metadata)

    def make_handmade_material_package(self, material_package_path, metadata=None):
        r'''Makes handmade material package.

        Returns none.
        '''
        metadata = metadata or {}
        metadata['material_package_manager_class_name'] = None
        metadata['should_have_illustration'] = True
        metadata['should_have_user_input_module'] = False
        self.make_material_package(material_package_path, metadata=metadata)

    def make_makermade_material_package(self,
        material_package_path, 
        material_package_manager_class_name, 
        metadata=None,
        ):
        r'''Makes makermade material package.

        Returns none.
        '''
        metadata = metadata or {}
        command = 'from scoremanager.materialpackagemanagers '
        command += 'import {} as material_package_manager_class'.format(
            material_package_manager_class_name)
        try:
            exec(command)
        except ImportError:
            command = 'from {} import {} as material_package_manager_class'.format(
                self.configuration.user_asset_library_material_package_managers_package_path,
                material_package_manager_class_name)
            exec(command)
        should_have_user_input_module = getattr(
            material_package_manager_class, 'should_have_user_input_module', True)
        should_have_illustration = hasattr(
            material_package_manager_class, 'illustration_builder')
        metadata['material_package_manager_class_name'] = material_package_manager_class_name
        metadata['should_have_illustration'] = should_have_illustration
        metadata['should_have_user_input_module'] = should_have_user_input_module
        self.make_material_package(material_package_path, metadata=metadata)

    def make_material_package(
        self, 
        package_path, 
        is_interactive=False, 
        metadata=None,
        ):
        r'''Makes material package.

        Returns none.
        '''
        metadata = collections.OrderedDict(metadata or {})
        metadata['is_material_package'] = True
        directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            package_path)
        assert not os.path.exists(directory_path)
        os.mkdir(directory_path)
        string = 'material_package_manager_class_name'
        material_package_manager_class_name = metadata.get(string)
        pair = (material_package_manager_class_name, package_path)
        material_package_manager = self._get_appropriate_material_package_manager(
            *pair)
        material_package_manager.initializer_file_manager._write_stub_to_disk()
        material_package_manager.write_metadata_to_disk(metadata)
        material_package_manager.conditionally_write_stub_material_definition_module_to_disk()
        material_package_manager.conditionally_write_stub_user_input_module_to_disk()
        line = 'material package {!r} created.'.format(package_path)
        self.session.io_manager.proceed(line, is_interactive=is_interactive)

    def make_numeric_sequence_package(self, package_path):
        r'''Makes numeric sequence package.

        Returns none.
        '''
        metadata = {'is_numeric_sequence': True}
        self.make_data_package(package_path, metadata=metadata)

    ### UI MANIFEST ###

    user_input_to_action = PackageWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'd': interactively_make_data_package,
        's': interactively_make_numeric_sequence_package,
        'h': interactively_make_handmade_material_package,
        'm': interactively_make_makermade_material_package,
        })
