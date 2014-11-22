# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import datastructuretools
from abjad.tools import documentationtools
from abjad.tools import rhythmmakertools
from abjad.tools import stringtools
from scoremanager.idetools.Controller import Controller


class Selector(Controller):
    r'''Selector.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_breadcrumb',
        '_is_numbered',
        '_is_ranged',
        '_items',
        '_menu_entries',
        '_return_value_attribute',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        breadcrumb=None,
        is_numbered=True,
        is_ranged=False,
        items=None,
        menu_entries=None,
        return_value_attribute='explicit',
        session=None,
        ):
        assert session is not None
        assert not (menu_entries and items)
        Controller.__init__(self, session=session)
        self._breadcrumb = breadcrumb
        self._is_numbered = is_numbered
        self._is_ranged = is_ranged
        self._items = items or []
        self._menu_entries = menu_entries or []
        self._return_value_attribute = return_value_attribute

    ### PRIVATE PROPERTIES ###

    @property
    def breadcrumb(self):
        r'''Gets selector breadcrumb.

        Returns string or none.
        '''
        if self._breadcrumb is None:
            return 'select:'
        else:
            return 'select {}:'.format(self._breadcrumb)

    ### PRIVATE METHODS ###

    def _make_asset_menu_section(self, menu):
        menu_entries = self.menu_entries
        menu_entries = menu_entries or self._make_menu_entries()
        if not menu_entries:
            return
        menu._make_section(
            group_by_annotation=False,
            is_asset_section=True,
            is_numbered=self.is_numbered,
            is_ranged=self.is_ranged,
            menu_entries=menu_entries,
            name='assets',
            return_value_attribute=self.return_value_attribute,
            )

    def _make_main_menu(self):
        name = self._spaced_class_name
        subtitle = stringtools.capitalize_start(self.breadcrumb)
        menu = self._io_manager._make_menu(name=name, subtitle=subtitle)
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

    def _run(self):
        with self._io_manager._controller(
            clear_terminal=True,
            consume_local_backtrack=True,
            controller=self,
            ):
            while True:
                menu = self._make_main_menu()
                result = menu._run()
                if self._session.is_backtracking:
                    return
                if result and not result == '<return>':
                    return result

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

    def make_autoeditable_class_selector(self):
        r'''Makes autoeditable class selector.

        Returns selector.
        '''
        from abjad.tools import handlertools
        classes = set()
        for class_ in documentationtools.list_all_abjad_classes():
            if hasattr(class_, '_attribute_manifest'):
                classes.add(class_)
        modules = (handlertools,)
        for class_ in documentationtools.list_all_experimental_classes(
            modules=modules):
            if hasattr(class_, '_attribute_manifest'):
                classes.add(class_)
        if self._session._ide is not None:
            wrangler = self._session._ide._maker_file_wrangler
            maker_classes = wrangler._list_maker_classes()
            for class_ in maker_classes:
                if hasattr(class_, '_attribute_manifest'):
                    classes.add(class_)
        classes.add(list)
        classes = sorted(classes, key=lambda x: x.__name__)
        selector = type(self)(
            session=self._session,
            items=classes,
            breadcrumb='autoeditable class',
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
        from scoremanager import idetools
        storehouse_paths = storehouse_paths or []
        forbidden_directory_entries = forbidden_directory_entries or []
        items = []
        for directory in storehouse_paths:
            manager = idetools.PackageManager(
                path=directory,
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
        directory = configuration.handler_tools_directory
        class_names = []
        for entry in sorted(os.listdir(directory)):
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

    def make_package_selector(self, output_material_class_name=''):
        r'''Makes material package selector.

        Returns selector.
        '''
        from scoremanager import idetools
        wrangler = idetools.MaterialPackageWrangler(session=self._session)
        paths = wrangler._list_asset_paths(
            output_material_class_name=output_material_class_name,
            )
        packages = []
        for path in paths:
            package = self._configuration.path_to_package(path)
            packages.append(package)
        selector = Selector(
            session=self._session,
            items=packages,
            )
        return selector

    def make_rhythm_maker_class_name_selector(self):
        r'''Makes rhythm-maker class name selector.

        Returns selector.
        '''
        configuration = self._configuration
        rhythm_maker_tools_directory = os.path.join(
            configuration.abjad_directory,
            'tools',
            'rhythmmakertools',
            )
        selector = self.make_directory_content_selector(
            storehouse_paths=[rhythm_maker_tools_directory],
            endswith='RhythmMaker',
            strip_file_extensions=True,
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
            is_ranged=is_ranged,
            menu_entries=menu_entries,
            return_value_attribute='display_string',
            session=self._session,
            )
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