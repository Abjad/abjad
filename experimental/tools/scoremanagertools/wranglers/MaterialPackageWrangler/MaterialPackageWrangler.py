import collections
import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools import predicates
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler


# TODO: write all iteration tests
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

    ### CLASS ATTRIBUTES ###
    
    asset_container_path_infix_parts = ('music', 'materials')

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        PackageWrangler.__init__(self,
            built_in_score_external_asset_container_packagesystem_path=\
                self.configuration.built_in_materials_package_path,
            user_score_external_asset_container_packagesystem_path=\
                self.configuration.user_materials_package_path,
            session=session,
            )
        self._material_package_maker_wrangler = \
            scoremanagertools.wranglers.MaterialPackageMakerWrangler(session=self._session)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'materials'

    ### PRIVATE METHODS ###

    def _get_asset_proxy(self, package_path):
        return self._material_package_maker_wrangler._get_asset_proxy(package_path)

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
            self.make_asset_container_packages(is_interactive=True)
        elif result == 'profile':
            self.profile_visible_assets()
        else:
            material_package_proxy = self._get_asset_proxy(result)
            material_package_proxy._run()

    def _list_asset_container_package_paths(self, head=None):
        '''Material package wrangler list asset container package paths:

        ::

            >>> for x in wrangler._list_asset_container_package_paths():
            ...     x
            'built_in_materials'
            'experimental.tools.scoremanagertools.built_in_scores.blue_example_score.music.materials'
            'experimental.tools.scoremanagertools.built_in_scores.green_example_score.music.materials'
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.materials'
            ...

        Output lists built-in materials, followed by built-in scores,
        followed by user scores.

        Return list.
        '''
        return super(type(self), self)._list_asset_container_package_paths(head=head)

    def _list_score_external_asset_container_filesystem_paths(self, head=None):
        '''Material package wrangler list score external asset container directory paths:

        ::

            >>> for x in wrangler._list_score_external_asset_container_filesystem_paths():
            ...     x
            '/Users/trevorbaca/Documents/abjad/experimental/built_in_materials'
            '/Users/trevorbaca/Documents/baca/music/materials'
            ...

        Output lists score-external materials followed by score internal materials.

        Return list.
        '''
        return super(type(self), self)._list_score_external_asset_container_filesystem_paths(head=head)

    def _list_score_internal_asset_container_filesystem_paths(self, head=None):
        '''Material package wrangler list score internal asset container directory paths:

        ::

            >>> for x in wrangler._list_score_internal_asset_container_filesystem_paths():
            ...     x
            '.../tools/scoremanagertools/built_in_scores/blue_example_score/music/materials'
            '.../tools/scoremanagertools/built_in_scores/green_example_score/music/materials'
            '.../tools/scoremanagertools/built_in_scores/red_example_score/music/materials'
            ...

        Return list.
        '''
        return super(type(self), self)._list_score_internal_asset_container_filesystem_paths(head=head)

    def _list_score_internal_asset_container_package_paths(self, head=None):
        '''Material package wrangler list score internal asset container package paths:

        ::

            >>> for x in wrangler._list_score_internal_asset_container_package_paths():
            ...     x
            'experimental.tools.scoremanagertools.built_in_scores.blue_example_score.music.materials'
            'experimental.tools.scoremanagertools.built_in_scores.green_example_score.music.materials'
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.materials'
            ...

        Output lists built-in scores followed by user scores.

        Return list.
        '''
        return super(type(self), self)._list_score_internal_asset_container_package_paths(head=head)

    def _list_user_asset_container_filesystem_paths(self, head=None):
        '''Material package wrangler list user asset container filesystem paths:

        ::

            >>> for x in wrangler._list_user_asset_container_filesystem_paths():
            ...     x
            '/Users/trevorbaca/Documents/baca/music/materials'
            ...

        Output lists score-external path followed
        by any score-internal paths.

        Return list.
        '''
        return super(type(self), self)._list_user_asset_container_filesystem_paths(head=head)

    def _make_main_menu(self, head=None):
        menu, section = self._io.make_menu(where=self._where, is_numbered=True, is_keyed=False)
        section.tokens = self._make_visible_asset_menu_tokens(head=head)
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
    def asset_container_proxy_class(self):
        '''Material package wrangler asset proxy class:

        ::

            >>> wrangler.asset_container_proxy_class.__name__
            'PackageProxy'

        Return class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.PackageProxy

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
    def built_in_score_external_asset_container_filesystem_path(self):
        '''Material package wrangler built-in asset container filesystem path:

        ::

            >>> wrangler.built_in_score_external_asset_container_filesystem_path
            '.../abjad/experimental/built_in_materials'

        Return string.
        '''
        return super(type(self), self).built_in_score_external_asset_container_filesystem_path

    @property
    def built_in_score_external_asset_container_packagesystem_path(self):
        '''Material package wrangler built-in asset container package path:

        ::

            >>> wrangler.built_in_score_external_asset_container_packagesystem_path
            'built_in_materials'

        Return string.
        '''
        return super(type(self), self).built_in_score_external_asset_container_packagesystem_path

    @property
    def current_asset_container_filesystem_path(self):
        '''Material filesystem wrangler current asset container filesystem path:

        ::

            >>> wrangler.current_asset_container_filesystem_path
            '/Users/trevorbaca/Documents/abjad/experimental/built_in_materials'

        While in built-in score:

        ::

            >>> wrangler_in_built_in_score.current_asset_container_filesystem_path
            '.../tools/scoremanagertools/built_in_scores/red_example_score/music/materials'

        Return string.
        '''
        return super(type(self), self).current_asset_container_filesystem_path

    @property
    def current_asset_container_packagesystem_path(self):
        '''Material package wrangler current asset container package path:

        ::

            >>> wrangler.current_asset_container_packagesystem_path
            'built_in_materials'

        While in built-in score:

        ::

            >>> wrangler_in_built_in_score.current_asset_container_packagesystem_path
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.materials'

        Return string.
        '''
        return super(type(self), self).current_asset_container_packagesystem_path

    @property
    def storage_format(self):
        '''Material package wrangler storage format:

        ::

            >>> wrangler.storage_format
            'wranglers.MaterialPackageWrangler()'

        Return string.
        '''
        return super(type(self), self).storage_format

    @property
    def user_score_external_asset_container_filesystem_path(self):
        '''Material package wrangler user asset container filesystem path:

        ::

            >>> wrangler.user_score_external_asset_container_filesystem_path
            '/Users/trevorbaca/Documents/baca/music/materials'

        Return string.
        '''
        return super(type(self), self).user_score_external_asset_container_filesystem_path

    @property
    def user_score_external_asset_container_packagesystem_path(self):
        '''Material package wrangler user score-external asset container package path:

        ::

            >>> wrangler.user_score_external_asset_container_packagesystem_path
            '...materials'

        Return string.
        '''
        return super(type(self), self).user_score_external_asset_container_packagesystem_path

    ### PUBLIC METHODS ###

    def get_appropriate_material_package_proxy(self,
        material_package_maker_class_name, material_package_path):
        from experimental.tools import scoremanagertools
        if material_package_maker_class_name is None:
            material_package_proxy = scoremanagertools.proxies.MaterialPackageProxy(
                material_package_path, session=self._session)
        else:
            command = 'material_package_proxy = '
            command += 'scoremanagertools.materialpackagemakers.{}(material_package_path, session=self._session)'
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

    def get_asset_proxies(self, head=None):
        '''Material package wranglger get asset proxies:

        ::

            >>> for x in wrangler.get_asset_proxies():
            ...     x
            MarkupInventoryMaterialPackageMaker('.../abjad/experimental/built_in_materials/red_directives')
            DynamicHandlerMaterialPackageMaker('.../abjad/experimental/built_in_materials/red_forte')
            ArticulationHandlerMaterialPackageMaker('.../abjad/experimental/built_in_materials/red_marcati')
            MaterialPackageProxy('.../abjad/experimental/built_in_materials/red_notes')
            MaterialPackageProxy('.../abjad/experimental/built_in_materials/red_numbers')
            SargassoMeasureMaterialPackageMaker('.../abjad/experimental/built_in_materials/red_sargasso_measures')
            MaterialPackageProxy('.../abjad/experimental/built_in_materials/sargasso_multipliers')
            ...
            TempoMarkInventoryMaterialPackageMaker('.../tools/scoremanagertools/built_in_scores/red_example_score/music/materials/tempo_inventory')
            ...

        Output lists score-external materials followed by score-internal materials. 

        Return list.
        '''
        return super(type(self), self).get_asset_proxies(head=head)

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
                self.current_asset_container_packagesystem_path, material_package_name])
            if self.configuration.packagesystem_path_exists(material_package_path):
                line = 'Material package {!r} already exists.'.format(material_package_path)
                self._io.display([line, ''])
            else:
                return material_package_path

    def get_score_external_asset_proxies(self, head=None):
        '''Material package wrangler get score-external asset proxies:

        ::

            >>> for x in wrangler.get_score_external_asset_proxies():
            ...     x
            MarkupInventoryMaterialPackageMaker('.../abjad/experimental/built_in_materials/red_directives')
            DynamicHandlerMaterialPackageMaker('.../abjad/experimental/built_in_materials/red_forte')
            ArticulationHandlerMaterialPackageMaker('.../abjad/experimental/built_in_materials/red_marcati')
            MaterialPackageProxy('.../abjad/experimental/built_in_materials/red_notes')
            MaterialPackageProxy('.../abjad/experimental/built_in_materials/red_numbers')
            SargassoMeasureMaterialPackageMaker('.../abjad/experimental/built_in_materials/red_sargasso_measures')
            MaterialPackageProxy('.../abjad/experimental/built_in_materials/sargasso_multipliers')
            ...

        Output lists built-in materials followed by user materials.

        Return list.
        '''
        return super(type(self), self).get_score_external_asset_proxies(head=head)

    def get_score_internal_asset_proxies(self, head=None):
        '''Material package wrangler get score-internal asset proxies:

        ::

            >>> for x in wrangler.get_score_internal_asset_proxies():
            ...     x
            TempoMarkInventoryMaterialPackageMaker('.../tools/scoremanagertools/built_in_scores/red_example_score/music/materials/tempo_inventory')
            ...

        Output lists proxies for built-in score-internal materials
        followed by proxies for user score-internal materials.

        Return list.
        '''
        return super(type(self), self).get_score_internal_asset_proxies(head=head)

    def get_user_asset_proxies(self, head=None):
        '''Material package wranglger get user asset proxies:

        ::

            >>> 1 <= len(wrangler.get_user_asset_proxies())
            True

        Return list.
        '''
        return super(type(self), self).get_user_asset_proxies(head=head)

    def list_asset_filesystem_paths(self, head=None):
        '''Material package wrangler list asset filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths():
            ...     x
            '.../abjad/experimental/built_in_materials/red_directives'
            '.../abjad/experimental/built_in_materials/red_forte'
            '.../abjad/experimental/built_in_materials/red_marcati'
            '.../abjad/experimental/built_in_materials/red_notes'
            '.../abjad/experimental/built_in_materials/red_numbers'
            '.../abjad/experimental/built_in_materials/red_sargasso_measures'
            '.../abjad/experimental/built_in_materials/sargasso_multipliers'
            ...

        User-specific output elided above.

        Return list.
        '''
        return super(type(self), self).list_asset_filesystem_paths(head=head) 

    def list_asset_packagesystem_paths(self, head=None):
        '''Material package wrangler list asset package paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths():
            ...     x
            'built_in_materials.red_directives'
            'built_in_materials.red_forte'
            'built_in_materials.red_marcati'
            'built_in_materials.red_notes'
            'built_in_materials.red_numbers'
            'built_in_materials.red_sargasso_measures'
            'built_in_materials.sargasso_multipliers'
            ...
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.materials.tempo_inventory'
            ...

        User-specific output elided above.

        Return list.
        '''
        return super(type(self), self).list_asset_packagesystem_paths(head=head) 

    def list_built_in_score_internal_asset_filesystem_paths(self, head=None):
        '''Material package wrangler list built-in score-internal asset filesystem paths:

        ::

            >>> for x in wrangler.list_built_in_score_internal_asset_filesystem_paths():
            ...     x
            '.../experimental/tools/scoremanagertools/built_in_scores/red_example_score/music/materials/tempo_inventory'

        Return list.
        '''
        return super(type(self), self).list_built_in_score_internal_asset_filesystem_paths(head=head)

    def list_built_in_score_internal_asset_packagesystem_paths(self, head=None):
        '''Material package wrangler list built-in score-internal asset package paths:

        ::

            >>> for x in wrangler.list_built_in_score_internal_asset_packagesystem_paths():
            ...     x
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.materials.tempo_inventory'

        Return list.
        '''
        return super(type(self), self).list_built_in_score_internal_asset_packagesystem_paths(head=head)

    def list_score_external_asset_filesystem_paths(self, head=None):
        '''Material package wrangler list score-external asset filesystem paths:

        ::

            >>> for x in wrangler.list_score_external_asset_filesystem_paths():
            ...     x
            '.../abjad/experimental/built_in_materials/red_directives'
            '.../abjad/experimental/built_in_materials/red_forte'
            '.../abjad/experimental/built_in_materials/red_marcati'
            '.../abjad/experimental/built_in_materials/red_notes'
            '.../abjad/experimental/built_in_materials/red_numbers'
            '.../abjad/experimental/built_in_materials/red_sargasso_measures'
            '.../abjad/experimental/built_in_materials/sargasso_multipliers'
            ...

        (User-specific output elided.)

        Return list.
        '''
        return super(type(self), self).list_score_external_asset_filesystem_paths(head=head)

    def list_score_external_asset_packagesystem_paths(self, head=None):
        '''Material package wrangler list score-external asset package paths:

        ::

            >>> for x in wrangler.list_score_external_asset_packagesystem_paths():
            ...     x
            'built_in_materials.red_directives'
            'built_in_materials.red_forte'
            'built_in_materials.red_marcati'
            'built_in_materials.red_notes'
            'built_in_materials.red_numbers'
            'built_in_materials.red_sargasso_measures'
            'built_in_materials.sargasso_multipliers'
            ...

        (User-specific output elided.)

        Return list.
        '''
        return super(type(self), self).list_score_external_asset_packagesystem_paths(head=head)

    def list_score_internal_asset_filesystem_paths(self, head=None):
        '''Material package wrangler list score-internal asset filesystem paths:

        ::

            >>> for x in wrangler.list_score_internal_asset_filesystem_paths():
            ...     x
            '.../experimental/tools/scoremanagertools/built_in_scores/red_example_score/music/materials/tempo_inventory'
            ...

        (User-specific output elided.)

        Return list.
        '''
        return super(type(self), self).list_score_internal_asset_filesystem_paths(head=head)

    def list_score_internal_asset_packagesystem_paths(self, head=None):
        '''Material package wrangler list score-internal asset package paths:

        ::

            >>> for x in wrangler.list_score_internal_asset_packagesystem_paths():
            ...     x
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music.materials.tempo_inventory'
            ...

        (User-specific output elided.)

        Return list.
        '''
        return super(type(self), self).list_score_internal_asset_packagesystem_paths(head=head)

    def list_user_asset_filesystem_paths(self, head=None):
        '''Material package wrangler list user asset filesystem paths:

        ::

            >>> for x in wrangler.list_user_asset_filesystem_paths():
            ...     x
            '...'
            ...

        Return list.
        '''
        return super(type(self), self).list_user_asset_filesystem_paths(head=head)

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
        proxy = self.get_appropriate_material_package_proxy(
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
        material_package_proxy = self.get_appropriate_material_package_proxy(*pair)
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
