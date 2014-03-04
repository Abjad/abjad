# -*- encoding: utf-8 -*-
import os
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class MaterialManagerWrangler(PackageWrangler):
    r'''material manager wrangler.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager()
            >>> wrangler = score_manager._material_manager_wrangler
            >>> wrangler
            MaterialManagerWrangler()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(MaterialManagerWrangler, self)
        superclass.__init__(session=session)
        self.abjad_storehouse_path = \
            self._configuration.abjad_material_managers_directory_path
        self.user_storehouse_path = \
            self._configuration.user_library_material_managers_directory_path
        self._human_readable_target_name = 'material manager'
        self.forbidden_directory_entries = (
            'InventoryMaterialManager.py',
            'MaterialManager.py',
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'material managers'

    @property
    def _user_input_to_action(self):
        superclass = super(MaterialManagerWrangler, self)
        _user_input_to_action = superclass._user_input_to_action
        _user_input_to_action = _user_input_to_action.copy()
        _user_input_to_action.update({
            })
        return _user_input_to_action

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        else:
            raise ValueError

    def _initialize_asset_manager(self, package_path):
        from scoremanager import managers
        if os.path.sep in package_path:
            path = package_path
            package_path = self._configuration.path_to_package(package_path)
        else:
            path = self._configuration.package_to_path(package_path)
        material_manager = managers.MaterialManager(
            path=path, 
            session=self._session,
            )
        if 'managers' in material_manager._path:
            most, last = os.path.split(
                material_manager._path)
            material_manager_class_name = last
        else:
            material_manager_class_name = \
                material_manager._read_material_manager_class_name()
        if material_manager_class_name is not None:
            material_manager_class = None
            command = 'from scoremanager'
            command += '.managers '
            command += 'import {} as material_manager_class'
            command = command.format(material_manager_class_name)
            try:
                exec(command)
            except ImportError:
                command = 'from {} import {} as material_manager_class'
                path = self._configuration.user_library_material_packages_directory_path
                package_path = self._configuration.path_to_package(path)
                command = command.format(
                    package_path,
                    material_manager_class_name,
                    )
                exec(command)
            material_manager = material_manager_class(
                path=path, 
                session=self._session,
                )
        return material_manager

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry in ('test', 'stylesheets'):
            return False
        if directory_entry.endswith('.pyc'):
            return False
        if directory_entry in self.forbidden_directory_entries:
            return False
        if not directory_entry.endswith('MaterialManager.py'):
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
        main_menu = self._io_manager.make_menu(where=self._where)
        asset_section = main_menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        asset_section.menu_entries = asset_menu_entries
        command_section = main_menu.make_command_section()
        command_section.append(('new material manager', 'new'))
        return main_menu

    ### PUBLIC METHODS ###

    def _list_asset_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Lists abjad material manager filesystem paths:

        ::

            >>> for x in wrangler._list_asset_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            '.../managers/ArticulationHandlerMaterialManager.py'
            '.../managers/DynamicHandlerMaterialManager.py'
            '.../managers/ListMaterialManager.py'
            '.../managers/MarkupInventoryMaterialManager.py'
            '.../managers/OctaveTranspositionMappingInventoryMaterialManager.py'
            '.../managers/PitchRangeInventoryMaterialManager.py'
            '.../managers/RhythmMakerMaterialManager.py'
            '.../managers/SargassoMeasureMaterialManager.py'
            '.../managers/TempoInventoryMaterialManager.py'

        Returns list.
        '''
        superclass = super(MaterialManagerWrangler, self)
        return superclass._list_asset_paths(
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

        Lists abjad material manager managers:

        ::

            >>> for x in wrangler._list_asset_managers(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            ArticulationHandlerMaterialManager('.../managers/ArticulationHandlerMaterialManager')
            DynamicHandlerMaterialManager('.../managers/DynamicHandlerMaterialManager')
            ListMaterialManager('.../managers/ListMaterialManager')
            MarkupInventoryMaterialManager('.../managers/MarkupInventoryMaterialManager')
            OctaveTranspositionMappingInventoryMaterialManager('.../managers/OctaveTranspositionMappingInventoryMaterialManager')
            PitchRangeInventoryMaterialManager('.../managers/PitchRangeInventoryMaterialManager')
            RhythmMakerMaterialManager('.../managers/RhythmMakerMaterialManager')
            SargassoMeasureMaterialManager('.../managers/SargassoMeasureMaterialManager')
            TempoInventoryMaterialManager('.../managers/TempoInventoryMaterialManager')

        Returns list.
        '''
        superclass = super(MaterialManagerWrangler, self)
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

        Lists abjad material manager names:

        ::

            >>> for x in wrangler._list_asset_names(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            'articulation handler material manager'
            'dynamic handler material manager'
            'list material manager'
            'markup inventory material manager'
            'octave transposition mapping inventory material manager'
            'pitch range inventory material manager'
            'rhythm maker material manager'
            'sargasso measure material manager'
            'tempo inventory material manager'

        Returns list.
        '''
        superclass = super(MaterialManagerWrangler, self)
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

        Lists abjad material manager package paths:

        ::

            >>> for x in wrangler._list_asset_package_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            'scoremanager.managers.ArticulationHandlerMaterialManager'
            'scoremanager.managers.DynamicHandlerMaterialManager'
            'scoremanager.managers.ListMaterialManager'
            'scoremanager.managers.MarkupInventoryMaterialManager'
            'scoremanager.managers.OctaveTranspositionMappingInventoryMaterialManager'
            'scoremanager.managers.PitchRangeInventoryMaterialManager'
            'scoremanager.managers.RhythmMakerMaterialManager'
            'scoremanager.managers.SargassoMeasureMaterialManager'
            'scoremanager.managers.TempoInventoryMaterialManager'

        Returns list.
        '''
        superclass = super(MaterialManagerWrangler, self)
        return superclass._list_asset_package_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_storehouse_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Lists abjad material manager storehouses:

        ::

            >>> for x in wrangler._list_storehouse_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            '.../scoremanager/managers'

        Returns list.
        '''
        superclass = super(MaterialManagerWrangler, self)
        return superclass._list_storehouse_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )
