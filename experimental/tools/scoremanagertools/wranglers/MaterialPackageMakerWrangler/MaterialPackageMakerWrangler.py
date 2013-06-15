import os
from abjad.tools import stringtools
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from experimental.tools.scoremanagertools.wranglers.PackageWrangler \
    import PackageWrangler


class MaterialPackageMakerWrangler(PackageWrangler):
    '''Material package maker wrangler.

    ::

        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> wrangler = score_manager.material_package_maker_wrangler
        >>> wrangler
        MaterialPackageMakerWrangler()

    Return material package maker wrangler.
    '''

    ### CLASS VARIABLES ###

    asset_storehouse_packagesystem_path_in_built_in_asset_library = \
        PackageWrangler.configuration.built_in_material_package_makers_package_path

    forbidden_directory_entries = (
        'FunctionInputMaterialPackageMaker',
        'InventoryMaterialPackageMaker',
        'MaterialPackageMaker',
        )

    score_package_asset_storehouse_path_infix_parts = None

    asset_storehouse_packagesystem_path_in_user_asset_library = \
        PackageWrangler.configuration.user_asset_library_material_package_makers_package_path

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'material package makers'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            raise ValueError

    def _initialize_asset_proxy(self, package_path):
        from experimental.tools import scoremanagertools
        if os.path.sep in package_path:
            package_path = self.configuration.filesystem_path_to_packagesystem_path(package_path)
        material_package_proxy = \
            scoremanagertools.proxies.MaterialPackageProxy(
            package_path, session=self._session)
        material_package_maker_class_name = \
            material_package_proxy.material_package_maker_class_name
        if material_package_maker_class_name is not None:
            material_package_maker_class = None
            command = 'from experimental.tools.scoremanagertools.materialpackagemakers '
            command += 'import {} as material_package_maker_class'
            command = command.format(material_package_maker_class_name)
            try:
                exec(command)
            except ImportError:
                command = 'from {} import {} as material_package_maker_class'
                command = command.format(
                    self.configuration.user_asset_library_material_package_makers_package_path,
                    material_package_maker_class_name)
                exec(command)
            material_package_proxy = material_package_maker_class(
                package_path, session=self._session)
        return material_package_proxy

    def _make_main_menu(self, head=None):
        menu_entries = self.list_asset_names(head=head)
        menu, menu_section = self._io.make_menu(
            where=self._where,
            menu_entries=menu_entries,
            is_numbered=True,
            )
        menu_section = menu.make_section(return_value_attribute='key')
        menu_section.append(('new material package maker', 'new'))
        return menu

    def _make_menu_entries(self, head=None):
        keys = self.list_asset_packagesystem_paths(head=head)
        display_strings = self.list_asset_names(head=head)
        return zip(display_strings, keys)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        '''Asset proxy class:

        ::

            >>> wrangler.asset_proxy_class.__name__
            'PackageProxy'

        Return class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.PackageProxy

    @property
    def storage_format(self):
        '''Material package maker wrangler storage format:

        ::

            >>> wrangler.storage_format
            'wranglers.MaterialPackageMakerWrangler()'

        Return string.
        '''
        return super(MaterialPackageMakerWrangler, self).storage_format

    ### PUBLIC METHODS ###

    def interactively_make_asset(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_material_package_maker_class_name(
            'material proxy name')
        getter.append_space_delimited_lowercase_string(
            'generic output product')
        result = getter._run()
        if self._session.backtrack():
            return
        material_package_maker_class_name, generic_output_product_name = result
        material_package_maker_directory = os.path.join(
            self.asset_storehouse_packagesystem_path_in_built_in_asset_library,
            material_package_maker_class_name)
        os.mkdir(material_package_maker_directory)
        self.make_asset_initializer(material_package_maker_class_name)
        self.make_asset_class_file(
            material_package_maker_class_name, generic_output_product_name)
        self.make_asset_stylesheet(material_package_maker_class_name)

    def list_asset_filesystem_paths(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None):
        '''List asset filesystem paths.

        Example. List built-in material package maker filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/materialpackagemakers/ArticulationHandlerMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/DynamicHandlerMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/ListMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/MarkupInventoryMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/OctaveTranspositionMappingInventoryMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/PitchRangeInventoryMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/RhythmMakerMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/SargassoMeasureMaterialPackageMaker'
            '.../tools/scoremanagertools/materialpackagemakers/TempoMarkInventoryMaterialPackageMaker'

        Return list.
        '''
        return super(MaterialPackageMakerWrangler, self).list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_names(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None):
        '''List asset names.

        Example. List built-in material package maker names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            'articulation handler material package maker'
            'dynamic handler material package maker'
            'list material package maker'
            'markup inventory material package maker'
            'octave transposition mapping inventory material package maker'
            'pitch range inventory material package maker'
            'rhythm maker material package maker'
            'sargasso measure material package maker'
            'tempo mark inventory material package maker'

        Return list.
        '''
        return super(MaterialPackageMakerWrangler, self).list_asset_names(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_packagesystem_paths(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None):
        '''List asset packagesystem_paths.

        Example. List built-in material package maker package paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            'experimental.tools.scoremanagertools.materialpackagemakers.ArticulationHandlerMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.DynamicHandlerMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.ListMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.MarkupInventoryMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.OctaveTranspositionMappingInventoryMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.PitchRangeInventoryMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.RhythmMakerMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker'
            'experimental.tools.scoremanagertools.materialpackagemakers.TempoMarkInventoryMaterialPackageMaker'

        Return list.
        '''
        return super(MaterialPackageMakerWrangler, self).list_asset_packagesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_proxies(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None):
        '''List asset proxies.

        Example. List built-in material package maker proxies:

        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackagemakers/ArticulationHandlerMaterialPackageMaker')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackagemakers/DynamicHandlerMaterialPackageMaker')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackagemakers/ListMaterialPackageMaker')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackagemakers/MarkupInventoryMaterialPackageMaker')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackagemakers/OctaveTranspositionMappingInventoryMaterialPackageMaker')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackagemakers/PitchRangeInventoryMaterialPackageMaker')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackagemakers/RhythmMakerMaterialPackageMaker')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackagemakers/SargassoMeasureMaterialPackageMaker')
            MaterialPackageProxy('.../tools/scoremanagertools/materialpackagemakers/TempoMarkInventoryMaterialPackageMaker')

        Return list.
        '''
        return super(MaterialPackageMakerWrangler, self).list_asset_proxies(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_storehouse_filesystem_paths(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True):
        '''List asset storehouse filesystem paths.

        Example. List built-in material package maker storehouses:

        ::

            >>> for x in wrangler.list_asset_storehouse_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/materialpackagemakers'

        Return list.
        '''
        return super(MaterialPackageMakerWrangler, self).list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages)

    # TODO: change to boilerplate
    def make_asset_class_file(self, package_name, generic_output_name):
        class_file_name = os.path.join(
            self.asset_storehouse_packagesystem_path_in_built_in_asset_library,
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

    # TODO: change to boilerplate
    def make_asset_initializer(self, package_name):
        initializer_file_name = os.path.join(
            self.asset_storehouse_packagesystem_path_in_built_in_asset_library,
            package_name, 
            '__init__.py')
        initializer = file(initializer_file_name, 'w')
        line = 'from abjad.tools import importtools\n'
        initializer.write(line)
        initializer.write('\n')
        initializer.write(
            "importtools.import_structured_package(__path__[0], globals())\n")
        initializer.close()

    # TODO: change to boilerplate
    def make_asset_stylesheet(self, package_name):
        stylesheet = lilypondfiletools.make_basic_lilypond_file()
        stylesheet.pop()
        stylesheet.file_initial_system_comments = []
        stylesheet.default_paper_size = 'letter', 'portrait'
        stylesheet.global_staff_size = 14
        stylesheet.layout_block.indent = 0
        stylesheet.layout_block.ragged_right = True
        stylesheet.paper_block.markup_system_spacing = \
            layouttools.make_spacing_vector(0, 0, 12, 0)
        stylesheet.paper_block.system_system_spacing = \
            layouttools.make_spacing_vector(0, 0, 10, 0)
        stylesheet_file_name = os.path.join(
            self.asset_storehouse_packagesystem_path_in_built_in_asset_library,
            package_name, 
            'stylesheet.ly')
        stylesheet_file_pointer = file(stylesheet_file_name, 'w')
        stylesheet_file_pointer.write(stylesheet.format)
        stylesheet_file_pointer.close()

    ### UI MANIFEST ###

    user_input_to_action = PackageWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'new': interactively_make_asset,
        })
