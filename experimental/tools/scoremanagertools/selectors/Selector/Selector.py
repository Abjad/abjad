# -*- encoding: utf-8 -*-
import os
from experimental.tools.scoremanagertools.scoremanager.ScoreManagerObject \
    import ScoreManagerObject


class Selector(ScoreManagerObject):

    ### INITIALIZER ###

    def __init__(
        self, 
        is_numbered=True,
        is_ranged=False, 
        items=None, 
        session=None,
        ):
        ScoreManagerObject.__init__(self, session=session)
        self.is_numbered = is_numbered
        self.is_ranged = is_ranged
        self.items = items or []

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if getattr(self, 'explicit_breadcrumb', None):
            return self.explicit_breadcrumb
        elif hasattr(self, 'space_delimited_lowercase_target_name'):
            return 'select {}:'.format(
                self.space_delimited_lowercase_target_name)
        else:
            return 'select:'

    ### PRIVATE METHODS ###

    def _make_main_menu(self, head=None):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        menu_section = main_menu._make_section(
            return_value_attribute='explicit',
            is_numbered=self.is_numbered,
            is_ranged=self.is_ranged,
            )
        menu_entries = self.make_menu_entries(head=head)
        menu_section.menu_entries = menu_entries
        return main_menu

    def _run(
        self, 
        cache=False,
        clear=True,
        head=None,
        pending_user_input=None,
        ):
        self.session.io_manager.assign_user_input(pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb(self._breadcrumb)
            menu = self._make_main_menu(head=head)
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            else:
                break
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        return result

    ### PUBLIC PROPERTIES ###

    @apply
    def items():
        def fget(self):
            if self._items:
                return self._items
            else:
                return self.list_items()
        def fset(self, items):
            self._items = items
        return property(**locals())

    ### PUBLIC METHODS ###

    def change_expr_to_menu_entry(self, expr):
        return (
            self.session.io_manager.get_one_line_menuing_summary(expr),
            None,
            None,
            expr,
            )

    def get_tag_from_directory_path(self, directory_path, tag_name):
        tags_file_name = os.path.join(directory_path, '__metadata__.py')
        if os.path.isfile(tags_file_name):
            tags_file = open(tags_file_name, 'r')
            tags_file_string = tags_file.read()
            tags_file.close()
            exec(tags_file_string)
            result = locals().get('tags') or OrderedDict([])
            return result.get(tag_name)

    def list_items(self):
        result = []
        return result

    def make_menu_entries(self, head=None):
        return [self.change_expr_to_menu_entry(item) for item in self.items]

    ### REAL PUBLIC METHODS ###

    @staticmethod
    def make_articulation_handler_selector(
        session=None,
        ):
        selector = Selector.make_material_package_selector(
            session=session,
            generic_output_name='articulation handler',
            )
        return selector

    @staticmethod
    def make_articulation_handler_class_name_selector(
        session=None, 
        ):
        selector = Selector.make_handler_class_name_selector(
            session=session,
            forbidden_directory_entries=['ArticulationHandler'],
            )
        return selector

    @staticmethod
    def make_clef_name_selector(
        session=None, 
        **kwargs
        ):
        from abjad.tools import contexttools
        selector = Selector(session=session, **kwargs)
        selector.items = contexttools.ClefMark.list_clef_names()
        return selector

    @staticmethod
    def make_directory_content_selector(
        session=None, 
        storehouse_filesystem_paths=None,
        forbidden_directory_entries=None,
        **kwargs
        ):
        from experimental.tools import scoremanagertools
        selector = Selector(session=session, **kwargs)
        storehouse_filesystem_paths = storehouse_filesystem_paths or []
        forbidden_directory_entries = forbidden_directory_entries or []
        items = []
        for directory_path in storehouse_filesystem_paths:
            proxy = scoremanagertools.proxies.DirectoryManager(
                filesystem_path=directory_path,
                session=session,
                )
            entries = proxy.list_directory(public_entries_only=True)
            for entry in entries:
                if entry not in forbidden_directory_entries:
                    items.append(entry)
            items.extend(entries)
        selector.items = items
        return selector

    @staticmethod
    def make_dynamic_handler_class_name_selector(
        session=None, 
        ):
        forbidden_directory_entries = [
            'Handler',
            'DynamicHandler',
            'test',
            ]
        selector = Selector.make_handler_class_name_selector(
            session=session,
            forbidden_directory_entries=forbidden_directory_entries,
            )
        return selector

    @staticmethod
    def make_dynamic_handler_package_selector(
        session=None,
        ):
        selector = Selector.make_material_package_selector(
            session=session,
            generic_output_name='dynamic handler',
            )
        return selector

    @staticmethod
    def make_handler_class_name_selector(
        session=None, 
        forbidden_directory_entries=None,
        **kwargs
        ):
        forbidden_directory_entries = forbidden_directory_entries or []
        handler_tools_directory_path = \
            Selector.configuration.handler_tools_directory_path
        selector = Selector.make_directory_content_selector(
            session=session,
            storehouse_filesystem_paths=[handler_tools_directory_path],
            forbidden_directory_entries=forbidden_directory_entries,
            )
        return selector

    @staticmethod
    def make_material_package_selector(
        session=None,
        generic_output_name='',
        ):
        selector = Selector(session=session)
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
            path = selector.session.current_materials_directory_path
            paths = list_public_directory_paths_with_initializers(path)
            for directory_path in paths:
                tag = selector.get_tag_from_directory_path(
                    directory_path, 
                    'generic_output_name',
                    )
                if tag == generic_output_name:
                    result.append(directory_path)
            return result
        items = []
        configuration = Selector.configuration
        for directory_path in list_current_material_directory_paths():
            package_path = configuration.filesystem_path_to_packagesystem_path(
                directory_path)
            items.append(package_path)
        selector.items = items
        return selector

    @staticmethod
    def make_rhythm_maker_class_name_selector(
        session=None,
        ):
        rhythm_maker_tools_directory_path = os.path.join(
            Selector.configuration.abjad_configuration.abjad_directory_path, 
            'tools', 
            'rhythmmakertools',
            )
        selector = Selector.make_directory_content_selector(
            session=session,
            storehouse_filesystem_paths=[rhythm_maker_tools_directory_path],
            )
        return selector

    @staticmethod
    def make_rhythm_maker_package_selector(
        session=None,
        ):
        selector = Selector.make_material_package_selector(
            session=session,
            generic_output_name='rhythm-maker',
            )
        return selector
