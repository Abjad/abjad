# -*- encoding: utf-8 -*-
import collections
import os
import traceback
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager import predicates
from scoremanager.wranglers.Wrangler import Wrangler


class MaterialPackageWrangler(Wrangler):
    r'''Material package wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.MaterialPackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MaterialPackageWrangler()

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> session._set_test_score('red_example_score')
            >>> wrangler_in_score = scoremanager.wranglers.MaterialPackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler_in_score
            MaterialPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_material_manager_wrangler', 
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(MaterialPackageWrangler, self)
        superclass.__init__(session=session)
        path = self._configuration.abjad_material_packages_directory_path
        self._abjad_storehouse_path = path
        path = \
            self._configuration.user_library_material_packages_directory_path
        self._user_storehouse_path = path
        self._score_storehouse_path_infix_parts = ('materials',)

    ### PRIVATE PROPERTIES ###

    @property
    def _asset_manager_class(self):
        from scoremanager import managers
        return managers.MaterialPackageManager

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            return 'materials'
        else:
            return 'material library'

    @property
    @systemtools.Memoize
    def _material_manager_wrangler(self):
        from scoremanager import wranglers
        return wranglers.MaterialManagerWrangler(session=self._session)

    @property
    def _user_input_to_action(self):
        superclass = super(MaterialPackageWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            '>': self._navigate_to_next_asset,
            '<': self._navigate_to_previous_asset,
            'd': self.make_data_package,
            'nmh': self.make_handmade_material_package,
            'nmm': self.make_managermade_material_package,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_materials = False

    def _get_appropriate_material_manager(
        self,
        material_manager_class_name, 
        path,
        ):
        import scoremanager
        from scoremanager import managers
        assert os.path.sep in path
        material_package_path = self._configuration.path_to_package_path(
            path)
        if material_manager_class_name is None:
            manager = managers.MaterialPackageManager(
                path=path,
                session=self._session,
                )
        else:
            command = 'manager = '
            command += 'scoremanager.managers.{}'
            command += '(path=path, session=self._session)'
            command = command.format(material_manager_class_name)
            try:
                exec(command)
            except AttributeError:
                command = 'from {0}.{1}.{1}'
                command += ' import {1} as material_manager_class'
                path = self._configuration.user_library_material_packages_directory_path
                package_path = self._configuration.path_to_package_path(path)
                command = command.format(
                    package_path,
                    material_manager_class_name,
                    )
                exec(command)
                manager = material_manager_class(
                    material_package_path, 
                    session=self._session,
                    )
        return manager

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            material_manager = self._initialize_asset_manager(result)
            if os.path.exists(material_manager._path):
                material_manager._run()

    def _initialize_asset_manager(self, package_path):
        wrangler = self._material_manager_wrangler
        manager = wrangler._initialize_asset_manager(package_path)
        return manager

    def _is_valid_directory_entry(self, expr):
        superclass = super(MaterialPackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _list_asset_paths(
        self, 
        abjad_library=True,
        user_library=True,
        abjad_score_packages=True,
        user_score_packages=True,
        generic_output_name='',
        output_class_name='',
        ):
        from scoremanager import managers
        superclass = super(MaterialPackageWrangler, self)
        paths = superclass._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )
        if not generic_output_name and not output_class_name:
            return paths
        result = []
        for path in paths:
            manager = managers.DirectoryManager(
                path=path,
                session=self._session,
                )
            metadatum = manager._get_metadatum('generic_output_name')
            if metadatum and metadatum == generic_output_name:
                result.append(path)
                continue
            metadatum = manager._get_metadatum('output_class_name')
            if metadatum and metadatum == output_class_name:
                result.append(path)
                continue
        return result

    def _make_data_package(self, path, metadata=None):
        metadata = metadata or {}
        self._make_material_package(path, metadata=metadata)

    def _make_handmade_material_package(self, path, metadata=None):
        metadata = metadata or {}
        self._make_material_package(path, metadata=metadata)

    # TODO: encapsulate in separate methods
    def _make_main_menu(self, name='material package wrangler'):
        menu = self._io_manager.make_menu(
            where=self._where,
            name=name,
            )
        asset_menu_entries = self._make_asset_menu_entries()
        if asset_menu_entries:
            section = menu.make_asset_section(name='assets')
            for menu_entry in asset_menu_entries:
                section.append(menu_entry)
        section = menu.make_command_section(name='material')
        section.append(('material - new by hand', 'nmh'))
        section.append(('material - new with manager', 'nmm'))
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _make_managermade_material_package(
        self,
        path, 
        material_manager_class_name, 
        metadata=None,
        ):
        metadata = metadata or {}
        command = 'from scoremanager.managers '
        command += 'import {} as material_manager_class'
        command = command.format(material_manager_class_name)
        try:
            exec(command)
        except ImportError:
            command = 'from {} import {} as material_manager_class'
            path = self._configuration.user_library_material_packages_directory_path
            package_path = self._configuration.path_to_package_path(path)
            command = command.format(
                package_path,
                material_manager_class_name,
                )
            try:
                exec(command)
            except:
                traceback.print_exc()
        if material_manager_class_name is not None:
            metadata['material_manager_class_name'] = \
                material_manager_class_name
        self._make_material_package(path, metadata=metadata)

    def _make_material_package(
        self, 
        path,
        prompt=False, 
        metadata=None,
        ):
        assert os.path.sep in path
        metadata = collections.OrderedDict(metadata or {})
        assert not os.path.exists(path)
        os.mkdir(path)
        string = 'material_manager_class_name'
        material_manager_class_name = metadata.get(string)
        pair = (material_manager_class_name, path)
        manager = self._get_appropriate_material_manager(*pair)
        manager._initializer_file_manager._write_stub()
        manager.rewrite_metadata_module(
            metadata, 
            prompt=False,
            )
        if not manager._read_material_manager_class_name():
            manager._write_definition_module_stub(prompt=False)
        if manager._user_input_wrapper_in_memory:
            manager._write_user_input_module_stub()
        message = 'material package created: {!r}.'.format(path)
        self._io_manager.proceed(message=message, prompt=prompt)

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_score_materials = True

    ### PUBLIC METHODS ###

    def make_data_package(self, metadata=None):
        r'''Makes data package.

        Returns none.
        '''
        if self._session.is_in_score:
            storehouse_path = self._current_storehouse_path
        else:
            storehouse_path = self._user_storehouse_path
        path = self.get_available_path(storehouse_path=storehouse_path)
        if self._should_backtrack():
            return
        self._make_data_package(path, metadata=metadata)

    def make_handmade_material_package(self):
        r'''Makes handmade material package.

        Returns none.
        '''
        if self._session.is_in_score:
            storehouse_path = self._current_storehouse_path
        else:
            storehouse_path = self._user_storehouse_path
        path = self.get_available_path(storehouse_path=storehouse_path)
        if self._should_backtrack():
            return
        self._make_handmade_material_package(path)

    def make_managermade_material_package(self):
        r'''Makes managermade material package.

        Returns none.
        '''
        wrangler = self._material_manager_wrangler
        result = wrangler.select_asset_package_path()
        if self._should_backtrack():
            return
        material_manager_package_path = result
        material_manager_class_name = \
            material_manager_package_path.split('.')[-1]
        if self._session.is_in_score:
            storehouse_path = self._current_storehouse_path
        else:
            storehouse_path = self._user_storehouse_path
        path = self.get_available_path(storehouse_path=storehouse_path)
        if self._should_backtrack():
            return
        self._make_managermade_material_package(
            path, 
            material_manager_class_name,
            )
        manager = self._get_appropriate_material_manager(
            material_manager_class_name, 
            path,
            )
        manager._run_first_time()