import collections
import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools import predicates
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler


# TODO: write all iteration tests
class MaterialPackageWrangler(PackageWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools.scoremanagertools.wranglers.MaterialPackageMakerWrangler import \
            MaterialPackageMakerWrangler
#        PackageWrangler.__init__(self,
#            score_external_asset_container_package_paths= \
#                [self.configuration.score_external_materials_package_path],
#            score_internal_asset_container_package_path_infix= \
#                self.configuration.score_internal_materials_package_path_infix,
#            session=session)
        PackageWrangler.__init__(self, session=session)
        self._score_external_asset_container_package_paths = [
            self.configuration.score_external_materials_package_path]
        self._score_internal_asset_container_package_path_infix = \
            self.configuration.score_internal_materials_package_path_infix
        self._material_package_maker_wrangler = MaterialPackageMakerWrangler(session=self.session)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'materials'

    @property
    def material_package_maker_wrangler(self):
        return self._material_package_maker_wrangler

    ### PUBLIC METHODS ###

    def get_appropriate_material_package_proxy(self,
        material_package_maker_class_name, material_package_path):
        from experimental.tools import scoremanagertools
        if material_package_maker_class_name is None:
            material_package_proxy = scoremanagertools.proxies.MaterialPackageProxy(
                material_package_path, session=self.session)
        else:
            command = 'material_package_proxy = '
            command += 'scoremanagertools.makers.{}(material_package_path, session=self.session)'
            command = command.format(material_package_maker_class_name)
            try:
                exec(command)
            except AttributeError:
                command = 'import {}.{} as material_package_maker_class'
                command = command.format(
                    self.configuration.user_makers_package_path, material_package_maker_class_name)
                exec(command)
                material_package_proxy = material_package_maker_class(
                    material_package_path, session=self.session)
        return material_package_proxy

    def get_asset_proxy(self, package_path):
        return self.material_package_maker_wrangler.get_asset_proxy(package_path)

    def get_available_material_package_path_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        while True:
            getter = self.make_getter(where=self.where())
            getter.append_space_delimited_lowercase_string('material name')
            self.push_backtrack()
            material_name = getter.run()
            self.pop_backtrack()
            if self.backtrack():
                return
            material_package_name = stringtools.string_to_strict_directory_name(material_name)
            material_package_path = self.dot_join([
                self.current_asset_container_package_path, material_package_name])
            if self.package_exists(material_package_path):
                line = 'Material package {!r} already exists.'.format(material_package_path)
                self.display([line, ''])
            else:
                return material_package_path

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

    def make_data_package(self, material_package_path, tags=None):
        tags = tags or {}
        tags['material_package_maker_class_name'] = None
        tags['should_have_illustration'] = False
        tags['should_have_user_input_module'] = False
        self.make_material_package(material_package_path, tags=tags)

    def make_data_package_interactively(self, tags=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.push_backtrack()
        material_package_path = self.get_available_material_package_path_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.make_data_package(material_package_path, tags=tags)

    def make_handmade_material_package(self, material_package_path, tags=None):
        tags = tags or {}
        tags['material_package_maker_class_name'] = None
        tags['should_have_illustration'] = True
        tags['should_have_user_input_module'] = False
        self.make_material_package(material_package_path, tags=tags)

    def make_handmade_material_package_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.push_backtrack()
        material_package_path = self.get_available_material_package_path_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.make_handmade_material_package(material_package_path)

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
        material_package_path, material_package_maker_class_name, tags=None):
        tags = tags or {}
        command = 'from experimental.tools.scoremanagertools.makers import {} as material_package_maker_class'.format(
            material_package_maker_class_name)
        try:
            exec(command)
        except ImportError:
            command = 'from {} import {} as material_package_maker_class'.format(
                self.configuration.user_makers_package_path, material_package_maker_class_name)
            exec(command)
        should_have_user_input_module = getattr(
            material_package_maker_class, 'should_have_user_input_module', True)
        should_have_illustration = hasattr(material_package_maker_class, 'illustration_maker')
        tags['material_package_maker_class_name'] = material_package_maker_class_name
        tags['should_have_illustration'] = should_have_illustration
        tags['should_have_user_input_module'] = should_have_user_input_module
        self.make_material_package(material_package_path, tags=tags)

    def make_makermade_material_package_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.push_backtrack()
        result = self.material_package_maker_wrangler.select_asset_package_path_interactively(
            cache=True, clear=False)
        self.pop_backtrack()
        if self.backtrack():
            return
        material_package_maker_package_path = result
        material_package_maker_class_name = material_package_maker_package_path.split('.')[-1]
        self.push_backtrack()
        material_package_path = self.get_available_material_package_path_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.make_makermade_material_package(
            material_package_path, material_package_maker_class_name)
        proxy = self.get_appropriate_material_package_proxy(
            material_package_maker_class_name, material_package_path)
        proxy.run_first_time()

    def make_material_package(self, material_package_path, is_interactive=False, tags=None):
        tags = collections.OrderedDict(tags or {})
        tags['is_material_package'] = True
        path = self.package_path_to_directory_path(material_package_path)
        assert not os.path.exists(path)
        os.mkdir(path)
        material_package_maker_class_name = tags.get('material_package_maker_class_name')
        pair = (material_package_maker_class_name, material_package_path)
        material_package_proxy = self.get_appropriate_material_package_proxy(*pair)
        material_package_proxy.initializer_file_proxy.write_stub_to_disk()
        material_package_proxy.tags_file_proxy.write_tags_to_disk(tags)
        material_package_proxy.conditionally_write_stub_material_definition_module_to_disk()
        material_package_proxy.conditionally_write_stub_user_input_module_to_disk()
        line = 'material package {!r} created.'.format(material_package_path)
        self.proceed(line, is_interactive=is_interactive)

    def make_numeric_sequence_package(self, package_path):
        tags = {'is_numeric_sequence': True}
        self.make_data_package(package_path, tags=tags)

    def make_numeric_sequence_package_interactively(self, user_input=None):
        tags = {'is_numeric_sequence': True}
        self.make_data_package_interactively(tags=tags, user_input=user_input)
