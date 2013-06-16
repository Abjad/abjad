import os
from abjad.tools import iotools
from abjad.tools import mathtools
from experimental.tools.scoremanagertools import wizards
from experimental.tools.scoremanagertools.proxies.PackageProxy \
    import PackageProxy


class MaterialPackageProxy(PackageProxy):
    '''Material package proxy:

    ::

        >>> package_path = \
        ...     'experimental.tools.scoremanagertools.materialpackages.red_numbers'
        >>> mpp = scoremanagertools.proxies.MaterialPackageProxy(package_path)
        >>> mpp
        MaterialPackageProxy('.../scoremanagertools/materialpackages/red_numbers')

    Return material package proxy.
    '''

    ### CLASS VARIABLES ###

    should_have_user_input_module = False

    ### INTIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        PackageProxy.__init__(self, 
            packagesystem_path=packagesystem_path, session=session)
        self._generic_output_name = None
        self.stylesheet_file_name_in_memory = None

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self._space_delimited_lowercase_name

    ### PRIVATE METHODS ###

    # TODO: audit
    def _handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        elif mathtools.is_integer_equivalent_expr(result):
            self.interactively_edit_user_input_wrapper_at_number(
                result, include_newline=False)
        else:
            raise ValueError

    def _make_main_menu(self):
        menu, hidden_section = self._io.make_menu(where=self._where)
        hidden_section.return_value_attribute = 'key'
        hidden_section.is_hidden = True
        self._make_main_menu_section_for_initializer(menu, hidden_section)
        self._make_main_menu_sections(menu, hidden_section)
        self._make_main_menu_section_for_illustration_ly(hidden_section)
        self._make_main_menu_section_for_illustration_pdf(menu, hidden_section)
        self._make_main_menu_section_for_hidden_entries(menu)
        return menu

    def _make_main_menu_section_for_hidden_entries(self, main_menu):
        hidden_section = main_menu.make_section()
        hidden_section.return_value_attribute='key'
        hidden_section.is_hidden = True
        hidden_section.append(('delete package', 'rm'))
        hidden_section.append(('list package', 'ls'))
        hidden_section.append(('rename package', 'ren'))
        hidden_section.append(('manage stylesheets', 'stl'))
        hidden_section.append(('manage tags', 'tags'))

    def _make_main_menu_section_for_illustration_builder(self, 
        main_menu, hidden_section):
        if self.has_output_material:
            if self.should_have_illustration:
                if not self.has_illustration_builder_module:
                    material_package_path = self.package_path
                    material_package_name = \
                        material_package_path.split('.')[-1]
                    self.illustration_builder_module_proxy.write_stub_to_disk(
                        material_package_path,
                        material_package_name,
                        prompt=False)
                menu_section = main_menu.make_section()
                menu_section.return_value_attribute = 'key'
                menu_section.append(
                    ('illustration builder - edit', 'ibe'))
                if self.has_output_material:
                    menu_section.append(
                        ('illustration builder - execute', 'ibx'))
                hidden_section.append(
                    ('illustration builder - delete', 'ibd'))
                hidden_section.append(
                    ('illustration builder - stub', 'ibt'))
                hidden_section.append(
                    ('illustration builder - edit & execute', 'ibex'))
                menu_section.append(
                    ('score stylesheet - select', 'sss'))
                hidden_section.append(
                    ('source stylesheet - edit', 'ssm'))

    def _make_main_menu_section_for_illustration_ly(self, hidden_section):
        if self.has_output_material:
            if self.has_illustration_builder_module or \
                self.has_material_package_maker:
                hidden_section.append(('output ly - make', 'lym'))
        if self.has_illustration_ly:
            hidden_section.append(('output ly - delete', 'lyd'))
            hidden_section.append(('output ly - view', 'lyv'))

    def _make_main_menu_section_for_illustration_pdf(self, 
        main_menu, hidden_section):
        has_illustration_pdf_section = False
        if self.has_output_material:
            if self.has_illustration_builder_module or \
                (self.has_material_package_maker and 
                getattr(self, 'illustration_maker', None)):
                menu_section = main_menu.make_section()
                menu_section.return_value_attribute = 'key'
                menu_section.append(('output pdf - make', 'pdf'))
                has_illustration_pdf_section = True
        if self.has_illustration_pdf:
            if not has_illustration_pdf_section:
                menu_section = main_menu.make_section()
                menu_section.return_value_attribute = 'key'
            hidden_section.append(('output pdf - delete', 'pdfd'))
            menu_section.append(('output pdf - view', 'pdfv'))

    def _make_main_menu_section_for_initializer(self, 
        main_menu, hidden_section):
        if not self.has_initializer:
            menu_section = main_menu.make_section()
            menu_section.title = '(Note: package has no initializer.)'
        hidden_section.append(('initializer - restore', 'inr'))
        hidden_section.append(('view package initializer', 'inv'))
        hidden_section.append(('copy canned package initializer', 'incanned'))
        hidden_section.append(('write stub package initializer', 'instub'))

    def _make_main_menu_section_for_material_definition(self, 
        main_menu, hidden_section):
        if not self.has_initializer:
            return
        if self.has_material_definition_module:
            menu_section = main_menu.make_section()
            menu_section.return_value_attribute = 'key'
            menu_section.append(
                ('material definition - edit', 'mde'))
            menu_section.append(
                ('material definition - execute', 'mdx'))
            hidden_section.append(
                ('material definition - copy canned module', 'mdcanned'))
            hidden_section.append(
                ('material definition - delete', 'mddelete'))
            hidden_section.append(
                ('material definition - stub', 'mdstub'))
            hidden_section.append(
                ('material definition - execute & edit', 'mdxe'))
        elif self.material_package_maker_class_name is None:
            menu_section = main_menu.make_section()
            menu_section.return_value_attribute = 'key'
            menu_section.append(
                ('material definition - stub', 'mdstub'))

    def _make_main_menu_section_for_output_material(self, 
        main_menu, hidden_section):
        if not self.has_initializer:
            return
        has_output_material_section = False
        if self.has_material_definition_module or \
            self.has_complete_user_input_wrapper_in_memory or \
            self.has_output_material_editor:
            if self.has_material_definition or \
                self.has_complete_user_input_wrapper_in_memory:
                menu_section = main_menu.make_section()
                menu_section.return_value_attribute = 'key'
                menu_section.append(('output material = make', 'omm'))
                has_output_material_section = True
            if self.has_output_material_editor:
                menu_section = main_menu.make_section()
                menu_section.return_value_attribute = 'key'
                menu_section.append(('output material - interact', 'omi'))
                if self.has_output_material:
                    output_material_editor = self.output_material_editor(
                        target=self.output_material, 
                        session=self._session)
                    target_summary_lines = \
                        output_material_editor.target_summary_lines
                    if target_summary_lines:
                        menu_section.title = target_summary_lines
                has_output_material_section = True
            if self.has_output_material_module:
                if not has_output_material_section:
                    menu_section = main_menu.make_section()
                    menu_section.return_value_attribute = 'key'
                menu_section.append(
                    ('output material - view', 'omv'))
                hidden_section.append(
                    ('output material - delete', 'omdelete'))
                hidden_section.append(
                    ('output material - fetch', 'omfetch'))
        hidden_section.append(
            ('output material - copy canned module', 'omcanned'))

    def _make_main_menu_sections(self, menu, hidden_section):
        self._make_main_menu_section_for_material_definition(
            menu, hidden_section)
        self._make_main_menu_section_for_output_material(
            menu, hidden_section)
        self._make_main_menu_section_for_illustration_builder(
            menu, hidden_section)

    ### PUBLIC PROPERTIES ###

    @property
    def has_complete_user_input_wrapper_in_memory(self):
        if self.has_user_input_wrapper_in_memory:
            return self.user_input_wrapper_in_memory.is_complete
        return False

    @property
    def has_complete_user_input_wrapper_on_disk(self):
        if self.has_user_input_wrapper_on_disk:
            return self.user_input_wrapper_on_disk.is_complete

    @property
    def has_illustration_builder_module(self):
        if self.should_have_illustration_builder_module:
            return os.path.exists(self.illustration_builder_module_file_name)
        return False

    @property
    def has_illustration_ly(self):
        if self.should_have_illustration_ly:
            return os.path.exists(self.illustration_ly_file_name)
        return False

    @property
    def has_illustration_pdf(self):
        if self.should_have_illustration_pdf:
            return os.path.exists(self.illustration_pdf_file_name)
        return False

    @property
    def has_initializer(self):
        if self.should_have_initializer:
            return os.path.exists(self.initializer_file_name)
        return False

    @property
    def has_material_definition(self):
        if self.should_have_material_definition_module:
            if self.has_material_definition_module:
                return bool(self.material_definition)
        return False

    @property
    def has_material_definition_module(self):
        if self.should_have_material_definition_module:
            return os.path.exists(self.material_definition_module_file_name)
        return False

    @property
    def has_material_package_maker(self):
        return bool(self.material_package_maker_class_name)

    @property
    def has_output_material(self):
        if self.should_have_output_material_module:
            if self.has_output_material_module:
                return True
        return False

    @property
    def has_output_material_editor(self):
        return bool(getattr(self, 'output_material_editor', None))

    @property
    def has_output_material_module(self):
        if self.should_have_output_material_module:
            return os.path.exists(self.output_material_module_file_name)
        return False

    # TODO: impelement
    @property
    def has_stylesheet(self):
        return False

    @property
    def has_user_finalized_illustration_builder_module(self):
        if self.has_illustration_builder_module:
            if self.illustration_builder_module_proxy.read_file():
                return self.illustration_builder_module_proxy.is_user_finalized

    @property
    def has_user_finalized_material_definition_module(self):
        if self.has_material_definition_module:
            return self.material_definition_module_proxy.is_user_finalized
        return False

    @property
    def has_user_input_module(self):
        if self.should_have_user_input_module:
            return os.path.exists(self.user_input_module_file_name)
        return False

    @property
    def has_user_input_wrapper_in_memory(self):
        if self.should_have_user_input_module:
            return bool(self.user_input_wrapper_in_memory)
        return False

    @property
    def has_user_input_wrapper_on_disk(self):
        if self.should_have_user_input_module:
            return bool(
                self.user_input_module_proxy.read_user_input_wrapper_from_disk())
        return False

    @property
    def illustration(self):
        if self.has_illustration_builder_module:
            return self.illustration_builder_module_proxy.import_illustration()

    @property
    def illustration_builder_module_file_name(self):
        if self.should_have_illustration_builder_module:
            return os.path.join(self.filesystem_path, 'illustration_builder.py')

    @property
    def illustration_builder_module_proxy(self):
        from experimental.tools import scoremanagertools
        if self.should_have_illustration_builder_module:
            if not self.has_illustration_builder_module:
                file(self.illustration_builder_module_file_name, 'w').write('')
            return scoremanagertools.proxies.IllustrationBuilderModuleProxy(
                self.illustration_builder_packagesystem_path, 
                session=self._session)

    @property
    def illustration_builder_packagesystem_path(self):
        if self.should_have_illustration_builder_module:
            return '.'.join([self.package_path, 'illustration_builder'])

    @property
    def illustration_ly_file_name(self):
        if self.should_have_illustration_ly:
            return os.path.join(self.filesystem_path, 'illustration.ly')

    @property
    def illustration_ly_file_proxy(self):
        from experimental.tools import scoremanagertools
        if self.should_have_illustration_ly:
            if not self.has_illustration_ly:
                file(self.illustration_ly_file_name, 'w').write('')
            return scoremanagertools.proxies.IllustrationLyFileProxy(
                self.illustration_ly_file_name, session=self._session)

    @property
    def illustration_pdf_file_name(self):
        if self.should_have_illustration_pdf:
            return os.path.join(self.filesystem_path, 'illustration.pdf')

    @property
    def illustration_pdf_file_proxy(self):
        from experimental.tools import scoremanagertools
        if self.should_have_illustration_pdf:
            if not self.has_illustration_pdf:
                file(self.illustration_pdf_file_name, 'w').write('')
            return scoremanagertools.proxies.IllustrationPdfFileProxy(
                self.illustration_pdf_file_name, session=self._session)

    @property
    def illustration_with_stylesheet(self):
        illustration = self.illustration
        if illustration and self.stylesheet_file_name_in_memory:
            illustration.file_initial_user_includes.append(
                self.stylesheet_file_name_in_memory)
        return illustration

    # TODO: port
    @property
    def is_changed(self):
        self._io.print_not_yet_implemented()
        material_definition = \
            self.material_definition_module_proxy.import_material_definition()
        output_material = \
            self.output_material_module_proxy.import_output_material_safely()
        return material_definition != output_material

    @property
    def is_data_only(self):
        return not self.should_have_illustration

    @property
    def is_handmade(self):
        return not(self.has_material_package_maker)

    @property
    def is_makermade(self):
        return self.has_material_package_maker

    # TODO: replace with method
    # TODO: replace with self.material_definition_module_proxy.material_definition
    @property
    def material_definition(self):
        if self.has_material_definition_module:
            if self.material_definition_module_proxy.read_file():
                pair = self.output_material_module_import_statements_and_material_definition
                material_definition = pair[1]
                return material_definition

    @property
    def material_definition_module_file_name(self):
        if self.should_have_material_definition_module:
            return os.path.join(self.filesystem_path, 'material_definition.py')

    @property
    def material_definition_module_proxy(self):
        from experimental.tools import scoremanagertools
        if self.should_have_material_definition_module:
            return scoremanagertools.proxies.MaterialDefinitionModuleProxy(
                self.material_definition_packagesystem_path, session=self._session)

    @property
    def material_definition_packagesystem_path(self):
        if self.should_have_material_definition_module:
            return '.'.join([self.package_path, 'material_definition'])

    @property
    def material_package_directory(self):
        if self._session.current_materials_directory_path:
            if self.material_package_name:
                return os.path.join(
                    self._session.current_materials_directory_path, 
                    self.material_package_name)

    @property
    def material_package_maker(self):
        if self.material_package_maker_class_name is not None:
            maker_class = self._safe_import(
                locals(), 
                'materialpackagemakers', 
                self.material_package_maker_class_name,
                source_parent_package_path=self.configuration.score_manager_tools_package_path)
            return maker_class

    @property
    def material_package_maker_class_name(self):
        return self.get_tag('material_package_maker_class_name')

    @property
    def material_package_name(self):
        return self.filesystem_basename

    @property
    def output_material(self):
        if self.has_output_material_module:
            if self.output_material_module_proxy.read_file():
                return self.output_material_module_proxy.import_output_material()

    @property
    def output_material_module_body_lines(self):
        if self.should_have_material_definition_module:
            return self.output_material_module_import_statements_and_output_material_module_body_lines[1]

    @property
    def output_material_module_file_name(self):
        if self.should_have_output_material_module:
            return os.path.join(self.filesystem_path, 'output_material.py')

    @property
    def output_material_module_import_statements_and_material_definition(self):
        if self.should_have_material_definition_module:
            tmp = self.material_definition_module_proxy
            return tmp.import_output_material_module_import_statements_and_material_definition()

    @property
    def output_material_module_import_statements_and_output_material_module_body_lines(self):
        if self.should_have_material_definition_module:
            pair = self.output_material_module_import_statements_and_material_definition
            output_material_module_import_statements, output_material = pair
        elif self.has_material_package_maker:
            output_material_module_import_statements = \
                self.output_material_module_import_statements
            output_material = \
                self.make_output_material_from_user_input_wrapper_in_memory()
        else:
            raise ValueError
        if hasattr(self, 'make_output_material_module_body_lines'):
            output_material_module_body_lines = \
                self.make_output_material_module_body_lines(output_material)
        else:
            line = '{} = {}'.format(
                self.material_package_name, 
                self.get_tools_package_qualified_repr(output_material))
            output_material_module_body_lines = [line]
        return (output_material_module_import_statements, 
            output_material_module_body_lines)

    @property
    def output_material_module_path(self):
        if self.should_have_output_material_module:
            return '{}.output_material'.format(self.package_path)

    @property
    def output_material_module_proxy(self):
        from experimental.tools import scoremanagertools
        if self.should_have_output_material_module:
            if self.has_output_material_module:
                return scoremanagertools.proxies.OutputMaterialModuleProxy(
                    self.output_material_module_path, session=self._session)

    @property
    def should_have_illustration(self):
        return self.get_tag('should_have_illustration')

    @property
    def should_have_illustration_builder_module(self):
        if self.should_have_illustration:
            if self.material_package_maker_class_name is None:
                return True
        return False

    @property
    def should_have_illustration_ly(self):
        return self.should_have_illustration

    @property
    def should_have_illustration_pdf(self):
        return self.should_have_illustration

    @property
    def should_have_initializer(self):
        return True

    @property
    def should_have_material_definition_module(self):
        return self.material_package_maker_class_name is None

    @property
    def should_have_output_material_module(self):
        return True

    @property
    def should_have_stylesheet(self):
        return self.should_have_illustration

    @property
    def space_delimited_material_package_name(self):
        return self.material_package_name.replace('_', ' ')

    @property
    def stylesheet_file_name_on_disk(self):
        if self.has_illustration_ly:
            for line in self.illustration_ly_file_proxy.read_lines():
                if line.startswith(r'\include') and 'stylesheets' in line:
                    file_name = line.split()[-1].replace('"', '')
                    return file_name

    @property
    def stylesheet_file_proxy(self):
        from experimental.tools import scoremanagertools
        if self.should_have_stylesheet:
            return scoremanagertools.proxies.StylesheetFileProxy(
                self.stylesheet_file_name, session=self._session)

    @property
    def user_input_module_file_name(self):
        if self.should_have_user_input_module:
            return os.path.join(self.filesystem_path, 'user_input.py')

    @property
    def user_input_module_packagesystem_path(self):
        if self.should_have_user_input_module:
            return '.'.join([self.package_path, 'user_input'])

    @property
    def user_input_module_proxy(self):
        from experimental.tools import scoremanagertools
        if self.should_have_user_input_module:
            if not self.has_user_input_module:
                file(self.user_input_module_file_name, 'w').write('')
            return scoremanagertools.proxies.UserInputModuleProxy(
                self.user_input_module_packagesystem_path, 
                session=self._session)

    ### PUBLIC METHODS ###

    def conditionally_write_stub_material_definition_module_to_disk(self, 
        is_interactive=False):
        if not self.get_tag('material_package_maker_class_name'):
            is_data_only = not self.get_tag('should_have_illustration')
            self.material_definition_module_proxy.write_stub_to_disk(
                is_data_only, is_interactive=is_interactive)

    def conditionally_write_stub_user_input_module_to_disk(self, 
        is_interactive=False):
        if self.should_have_user_input_module:
            self.write_stub_user_input_module_to_disk(
                is_interactive=is_interactive)

    def display_output_material(self):
        self.output_material_module_proxy.display_output_material()

    def get_tools_package_qualified_repr(self, expr):
        return getattr(expr, '_tools_package_qualified_repr', repr(expr))

    def interactively_edit_illustration_builder_module(self):
        self.illustration_builder_module_proxy.edit()

    def interactively_edit_material_definition_module(self):
        self.material_definition_module_proxy.edit()

    def interactively_edit_output_material(self):
        if not self.has_output_material_editor:
            return
        output_material = self.output_material
        if not hasattr(self, 'output_material_maker'):
            output_material_handler_callable = self.output_material_editor
        elif output_material is None and self.output_material_maker and \
            issubclass(self.output_material_maker, wizards.Wizard):
            output_material_handler_callable = self.output_material_maker
        else:
            output_material_handler_callable = self.output_material_editor
        output_material_handler = output_material_handler_callable(
            target=output_material, session=self._session)
        output_material_handler._run()
        if self._session.backtrack():
            return
        output_material_module_import_statements = \
            self.output_material_module_import_statements
        if hasattr(self, 'make_output_material_module_body_lines'):
            output_material_module_body_lines = \
                self.make_output_material_module_body_lines(
                output_material_handler.target)
        else:
            line = '{} = {}'.format(
                self.material_package_name,
                self.get_tools_package_qualified_repr(
                    output_material_handler.target))
            output_material_module_body_lines = [line]
        self.write_output_material_to_disk(
            output_material_module_import_statements=output_material_module_import_statements,
            output_material_module_body_lines=output_material_module_body_lines)

    def interactively_edit_stylesheet_file(self):
        self.stylesheet_file_proxy.edit()

    def interactively_remove(self):
        #self.remove_material_from_materials_initializer()
        PackageProxy.interactively_remove(self)

    def interactively_rename_material(self):
        line = 'current material name: {}'.format(self.material_package_name)
        self._io.display(line)
        getter = self._io.make_getter(where=self._where)
        getter.append_underscore_delimited_lowercase_package_name('new material name')
        new_material_package_name = getter._run()
        if self._session.backtrack():
            return
        lines = []
        lines.append('current material name: {}'.format(
            self.material_package_name))
        lines.append('new material name:     {}'.format(
            new_material_package_name))
        lines.append('')
        self._io.display(lines)
        if not self._io.confirm():
            return
        if self.is_versioned():
            # rename package directory
            new_directory_path = self.filesystem_path.replace(
                self.material_package_name, new_material_package_name)
            command = 'svn mv {} {}'.format(
                self.filesystem_path, new_directory_path)
            os.system(command)
            # update package initializer
            parent_directory_filesystem_path = \
                os.path.dirname(self.filesystem_path)
            new_package_directory = os.path.join(
                parent_directory_filesystem_path, 
                new_material_package_name)
            new_initializer = os.path.join(
                new_package_directory, '__init__.py')
            self.replace_in_file(
                new_initializer, 
                self.material_package_name, 
                new_material_package_name)
            # rename output material
            new_output_material = os.path.join(
                new_package_directory, 
                'output_material.py')
            self.replace_in_file(
                new_output_material, 
                self.material_package_name, 
                new_material_package_name)
            # commit
            commit_message = 'renamed {} to {}.'.format(
                self.material_package_name, 
                new_material_package_name)
            commit_message = commit_message.replace('_', ' ')
            command = 'svn commit -m "{}" {}'.format(
                commit_message, 
                self.parent_directory_filesystem_path)
            os.system(command)
            # update path name to reflect change
            self._path = new_package_directory
        else:
            raise NotImplementedError('commit to repository and then rename.')

    def interactively_select_material_package_maker(self, prompt=True):
        from experimental.tools import scoremanagertools
        material_proxy_wrangler = \
            scoremanagertools.wranglers.MaterialPackageMakerWrangler(
            session=self._session)
        with self.backtracking:
            material_package_maker = \
                material_proxy_wrangler.select_material_proxy_class_name_interactively()
        if self._session.backtrack():
            return
        self.add_tag('material_package_maker', material_package_maker.class_name)
        line = 'user input handler selected.'
        self._io.proceed(line, is_interactive=prompt)

    def interactively_select_stylesheet(self, prompt=True):
        from experimental.tools import scoremanagertools
        stylesheet_file_wrangler = \
            scoremanagertools.wranglers.StylesheetFileWrangler(
            session=self._session)
        with self.backtracking:
            stylesheet_file_name = stylesheet_file_wrangler.interactively_select_asset_filesystem_path()
        if self._session.backtrack():
            return
        self.stylesheet_file_name_in_memory = stylesheet_file_name
        self._io.proceed('stylesheet selected.', is_interactive=prompt)

    def interactively_view_illustration_ly(self):
        self.illustration_ly_file_proxy.view()

    def interactively_view_illustration_pdf(self):
        self.illustration_pdf_file_proxy.view()

    def interactively_view_output_material_module(self):
        self.output_material_module_proxy.view()

    def interactively_write_material_definition_module_boilerplate(self):
        self.material_definition_module_proxy.interactively_write_boilerplate()

    def interactively_write_output_material_module_boilerplate(self):
        self.output_material_module_proxy.interactively_write_boilerplate()

    def manage_stylesheets(self):
        from experimental.tools import scoremanagertools
        stylesheet_file_wrangler = \
            scoremanagertools.wranglers.StylesheetFileWrangler(
            session=self._session)
        stylesheet_file_wrangler._run()

    def overwrite_output_material_module(self):
        file(self.output_material_module_file_name, 'w').write('')

    def remove(self):
        #self.remove_material_from_materials_initializer()
        PackageProxy.remove(self)

    def remove_illustration_builder_module(self, prompt=True):
        self.remove_illustration_pdf(prompt=False)
        if self.has_illustration_builder_module:
            self.illustration_builder_module_proxy.remove()

    def remove_illustration_ly(self, prompt=True):
        if self.has_illustration_ly:
            self.illustration_ly_file_proxy.remove()

    def remove_illustration_pdf(self, prompt=True):
        self.remove_illustration_ly(prompt=False)
        if self.has_illustration_pdf:
            self.illustration_pdf_file_proxy.remove()

    def remove_material_definition_module(self, prompt=True):
        self.remove_output_material_module(prompt=False)
        self.remove_illustration_builder_module(prompt=False)
        if self.has_material_definition_module:
            self.material_definition_module_proxy.remove()

    def remove_material_package(self):
        self.remove()
        self._session.is_backtracking_locally = True

    def remove_output_material_module(self, prompt=True):
        self.remove_illustration_builder_module(prompt=False)
        if self.has_output_material_module:
            self.output_material_module_proxy.remove()

    def remove_user_input_module(self, prompt=True):
        if self.has_user_input_module:
            self.user_input_module_proxy.remove()

    @staticmethod
    def replace_in_file(file_path, old, new):
        file_pointer = file(file_path, 'r')
        new_file_lines = []
        for line in file_pointer.readlines():
            line = line.replace(old, new)
            new_file_lines.append(line)
        file_pointer.close()
        file_pointer = file(file_path, 'w')
        file_pointer.write(''.join(new_file_lines))
        file_pointer.close()

    def run_abjad_on_illustration_builder_module(self):
        self.illustration_builder_module_proxy.run_abjad(prompt=True)

    def run_abjad_on_material_definition_module(self):
        self.material_definition_module_proxy.run_abjad()

    def run_first_time(self):
        self._run(user_input='omi')

    def run_python_on_illustration_builder_module(self):
        self.illustration_builder_module_proxy.run_python(prompt=True)

    def run_python_on_material_definition_module(self):
        self.material_definition_module_proxy.run_python()

    def write_illustration_ly_and_pdf_to_disk(self, prompt=True):
        illustration = self.illustration_with_stylesheet
        iotools.write_expr_to_pdf(
            illustration, 
            self.illustration_pdf_file_name, 
            print_status=False)
        iotools.write_expr_to_ly(
            illustration, 
            self.illustration_ly_file_name, 
            print_status=False)
        self._io.proceed(
            'PDF and LilyPond file written to disk.', 
            is_interactive=prompt)

    def write_illustration_ly_to_disk(self, prompt=True):
        illustration = self.illustration_with_stylesheet
        iotools.write_expr_to_ly(
            illustration, 
            self.illustration_ly_file_name, 
            print_status=False)
        self._io.proceed(
            'LilyPond file written to disk.', 
            is_interactive=prompt)

    def write_illustration_pdf_to_disk(self, prompt=True):
        illustration = self.illustration_with_stylesheet
        iotools.write_expr_to_pdf(
            illustration, 
            self.illustration_pdf_file_name, 
            print_status=False)
        self._io.proceed(
            'PDF written to disk.', 
            is_interactive=prompt)

    def write_output_material_to_disk(self, 
        output_material_module_import_statements=None,
        output_material_module_body_lines=None, 
        prompt=True):
        #self.remove_material_from_materials_initializer()
        self.overwrite_output_material_module()
        output_material_module_proxy = self.output_material_module_proxy
        if output_material_module_import_statements is None or \
            output_material_module_body_lines is None:
            pair = self.output_material_module_import_statements_and_output_material_module_body_lines
            output_material_module_import_statements, output_material_module_body_lines = pair
        output_material_module_import_statements = [
            x + '\n' for x in output_material_module_import_statements]
        output_material_module_proxy.setup_statements = \
            output_material_module_import_statements
        output_material_module_proxy.body_lines[:] = \
            output_material_module_body_lines
        output_material_module_proxy.write_to_disk()
        self.write_tags_to_disk()
        self._io.proceed(
            'output material written to disk.', 
            is_interactive=prompt)

    def write_stub_illustration_builder_module_to_disk(self):
        self.illustration_builder_module_proxy.write_stub_to_disk(prompt=True)

    def write_stub_material_definition_module_to_disk(self):
        if self.should_have_material_definition_module:
            file(self.material_definition_module_file_name, 'w').write('')
            self.material_definition_module_proxy.write_stub_to_disk(
                self.is_data_only, is_interactive=True)

    def write_tags_to_disk(self):
        self.add_tag('is_material_package', True)
        if hasattr(self, 'generic_output_name'):
            self.add_tag('generic_output_name', self.generic_output_name)

    ### UI MANIFEST ###

    user_input_to_action = PackageProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'ibd': remove_illustration_builder_module,
        'ibe': interactively_edit_illustration_builder_module,
        'ibt': write_stub_illustration_builder_module_to_disk,
        'ibx': run_python_on_illustration_builder_module,
        'ibxi': run_abjad_on_illustration_builder_module,
        'lyd': remove_illustration_ly,
        'lym': write_illustration_ly_to_disk,
        'lyv': illustration_ly_file_proxy,
        'mdcanned': interactively_write_material_definition_module_boilerplate,
        'mde': interactively_edit_material_definition_module,
        'mddelete': remove_material_definition_module,
        'mdstub': write_stub_material_definition_module_to_disk,
        'mdx': run_python_on_material_definition_module,
        'mdxe': run_abjad_on_material_definition_module,
        'omcanned': interactively_write_output_material_module_boilerplate,
        'omdelete': remove_output_material_module,
        'omfetch': display_output_material,
        'omm': write_output_material_to_disk,
        'omi': interactively_edit_output_material,
        'omv': interactively_view_output_material_module,
        'pdfm': write_illustration_ly_and_pdf_to_disk,
        'pdfd': remove_illustration_pdf,
        'pdfv': illustration_pdf_file_proxy,
        'ren': interactively_rename_material,
        'rm': remove_material_package,
        'ssm': interactively_edit_stylesheet_file,
        'sss': interactively_select_stylesheet,
        'stl': manage_stylesheets,
        'uid': remove_user_input_module,
        })
