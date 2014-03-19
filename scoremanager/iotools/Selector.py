# -*- encoding: utf-8 -*-
import collections
import os
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Selector(ScoreManagerObject):
    r'''Selector.
    '''

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
        self.is_numbered = is_numbered
        self.is_ranged = is_ranged
        self._items = items or []
        self.return_value_attribute = return_value_attribute
        self.where = where

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if getattr(self, 'explicit_breadcrumb', None):
            return self.explicit_breadcrumb
        elif hasattr(self, 'space_delimited_lowercase_target_name'):
            string = 'select {}:'
            string = string.format(self.space_delimited_lowercase_target_name)
            return string
        else:
            return 'select:'

    ### PRIVATE METHODS ###

    def _change_expr_to_menu_entry(self, expr):
        return (
            self._io_manager._get_one_line_menu_summary(expr),
            None,
            None,
            expr,
            )

    def _get_metadata_from_directory_path(
        self, 
        directory_path, 
        metadatum_name,
        ):
        metadata_module_path = os.path.join(directory_path, '__metadata__.py')
        if os.path.isfile(metadata_module_path):
            metadata_module = open(metadata_module_path, 'r')
            metadata_module_string = metadata_module.read()
            metadata_module.close()
            try:
                exec(metadata_module_string)
            except:
                pass
            result = locals().get('metadata') or collections.OrderedDict([])
            return result.get(metadatum_name)

    def _list_items(self):
        result = []
        return result

    def _make_asset_menu_section(self, menu):
        section = menu._make_section(
            name='assets',
            is_asset_section=True,
            is_numbered=self.is_numbered,
            is_ranged=self.is_ranged,
            return_value_attribute=self.return_value_attribute,
            )
        if hasattr(self, 'menu_entries'):
            menu_entries = self.menu_entries
        else:
            menu_entries = self._make_menu_entries()
        for menu_entry in menu_entries:
            section.append(menu_entry)
        return section

    def _make_main_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        self._make_asset_menu_section(menu)
        return menu

    def _make_menu_entries(self):
        return [self._change_expr_to_menu_entry(item) for item in self.items]

    def _run(
        self, 
        cache=False,
        clear=True,
        pending_user_input=None,
        ):
        self._io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        while True:
            self._session._push_breadcrumb(self._breadcrumb)
            menu = self._make_main_menu()
            result = menu._run(clear=clear)
            if self._session._backtrack():
                break
            elif not result:
                self._session._pop_breadcrumb()
                continue
            else:
                break
        self._session._pop_breadcrumb()
        self._session._restore_breadcrumbs(cache=cache)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets selector items.

        Returns list.
        '''
        return self._items

    ### PUBLIC METHODS ###

    @staticmethod
    def make_articulation_handler_class_name_selector(
        session=None, 
        ):
        r'''Makes articulation handler class name selector.

        Returns selector.
        '''
        selector = Selector.make_handler_class_name_selector(
            session=session,
            base_class_names=('ArticulationHandler',),
            forbidden_class_names=('ArticulationHandler',),
            )
        return selector

    @staticmethod
    def make_articulation_handler_selector(
        session=None,
        ):
        r'''Makes articulation handler selector.

        Returns selector.
        '''
        selector = Selector.make_material_package_selector(
            session=session,
            generic_output_name='articulation handler',
            )
        return selector

    @staticmethod
    def make_clef_name_selector(
        session=None, 
        ):
        r'''Makes clef name selector.

        Returns selector.
        '''
        from abjad.tools import indicatortools
        items = indicatortools.Clef._list_clef_names()
        selector = Selector(
            session=session,
            items=items,
            )
        return selector

    @staticmethod
    def make_directory_content_selector(
        session=None, 
        storehouse_paths=None,
        forbidden_directory_entries=None,
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
                session=session,
                )
            entries = manager._list(public_entries_only=True)
            for entry in entries:
                if strip_file_extensions:
                    entry = os.path.splitext(entry)[0]
                if entry not in forbidden_directory_entries:
                    items.append(entry)
        selector = Selector(
            session=session,
            items=items,
            )
        return selector

    @staticmethod
    def make_dynamic_handler_class_name_selector(
        session=None, 
        ):
        r'''Makes dynamic handler class name selector.

        Returns selector.
        '''
        selector = Selector.make_handler_class_name_selector(
            session=session,
            base_class_names=('DynamicHandler', 'DynamicsHandler'),
            forbidden_class_names=('DynamicHandler',)
            )
        return selector

    @staticmethod
    def make_dynamic_handler_package_selector(
        session=None,
        ):
        r'''Makes dynamic handler package selector.

        Returns selector.
        '''
        selector = Selector.make_material_package_selector(
            session=session,
            generic_output_name='dynamic handler',
            )
        return selector

    @staticmethod
    def make_handler_class_name_selector(
        session=None, 
        base_class_names=None,
        forbidden_class_names=None,
        ):
        r'''Makes handler class name selector.

        Returns seelctor.
        '''
        from scoremanager import core
        configuration = core.ScoreManagerConfiguration()
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
            session=session,
            items=class_names,
            )
        return selector

    @staticmethod
    def make_material_package_selector(
        session=None,
        generic_output_name='',
        ):
        r'''Makes material package selector.

        Returns selector.
        '''
        from scoremanager import core
        configuration = core.ScoreManagerConfiguration()
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
        def list_public_directory_paths_with_initializers(subtree_path):
            result = []
            for directory_path in list_public_directory_paths(subtree_path):
                if '__init__.py' in os.listdir(directory_path):
                    result.append(directory_path)
            return result
        def list_current_material_directory_paths():
            result = []
            tmp_selector = Selector(session=session)
            path = tmp_selector._session.current_materials_directory_path
            paths = list_public_directory_paths_with_initializers(path)
            for directory_path in paths:
                metadatum = tmp_selector._get_metadata_from_directory_path(
                    directory_path, 
                    'generic_output_name',
                    )
                if metadatum == generic_output_name:
                    result.append(directory_path)
            return result
        items = []
        for directory_path in list_current_material_directory_paths():
            package_path = configuration.path_to_package_path(directory_path)
            items.append(package_path)
        selector = Selector(
            session=session,
            items=items,
            )
        return selector

    @staticmethod
    def make_performer_selector(
        session=None,
        ):
        r'''Makes performer selector.

        Returns selector.
        '''
        items = []
        manager = session.current_score_package_manager
        if hasattr(manager, '_get_instrumentation'):
            instrumentation = manager._get_instrumentation()
            items.extend(instrumentation.performers)
        selector = Selector(
            session=session,
            items=items,
            )
        return selector

    @staticmethod
    def make_pitch_class_reservoir_selector(
        session=None,
        ):
        r'''Makes pitch-class reservoir selector.

        Returns selector.
        '''
        selector = Selector.make_material_package_selector(
            session=session,
            generic_output_name='pitch class reservoir',
            )
        return selector

    @staticmethod
    def make_rhythm_maker_class_name_selector(
        session=None,
        ):
        r'''Makes rhythm-maker class name selector.

        Returns selector.
        '''
        from scoremanager import core
        configuration = core.ScoreManagerConfiguration()
        rhythm_maker_tools_directory_path = os.path.join(
            configuration.abjad_directory_path, 
            'tools', 
            'rhythmmakertools',
            )
        selector = Selector.make_directory_content_selector(
            session=session,
            storehouse_paths=[rhythm_maker_tools_directory_path],
            strip_file_extensions=True,
            )
        return selector

    @staticmethod
    def make_rhythm_maker_package_selector(
        session=None,
        ):
        r'''Makes rhythm-maker package selector.

        Returns selector.
        '''
        selector = Selector.make_material_package_selector(
            session=session,
            generic_output_name='rhythm-maker',
            )
        return selector

    @staticmethod
    def make_score_instrument_selector(
        session=None,
        ):
        r'''Makes score instrument selector.

        Returns selector.
        '''
        items = []
        if session.is_in_score:
            manager = session.current_score_package_manager
            instrumentation = manager._get_instrumentation()
            items.extend(instrumentation.instruments)
            items.append('other')
        selector = Selector(
            session=session,
            items=items,
            )
        return selector

    @staticmethod
    def make_score_tools_performer_name_selector(
        session=None,
        ):
        r'''Makes scoretools performer name selector.

        Returns selector.
        '''
        from abjad.tools import instrumenttools
        performer_pairs = \
            instrumenttools.Performer.list_primary_performer_names()
        performer_pairs.append(('percussionist', 'perc.'))
        performer_pairs.sort()
        menu_entries = []
        for performer_pair in performer_pairs:
            performer_name, performer_abbreviation = performer_pair
            performer_abbreviation = performer_abbreviation.split()[-1]
            performer_abbreviation = performer_abbreviation.strip('.')
            menu_entries.append((performer_name, performer_abbreviation)) 
        selector = Selector(session=session)
        selector.return_value_attribute = 'display_string'
        selector.menu_entries = menu_entries
        return selector

    @staticmethod
    def make_tempo_selector(
        session=None,
        ):
        r'''Makes tempo selector.

        Returns selector.
        '''
        items = []
        manager = session.current_score_package_manager
        if hasattr(manager, '_get_tempo_inventory'):
            items = manager._get_tempo_inventory()
        selector = Selector(
            session=session,
            items=items,
            )
        return selector
