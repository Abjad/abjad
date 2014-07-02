# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import systemtools
from scoremanager.idetools.ScoreInternalPackageWrangler import \
    ScoreInternalPackageWrangler


class SegmentPackageWrangler(ScoreInternalPackageWrangler):
    r'''Segment package wrangler.

    ..  container:: example

        ::

            >>> ide = scoremanager.idetools.AbjadIDE(is_test=True)
            >>> wrangler = ide._segment_package_wrangler
            >>> wrangler
            SegmentPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import idetools
        superclass = super(SegmentPackageWrangler, self)
        superclass.__init__(session=session)
        self._asset_identifier = 'segment package'
        self._basic_breadcrumb = 'segments'
        self._manager_class = idetools.SegmentPackageManager
        self._score_storehouse_path_infix_parts = ('segments',)

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(SegmentPackageWrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'de*': self.edit_every_definition_py,
            #
            'ki*': self.interpret_every_make_py,
            'ke*': self.open_every_make_py,
            'ks*': self.write_every_make_py_stub,
            #
            'ii*': self.interpret_every_output_ly,
            'io*': self.open_every_output_pdf,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_segments = False

    def _handle_numeric_user_input(self, result):
        manager = self._initialize_manager(result)
        manager._run()

    def _is_valid_directory_entry(self, expr):
        superclass = super(SegmentPackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _make_all_packages_menu_section(self, menu):
        superclass = super(SegmentPackageWrangler, self)
        commands = superclass._make_all_packages_menu_section(
            menu, commands_only=True)
        commands.append(('all packages - __make.py__ - edit', 'ke*'))
        commands.append(('all packages - __make.py__ - interpret', 'ki*'))
        commands.append(('all packages - __make.py__ - stub', 'ks*'))
        commands.append(('all packages - definition.py - edit', 'de*'))
        commands.append(('all packages - illustration.ly - interpret', 'ii*'))
        commands.append(('all packages - illustration.pdf - open', 'io*'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='all packages',
            )

    def _make_asset(self, path, metadata=None):
        metadata = collections.OrderedDict(metadata or {})
        assert not os.path.exists(path)
        os.mkdir(path)
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        manager.write_init_py()
        manager.write_definition_py()
        if not os.path.exists(manager._versions_directory):
            os.mkdir(manager._versions_directory)

    def _make_main_menu(self):
        superclass = super(SegmentPackageWrangler, self)
        menu = superclass._make_main_menu()
        self._make_all_packages_menu_section(menu)
        self._make_init_py_menu_section(menu)
        self._make_segments_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _make_segments_menu_section(self, menu):
        commands = []
        commands.append(('segments - copy', 'cp'))
        commands.append(('segments - new', 'new'))
        commands.append(('segments - rename', 'ren'))
        commands.append(('segments - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='segments',
            )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_segments = True

    ### PUBLIC METHODS ###

    def copy_package(self):
        r'''Copies package.

        Returns none.
        '''
        self._copy_asset()

    def edit_every_definition_py(self):
        r'''Edits ``definition.py`` in every package.

        Returns none.
        '''
        self._open_in_every_package('definition.py', verb='edit')

    def interpret_every_make_py(self):
        r'''Interprets ``__make.py__`` in every package.
        
        Makes ``illustration.ly`` and ``illustration.pdf`` in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        for manager in managers:
            inputs_, outputs_ = manager.interpret_make_py(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._io_manager._silent():
            for manager in managers:
                manager.interpret_make_py()

    def interpret_every_output_ly(self, open_every_output_pdf=True):
        r'''Interprets ``illustration.ly`` in every package.

        Makes ``illustration.pdf`` in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        for manager in managers:
            inputs_, outputs_ = manager.interpret_make_py(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._io_manager._silent():
            for manager in managers:
                manager.interpret_illustration_ly()

    def open_every_make_py(self):
        r'''Opens ``__make__.py`` in every package.

        Returns none.
        '''
        self._open_in_every_package('__make__.py')

    def open_every_output_pdf(self):
        r'''Opens ``illustration.pdf`` file in every package.

        Returns none.
        '''
        self._open_in_every_package('illustration.pdf')

    def remove_packages(self):
        r'''Removes one or more packages.
        
        Returns none.
        '''
        self._remove_assets()

    def rename_package(self):
        r'''Renames package.

        Returns none.
        '''
        self._rename_asset()

    def write_every_make_py_stub(self):
        r'''Writes stub ``__make__.py`` in every package.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()