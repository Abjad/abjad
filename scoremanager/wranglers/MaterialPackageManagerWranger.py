# -*- encoding: utf-8 -*-
import os
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class MaterialPackageManagerWrangler(PackageWrangler):
    r'''Material package manager wrangler.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager()
            >>> wrangler = score_manager._material_package_manager_wrangler
            >>> wrangler
            MaterialPackageManagerWrangler()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(MaterialPackageManagerWrangler, self)
        superclass.__init__(session=session)
        self.abjad_storehouse_directory_path = \
            self._configuration.abjad_material_package_managers_directory_path
        self.user_storehouse_directory_path = \
            self._configuration.user_library_material_package_managers_directory_path
        self._human_readable_target_name = 'material package manager'
        self.forbidden_directory_entries = (
            'InventoryMaterialPackageManager.py',
            'MaterialPackageManager.py',
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'material package managers'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result](self)
        else:
            raise ValueError

    def _initialize_asset_manager(self, package_path):
        from scoremanager import managers
        if os.path.sep in package_path:
            package_path = \
                self._configuration.filesystem_path_to_package_path(
                    package_path)
        material_package_manager = managers.MaterialPackageManager(
            package_path, session=self._session)
        if 'materialpackagemanagers' in material_package_manager._filesystem_path:
            most, last = os.path.split(
                material_package_manager._filesystem_path)
            material_package_manager_class_name = last
        else:
            material_package_manager_class_name = \
                material_package_manager.material_package_manager_class_name
        if material_package_manager_class_name is not None:
            material_package_manager_class = None
            command = 'from scoremanager'
            command += '.materialpackagemanagers '
            command += 'import {} as material_package_manager_class'
            command = command.format(material_package_manager_class_name)
            try:
                exec(command)
            except ImportError:
                command = 'from {} import {} as material_package_manager_class'
                package_path = '.'.join([
                    self._configuration._user_library_directory_name,
                    'material_packges',
                    ])
                command = command.format(
                    package_path,
                    material_package_manager_class_name,
                    )
                exec(command)
            material_package_manager = material_package_manager_class(
                package_path, session=self._session)
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
        names = self._list_asset_names(head=head)
        paths = self._list_asset_package_paths(head=head)
        assert len(names) == len(paths)
        sequences = (names, [None], [None], paths)
        return sequencetools.zip_sequences(sequences, cyclic=True)

    def _make_main_menu(self, head=None):
        main_menu = self._session.io_manager.make_menu(where=self._where)
        asset_section = main_menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        asset_section.menu_entries = asset_menu_entries
        command_section = main_menu.make_command_section()
        command_section.append(('new material package manager', 'new'))
        return main_menu

    ### PUBLIC METHODS ###

    def _list_asset_filesystem_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Lists abjad material package manager filesystem paths:

        ::

            >>> for x in wrangler._list_asset_filesystem_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            '.../materialpackagemanagers/ArticulationHandlerMaterialPackageManager.py'
            '.../materialpackagemanagers/DynamicHandlerMaterialPackageManager.py'
            '.../materialpackagemanagers/ListMaterialPackageManager.py'
            '.../materialpackagemanagers/MarkupInventoryMaterialPackageManager.py'
            '.../materialpackagemanagers/OctaveTranspositionMappingInventoryMaterialPackageManager.py'
            '.../materialpackagemanagers/PitchRangeInventoryMaterialPackageManager.py'
            '.../materialpackagemanagers/RhythmMakerMaterialPackageManager.py'
            '.../materialpackagemanagers/SargassoMeasureMaterialPackageManager.py'
            '.../materialpackagemanagers/TempoInventoryMaterialPackageManager.py'

        Returns list.
        '''
        superclass = super(MaterialPackageManagerWrangler, self)
        return superclass._list_asset_filesystem_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_managers(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        Lists abjad material package manager managers:

        ::

            >>> for x in wrangler._list_asset_managers(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            ArticulationHandlerMaterialPackageManager('.../materialpackagemanagers/ArticulationHandlerMaterialPackageManager')
            DynamicHandlerMaterialPackageManager('.../materialpackagemanagers/DynamicHandlerMaterialPackageManager')
            ListMaterialPackageManager('.../materialpackagemanagers/ListMaterialPackageManager')
            MarkupInventoryMaterialPackageManager('.../materialpackagemanagers/MarkupInventoryMaterialPackageManager')
            OctaveTranspositionMappingInventoryMaterialPackageManager('.../materialpackagemanagers/OctaveTranspositionMappingInventoryMaterialPackageManager')
            PitchRangeInventoryMaterialPackageManager('.../materialpackagemanagers/PitchRangeInventoryMaterialPackageManager')
            RhythmMakerMaterialPackageManager('.../materialpackagemanagers/RhythmMakerMaterialPackageManager')
            SargassoMeasureMaterialPackageManager('.../materialpackagemanagers/SargassoMeasureMaterialPackageManager')
            TempoInventoryMaterialPackageManager('.../materialpackagemanagers/TempoInventoryMaterialPackageManager')

        Returns list.
        '''
        superclass = super(MaterialPackageManagerWrangler, self)
        return superclass._list_asset_managers(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_names(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset names.

        Lists abjad material package manager names:

        ::

            >>> for x in wrangler._list_asset_names(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            'articulation handler material package manager'
            'dynamic handler material package manager'
            'list material package manager'
            'markup inventory material package manager'
            'octave transposition mapping inventory material package manager'
            'pitch range inventory material package manager'
            'rhythm maker material package manager'
            'sargasso measure material package manager'
            'tempo inventory material package manager'

        Returns list.
        '''
        superclass = super(MaterialPackageManagerWrangler, self)
        return superclass._list_asset_names(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_package_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset package_paths.

        Lists abjad material package manager package paths:

        ::

            >>> for x in wrangler._list_asset_package_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            'scoremanager.materialpackagemanagers.ArticulationHandlerMaterialPackageManager'
            'scoremanager.materialpackagemanagers.DynamicHandlerMaterialPackageManager'
            'scoremanager.materialpackagemanagers.ListMaterialPackageManager'
            'scoremanager.materialpackagemanagers.MarkupInventoryMaterialPackageManager'
            'scoremanager.materialpackagemanagers.OctaveTranspositionMappingInventoryMaterialPackageManager'
            'scoremanager.materialpackagemanagers.PitchRangeInventoryMaterialPackageManager'
            'scoremanager.materialpackagemanagers.RhythmMakerMaterialPackageManager'
            'scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager'
            'scoremanager.materialpackagemanagers.TempoInventoryMaterialPackageManager'

        Returns list.
        '''
        superclass = super(MaterialPackageManagerWrangler, self)
        return superclass._list_asset_package_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_storehouse_directory_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Lists abjad material package manager storehouses:

        ::

            >>> for x in wrangler._list_storehouse_directory_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            '.../scoremanager/materialpackagemanagers'

        Returns list.
        '''
        superclass = super(MaterialPackageManagerWrangler, self)
        return superclass._list_storehouse_directory_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )

    ### UI MANIFEST ###

    _user_input_to_action = PackageWrangler._user_input_to_action.copy()
    _user_input_to_action.update({
        })
