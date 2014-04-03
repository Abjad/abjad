# -*- encoding: utf-8 -*-
import os
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class MaterialManagerWrangler(Wrangler):
    r'''material manager wrangler.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager(is_test=True)
            >>> wrangler = score_manager._material_manager_wrangler
            >>> wrangler
            MaterialManagerWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_human_readable_target_name',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(MaterialManagerWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = \
            self._configuration.abjad_material_managers_directory_path
        self._user_storehouse_path = \
            self._configuration.user_library_material_managers_directory_path
        self._human_readable_target_name = 'material manager'
        self._forbidden_directory_entries = (
            'InventoryMaterialManager.py',
            'MaterialPackageManager.py',
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _asset_manager_class(self):
        from scoremanager import managers
        return managers.MaterialManagerWrangler

    @property
    def _breadcrumb(self):
        return 'material managers'

    @property
    def _user_input_to_action(self):
        superclass = super(MaterialManagerWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            })
        return result

    ### PRIVATE METHODS ###

    def _get_current_directory_path_of_interest(self):
        pass

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        else:
            raise ValueError

    def _initialize_asset_manager(self, path):
        from scoremanager import managers
        assert os.path.sep in path, repr(path)
        manager = managers.MaterialPackageManager(
            path=path, 
            session=self._session,
            )
        class_name = manager._get_metadatum('material_manager_class_name')
        if class_name == 'TempoInventoryMaterialManager':
            return manager
        if class_name is None:
            return manager
        class_ = None
        command = 'from scoremanager.managers import {} as class_'
        command = command.format(class_name)
        try:
            exec(command)
        except ImportError:
            command = 'from {} import {} as class_'
            configuration = self._configuration
            path = configuration.user_library_material_packages_directory_path
            package_path = self._configuration.path_to_package_path(path)
            command = command.format(
                package_path,
                class_name,
                )
            exec(command)
        manager = class_(path=path, session=self._session)
        return manager

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry in ('test', 'stylesheets'):
            return False
        if directory_entry.endswith('.pyc'):
            return False
        if directory_entry in self._forbidden_directory_entries:
            return False
        if not directory_entry.endswith('MaterialManager.py'):
            return False
        if directory_entry[0].isalpha():
            if directory_entry[0].isupper():
                return True
        return False

    def _make_main_menu(self, name='material manager wrangler'):
        menu = self._io_manager.make_menu(
            where=self._where,
            name=name,
            )
        section = menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries()
        for menu_entry in asset_menu_entries:
            section.append(menu_entry)
        section = menu.make_command_section()
        section.append(('material manager - new', 'new'))
        return menu