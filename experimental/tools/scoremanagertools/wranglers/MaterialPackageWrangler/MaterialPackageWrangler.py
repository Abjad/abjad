import collections
import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools import predicates
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler


class MaterialPackageWrangler(PackageWrangler):
    '''Material package wrangler:

    ::

        >>> wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
        >>> wrangler
        MaterialPackageWrangler()

    Wrangler in built-in score:

    ::

        >>> wrangler_in_built_in_score = scoremanagertools.wranglers.MaterialPackageWrangler()
        >>> wrangler_in_built_in_score._session.underscore_delimited_current_score_name = 'red_example_score'
        >>> wrangler_in_built_in_score
        MaterialPackageWrangler()
    
    Return material package wrangler.
    '''

    ### CLASS VARIABLES ###
    
    score_package_asset_storehouse_path_infix_parts = ('music', 'materials')

    asset_storehouse_packagesystem_path_in_built_in_asset_library = \
        PackageWrangler.configuration.built_in_material_packages_package_path

    asset_storehouse_packagesystem_path_in_user_asset_library = \
        PackageWrangler.configuration.user_asset_library_material_packages_package_path

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        PackageWrangler.__init__(self, session=session)
        self._material_package_maker_wrangler = \
            scoremanagertools.wranglers.MaterialPackageMakerWrangler(session=self._session)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'materials'

    ### PRIVATE METHODS ###

    def _get_appropriate_material_package_proxy(self,
        material_package_maker_class_name, material_package_path):
        from experimental.tools import scoremanagertools
        if material_package_maker_class_name is None:
            material_package_proxy = scoremanagertools.proxies.MaterialPackageProxy(
                material_package_path, session=self._session)
        else:
            command = 'material_package_proxy = '
            command += 'scoremanagertools.materialpackagemakers.{}'
            command += '(material_package_path, session=self._session)'
            command = command.format(material_package_maker_class_name)
            try:
                exec(command)
            except AttributeError:
                command = 'import {}.{} as material_package_maker_class'
                command = command.format(
                    self.configuration.user_asset_library_material_package_makers_package_path, 
                    material_package_maker_class_name)
                exec(command)
                material_package_proxy = material_package_maker_class(
                    material_package_path, session=self._session)
        return material_package_proxy

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            material_package_proxy = self._initialize_asset_proxy(result)
            material_package_proxy._run()

    def _initialize_asset_proxy(self, package_path):
        return self._material_package_maker_wrangler._initialize_asset_proxy(package_path)

    def _make_main_menu(self, head=None):
        menu, section = self._io.make_menu(
            where=self._where, 
            return_value_attribute='key',
            is_numbered=True, 
            is_keyed=False,
            )
        section.menu_tokens = self._make_menu_tokens(head=head)
        menu_tokens = [
            ('d', 'data-only'),
            ('h', 'handmade'),
            ('m', 'maker-made'),
            ]
        section = menu.make_section(
            menu_tokens=menu_tokens,
            is_keyed=True,
            return_value_attribute='key',
            )
        menu_tokens = [
            ('s', 'create numeric sequence'),
            ('missing', 'create missing packages'),
            ('profile', 'profile packages'),
            ]
        hidden_section = menu.make_section(
            menu_tokens=menu_tokens,
            return_value_attribute='key',
            is_hidden=True, 
            )
        return menu

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        '''Material package wrangler asset proxy class:

        ::

            >>> wrangler.asset_proxy_class.__name__
            'PackageProxy'

        Return class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.PackageProxy

    @property
    def storage_format(self):
        '''Material package wrangler storage format:

        ::

            >>> wrangler.storage_format
            'wranglers.MaterialPackageWrangler()'

        Return string.
        '''
        return super(MaterialPackageWrangler, self).storage_format

    ### PUBLIC METHODS ###

    def interactively_get_available_material_packagesystem_path(self, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        while True:
            getter = self._io.make_getter(where=self._where)
            getter.append_space_delimited_lowercase_string('material name')
            with self.backtracking:
                package_name = getter._run()
            if self._session.backtrack():
                return
            material_package_name = stringtools.string_to_accent_free_underscored_delimited_lowercase(
                package_name)
            material_package_path = '.'.join([
                self._current_storehouse_packagesystem_path, material_package_name])
            if self.configuration.packagesystem_path_exists(material_package_path):
                line = 'Material package {!r} already exists.'.format(material_package_path)
                self._io.display([line, ''])
            else:
                return material_package_path

    def interactively_make_data_package(self, tags=None, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        with self.backtracking:
            material_package_path = self.interactively_get_available_material_packagesystem_path()
        if self._session.backtrack():
            return
        self.make_data_package(material_package_path, tags=tags)

    def interactively_make_handmade_material_package(self, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        with self.backtracking:
            material_package_path = self.interactively_get_available_material_packagesystem_path()
        if self._session.backtrack():
            return
        self.make_handmade_material_package(material_package_path)

    def interactively_make_makermade_material_package(self, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        with self.backtracking:
            result = self._material_package_maker_wrangler.interactively_select_asset_packagesystem_path(
                cache=True, clear=False)
        if self._session.backtrack():
            return
        material_package_maker_package_path = result
        material_package_maker_class_name = material_package_maker_package_path.split('.')[-1]
        with self.backtracking:
            material_package_path = self.interactively_get_available_material_packagesystem_path()
        if self._session.backtrack():
            return
        self.make_makermade_material_package(
            material_package_path, material_package_maker_class_name)
        proxy = self._get_appropriate_material_package_proxy(
            material_package_maker_class_name, material_package_path)
        proxy.run_first_time()

    def interactively_make_numeric_sequence_package(self, user_input=None):
        tags = {'is_numeric_sequence': True}
        self.interactively_make_data_package(tags=tags, user_input=user_input)

    def list_asset_filesystem_paths(self,
        in_built_in_asset_library=True, in_user_asset_library=True,
        in_built_in_score_packages=True, in_user_score_packages=True, head=None):
        '''List asset filesystem paths.

        Example. List built-in material package filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     in_user_asset_library=False, in_user_score_packages=False):
            ...     x
            '.../abjad/experimental/tools/scoremanagertools/materialpackages/red_directives'
            '.../abjad/experimental/tools/scoremanagertools/materialpackages/red_forte'
            '.../abjad/experimental/tools/scoremanagertools/materialpackages/red_marcati'
            '.../abjad/experimental/tools/scoremanagertools/materialpackages/red_notes'
            '.../abjad/experimental/tools/scoremanagertools/materialpackages/red_numbers'
            '.../abjad/experimental/tools/scoremanagertools/materialpackages/red_sargasso_measures'
            '.../abjad/experimental/tools/scoremanagertools/materialpackages/sargasso_multipliers'
            '.../tools/scoremanagertools/scorepackages/red_example_score/music/materials/tempo_inventory'

        Return list.
        '''
        return super(MaterialPackageWrangler, self).list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_names(self,
        in_built_in_asset_library=True, in_user_asset_library=True,
        in_built_in_score_packages=True, in_user_score_packages=True, head=None):
        '''List asset names.

        Example. List built-in material package names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     in_user_asset_library=False, in_user_score_packages=False):
            ...     x
            'black music specifier'
            'green music specifier'
            'red directives'
            'red forte'
            'red marcati'
            'red notes'
            'red numbers'
            'red sargasso measures'
            'sargasso multipliers'
            'tempo inventory'

        Return list.
        '''
        return super(MaterialPackageWrangler, self).list_asset_names(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_packagesystem_paths(self,
        in_built_in_asset_library=True, in_user_asset_library=True,
        in_built_in_score_packages=True, in_user_score_packages=True, head=None):
        '''List asset packagesystem paths.

        Example. List built-in material package paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths(
            ...     in_user_asset_library=False, in_user_score_packages=False):
            ...     x
            'experimental.tools.scoremanagertools.materialpackages.black_music_specifier'
            'experimental.tools.scoremanagertools.materialpackages.green_music_specifier'
            'experimental.tools.scoremanagertools.materialpackages.red_directives'
            'experimental.tools.scoremanagertools.materialpackages.red_forte'
            'experimental.tools.scoremanagertools.materialpackages.red_marcati'
            'experimental.tools.scoremanagertools.materialpackages.red_notes'
            'experimental.tools.scoremanagertools.materialpackages.red_numbers'
            'experimental.tools.scoremanagertools.materialpackages.red_sargasso_measures'
            'experimental.tools.scoremanagertools.materialpackages.sargasso_multipliers'
            'experimental.tools.scoremanagertools.scorepackages.red_example_score.music.materials.tempo_inventory'

        Return list.
        '''
        return super(MaterialPackageWrangler, self).list_asset_packagesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_proxies(self, in_built_in_asset_library=True, in_user_asset_library=True,
        in_built_in_score_packages=True, in_user_score_packages=True, head=None):
        '''List asset proxies.

        Example. List built-in material package proxies:
            
        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     in_user_asset_library=False, in_user_score_packages=False):
            ...     x
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackages/black_music_specifier')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackages/green_music_specifier')
            MarkupInventoryMaterialPackageMaker('.../tools/scoremanagertools/materialpackages/red_directives')
            DynamicHandlerMaterialPackageMaker('.../tools/scoremanagertools/materialpackages/red_forte')
            ArticulationHandlerMaterialPackageMaker('.../tools/scoremanagertools/materialpackages/red_marcati')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackages/red_notes')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackages/red_numbers')
            SargassoMeasureMaterialPackageMaker('.../tools/scoremanagertools/materialpackages/red_sargasso_measures')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackages/sargasso_multipliers')
            TempoMarkInventoryMaterialPackageMaker('.../tools/scoremanagertools/scorepackages/red_example_score/music/materials/tempo_inventory')

        Return list.
        '''
        return super(MaterialPackageWrangler, self).list_asset_proxies(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_storehouse_filesystem_paths(self,
        in_built_in_asset_library=True, in_user_asset_library=True,
        in_built_in_score_packages=True, in_user_score_packages=True):
        '''List asset storehouse filesystem paths.

        Example. List built-in material package storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_asset_storehouse_filesystem_paths(
            ...     in_user_asset_library=False, in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/materialpackages'
            '.../tools/scoremanagertools/scorepackages/blue_example_score/music/materials'
            '.../tools/scoremanagertools/scorepackages/green_example_score/music/materials'
            '.../tools/scoremanagertools/scorepackages/red_example_score/music/materials'

        Return list.
        '''
        return super(MaterialPackageWrangler, self).list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages)

    def make_data_package(self, material_package_path, tags=None):
        tags = tags or {}
        tags['material_package_maker_class_name'] = None
        tags['should_have_illustration'] = False
        tags['should_have_user_input_module'] = False
        self.make_material_package(material_package_path, tags=tags)

    def make_handmade_material_package(self, material_package_path, tags=None):
        tags = tags or {}
        tags['material_package_maker_class_name'] = None
        tags['should_have_illustration'] = True
        tags['should_have_user_input_module'] = False
        self.make_material_package(material_package_path, tags=tags)

    def make_makermade_material_package(self,
        material_package_path, material_package_maker_class_name, tags=None):
        tags = tags or {}
        command = 'from experimental.tools.scoremanagertools.materialpackagemakers '
        command += 'import {} as material_package_maker_class'.format(
            material_package_maker_class_name)
        try:
            exec(command)
        except ImportError:
            command = 'from {} import {} as material_package_maker_class'.format(
                self.configuration.user_asset_library_material_package_makers_package_path, 
                material_package_maker_class_name)
            exec(command)
        should_have_user_input_module = getattr(
            material_package_maker_class, 'should_have_user_input_module', True)
        should_have_illustration = hasattr(material_package_maker_class, 'illustration_maker')
        tags['material_package_maker_class_name'] = material_package_maker_class_name
        tags['should_have_illustration'] = should_have_illustration
        tags['should_have_user_input_module'] = should_have_user_input_module
        self.make_material_package(material_package_path, tags=tags)

    def make_material_package(self, material_package_path, is_interactive=False, tags=None):
        tags = collections.OrderedDict(tags or {})
        tags['is_material_package'] = True
        directory_path = self.configuration.packagesystem_path_to_filesystem_path(
            material_package_path)
        assert not os.path.exists(directory_path)
        os.mkdir(directory_path)
        material_package_maker_class_name = tags.get('material_package_maker_class_name')
        pair = (material_package_maker_class_name, material_package_path)
        material_package_proxy = self._get_appropriate_material_package_proxy(*pair)
        material_package_proxy.initializer_file_proxy.write_stub_to_disk()
        material_package_proxy.tags_file_proxy.write_stub_to_disk()
        material_package_proxy.tags_file_proxy.write_tags_to_disk(tags)
        material_package_proxy.conditionally_write_stub_material_definition_module_to_disk()
        material_package_proxy.conditionally_write_stub_user_input_module_to_disk()
        line = 'material package {!r} created.'.format(material_package_path)
        self._io.proceed(line, is_interactive=is_interactive)

    def make_numeric_sequence_package(self, package_path):
        tags = {'is_numeric_sequence': True}
        self.make_data_package(package_path, tags=tags)

    ### UI MANIFEST ###

    user_input_to_action = PackageWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'd': interactively_make_data_package,
        's': interactively_make_numeric_sequence_package,
        'h': interactively_make_handmade_material_package,
        'm': interactively_make_makermade_material_package,
        })
