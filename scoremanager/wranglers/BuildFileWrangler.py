# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.FileWrangler import FileWrangler


class BuildFileWrangler(FileWrangler):
    r'''Build wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.BuildFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            BuildFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_extensions',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(BuildFileWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._user_storehouse_path = None
        self._score_storehouse_path_infix_parts = ('build',)
        self._include_extensions = True

    ### PRIVATE PROPERTIES ###

    @property
    def _asset_manager_class(self):
        from scoremanager import managers
        return managers.FileManager

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            return 'build directory'
        else:
            return 'build file library'

    @property
    def _user_input_to_action(self):
        superclass = super(BuildFileWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            })
        return result

    ### PRIVATE METHODS ###

    def _edit_file(self, path):
        manager = self._asset_manager_class(
            path=path, 
            session=self._session,
            )
        manager.edit()

    def _enter_run(self):
        self._session._is_navigating_to_score_build_files = False

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._edit_file(result)

    def _make_asset_menu_section(self, menu):
        include_annotation = not self._session.is_in_score
        menu_entries = self._make_asset_menu_entries(
            human_readable=False,
            include_annotation=include_annotation,
            include_extensions=True,
            )
        if not menu_entries:
            return
        section = menu.make_asset_section()
        menu._asset_section = section
        for menu_entry in menu_entries:
            section.append(menu_entry)
        return section

    def _make_files_menu_section(self, menu):
        section = menu.make_command_section(name='files')
        section.append(('files - copy', 'cp'))
        section.append(('files - new', 'new'))
        section.append(('files - rename', 'ren'))
        section.append(('files - remove', 'rm'))
        return section

    def _make_main_menu(self, name='build wrangler'):
        menu = self._io_manager.make_menu(
            where=self._where,
            name=name,
            )
        self._main_menu = menu
        self._make_asset_menu_section(menu)
        self._make_files_menu_section(menu)
        return menu