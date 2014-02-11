# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from experimental.tools.scoremanagertools.wranglers.PackageWrangler \
    import PackageWrangler


class MaterialPackageMakerWrangler(PackageWrangler):
    r'''Material package maker wrangler.

    ::

        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> wrangler = score_manager.material_package_maker_wrangler
        >>> wrangler
        MaterialPackageMakerWrangler()

    '''

    ### CLASS VARIABLES ###

    asset_storehouse_packagesystem_path_in_built_in_asset_library = \
        PackageWrangler.configuration.built_in_material_package_makers_package_path

    forbidden_directory_entries = (
        'InventoryMaterialPackageMaker.py',
        'MaterialPackageMaker.py',
        )

    score_package_asset_storehouse_path_infix_parts = None

    asset_storehouse_packagesystem_path_in_user_asset_library = \
        PackageWrangler.configuration.user_asset_library_material_package_makers_package_path

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'material package makers'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            raise ValueError

    def _initialize_asset_manager(self, package_path):
        from experimental.tools import scoremanagertools
        if os.path.sep in package_path:
            package_path = \
                self.configuration.filesystem_path_to_packagesystem_path(
                    package_path)
        material_package_manager = \
            scoremanagertools.managers.MaterialPackageManager(
            package_path, session=self.session)
        if 'materialpackagemakers' in material_package_manager.filesystem_path:
            most, last = os.path.split(
                material_package_manager.filesystem_path)
            material_package_maker_class_name = last
        else:
            material_package_maker_class_name = \
                material_package_manager.material_package_maker_class_name
        if material_package_maker_class_name is not None:
            material_package_maker_class = None
            command = 'from experimental.tools.scoremanagertools'
            command += '.materialpackagemakers '
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
            material_package_manager = material_package_maker_class(
                package_path, session=self.session)
        return material_package_manager

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry in ('test', 'stylesheets'):
            return False
        if directory_entry.endswith('.pyc'):
            return False
        if directory_entry in self.forbidden_directory_entries:
            return False
        if directory_entry[0].isalpha():
            if directory_entry[0].isupper():
                return True
        return False

    def _make_asset_menu_entries(self, head=None):
        names = self.list_asset_names(head=head)
        paths = self.list_asset_packagesystem_paths(head=head)
        assert len(names) == len(paths)
        sequences = (names, [None], [None], paths)
        return sequencetools.zip_sequences(sequences, cyclic=True)

    def _make_main_menu(self, head=None):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        asset_section = main_menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        asset_section.menu_entries = asset_menu_entries
        command_section = main_menu.make_command_section()
        command_section.append(('new material package maker', 'new'))
        return main_menu

    ### PUBLIC METHODS ###

    def interactively_make_asset(
        self,
        pending_user_input=None,
        ):
        r'''Interactively makes asset.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_material_package_maker_class_name(
            'material manager name')
        getter.append_space_delimited_lowercase_string(
            'generic output product')
        result = getter._run()
        if self.session.backtrack():
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

    def list_asset_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Example. List built-in material package maker filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../materialpackagemakers/ArticulationHandlerMaterialPackageMaker.py'
            '.../materialpackagemakers/DynamicHandlerMaterialPackageMaker.py'
            '.../materialpackagemakers/ListMaterialPackageMaker.py'
            '.../materialpackagemakers/MarkupInventoryMaterialPackageMaker.py'
            '.../materialpackagemakers/OctaveTranspositionMappingInventoryMaterialPackageMaker.py'
            '.../materialpackagemakers/PitchRangeInventoryMaterialPackageMaker.py'
            '.../materialpackagemakers/RhythmMakerMaterialPackageMaker.py'
            '.../materialpackagemakers/SargassoMeasureMaterialPackageMaker.py'
            '.../materialpackagemakers/TempoInventoryMaterialPackageMaker.py'

        Returns list.
        '''
        superclass = super(MaterialPackageMakerWrangler, self)
        return superclass.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_managers(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        Example. List built-in material package maker managers:

        ::

            >>> for x in wrangler.list_asset_managers(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            ArticulationHandlerMaterialPackageMaker('.../materialpackagemakers/ArticulationHandlerMaterialPackageMaker')
            DynamicHandlerMaterialPackageMaker('.../materialpackagemakers/DynamicHandlerMaterialPackageMaker')
            ListMaterialPackageMaker('.../materialpackagemakers/ListMaterialPackageMaker')
            MarkupInventoryMaterialPackageMaker('.../materialpackagemakers/MarkupInventoryMaterialPackageMaker')
            OctaveTranspositionMappingInventoryMaterialPackageMaker('.../materialpackagemakers/OctaveTranspositionMappingInventoryMaterialPackageMaker')
            PitchRangeInventoryMaterialPackageMaker('.../materialpackagemakers/PitchRangeInventoryMaterialPackageMaker')
            RhythmMakerMaterialPackageMaker('.../materialpackagemakers/RhythmMakerMaterialPackageMaker')
            SargassoMeasureMaterialPackageMaker('.../materialpackagemakers/SargassoMeasureMaterialPackageMaker')
            TempoInventoryMaterialPackageMaker('.../materialpackagemakers/TempoInventoryMaterialPackageMaker')

        Returns list.
        '''
        superclass = super(MaterialPackageMakerWrangler, self)
        return superclass.list_asset_managers(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_names(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset names.

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
            'tempo inventory material package maker'

        Returns list.
        '''
        superclass = super(MaterialPackageMakerWrangler, self)
        return superclass.list_asset_names(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_packagesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset packagesystem_paths.

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
            'experimental.tools.scoremanagertools.materialpackagemakers.TempoInventoryMaterialPackageMaker'

        Returns list.
        '''
        superclass = super(MaterialPackageMakerWrangler, self)
        return superclass.list_asset_packagesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_storehouse_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Example. List built-in material package maker storehouses:

        ::

            >>> for x in wrangler.list_asset_storehouse_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/materialpackagemakers'

        Returns list.
        '''
        superclass = super(MaterialPackageMakerWrangler, self)
        return superclass.list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            )

    # TODO: change to boilerplate
    def make_asset_class_file(self, package_name, generic_output_name):
        r'''Makes asset class file.

        Returns none.
        '''
        class_file_name = os.path.join(
            self.asset_storehouse_packagesystem_path_in_built_in_asset_library,
            package_name, package_name + '.py')
        class_file = file(class_file_name, 'w')
        lines = []
        lines.append('from foo import foo')
        lines.append('from foo import make_illustration_from_output_material')
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
        lines.append('    ### PUBLIC PROPERTIES ###')
        lines.append('')
        lines.append('    generic_output_name = {!r}'.format(generic_output_name))
        lines.append('')
        lines.append('    illustration_builder = staticmethod(make_illustration_from_output_material)')
        lines.append('')
        lines.append('    output_material_checker = staticmethod(scoretools.all_are_components)')
        lines.append('')
        lines.append('    output_material_maker = staticmethod(foo)')
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
        r'''Makes asset initializer.

        Returns none.
        '''
        initializer_file_name = os.path.join(
            self.asset_storehouse_packagesystem_path_in_built_in_asset_library,
            package_name, 
            '__init__.py',
            )
        initializer = file(initializer_file_name, 'w')
        line = 'from abjad.tools import systemtools\n'
        initializer.write(line)
        initializer.write('\n')
        initializer.write(
            "systemtools.ImportManager.import_structured_package(__path__[0], globals())\n")
        initializer.close()

    # TODO: change to boilerplate
    def make_asset_stylesheet(self, package_name):
        r'''Makes asset stylesheet.

        Returns none.
        '''
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
