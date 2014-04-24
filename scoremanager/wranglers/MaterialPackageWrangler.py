# -*- encoding: utf-8 -*-
import collections
import os
import traceback
from abjad.tools import systemtools
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
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(MaterialPackageWrangler, self)
        superclass.__init__(session=session)
        configuration = self._configuration
        path = configuration.abjad_material_packages_directory_path
        self._abjad_storehouse_path = path
        path = configuration.user_library_material_packages_directory_path
        self._user_storehouse_path = path
        self._score_storehouse_path_infix_parts = ('materials',)
        self._asset_identifier = 'material package'
        self._manager_class = managers.MaterialPackageManager

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        breadcrumb = 'materials'
        view_name = self._read_view_name()
        if not view_name:
            return breadcrumb
        view_inventory = self._read_view_inventory()
        if view_name in view_inventory:
            breadcrumb = '{} ({})'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _user_input_to_action(self):
        superclass = super(MaterialPackageWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            '>': self._navigate_to_next_asset,
            '<': self._navigate_to_previous_asset,
            'cp': self.copy_material_package,
            'new': self.make_material_package,
            'ren': self.rename_material_package,
            'rm': self.remove_material_packages,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_materials = False

    def _get_material_package_manager(self, class_name, path):
        import scoremanager
        from scoremanager import managers
        assert os.path.sep in path
        assert class_name is not None
        command = 'manager = scoremanager.managers.{}'
        command += '(path=path, session=self._session)'
        command = command.format(class_name)
        try:
            exec(command)
            return manager
        except AttributeError:
            pass
        command = 'from {0}.{1}.{1} import {1} as class_'
        configuration = self._configuration
        library_path = \
            configuration.user_library_material_packages_directory_path
        package_path = self._configuration.path_to_package_path(library_path)
        command = command.format(
            package_path,
            class_name,
            )
        try:
            exec(command)
        except ImportError:
            return
        package_path = self._configuration.path_to_package_path(path)
        manager = class_(package_path, session=self._session)
        return manager

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            manager = self._initialize_manager(result)
            if os.path.exists(manager._path):
                manager._run()

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
        example_score_packages=True,
        user_score_packages=True,
        output_material_class_name='',
        ):
        from scoremanager import managers
        superclass = super(MaterialPackageWrangler, self)
        paths = superclass._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        if not output_material_class_name:
            return paths
        result = []
        for path in paths:
            manager = managers.DirectoryManager(
                path=path,
                session=self._session,
                )
            metadatum = manager._get_metadatum('output_material_class_name')
            if metadatum and metadatum == output_material_class_name:
                result.append(path)
        return result

    def _make_asset_menu_section(self, menu):
        include_annotation = not self._session.is_in_score
        entries = self._make_asset_menu_entries(
            include_annotation=include_annotation,
            )
        if not entries:
            return
        menu.make_asset_section(
            menu_entries=entries,
            )

    def _make_main_menu(self, name='material package wrangler'):
        superclass = super(MaterialPackageWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_material_command_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _make_material_command_menu_section(self, menu):
        commands = []
        commands.append(('materials - copy', 'cp'))
        commands.append(('materials - new', 'new'))
        commands.append(('materials - remove', 'rm'))
        commands.append(('materials - rename', 'ren'))
        menu.make_command_section(
            commands=commands,
            name='material',
            )

    # TODO: migrate to MaterialPackageManager
    def _make_material_package(
        self,
        path,
        prompt=False,
        metadata=None,
        definition_module_stub=True,
        ):
        from scoremanager import managers
        assert os.path.sep in path
        metadata = collections.OrderedDict(metadata or {})
        assert not os.path.exists(path)
        os.mkdir(path)
        manager = managers.MaterialPackageManager(
            path=path,
            session=self._session,
            )
        manager._initializer_file_manager._write_stub()
        manager.rewrite_metadata_module(metadata, prompt=False)
        if definition_module_stub:
            manager._write_definition_module_stub(prompt=False)
        message = 'material package created: {!r}.'.format(path)
        self._io_manager.proceed(message=message, prompt=prompt)

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_score_materials = True

    ### PUBLIC METHODS ###

    def copy_material_package(self):
        r'''Copies material package.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def make_material_package(self):
        r'''Makes material package.

        Returns none.
        '''
        if self._session.is_in_score:
            storehouse_path = self._current_storehouse_path
        else:
            storehouse_path = self._user_storehouse_path
        prompt_string = 'Enter material package name'
        path = self._get_available_path(
            prompt_string=prompt_string,
            storehouse_path=storehouse_path,
            )
        if self._should_backtrack():
            return
        if not path:
            return
        self._make_material_package(path)
        manager = self._get_manager(path)
        manager._run()

    def remove_material_packages(self):
        r'''Removes material package.

        Returns none.
        '''
        self._remove_assets()

    def rename_material_package(self):
        r'''Renames material package.

        Returns none.
        '''
        self._rename_asset()