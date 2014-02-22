# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import stringtools
from scoremanager import predicates
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class MaterialPackageWrangler(PackageWrangler):
    r'''Material package wrangler.

    ..  container:: example

        ::

            >>> from scoremanager import wranglers
            >>> wrangler = wranglers.MaterialPackageWrangler()
            >>> wrangler
            MaterialPackageWrangler()

    ..  container:: example

        ::

            >>> wrangler_in_score = wranglers.MaterialPackageWrangler()
            >>> session = wrangler_in_score._session
            >>> session.current_score_snake_case_name = 'red_example_score'
            >>> wrangler_in_score
            MaterialPackageWrangler()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import wranglers
        superclass = super(MaterialPackageWrangler, self)
        superclass.__init__(session=session)
        self._material_package_manager_wrangler = \
            wranglers.MaterialPackageManagerWrangler(session=self._session)
        self.abjad_storehouse_directory_path = \
            self.configuration.abjad_material_packages_directory_path
        self.user_storehouse_directory_path = \
            self.configuration.user_library_material_packages_directory_path
        self.score_storehouse_path_infix_parts = ('materials',)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            return 'materials'
        else:
            return 'material library'

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
                session=self._session,
                )
        else:
            command = 'material_package_manager = '
            command += 'scoremanager.materialpackagemanagers.{}'
            command += '(material_package_path, session=self._session)'
            command = command.format(material_package_manager_class_name)
            try:
                exec(command)
            except AttributeError:
                command = 'from {0}.{1}.{1}'
                command += ' import {1} as material_package_manager_class'
                package_path = '.'.join([
                    self.configuration._user_library_directory_name,
                    'material_packages',
                    ])
                command = command.format(
                    package_path,
                    material_package_manager_class_name,
                    )
                exec(command)
                material_package_manager = material_package_manager_class(
                    material_package_path, 
                    session=self._session,
                    )
        return material_package_manager

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result](self)
        else:
            material_package_manager = self._initialize_asset_manager(result)
            if os.path.exists(material_package_manager._filesystem_path):
                material_package_manager._run()

    def _initialize_asset_manager(self, package_path):
        wrangler = self._material_package_manager_wrangler
        manager = wrangler._initialize_asset_manager(package_path)
        return manager

    def _make_main_menu(self, head=None):
        main_menu = self._session.io_manager.make_menu(where=self._where)
        asset_section = main_menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        asset_section.menu_entries = asset_menu_entries
        command_section = main_menu.make_command_section()
        command_section.append(('new material - by hand', 'nmh'))
        command_section.append(('new material - with manager', 'nmm'))
        return main_menu

    ### PUBLIC METHODS ###

    def make_data_package(
        self, 
        metadata=None, 
        pending_user_input=None,
        ):
        r'''Interactively makes data package.

        Returns none.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
        with self.backtracking:
            material_package_path = \
                self.get_available_package_path()
        if self._session._backtrack():
            return
        self._make_data_package(material_package_path, metadata=metadata)

    def make_handmade_material_package(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively makes handmade material package.

        Returns none.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
        with self.backtracking:
            package_path = \
                self.get_available_package_path()
        if self._session._backtrack():
            return
        self._make_handmade_material_package(package_path)

    def make_managermade_material_package(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively makes managermade material package.

        Returns none.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
        with self.backtracking:
            wrangler = self._material_package_manager_wrangler
            result = wrangler.select_asset_package_path(
                cache=True, clear=False)
        if self._session._backtrack():
            return
        material_package_manager_package_path = result
        material_package_manager_class_name = \
            material_package_manager_package_path.split('.')[-1]
        with self.backtracking:
            material_package_path = \
                self.get_available_package_path()
        if self._session._backtrack():
            return
        self._make_managermade_material_package(
            material_package_path, material_package_manager_class_name)
        manager = self._get_appropriate_material_package_manager(
            material_package_manager_class_name, material_package_path)
        manager.run_first_time()

    def list_asset_filesystem_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Lists abjad material package filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            '.../scoremanager/materialpackages/red_forte'
            '.../scoremanager/materialpackages/red_marcati'
            '.../scoremanager/materialpackages/red_markup'
            '.../scoremanager/materialpackages/red_notes'
            '.../scoremanager/materialpackages/red_numbers'
            '.../scoremanager/materialpackages/red_sargasso_measures'
            '.../scorepackages/red_example_score/materials/tempo_inventory'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_filesystem_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def list_asset_managers(
        self, 
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        Lists abjad material package managers:

        ::

            >>> for x in wrangler.list_asset_managers(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            DynamicHandlerMaterialPackageManager('.../scoremanager/materialpackages/red_forte')
            ArticulationHandlerMaterialPackageManager('.../scoremanager/materialpackages/red_marcati')
            MarkupInventoryMaterialPackageManager('.../scoremanager/materialpackages/red_markup')
            MaterialPackageManager('.../scoremanager/materialpackages/red_notes')
            MaterialPackageManager('.../scoremanager/materialpackages/red_numbers')
            SargassoMeasureMaterialPackageManager('.../scoremanager/materialpackages/red_sargasso_measures')
            TempoInventoryMaterialPackageManager('.../scoremanager/scorepackages/red_example_score/materials/tempo_inventory')

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_managers(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def list_asset_names(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset names.

        Lists abjad material package names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     user_library=False, user_score_packages=False):
            ...     x
            'red forte'
            'red marcati'
            'red markup'
            'red notes'
            'red numbers'
            'red sargasso measures'
            'tempo inventory'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_names(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def list_asset_package_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset packagesystem paths.

        Lists abjad material package paths:

        ::

            >>> for x in wrangler.list_asset_package_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            'scoremanager.materialpackages.red_forte'
            'scoremanager.materialpackages.red_marcati'
            'scoremanager.materialpackages.red_markup'
            'scoremanager.materialpackages.red_notes'
            'scoremanager.materialpackages.red_numbers'
            'scoremanager.materialpackages.red_sargasso_measures'
            'scoremanager.scorepackages.red_example_score.materials.tempo_inventory'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_asset_package_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def list_storehouse_directory_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Lists abjad material package storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_storehouse_directory_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            '.../scoremanager/materialpackages'
            '.../scoremanager/scorepackages/blue_example_score/materials'
            '.../scoremanager/scorepackages/green_example_score/materials'
            '.../scoremanager/scorepackages/red_example_score/materials'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass.list_storehouse_directory_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )

    def _make_data_package(self, material_package_path, metadata=None):
        metadata = metadata or {}
        metadata['material_package_manager_class_name'] = None
        metadata['should_have_illustration'] = False
        metadata['should_have_user_input_module'] = False
        self._make_material_package(material_package_path, metadata=metadata)

    def _make_handmade_material_package(self, material_package_path, metadata=None):
        metadata = metadata or {}
        metadata['material_package_manager_class_name'] = None
        metadata['should_have_illustration'] = True
        metadata['should_have_user_input_module'] = False
        self._make_material_package(material_package_path, metadata=metadata)

    def _make_managermade_material_package(
        self,
        material_package_path, 
        material_package_manager_class_name, 
        metadata=None,
        ):
        metadata = metadata or {}
        command = 'from scoremanager.materialpackagemanagers '
        command += 'import {} as material_package_manager_class'
        command = command.format(material_package_manager_class_name)
        try:
            exec(command)
        except ImportError:
            command = 'from {} import {} as material_package_manager_class'
            package_path = '.'.join([
                self.configuration._user_library_directory_name,
                'material_packages',
                ])
            command = command.format(
                package_path,
                material_package_manager_class_name,
                )
            exec(command)
        should_have_user_input_module = getattr(
            material_package_manager_class, 
            'should_have_user_input_module', 
            True,
            )
        should_have_illustration = hasattr(
            material_package_manager_class, 
            'illustration_builder',
            )
        metadata['material_package_manager_class_name'] = \
            material_package_manager_class_name
        metadata['should_have_illustration'] = \
            should_have_illustration
        metadata['should_have_user_input_module'] = \
            should_have_user_input_module
        self._make_material_package(material_package_path, metadata=metadata)

    def _make_material_package(
        self, 
        package_path, 
        prompt=False, 
        metadata=None,
        ):
        metadata = collections.OrderedDict(metadata or {})
        metadata['is_material_package'] = True
        directory_path = \
            self.configuration.package_path_to_filesystem_path(
            package_path)
        assert not os.path.exists(directory_path)
        os.mkdir(directory_path)
        string = 'material_package_manager_class_name'
        material_package_manager_class_name = metadata.get(string)
        pair = (material_package_manager_class_name, package_path)
        material_package_manager = self._get_appropriate_material_package_manager(
            *pair)
        material_package_manager._initializer_file_manager._write_stub()
        material_package_manager.rewrite_metadata_module(metadata)
        material_package_manager.conditionally_write_stub_material_definition_module()
        material_package_manager.conditionally_write_stub_user_input_module()
        message = 'material package {!r} created.'.format(package_path)
        self._session.io_manager.proceed(message=message, prompt=prompt)

    ### UI MANIFEST ###

    _user_input_to_action = PackageWrangler._user_input_to_action.copy()
    _user_input_to_action.update({
        'd': make_data_package,
        'nmh': make_handmade_material_package,
        'nmm': make_managermade_material_package,
        })
