# -*- encoding: utf-8 -*-
import collections
import os
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Selector(ScoreManagerObject):
    r'''Selector.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_numbered',
        '_is_ranged',
        '_items',
        '_menu_entries',
        '_my_where',
        '_return_value_attribute',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        is_numbered=True,
        is_ranged=False, 
        items=None, 
        return_value_attribute='explicit',
        session=None,
        where=None,
        ):
        ScoreManagerObject.__init__(self, session=session)
        self._is_numbered = is_numbered
        self._is_ranged = is_ranged
        self._items = items or []
        self._return_value_attribute = return_value_attribute
        self._my_where = where

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'select:'

    ### PRIVATE METHODS ###

    def _make_asset_menu_section(self, menu):
        if hasattr(self, 'menu_entries'):
            menu_entries = self.menu_entries
        else:
            menu_entries = self._make_menu_entries()
        if not menu_entries:
            return
        section = menu._make_section(
            name='assets',
            is_asset_section=True,
            is_numbered=self.is_numbered,
            is_ranged=self.is_ranged,
            return_value_attribute=self.return_value_attribute,
            )
        for menu_entry in menu_entries:
            section.append(menu_entry)
        return section

    def _make_main_menu(self, name='selector'):
        menu = self._io_manager.make_menu(
            where=self._where,
            name=name,
            )
        self._make_asset_menu_section(menu)
        return menu

    def _make_menu_entries(self):
        entries = []
        for item in self.items:
            entry = (
                self._io_manager._get_one_line_menu_summary(item),
                None,
                None,
                item,
                )
            entries.append(entry)
        return entries

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        with iotools.ControllerContext(self):
            while True:
                menu = self._make_main_menu()
                result = menu._run()
                if self._should_backtrack():
                    return
                if result:
                    return result

    def _should_backtrack(self):
        if self._session.is_complete:
            return True
        elif self._session.is_backtracking_to_score_manager:
            return True
        # keep on backtracking ... do not consume this backtrack
        elif self._session.is_backtracking_locally:
            return True
        elif self._session.is_backtracking_to_score:
            return True
        elif self._session.is_autonavigating_within_score:
            return True
        else:
            return False

    ### PUBLIC PROPERTIES ###

    @property
    def is_numbered(self):
        r'''Is true when selector is numbered. Otherwise false.

        Returns boolean.
        '''
        return self._is_numbered

    @property
    def is_ranged(self):
        r'''Is true when selector is ranged. Otherwise false.

        Returns boolean.
        '''
        return self._is_ranged

    @property
    def items(self):
        r'''Gets selector items.

        Returns list.
        '''
        return self._items

    @property
    def menu_entries(self):
        r'''Gets menu entries of selector.

        Returns list.
        '''
        return self._menu_entries

    @property
    def return_value_attribute(self):
        r'''Gets return value attribute of selector.

        Returns string.
        '''
        return self._return_value_attribute

    @property
    def where(self):
        r'''Gets where of selector.

        Returns stack or none.
        '''
        return self._my_where

    ### PUBLIC METHODS ###

    def make_articulation_handler_class_name_selector(self):
        r'''Makes articulation handler class name selector.

        Returns selector.
        '''
        selector = self.make_handler_class_name_selector(
            base_class_names=('ArticulationHandler',),
            forbidden_class_names=('ArticulationHandler',),
            )
        return selector

    def make_clef_name_selector(self):
        r'''Makes clef name selector.

        Returns selector.
        '''
        from abjad.tools import indicatortools
        items = indicatortools.Clef._list_clef_names()
        selector = Selector(
            session=self._session,
            items=items,
            )
        return selector

    def make_directory_content_selector(
        self,
        storehouse_paths=None,
        forbidden_directory_entries=None,
        endswith=None,
        strip_file_extensions=False,
        ):
        r'''Makes directory content selector.

        Returns selector.
        '''
        from scoremanager import managers
        storehouse_paths = storehouse_paths or []
        forbidden_directory_entries = forbidden_directory_entries or []
        items = []
        for directory_path in storehouse_paths:
            manager = managers.DirectoryManager(
                path=directory_path,
                session=self._session,
                )
            entries = manager._list(public_entries_only=True)
            for entry in entries:
                if strip_file_extensions:
                    entry = os.path.splitext(entry)[0]
                if entry not in forbidden_directory_entries:
                    if not endswith:
                        items.append(entry)
                    elif entry.endswith(endswith):
                        items.append(entry)
        selector = Selector(
            session=self._session,
            items=items,
            )
        return selector

    def make_dynamic_handler_class_name_selector(self):
        r'''Makes dynamic handler class name selector.

        Returns selector.
        '''
        selector = self.make_handler_class_name_selector(
            base_class_names=('DynamicHandler', 'DynamicsHandler'),
            forbidden_class_names=('DynamicHandler',)
            )
        return selector

    def make_handler_class_name_selector(
        self,
        base_class_names=None,
        forbidden_class_names=None,
        ):
        r'''Makes handler class name selector.

        Returns seelctor.
        '''
        configuration = self._configuration
        base_class_names = base_class_names or ()
        forbidden_class_names = forbidden_class_names or ()
        directory_path = configuration.handler_tools_directory_path
        class_names = []
        for entry in os.listdir(directory_path):
            if entry.endswith('.py'):
                for base_class_name in base_class_names:
                    if base_class_name in entry:
                        class_name, extension = os.path.splitext(entry)
                        if class_name not in forbidden_class_names:
                            class_names.append(class_name)
                        continue
        selector = Selector(
            session=self._session,
            items=class_names,
            )
        return selector

    def make_material_package_selector(
        self,
        generic_output_name='',
        output_class_name='',
        ):
        r'''Makes material package selector.

        Returns selector.
        '''
        from scoremanager import managers
        configuration = self._configuration
        def list_public_directory_paths(subtree_path):
            result = []
            for triple in os.walk(subtree_path):
                subtree_path = triple[0]
                directory_names = triple[1]
                if '.svn' not in subtree_path:
                    for directory_name in directory_names:
                        if '.svn' not in directory_name:
                            if directory_name[0].isalpha():
                                directory_path = os.path.join(
                                    subtree_path, 
                                    directory_name,
                                    )
                                result.append(directory_path)
            return result
        def list_current_material_directory_paths():
            result = []
            path = self._session.current_materials_directory_path
            paths = list_public_directory_paths(path)
            for directory_path in paths:
                manager = managers.DirectoryManager(
                    path=directory_path,
                    session=self._session,
                    )
                metadatum = manager._get_metadatum('generic_output_name')
                if metadatum and metadatum == generic_output_name:
                    result.append(directory_path)
                    continue
                metadatum = manager._get_metadatum('output_class_name')
                if metadatum and metadatum == output_class_name:
                    result.append(directory_path)
                    continue
            return result
        #wrangler = wranglers.MaterialPackageWrangler(session=self._session)
        package_paths = []
        for path in list_current_material_directory_paths():
            package_path = configuration.path_to_package_path(path)
            package_paths.append(package_path)
        selector = Selector(
            session=self._session,
            items=package_paths,
            )
        return selector

    def make_performer_selector(self):
        r'''Makes performer selector.

        Returns selector.
        '''
        items = []
        manager = self._session.current_score_package_manager
        if hasattr(manager, '_get_instrumentation'):
            instrumentation = manager._get_instrumentation()
            items.extend(instrumentation.performers)
        selector = Selector(
            session=self._session,
            items=items,
            )
        return selector

    def make_rhythm_maker_class_name_selector(self):
        r'''Makes rhythm-maker class name selector.

        Returns selector.
        '''
        configuration = self._configuration
        rhythm_maker_tools_directory_path = os.path.join(
            configuration.abjad_directory_path, 
            'tools', 
            'rhythmmakertools',
            )
        selector = self.make_directory_content_selector(
            storehouse_paths=[rhythm_maker_tools_directory_path],
            endswith='RhythmMaker',
            strip_file_extensions=True,
            )
        return selector

    def make_score_instrument_selector(self):
        r'''Makes score instrument selector.

        Returns selector.
        '''
        items = []
        if self._session.is_in_score:
            manager = self._session.current_score_package_manager
            instrumentation = manager._get_instrumentation()
            items.extend(instrumentation.instruments)
            items.append('other')
        selector = Selector(
            session=self._session,
            items=items,
            )
        return selector

    def make_score_tools_performer_name_selector(self, is_ranged=False):
        r'''Makes scoretools performer name selector.

        Returns selector.
        '''
        from abjad.tools import instrumenttools
        class_ = instrumenttools.Performer
        performer_pairs = class_.list_primary_performer_names()
        performer_pairs.append(('percussionist', 'perc.'))
        performer_pairs.sort()
        menu_entries = []
        for performer_pair in performer_pairs:
            performer_name, performer_abbreviation = performer_pair
            performer_abbreviation = performer_abbreviation.split()[-1]
            performer_abbreviation = performer_abbreviation.strip('.')
            menu_entries.append((performer_name, performer_abbreviation)) 
        selector = Selector(
            session=self._session,
            is_ranged=is_ranged,
            return_value_attribute='display_string',
            )
        selector._menu_entries = menu_entries
        return selector

    def make_tempo_selector(self):
        r'''Makes tempo selector.

        Returns selector.
        '''
        items = []
        manager = self._session.current_score_package_manager
        if hasattr(manager, '_get_tempo_inventory'):
            items = manager._get_tempo_inventory()
        selector = type(self)(
            session=self._session,
            items=items,
            )
        return selector