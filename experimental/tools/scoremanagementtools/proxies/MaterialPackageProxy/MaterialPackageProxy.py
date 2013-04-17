import os
from abjad.tools import iotools
from abjad.tools import markuptools
from abjad.tools import mathtools
from experimental.tools.scoremanagementtools import helpers
from experimental.tools.scoremanagementtools import wizards
from experimental.tools.scoremanagementtools.proxies.IllustrationBuilderModuleProxy import IllustrationBuilderModuleProxy
from experimental.tools.scoremanagementtools.proxies.IllustrationLyFileProxy import IllustrationLyFileProxy
from experimental.tools.scoremanagementtools.proxies.IllustrationPdfFileProxy import IllustrationPdfFileProxy
from experimental.tools.scoremanagementtools.proxies.MaterialDefinitionModuleProxy import MaterialDefinitionModuleProxy
from experimental.tools.scoremanagementtools.wranglers.MaterialPackageMakerWrangler import MaterialPackageMakerWrangler
from experimental.tools.scoremanagementtools.proxies.OutputMaterialModuleProxy import OutputMaterialModuleProxy
from experimental.tools.scoremanagementtools.proxies.PackageProxy import PackageProxy
from experimental.tools.scoremanagementtools.proxies.StylesheetFileProxy import StylesheetFileProxy
from experimental.tools.scoremanagementtools.wranglers.StylesheetFileWrangler import StylesheetFileWrangler
from experimental.tools.scoremanagementtools.proxies.UserInputModuleProxy import UserInputModuleProxy
from experimental.tools.scoremanagementtools.helpers import safe_import


class MaterialPackageProxy(PackageProxy):

    ### CLASS ATTRIBUTES ###

    should_have_user_input_module = False

    ### INTIALIZER ###

    def __init__(self, package_importable_name=None, session=None):
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        self._generic_output_name = None
        self.stylesheet_file_name_in_memory = None

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return self.human_readable_name

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

    @property
    def has_readable_illustration_builder_module(self):
        if self.has_illustration_builder_module:
            return self.illustration_builder_module_proxy.is_readable
        return False

    @property
    def has_readable_initializer(self):
        if self.has_initializer:
            return self.initializer_file_proxy.is_readable
        return False

    @property
    def has_readable_material_definition_module(self):
        if self.has_material_definition_module:
            return self.material_definition_module_proxy.is_readable
        return False

    @property
    def has_readable_output_material_module(self):
        if self.has_output_material_module:
            return self.output_material_module_proxy.is_readable
        return False

    @property
    def has_readable_user_input_module(self):
        if self.has_user_input_module:
            return self.user_input_module_proxy.is_readable
        return False

    # TODO: impelement
    @property
    def has_stylesheet(self):
        return False

    @property
    def has_user_finalized_illustration_builder_module(self):
        if self.has_readable_illustration_builder_module:
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
            return bool(self.user_input_module_proxy.read_user_input_wrapper_from_disk())
        return False

    @property
    def illustration(self):
        if self.has_illustration_builder_module:
            return self.illustration_builder_module_proxy.import_illustration()

    @property
    def illustration_builder_module_file_name(self):
        if self.should_have_illustration_builder_module:
            return os.path.join(self.path_name, 'illustration_builder.py')

    @property
    def illustration_builder_module_importable_name(self):
        if self.should_have_illustration_builder_module:
            return self.dot_join([self.importable_name, 'illustration_builder'])

    @property
    def illustration_builder_module_proxy(self):
        if self.should_have_illustration_builder_module:
            if not self.has_illustration_builder_module:
                file(self.illustration_builder_module_file_name, 'w').write('')
            return IllustrationBuilderModuleProxy(
                self.illustration_builder_module_importable_name, session=self.session)

    @property
    def illustration_ly_file_name(self):
        if self.should_have_illustration_ly:
            return os.path.join(self.path_name, 'illustration.ly')

    @property
    def illustration_ly_file_proxy(self):
        if self.should_have_illustration_ly:
            if not self.has_illustration_ly:
                file(self.illustration_ly_file_name, 'w').write('')
            return IllustrationLyFileProxy(self.illustration_ly_file_name, session=self.session)

    @property
    def illustration_pdf_file_name(self):
        if self.should_have_illustration_pdf:
            return os.path.join(self.path_name, 'illustration.pdf')

    @property
    def illustration_pdf_file_proxy(self):
        if self.should_have_illustration_pdf:
            if not self.has_illustration_pdf:
                file(self.illustration_pdf_file_name, 'w').write('')
            return IllustrationPdfFileProxy(self.illustration_pdf_file_name, session=self.session)

    @property
    def illustration_with_stylesheet(self):
        illustration = self.illustration
        if illustration and self.stylesheet_file_name_in_memory:
            illustration.file_initial_user_includes.append(self.stylesheet_file_name_in_memory)
        return illustration

    @property
    def initializer_has_output_material_safe_import_statement(self):
        if self.has_initializer:
            return self.initializer_file_proxy.has_safe_import_statement(
                'output_material', self.material_underscored_name)

    # TODO: port
    @property
    def is_changed(self):
        self.print_not_yet_implemented()
        material_definition = self.material_definition_module_proxy.import_material_definition()
        output_material = self.output_material_module_proxy.import_output_material_safely()
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

    # TODO: replace with self.material_definition_module_proxy.material_definition
    @property
    def material_definition(self):
        if self.has_readable_material_definition_module:
            pair = self.output_material_module_import_statements_and_material_definition
            material_definition = pair[1]
            return material_definition

    @property
    def material_definition_module_file_name(self):
        if self.should_have_material_definition_module:
            return os.path.join(self.path_name, 'material_definition.py')

    @property
    def material_definition_module_importable_name(self):
        if self.should_have_material_definition_module:
            return self.dot_join([self.importable_name, 'material_definition'])

    @property
    def material_definition_module_proxy(self):
        if self.should_have_material_definition_module:
            return MaterialDefinitionModuleProxy(
                self.material_definition_module_importable_name, session=self.session)

    @property
    def material_package_directory(self):
        if self.session.current_materials_package_path_name:
            if self.material_package_short_name:
                return os.path.join(
                    self.session.current_materials_package_path_name, self.material_package_short_name)

    @property
    def material_package_maker(self):
        if self.material_package_maker_class_name is not None:
            #maker_class = safe_import(
            #    locals(), 'makers', self.material_package_maker_class_name,
            #    source_parent_package_importable_name=self.scf_package_importable_name)
            maker_class = safe_import(
                locals(), 'makers', self.material_package_maker_class_name,
                source_parent_package_importable_name=self.scf_fully_qualified_package_name)
            return maker_class

    @property
    def material_package_maker_class_name(self):
        return self.get_tag('material_package_maker_class_name')

    @property
    def material_package_short_name(self):
        return self.material_underscored_name

    @property
    def material_spaced_name(self):
        return self.material_underscored_name.replace('_', ' ')

    @property
    def material_underscored_name(self):
        return self.short_name

    @property
    def output_material(self):
        if self.has_readable_output_material_module:
            return self.output_material_module_proxy.import_output_material()

    @property
    def output_material_module_body_lines(self):
        if self.should_have_material_definition_module:
            return self.output_material_module_import_statements_and_output_material_module_body_lines[1]

    @property
    def output_material_module_file_name(self):
        if self.should_have_output_material_module:
            return os.path.join(self.path_name, 'output_material.py')

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
            output_material_module_import_statements = self.output_material_module_import_statements
            output_material = self.make_output_material_from_user_input_wrapper_in_memory()
        else:
            raise ValueError
        if hasattr(self, 'make_output_material_module_body_lines'):
            output_material_module_body_lines = self.make_output_material_module_body_lines(output_material)
        else:
            line = '{} = {}'.format(
                self.material_underscored_name, self.get_tools_package_qualified_repr(output_material))
            output_material_module_body_lines = [line]
        return output_material_module_import_statements, output_material_module_body_lines

    @property
    def output_material_module_importable_name(self):
        if self.should_have_output_material_module:
            return '{}.output_material'.format(self.importable_name)

    @property
    def output_material_module_proxy(self):
        if self.should_have_output_material_module:
            if self.has_output_material_module:
                return OutputMaterialModuleProxy(
                    self.output_material_module_importable_name, session=self.session)

    @property
    def parent_initializer_has_output_material_safe_import_statement(self):
        if self.has_parent_initializer:
            return self.parent_initializer_file_proxy.has_safe_import_statement(
            self.material_underscored_name, self.material_underscored_name)

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
    def stylesheet_file_name_on_disk(self):
        if self.has_illustration_ly:
            for line in self.illustration_ly_file_proxy.file_lines:
                if line.startswith(r'\include') and 'stylesheets' in line:
                    file_name = line.split()[-1].replace('"', '')
                    return file_name

    @property
    def stylesheet_file_proxy(self):
        if self.should_have_stylesheet:
            return StylesheetFileProxy(self.stylesheet_file_name, session=self.session)

    @property
    def user_input_module_file_name(self):
        if self.should_have_user_input_module:
            return os.path.join(self.path_name, 'user_input.py')

    @property
    def user_input_module_importable_name(self):
        if self.should_have_user_input_module:
            return self.dot_join([self.importable_name, 'user_input'])

    @property
    def user_input_module_proxy(self):
        if self.should_have_user_input_module:
            if not self.has_user_input_module:
                file(self.user_input_module_file_name, 'w').write('')
            return UserInputModuleProxy(self.user_input_module_importable_name, session=self.session)

    ### PUBLIC METHODS ###

    def add_material_to_material_initializer(self):
        self.initializer_file_proxy.add_safe_import_statement(
            'output_material', self.material_underscored_name)

    def add_material_to_materials_initializer(self):
        parent_package = PackageProxy(self.parent_package_importable_name, session=self.session)
        parent_package.initializer_file_proxy.add_safe_import_statement(
            self.material_underscored_name, self.material_underscored_name)

    def conditionally_write_stub_material_definition_module_to_disk(self, is_interactive=False):
        if not self.get_tag('material_package_maker_class_name'):
            is_data_only = not self.get_tag('should_have_illustration')
            self.material_definition_module_proxy.write_stub_to_disk(
                is_data_only, is_interactive=is_interactive)

    def conditionally_write_stub_user_input_module_to_disk(self, is_interactive=False):
        if self.should_have_user_input_module:
            self.write_stub_user_input_module_to_disk(is_interactive=is_interactive)

    def edit_output_material_interactively(self):
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
            target=output_material, session=self.session)
        output_material_handler.run()
        if self.backtrack():
            return
        output_material_module_import_statements = self.output_material_module_import_statements
        if hasattr(self, 'make_output_material_module_body_lines'):
            output_material_module_body_lines = self.make_output_material_module_body_lines(
                output_material_handler.target)
        else:
            line = '{} = {}'.format(self.material_underscored_name,
                self.get_tools_package_qualified_repr(output_material_handler.target))
            output_material_module_body_lines = [line]
        self.write_output_material_to_disk(
            output_material_module_import_statements=output_material_module_import_statements,
            output_material_module_body_lines=output_material_module_body_lines)

    # TODO: audit
    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'uic':
            self.clear_user_input_wrapper(prompt=False)
        elif result == 'uid':
            self.remove_user_input_module(prompt=True)
        elif result == 'uil':
            self.load_user_input_wrapper_demo_values(prompt=False)
        elif result == 'uip':
            self.populate_user_input_wrapper(prompt=False)
        elif result == 'uis':
            self.show_user_input_demo_values(prompt=True)
        elif result == 'uit':
            self.session.swap_user_input_values_default_status()
        elif result == 'uimv':
            self.user_input_module_proxy.view()
        elif result == 'mdcanned':
            self.material_definition_module_proxy.write_boilerplate_asset_to_disk_interactively()
        elif result == 'mddelete':
            self.remove_material_definition_module(prompt=True)
        elif result == 'mde':
            self.material_definition_module_proxy.edit()
        elif result == 'mdstub':
            self.write_stub_material_definition_module_to_disk()
        elif result == 'mdx':
            self.material_definition_module_proxy.run_python(prompt=True)
        elif result == 'mdxe':
            self.material_definition_module_proxy.run_abjad(prompt=True)
        elif result == 'ibd':
            self.remove_illustration_builder_module(prompt=True)
        elif result == 'ibe':
            self.illustration_builder_module_proxy.edit()
        elif result == 'ibt':
            self.illustration_builder_module_proxy.write_stub_to_disk(prompt=True)
        elif result == 'ibx':
            self.illustration_builder_module_proxy.run_python(prompt=True)
        elif result == 'ibxi':
            self.illustration_builder_module_proxy.run_abjad(prompt=True)
        elif result == 'ssm':
            self.stylesheet_file_proxy.edit()
        elif result == 'sss':
            self.select_stylesheet_interactively()
        elif result == 'stl':
            self.manage_stylesheets()
        elif result == 'omm':
            self.write_output_material_to_disk()
        elif result == 'omi':
            self.edit_output_material_interactively()
        elif result == 'omcanned':
            self.output_material_module_proxy.write_boilerplate_asset_to_disk_interactively()
        elif result == 'omdelete':
            self.remove_output_material_module(prompt=True)
        elif result == 'omv':
            self.output_material_module_proxy.view()
        elif result == 'omfetch':
            self.output_material_module_proxy.display_output_material()
        elif result == 'lym':
            self.write_illustration_ly_to_disk(True)
        elif result == 'lyd':
            self.remove_illustration_ly(prompt=True)
        elif result == 'lyv':
            self.illustration_ly_file_proxy.view()
        elif result == 'pdfm':
            self.write_illustration_ly_and_pdf_to_disk(True)
        elif result == 'pdfd':
            self.remove_illustration_pdf(prompt=True)
        elif result == 'pdfv':
            self.illustration_pdf_file_proxy.view()
        elif result == 'rm':
            self.remove_material_package()
        elif result == 'inr':
            self.initializer_file_proxy.restore_interactively(prompt=True)
        elif result == 'inv':
            self.initializer_file_proxy.view()
        elif result == 'incanned':
            self.initializer_file_proxy.write_boilerplate_asset_to_disk_interactively()
        elif result == 'instub':
            self.initializer_file_proxy.write_stub_file_to_disk(prompt=True)
        elif result == 'ren':
            self.rename_material_interactively()
        elif result == 'reg':
            self.regenerate_everything(prompt=True)
        # TODO: add to package-level hidden menu
        elif result == 'tags':
            self.manage_tags()
        # TODO: add to directory-level hidden menu
        elif result == 'ls':
            self.print_directory_contents()
        elif mathtools.is_integer_equivalent_expr(result):
            self.edit_user_input_wrapper_at_number(result, include_newline=False)
        else:
            raise ValueError

    def load_user_input_wrapper_demo_values(self, prompt=False):
        pass

    def make_main_menu(self):
        menu, hidden_section = self.make_menu(where=self.where(), is_hidden=True)
        self.make_main_menu_section_for_initializer(menu, hidden_section)
        self.make_main_menu_sections(menu, hidden_section)
        self.make_main_menu_section_for_illustration_ly(hidden_section)
        self.make_main_menu_section_for_illustration_pdf(menu, hidden_section)
        self.make_main_menu_section_for_hidden_entries(menu)
        return menu

    def make_main_menu_section_for_hidden_entries(self, main_menu):
        hidden_section = main_menu.make_section(is_hidden=True)
        hidden_section.append(('rm', 'delete package'))
        hidden_section.append(('ls', 'list package'))
        hidden_section.append(('reg', 'regenerate package'))
        hidden_section.append(('ren', 'rename package'))
        hidden_section.append(('stl', 'manage stylesheets'))
        hidden_section.append(('tags', 'manage tags'))

    def make_main_menu_section_for_illustration_builder(self, main_menu, hidden_section):
        section = main_menu.make_section()
        if self.has_output_material:
            if self.should_have_illustration:
                if not self.has_illustration_builder_module:
                    self.illustration_builder_module_proxy.write_stub_to_disk(prompt=False)
                section.append(('ibe', 'illustration builder - edit'))
                if self.has_output_material:
                    section.append(('ibx', 'illustration builder - execute'))
                hidden_section.append(('ibd', 'illustration builder - delete'))
                hidden_section.append(('ibt', 'illustration builder - stub'))
                hidden_section.append(('ibex', 'illustration builder - edit & execute'))
                section.append(('sss', 'score stylesheet - select'))
                hidden_section.append(('ssm', 'source stylesheet - edit'))

    def make_main_menu_section_for_illustration_ly(self, hidden_section):
        if self.has_output_material:
            if self.has_illustration_builder_module or self.has_material_package_maker:
                hidden_section.append(('lym', 'output ly - make'))
        if self.has_illustration_ly:
            hidden_section.append(('lyd', 'output ly - delete'))
            hidden_section.append(('lyv', 'output ly - view'))

    def make_main_menu_section_for_illustration_pdf(self, main_menu, hidden_section):
        has_illustration_pdf_section = False
        if self.has_output_material:
            if self.has_illustration_builder_module or \
                (self.has_material_package_maker and getattr(self, 'illustration_maker', None)):
                section = main_menu.make_section()
                has_illustration_pdf_section = True
                section.append(('pdfm', 'output pdf - make'))
        if self.has_illustration_pdf:
            if not has_illustration_pdf_section:
                section = main_menu.make_section()
            hidden_section.append(('pdfd', 'output pdf - delete'))
            section.append(('pdfv', 'output pdf - view'))

    def make_main_menu_section_for_initializer(self, main_menu, hidden_section):
        if not self.has_initializer:
            section = main_menu.make_section()
            section.title = '(Note: package has no initializer.)'
            section.append(('inr', 'initializer - restore'))
        elif not self.has_readable_initializer:
            section = main_menu.make_section()
            section.title = '(Note: package has invalid initializer.)'
            section.append(('inr', 'initializer - restore'))
        hidden_section.append(('inv', 'view package initializer'))
        hidden_section.append(('incanned', 'copy canned package initializer'))
        hidden_section.append(('instub', 'write stub package initializer'))

    def make_main_menu_section_for_material_definition(self, main_menu, hidden_section):
        if not self.has_readable_initializer:
            return
        section = main_menu.make_section()
        if self.has_material_definition_module:
            has_invalid_material_definition_module = not self.has_readable_material_definition_module
            if has_invalid_material_definition_module:
                section.title = '(Note: has invalid material definition module.)'
            section.append(('mde', 'material definition - edit'))
            if not has_invalid_material_definition_module:
                section.append(('mdx', 'material definition - execute'))
            hidden_section.append(('mdcanned', 'material definition - copy canned module'))
            hidden_section.append(('mddelete', 'material definition - delete'))
            hidden_section.append(('mdstub', 'material definition - stub'))
            if not has_invalid_material_definition_module:
                hidden_section.append(('mdxe', 'material definition - execute & edit'))
        elif self.material_package_maker_class_name is None:
            section.append(('mdstub', 'material definition - stub'))

    def make_main_menu_section_for_output_material(self, main_menu, hidden_section):
        if not self.has_readable_initializer:
            return
        has_output_material_section = False
        if self.has_material_definition_module or \
            self.has_complete_user_input_wrapper_in_memory or \
            self.has_output_material_editor:
            if self.has_material_definition or \
                self.has_complete_user_input_wrapper_in_memory:
                section = main_menu.make_section()
                section.append(('omm', 'output material - make'))
                has_output_material_section = True
            if self.has_output_material_editor:
                section = main_menu.make_section()
                if self.has_output_material:
                    output_material_editor = self.output_material_editor(
                        target=self.output_material, session=self.session)
                    target_summary_lines = output_material_editor.target_summary_lines
                    if target_summary_lines:
                        section.title = target_summary_lines
                section.append(('omi', 'output material - interact'))
                has_output_material_section = True
            if self.has_output_material_module:
                if not has_output_material_section:
                    section = main_menu.make_section()
                section.append(('omv', 'output material - view'))
                hidden_section.append(('omdelete', 'output material - delete'))
                hidden_section.append(('omfetch', 'output material - fetch'))
        hidden_section.append(('omcanned', 'output material - copy canned module'))

    def make_main_menu_sections(self, menu, hidden_section):
        self.make_main_menu_section_for_material_definition(menu, hidden_section)
        self.make_main_menu_section_for_output_material(menu, hidden_section)
        self.make_main_menu_section_for_illustration_builder(menu, hidden_section)

    def manage_stylesheets(self):
        stylesheet_file_wrangler = StylesheetFileWrangler(session=self.session)
        stylesheet_file_wrangler.run()

    def overwrite_output_material_module(self):
        file(self.output_material_module_file_name, 'w').write('')

    def populate_user_input_wrapper(self, prompt=False):
        pass

    # TODO: port
    def regenerate_everything(self, prompt=True):
        self.print_not_yet_implemented()
        self.proceed(is_interactive=prompt)

    def remove(self):
        self.remove_material_from_materials_initializer()
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

    def remove_interactively(self):
        self.remove_material_from_materials_initializer()
        PackageProxy.remove_interactively(self)

    def remove_material_definition_module(self, prompt=True):
        self.remove_output_material_module(prompt=False)
        self.remove_illustration_builder_module(prompt=False)
        if self.has_material_definition_module:
            self.material_definition_module_proxy.remove()

    def remove_material_from_materials_initializer(self):
        import_statement = 'safe_import(globals(), {!r}, {!r})\n'
        import_statement = import_statement.format(
            self.material_underscored_name, self.material_underscored_name)
        parent_package = PackageProxy(self.parent_package_importable_name, session=self.session)
        parent_package_initializer_file_proxy = parent_package.initializer_file_proxy
        filtered_import_statements = []
        for safe_import_statement in parent_package_initializer_file_proxy.safe_import_statements:
            if not safe_import_statement == import_statement:
                filtered_import_statements.append(safe_import_statement)
        parent_package_initializer_file_proxy.safe_import_statements[:] = filtered_import_statements
        parent_package_initializer_file_proxy.write_to_disk()

    def remove_material_package(self):
        self.remove()
        self.session.is_backtracking_locally = True

    def remove_output_material_module(self, prompt=True):
        self.remove_illustration_builder_module(prompt=False)
        if self.has_output_material_module:
            self.output_material_module_proxy.remove()

    # NOTE: not currently used
    def remove_parent_initializer_pyc_file(self):
        if self.has_parent_initializer:
            parent_initializer_pyc_file_name = self.parent_initializer_file_name + 'c'
            if os.path.exists(parent_initializer_pyc_file_name):
                os.remove(parent_initializer_pyc_file_name)

    def remove_user_input_module(self, prompt=True):
        if self.has_user_input_module:
            self.user_input_module_proxy.remove()

    def rename_material_interactively(self):
        line = 'current material name: {}'.format(self.material_underscored_name)
        self.display(line)
        getter = self.make_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_package_name('new material name')
        new_material_underscored_name = getter.run()
        if self.backtrack():
            return
        lines = []
        lines.append('current material name: {}'.format(self.material_underscored_name))
        lines.append('new material name:     {}'.format(new_material_underscored_name))
        lines.append('')
        self.display(lines)
        if not self.confirm():
            return
        if self.is_versioned:
            # rename package directory
            new_directory_name = self.path_name.replace(
                self.material_underscored_name, new_material_underscored_name)
            command = 'svn mv {} {}'.format(self.path_name, new_directory_name)
            os.system(command)
            # update package initializer
            parent_directory_name = os.path.dirname(self.path_name)
            new_package_directory = os.path.join(parent_directory_name, new_material_underscored_name)
            new_initializer = os.path.join(new_package_directory, '__init__.py')
            helpers.globally_replace_in_file(
                new_initializer, self.material_underscored_name, new_material_underscored_name)
            # rename output material
            new_output_material = os.path.join(new_package_directory, 'output_material.py')
            helpers.globally_replace_in_file(
                new_output_material, self.material_underscored_name, new_material_underscored_name)
            # commit
            commit_message = 'renamed {} to {}.'.format(
                self.material_underscored_name, new_material_underscored_name)
            commit_message = commit_message.replace('_', ' ')
            command = 'svn commit -m "{}" {}'.format(commit_message, self.parent_directory_name)
            os.system(command)
            # update path name to reflect change
            self._path_name = new_package_directory
        else:
            raise NotImplementedError('commit to repository and then rename.')

    def run_first_time(self):
        self.run(user_input='omi')

    def select_material_package_maker_interactively(self, prompt=True):
        material_proxy_wrangler = MaterialPackageMakerWrangler(session=self.session)
        self.push_backtrack()
        material_package_maker = material_proxy_wrangler.select_material_proxy_class_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.add_tag('material_package_maker', material_package_maker.class_name)
        line = 'user input handler selected.'
        self.proceed(line, is_interactive=prompt)

    def select_stylesheet_interactively(self, prompt=True):
        stylesheet_file_wrangler = StylesheetFileWrangler(session=self.session)
        self.push_backtrack()
        stylesheet_file_name = stylesheet_file_wrangler.select_stylesheet_file_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.stylesheet_file_name_in_memory = stylesheet_file_name
        self.proceed('stylesheet selected.', is_interactive=prompt)

    # NOTE: not currently used
    def touch_parent_initializer(self):
        if self.has_parent_initializer:
            self.parent_initializer_file_proxy.touch()

    def write_illustration_ly_and_pdf_to_disk(self, prompt=True):
        illustration = self.illustration_with_stylesheet
        iotools.write_expr_to_pdf(illustration, self.illustration_pdf_file_name, print_status=False)
        iotools.write_expr_to_ly(illustration, self.illustration_ly_file_name, print_status=False)
        self.proceed('PDF and LilyPond file written to disk.', is_interactive=prompt)

    def write_illustration_ly_to_disk(self, prompt=True):
        illustration = self.illustration_with_stylesheet
        iotools.write_expr_to_ly(illustration, self.illustration_ly_file_name, print_status=False)
        self.proceed('LilyPond file written to disk.', is_interactive=prompt)

    def write_illustration_pdf_to_disk(self, prompt=True):
        illustration = self.illustration_with_stylesheet
        iotools.write_expr_to_pdf(illustration, self.illustration_pdf_file_name, print_status=False)
        self.proceed('PDF written to disk.', is_interactive=prompt)

    def write_output_material_to_disk(self, output_material_module_import_statements=None,
        output_material_module_body_lines=None, prompt=True):
        self.remove_material_from_materials_initializer()
        self.overwrite_output_material_module()
        output_material_module_proxy = self.output_material_module_proxy
        if output_material_module_import_statements is None or \
            output_material_module_body_lines is None:
            pair = self.output_material_module_import_statements_and_output_material_module_body_lines
            output_material_module_import_statements, output_material_module_body_lines = pair
        output_material_module_import_statements = [x + '\n' for x in output_material_module_import_statements]
        output_material_module_proxy.setup_statements = output_material_module_import_statements
        output_material_module_proxy.body_lines[:] = output_material_module_body_lines
        output_material_module_proxy.write_to_disk()
        self.add_material_to_materials_initializer()
        self.add_material_to_material_initializer()
        self.write_tags_to_disk()
        self.proceed('output material written to disk.', is_interactive=prompt)

    def write_stub_material_definition_module_to_disk(self):
        if self.should_have_material_definition_module:
            file(self.material_definition_module_file_name, 'w').write('')
            self.material_definition_module_proxy.write_stub_to_disk(self.is_data_only, is_interactive=True)

    def write_tags_to_disk(self):
        self.add_tag('is_material_package', True)
        if hasattr(self, 'generic_output_name'):
            self.add_tag('generic_output_name', self.generic_output_name)
