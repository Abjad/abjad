import collections
import os
from abjad.tools import stringtools
from scf import predicates
from scf.wranglers.PackageWrangler import PackageWrangler


# TODO: write all iteration tests
class MaterialPackageWrangler(PackageWrangler):

    def __init__(self, session=None):
        from scf.wranglers.MaterialPackageMakerWrangler import MaterialPackageMakerWrangler
        PackageWrangler.__init__(self,
            score_external_asset_container_importable_names= \
                [self.score_external_materials_package_importable_name],
            score_internal_asset_container_importable_name_infix= \
                self.score_internal_materials_package_importable_name_infix,
            session=session)
        self._material_package_maker_wrangler = MaterialPackageMakerWrangler(session=self.session)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'materials'

    @property
    def material_package_maker_wrangler(self):
        return self._material_package_maker_wrangler

    ### PUBLIC METHODS ###

    def get_asset_proxy(self, package_importable_name):
        return self.material_package_maker_wrangler.get_asset_proxy(package_importable_name)

    def get_appropriate_material_package_proxy(self,
        material_package_maker_class_name, material_package_importable_name):
        import scf
        if material_package_maker_class_name is None:
            material_package_proxy = scf.proxies.MaterialPackageProxy(
                material_package_importable_name, session=self.session)
        else:
            command = 'material_package_proxy = '
            command += 'scf.makers.{}(material_package_importable_name, session=self.session)'
            command = command.format(material_package_maker_class_name)
            exec(command)
        return material_package_proxy

    def get_available_material_package_importable_name_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        while True:
            getter = self.make_getter(where=self.where())
            getter.append_space_delimited_lowercase_string('material name')
            self.push_backtrack()
            material_name = getter.run()
            self.pop_backtrack()
            if self.backtrack():
                return
            material_package_short_name = stringtools.string_to_strict_directory_name(material_name)
            material_package_importable_name = self.dot_join([
                self.current_asset_container_importable_name, material_package_short_name])
            if self.package_exists(material_package_importable_name):
                line = 'Material package {!r} already exists.'.format(material_package_importable_name)
                self.display([line, ''])
            else:
                return material_package_importable_name

    def handle_main_menu_result(self, result):
        if result == 'd':
            self.make_data_package_interactively()
        elif result == 's':
            self.make_numeric_sequence_package_interactively()
        elif result == 'h':
            self.make_handmade_material_package_interactively()
        elif result == 'm':
            self.make_makermade_material_package_interactively()
        elif result == 'missing':
            self.conditionally_make_asset_container_packages(is_interactive=True)
        elif result == 'profile':
            self.profile_visible_assets()
        else:
            material_package_proxy = self.get_asset_proxy(result)
            material_package_proxy.run()

    def make_asset_interactively(self):
        return NotImplemented

    def make_data_package(self, material_package_importable_name, tags=None):
        tags = tags or {}
        tags['material_package_maker_class_name'] = None
        tags['should_have_illustration'] = False
        tags['should_have_user_input_module'] = False
        self.make_material_package(material_package_importable_name, tags=tags)

    def make_data_package_interactively(self, tags=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.push_backtrack()
        material_package_importable_name = self.get_available_material_package_importable_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.make_data_package(material_package_importable_name, tags=tags)

    def make_handmade_material_package(self, material_package_importable_name, tags=None):
        tags = tags or {}
        tags['material_package_maker_class_name'] = None
        tags['should_have_illustration'] = True
        tags['should_have_user_input_module'] = False
        self.make_material_package(material_package_importable_name, tags=tags)

    def make_handmade_material_package_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.push_backtrack()
        material_package_importable_name = self.get_available_material_package_importable_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.make_handmade_material_package(material_package_importable_name)

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_numbered=True, is_keyed=False)
        section.tokens = self.make_visible_asset_menu_tokens(head=head)
        section = menu.make_section()
        section.append(('d', 'data-only'))
        section.append(('h', 'handmade'))
        section.append(('m', 'maker-made'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('s', 'create numeric sequence'))
        hidden_section.append(('missing', 'create missing packages'))
        hidden_section.append(('profile', 'profile packages'))
        return menu

    def make_makermade_material_package(self,
        material_package_importable_name, material_package_maker_class_name, tags=None):
        tags = tags or {}
        command = 'from scf.makers import {} as material_package_maker_class'.format(
            material_package_maker_class_name)
        #material_package_importable_parts = material_package_importable_name.split('.')
        #material_package_maker_head = '.'.join(material_package_importable_parts[:-1])
        #material_package_maker_class_name = material_package_importable_parts[-1]
        #command = 'from {} import {} as material_package_maker_class'.format(
        #    material_package_maker_head, material_package_maker_class_name)
        #self.debug(command, 'COMMAND')
        exec(command)
        should_have_user_input_module = getattr(
            material_package_maker_class, 'should_have_user_input_module', True)
        should_have_illustration = hasattr(material_package_maker_class, 'illustration_maker')
        tags['material_package_maker_class_name'] = material_package_maker_class_name
        tags['should_have_illustration'] = should_have_illustration
        tags['should_have_user_input_module'] = should_have_user_input_module
        self.make_material_package(material_package_importable_name, tags=tags)

    def make_makermade_material_package_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.push_backtrack()
        result = self.material_package_maker_wrangler.select_asset_importable_name_interactively(
            cache=True, clear=False)
        self.pop_backtrack()
        if self.backtrack():
            return
        material_package_maker_importable_name = result
        material_package_maker_class_name = material_package_maker_importable_name.split('.')[-1]
        self.push_backtrack()
        material_package_importable_name = self.get_available_material_package_importable_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.make_makermade_material_package(
            material_package_importable_name, material_package_maker_class_name)
        proxy = self.get_appropriate_material_package_proxy(
            material_package_maker_class_name, material_package_importable_name)
        proxy.run_first_time()

    def make_material_package(self, material_package_importable_name, is_interactive=False, tags=None):
        tags = collections.OrderedDict(tags or {})
        tags['is_material_package'] = True
        path_name = self.package_importable_name_to_path_name(material_package_importable_name)
        assert not os.path.exists(path_name)
        os.mkdir(path_name)
        material_package_maker_class_name = tags.get('material_package_maker_class_name')
        pair = (material_package_maker_class_name, material_package_importable_name)
        material_package_proxy = self.get_appropriate_material_package_proxy(*pair)
        material_package_proxy.initializer_file_proxy.write_stub_to_disk()
        material_package_proxy.tags_file_proxy.write_tags_to_disk(tags)
        material_package_proxy.conditionally_write_stub_material_definition_module_to_disk()
        material_package_proxy.conditionally_write_stub_user_input_module_to_disk()
        line = 'material package {!r} created.'.format(material_package_importable_name)
        self.proceed(line, is_interactive=is_interactive)

    def make_numeric_sequence_package(self, package_importable_name):
        tags = {'is_numeric_sequence': True}
        self.make_data_package(package_importable_name, tags=tags)

    def make_numeric_sequence_package_interactively(self, user_input=None):
        tags = {'is_numeric_sequence': True}
        self.make_data_package_interactively(tags=tags, user_input=user_input)
