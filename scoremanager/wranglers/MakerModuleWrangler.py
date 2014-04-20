# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class MakerModuleWrangler(Wrangler):
    r'''Maker module wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.MakerModuleWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MakerModuleWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_extensions',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(MakerModuleWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._user_storehouse_path = \
            self._configuration.user_library_makers_directory_path
        self._score_storehouse_path_infix_parts = ('makers',)
        self._include_extensions = True
        self._manager_class = managers.FileManager

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            breadcrumb = 'makers'
        else:
            breadcrumb = 'maker module library'
        view_name = self._read_view_name()
        if view_name:
            breadcrumb = '{} ({} view)'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _user_input_to_action(self):
        superclass = super(MakerModuleWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'cp': self.copy_maker_module,
            'new': self.make_maker_module,
            'ren': self.rename_maker_module,
            'rm': self.remove_maker_modules,
            })
        return result

    ### PRIVATE METHODS ###

    def _edit_maker_module(self, path):
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        manager.edit()

    def _enter_run(self):
        self._session._is_navigating_to_score_maker_modules = False

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._edit_maker_module(result)

#    def _make_asset_menu_entries(
#        self,
#        apply_view=True,
#        include_annotation=True,
#        include_extensions=True,
#        include_asset_name=True,
#        include_year=False,
#        human_readable=False,
#        packages_instead_of_paths=False,
#        sort_by_annotation=True,
#        ):
#        superclass = super(StylesheetWrangler, self)
#        menu_entries = superclass._make_asset_menu_entries(
#            apply_view=apply_view,
#            include_annotation=include_annotation,
#            include_extensions=include_extensions,
#            include_asset_name=include_asset_name,
#            include_year=include_year,
#            human_readable=human_readable,
#            packages_instead_of_paths=packages_instead_of_paths,
#            sort_by_annotation=sort_by_annotation,
#            )
#        return menu_entries

    def _make_asset_menu_section(self, menu):
        include_annotation = not self._session.is_in_score
        menu_entries = self._make_asset_menu_entries(
            human_readable=False,
            include_annotation=include_annotation,
            include_extensions=True,
            )
        if not menu_entries:
            return
        section = menu.make_asset_section(
            menu_entries=menu_entries,
            )
        menu._asset_section = section

    def _make_main_menu(self, name='make module wrangler'):
        superclass = super(MakerModuleWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_maker_modules_menu_section(menu)
        return menu

    def _make_maker_modules_menu_section(self, menu):
        commands = []
        commands.append(('maker modules - copy', 'cp'))
        commands.append(('maker modules - new', 'new'))
        commands.append(('maker modules - rename', 'ren'))
        commands.append(('maker modules - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='maker modules',
            )

    ### PUBLIC METHODS ###

    def copy_maker_module(self):
        r'''Copies maker module.

        Returns none.
        '''
        self._copy_asset(
            extension='.py',
            force_lowercase=False,
            item_identifier='maker module',
            )

    def make_maker_module(self):
        r'''Makes maker module.

        Returns none.
        '''
        self._make_file(
            extension='.py',
            force_lowercase=False,
            prompt_string='maker name', 
            )

    def remove_maker_modules(self):
        r'''Removes one or more maker modules.

        Returns none.
        '''
        self._remove_assets(
            item_identifier='maker module',
            )

    def rename_maker_module(self):
        r'''Renames make module.

        Returns none.
        '''
        self._rename_asset(
            item_identifier='maker module',
            )