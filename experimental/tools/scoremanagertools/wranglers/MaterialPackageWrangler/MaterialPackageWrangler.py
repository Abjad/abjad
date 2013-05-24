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
    
    storehouse_path_infix_parts = ('music', 'materials')
    built_in_external_storehouse_packagesystem_path = \
        PackageWrangler.configuration.built_in_materials_package_path
    user_external_storehouse_packagesystem_path = \
        PackageWrangler.configuration.user_materials_package_path

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
                    self.configuration.user_material_package_makers_package_path, 
                    material_package_maker_class_name)
                exec(command)
                material_package_proxy = material_package_maker_class(
                    material_package_path, session=self._session)
        return material_package_proxy

    def _handle_main_menu_result(self, result):
        if result == 'd':
            self.make_data_package_interactively()
        elif result == 's':
            self.make_numeric_sequence_package_interactively()
        elif result == 'h':
            self.make_handmade_material_package_interactively()
        elif result == 'm':
            self.make_makermade_material_package_interactively()
        elif result == 'missing':
            self.make_storehouse_packages(is_interactive=True)
        elif result == 'profile':
            self.profile_visible_assets()
        else:
            material_package_proxy = self._initialize_asset_proxy(result)
            material_package_proxy._run()

    def _initialize_asset_proxy(self, package_path):
        return self._material_package_maker_wrangler._initialize_asset_proxy(package_path)

    def _list_score_storehouse_package_paths(self, head=None):
        '''Material package wrangler list score internal storehouse package paths:

        ::

            >>> for x in wrangler._list_score_storehouse_package_paths():
            ...     x
            'experimental.tools.scoremanagertools.built_in_scores.blue_example_score.music.materials'
            'experimental.tools.scoremanagertools.built_in_scores.green_example_score.music.materials'
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.materials'
            ...

        Output lists built-in scores followed by user scores.

        Return list.
        '''
        return super(type(self), self)._list_score_storehouse_package_paths(head=head)

    def _list_storehouse_package_paths(self, head=None):
        '''Material package wrangler list storehouse package paths:

        ::

            >>> for x in wrangler._list_storehouse_package_paths():
            ...     x
            'experimental.tools.scoremanagertools.built_in_materials'
            'experimental.tools.scoremanagertools.built_in_scores.blue_example_score.music.materials'
            'experimental.tools.scoremanagertools.built_in_scores.green_example_score.music.materials'
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.materials'
            ...

        Output lists built-in materials, followed by built-in scores,
        followed by user scores.

        Return list.
        '''
        return super(type(self), self)._list_storehouse_package_paths(head=head)

    def _make_main_menu(self, head=None):
        menu, section = self._io.make_menu(where=self._where, is_numbered=True, is_keyed=False)
        section.tokens = self._make_menu_tokens(head=head)
        section = menu.make_section()
        section.append(('d', 'data-only'))
        section.append(('h', 'handmade'))
        section.append(('m', 'maker-made'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('s', 'create numeric sequence'))
        hidden_section.append(('missing', 'create missing packages'))
        hidden_section.append(('profile', 'profile packages'))
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
        return super(type(self), self).storage_format

    ### PUBLIC METHODS ###

    def get_available_material_packagesystem_path_interactively(self, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        while True:
            getter = self._io.make_getter(where=self._where)
            getter.append_space_delimited_lowercase_string('material name')
            self._session.push_backtrack()
            package_name = getter._run()
            self._session.pop_backtrack()
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

    def list_asset_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset filesystem paths.

        Example. List built-in material package filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../abjad/experimental/tools/scoremanagertools/built_in_materials/red_directives'
            '.../abjad/experimental/tools/scoremanagertools/built_in_materials/red_forte'
            '.../abjad/experimental/tools/scoremanagertools/built_in_materials/red_marcati'
            '.../abjad/experimental/tools/scoremanagertools/built_in_materials/red_notes'
            '.../abjad/experimental/tools/scoremanagertools/built_in_materials/red_numbers'
            '.../abjad/experimental/tools/scoremanagertools/built_in_materials/red_sargasso_measures'
            '.../abjad/experimental/tools/scoremanagertools/built_in_materials/sargasso_multipliers'
            '.../tools/scoremanagertools/built_in_scores/red_example_score/music/materials/tempo_inventory'

        Return list.
        '''
        return super(type(self), self).list_asset_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_asset_names(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset names.

        Example. List built-in material package names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     user_external=False, user_score=False):
            ...     x
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
        return super(type(self), self).list_asset_names(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_asset_packagesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset packagesystem paths.

        Example. List built-in material package paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            'experimental.tools.scoremanagertools.built_in_materials.red_directives'
            'experimental.tools.scoremanagertools.built_in_materials.red_forte'
            'experimental.tools.scoremanagertools.built_in_materials.red_marcati'
            'experimental.tools.scoremanagertools.built_in_materials.red_notes'
            'experimental.tools.scoremanagertools.built_in_materials.red_numbers'
            'experimental.tools.scoremanagertools.built_in_materials.red_sargasso_measures'
            'experimental.tools.scoremanagertools.built_in_materials.sargasso_multipliers'
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.materials.tempo_inventory'

        Return list.
        '''
        return super(type(self), self).list_asset_packagesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_asset_proxies(self, built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset proxies.

        Example. List built-in material package proxies:
            
        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     user_external=False, user_score=False):
            ...     x
            MarkupInventoryMaterialPackageMaker('.../tools/scoremanagertools/built_in_materials/red_directives')
            DynamicHandlerMaterialPackageMaker('.../tools/scoremanagertools/built_in_materials/red_forte')
            ArticulationHandlerMaterialPackageMaker('.../tools/scoremanagertools/built_in_materials/red_marcati')
            MaterialPackageProxy('.../tools/scoremanagertools/built_in_materials/red_notes')
            MaterialPackageProxy('.../tools/scoremanagertools/built_in_materials/red_numbers')
            SargassoMeasureMaterialPackageMaker('.../tools/scoremanagertools/built_in_materials/red_sargasso_measures')
            MaterialPackageProxy('.../tools/scoremanagertools/built_in_materials/sargasso_multipliers')
            TempoMarkInventoryMaterialPackageMaker('.../tools/scoremanagertools/built_in_scores/red_example_score/music/materials/tempo_inventory')

        Return list.
        '''
        return super(type(self), self).list_asset_proxies(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_storehouse_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List storehouse filesystem paths.

        Example. List built-in material package storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_storehouse_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../tools/scoremanagertools/built_in_materials'
            '.../tools/scoremanagertools/built_in_scores/blue_example_score/music/materials'
            '.../tools/scoremanagertools/built_in_scores/green_example_score/music/materials'
            '.../tools/scoremanagertools/built_in_scores/red_example_score/music/materials'

        Return list.
        '''
        return super(type(self), self).list_storehouse_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def make_data_package(self, material_package_path, tags=None):
        tags = tags or {}
        tags['material_package_maker_class_name'] = None
        tags['should_have_illustration'] = False
        tags['should_have_user_input_module'] = False
        self.make_material_package(material_package_path, tags=tags)

    def make_data_package_interactively(self, tags=None, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._session.push_backtrack()
        material_package_path = self.get_available_material_packagesystem_path_interactively()
        self._session.pop_backtrack()
        if self._session.backtrack():
            return
        self.make_data_package(material_package_path, tags=tags)

    def make_handmade_material_package(self, material_package_path, tags=None):
        tags = tags or {}
        tags['material_package_maker_class_name'] = None
        tags['should_have_illustration'] = True
        tags['should_have_user_input_module'] = False
        self.make_material_package(material_package_path, tags=tags)

    def make_handmade_material_package_interactively(self, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._session.push_backtrack()
        material_package_path = self.get_available_material_packagesystem_path_interactively()
        self._session.pop_backtrack()
        if self._session.backtrack():
            return
        self.make_handmade_material_package(material_package_path)

    def make_makermade_material_package(self,
        material_package_path, material_package_maker_class_name, tags=None):
        tags = tags or {}
        command = 'from experimental.tools.scoremanagertools.materialpackagemakers import {} as material_package_maker_class'.format(
            material_package_maker_class_name)
        try:
            exec(command)
        except ImportError:
            command = 'from {} import {} as material_package_maker_class'.format(
                self.configuration.user_material_package_makers_package_path, 
                material_package_maker_class_name)
            exec(command)
        should_have_user_input_module = getattr(
            material_package_maker_class, 'should_have_user_input_module', True)
        should_have_illustration = hasattr(material_package_maker_class, 'illustration_maker')
        tags['material_package_maker_class_name'] = material_package_maker_class_name
        tags['should_have_illustration'] = should_have_illustration
        tags['should_have_user_input_module'] = should_have_user_input_module
        self.make_material_package(material_package_path, tags=tags)

    def make_makermade_material_package_interactively(self, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._session.push_backtrack()
        result = self._material_package_maker_wrangler.select_asset_packagesystem_path_interactively(
            cache=True, clear=False)
        self._session.pop_backtrack()
        if self._session.backtrack():
            return
        material_package_maker_package_path = result
        material_package_maker_class_name = material_package_maker_package_path.split('.')[-1]
        self._session.push_backtrack()
        material_package_path = self.get_available_material_packagesystem_path_interactively()
        self._session.pop_backtrack()
        if self._session.backtrack():
            return
        self.make_makermade_material_package(
            material_package_path, material_package_maker_class_name)
        proxy = self._get_appropriate_material_package_proxy(
            material_package_maker_class_name, material_package_path)
        proxy.run_first_time()

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
        material_package_proxy.tags_file_proxy.write_tags_to_disk(tags)
        material_package_proxy.conditionally_write_stub_material_definition_module_to_disk()
        material_package_proxy.conditionally_write_stub_user_input_module_to_disk()
        line = 'material package {!r} created.'.format(material_package_path)
        self._io.proceed(line, is_interactive=is_interactive)

    def make_numeric_sequence_package(self, package_path):
        tags = {'is_numeric_sequence': True}
        self.make_data_package(package_path, tags=tags)

    def make_numeric_sequence_package_interactively(self, user_input=None):
        tags = {'is_numeric_sequence': True}
        self.make_data_package_interactively(tags=tags, user_input=user_input)
