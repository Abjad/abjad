# -*- encoding: utf-8 -*-
import collections
import os
import traceback
from abjad.tools import systemtools
from scoremanager.idetools.ScoreInternalPackageWrangler import \
    ScoreInternalPackageWrangler


class MaterialPackageWrangler(ScoreInternalPackageWrangler):
    r'''Material package wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.idetools.Session()
            >>> wrangler = scoremanager.idetools.MaterialPackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MaterialPackageWrangler()

    ..  container:: example

        ::

            >>> session = scoremanager.idetools.Session()
            >>> session._set_test_score('red_example_score')
            >>> wrangler_in_score = scoremanager.idetools.MaterialPackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler_in_score
            MaterialPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_annotate_autoeditor',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import idetools
        superclass = super(MaterialPackageWrangler, self)
        superclass.__init__(session=session)
        configuration = self._configuration
        self._annotate_autoeditor = True
        self._asset_identifier = 'material package'
        self._basic_breadcrumb = 'materials'
        self._in_library = True
        self._manager_class = idetools.MaterialPackageManager
        self._score_storehouse_path_infix_parts = ('materials',)
        path = configuration.materials_library
        self._user_storehouse_path = path

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        superclass = super(MaterialPackageWrangler, self)
        breadcrumb = superclass._breadcrumb
        if self._session.is_in_library:
            breadcrumb = '{} - library'.format(breadcrumb)
        return breadcrumb

    @property
    def _command_to_method(self):
        superclass = super(MaterialPackageWrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'dp*': self.output_every_definition_py,
            #
            'oc*': self.check_every_output_py,
            'oe*': self.edit_every_output_py,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_materials = False

    def _get_material_package_manager(self, class_name, path):
        assert os.path.sep in path
        assert class_name is not None
        command = 'manager = scoremanager.idetools.{}'
        command += '(path=path, session=self._session)'
        command = command.format(class_name)
        try:
            result = self._io_manager.execute_string(
                command,
                attribute_names=('manager',),
                )
            manager = result[0]
            return manager
        except AttributeError:
            pass
        command = 'from {0}.{1}.{1} import {1} as class_'
        configuration = self._configuration
        library_path = \
            configuration.materials_library
        package = self._configuration.path_to_package(library_path)
        command = command.format(
            package,
            class_name,
            )
        try:
            result = self._io_manager.execute_string(
                command,
                attribute_names=('class_',),
                )
            class_ = result[0]
        except ImportError:
            return
        package = self._configuration.path_to_package(path)
        manager = class_(package, session=self._session)
        return manager

    def _handle_numeric_user_input(self, result):
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
        abjad_material_packages_and_stylesheets=True,
        library=True,
        example_score_packages=True,
        user_score_packages=True,
        output_material_class_name='',
        ):
        from scoremanager import idetools
        superclass = super(MaterialPackageWrangler, self)
        paths = superclass._list_asset_paths(
            abjad_material_packages_and_stylesheets=abjad_material_packages_and_stylesheets,
            library=library,
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        if not output_material_class_name:
            return paths
        result = []
        for path in paths:
            manager = idetools.PackageManager(
                path=path,
                session=self._session,
                )
            metadatum = manager._get_metadatum('output_material_class_name')
            if metadatum and metadatum == output_material_class_name:
                result.append(path)
        return result

    def _make_all_packages_menu_section(self, menu):
        superclass = super(MaterialPackageWrangler, self)
        commands = superclass._make_all_packages_menu_section(
            menu, commands_only=True)
        commands.append(('all packages - definition.py - output', 'dp*'))
        commands.append(('all packages - output.py - check', 'oc*'))
        commands.append(('all packages - output.py - edit', 'oe*'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='all packages',
            )

    def _make_main_menu(self):
        superclass = super(MaterialPackageWrangler, self)
        menu = superclass._make_main_menu()
        self._make_all_packages_menu_section(menu)
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

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_materials = True

    ### PUBLIC METHODS ###

    # TODO: factor out check_every_definition_py shared code
    def check_every_output_py(self):
        r'''Checks ``output.py`` in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        method_name = 'check_output_py'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='check')
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        for manager in managers:
            method = getattr(manager, method_name)
            method()

    def copy_package(self):
        r'''Copies package.

        Returns none.
        '''
        self._copy_asset()

    def edit_every_definition_py(self):
        r'''Opens ``definition.py`` in every package.

        Returns none.
        '''
        self._open_in_every_package('definition.py')

    def edit_every_output_py(self):
        r'''Opens ``output.py`` in every package.

        Returns none.
        '''
        self._open_in_every_package('output.py')

    def open_every_illustration_pdf(self):
        r'''Opens ``illustration.pdf`` in every package.

        Returns none.
        '''
        self._open_in_every_package('illustration.pdf')

    def output_every_definition_py(self):
        r'''Outputs ``definition.py`` to ``output.py`` in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        method_name = 'output_definition_py'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='output')
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._io_manager._silent():
            for manager in managers:
                method = getattr(manager, method_name)
                method()

    def remove_packages(self):
        r'''Removes one or more packages.

        Returns none.
        '''
        self._remove_assets()

    def rename_package(self):
        r'''Renames package.

        Returns none.
        '''
        self._rename_asset()