import os
from abjad.tools import stringtools
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler


class MaterialPackageMakerWrangler(PackageWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
#        PackageWrangler.__init__(self,
#            score_external_asset_container_package_paths=[self.makers_package_path],
#            score_internal_asset_container_package_path_infix=None,
#            session=session,
#            user_asset_container_package_paths=[self.configuration.user_specific_makers_package_path],
#            user_asset_container_paths=[self.configuration.user_specific_makers_directory_path])
        PackageWrangler.__init__(self, session=session)
        self._score_external_asset_container_package_paths = [
            self.configuration.makers_package_path]
        self._score_internal_asset_container_package_path_infix = None
        self._user_asset_container_package_paths = [self.configuration.user_specific_makers_package_path]
        self._user_asset_container_paths = [self.configuration.user_specific_makers_directory_path]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'material package makers'

    # TODO: derive programmatically
    @property
    def forbidden_class_names(self):
        return (
            'FunctionInputMaterialPackageMaker',
            'InventoryMaterialPackageMaker',
            'MaterialPackageMaker',
            )

    @property
    def forbidden_package_paths(self):
        return ['scoremanagertools.materialpackagemakers.' + class_name for class_name in self.forbidden_class_names]

    ### PUBLIC METHODS ###

    def get_asset_proxy(self, package_path):
        from experimental.tools.scoremanagertools.proxies.MaterialPackageProxy import MaterialPackageProxy
        material_package_proxy = MaterialPackageProxy(package_path, session=self.session)
        material_package_maker_class_name = material_package_proxy.material_package_maker_class_name
        if material_package_maker_class_name is not None:
            material_package_maker_class = None
            command = 'from experimental.tools.scoremanagertools.materialpackagemakers import {} as material_package_maker_class'
            command = command.format(material_package_maker_class_name)
            try:
                exec(command)
            except ImportError:
                command = 'from {} import {} as material_package_maker_class'
                command = command.format(
                    self.configuration.user_specific_makers_package_path, material_package_maker_class_name)
                exec(command)
            material_package_proxy = material_package_maker_class(
                package_path, session=self.session)
        return material_package_proxy

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_asset_interactively()
        else:
            raise ValueError

    def list_asset_space_delimited_lowercase_names(self, head=None):
        result = []
        for asset_filesystem_path in self.list_asset_filesystem_paths(head=head):
            asset_filesystem_path = os.path.normpath(asset_filesystem_path)
            asset_name = os.path.basename(asset_filesystem_path)
            if asset_name in self.forbidden_class_names:
                continue
            space_delimited_lowercase_asset_name = stringtools.uppercamelcase_to_space_delimited_lowercase(asset_name)
            result.append(space_delimited_lowercase_asset_name)
        return result

    def list_score_external_asset_package_paths(self, head=None):
        result = PackageWrangler.list_score_external_asset_package_paths(self, head=head)
        #if self.base_class_name in result:
        #    result.remove(self.base_class_name)
        for forbidden_package_path in self.forbidden_package_paths:
            if forbidden_package_path in result:
                result.remove(forbidden_package_path)
        return result

    def list_score_internal_asset_container_package_paths(self, head=None):
        return []

    # TODO: implement MaterialPackageProxyClassFile object to model and customize these settings
    def make_asset_class_file(self, package_name, generic_output_name):
        class_file_name = os.path.join(
            self.list_score_external_asset_container_package_paths()[0],
            package_name, package_name + '.py')
        class_file = file(class_file_name, 'w')
        lines = []
        lines.append('from music.foo import foo')
        lines.append('from music.foo import make_illustration_from_output_material')
        lines.append('from experimental.tools.scoremanagertools.materialpackagemakers.MaterialPackageMaker import MaterialPackageMaker')
        lines.append('from experimental.tools.scoremanagertools.editors.UserInputWrapper import UserInputWrapper')
        lines.append('from experimental.tools import scoremanagertools')
        lines.append('')
        lines.append('')
        lines.append('class {}(MaterialPackageMaker):'.format(package_name))
        lines.append('')
        lines.append('    def __init__(self, package_path=None, session=None):')
        lines.append('        MaterialPackageMaker.__init__(')
        lines.append('            self, package_path=package_path, session=seession')
        lines.append('')
        lines.append('    ### READ-ONLY PUBLIC PROPERTIES ###')
        lines.append('')
        lines.append('    generic_output_name = {!r}'.format(generic_output_name))
        lines.append('')
        lines.append('    illustration_maker = staticmethod(make_illustration_from_output_material)')
        lines.append('')
        lines.append('    output_material_checker = staticmethod(componenttools.all_are_components)')
        lines.append('')
        lines.append('    output_material_maker = staticmethod(music.foo)')
        lines.append('')
        lines.append('    output_material_module_import_statements = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_demo_values = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_module_import_statements = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_tests = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    ### PUBLIC METHODS ###')
        lines.append('')
        lines.append('    @property')
        lines.append('    def output_material_module_body_lines(self):')
        lines.append('        lines = []')
        lines.append('        output_material = self.output_material')
        lines.append("        lines.append('{} = {!r}'.format(self.material_package_name, output_material)")
        class_file.write('\n'.join(lines))
        class_file.close()

    # TODO: change to boilerplate file stored in material_package_maker package
    def make_asset_initializer(self, package_name):
        initializer_file_name = os.path.join(
            self.list_score_external_asset_container_package_paths()[0],
            package_name, '__init__.py')
        initializer = file(initializer_file_name, 'w')
        line = 'from abjad.tools import importtools\n'
        initializer.write(line)
        initializer.write('\n')
        initializer.write("importtools.import_structured_package(__path__[0], globals())\n")
        initializer.close()

    def make_asset_interactively(self):
        getter = self.io.make_getter(where=self.where())
        getter.append_material_package_maker_class_name('material proxy name')
        getter.append_space_delimited_lowercase_string('generic output product')
        result = getter.run()
        if self.session.backtrack():
            return
        material_package_maker_class_name, generic_output_product_name = result
        material_package_maker_directory = os.path.join(
            self.list_score_external_asset_container_package_paths[0],
            material_package_maker_class_name)
        os.mkdir(material_package_maker_directory)
        self.make_asset_initializer(material_package_maker_class_name)
        self.make_asset_class_file(
            material_package_maker_class_name, generic_output_product_name)
        self.make_asset_stylesheet(material_package_maker_class_name)

    # TODO: change to boilerplate file stored somewhere
    def make_asset_stylesheet(self, package_name):
        stylesheet = lilypondfiletools.make_basic_lilypond_file()
        stylesheet.pop()
        stylesheet.file_initial_system_comments = []
        stylesheet.default_paper_size = 'letter', 'portrait'
        stylesheet.global_staff_size = 14
        stylesheet.layout_block.indent = 0
        stylesheet.layout_block.ragged_right = True
        stylesheet.paper_block.markup_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)
        stylesheet.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 10, 0)
        stylesheet_file_name = os.path.join(
            self.list_score_external_asset_container_package_paths()[0],
            package_name, 'stylesheet.ly')
        stylesheet_file_pointer = file(stylesheet_file_name, 'w')
        stylesheet_file_pointer.write(stylesheet.format)
        stylesheet_file_pointer.close()

    def make_main_menu(self, head=None):
        menu, section = self.io.make_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_asset_space_delimited_lowercase_names(head=head)
        section = menu.make_section()
        section.append(('new', 'new material package maker'))
        return menu

    def make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_asset_package_paths(head=head)
        bodies = self.list_asset_space_delimited_lowercase_names(head=head)
        return zip(keys, bodies)
