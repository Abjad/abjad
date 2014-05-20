# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import systemtools
from scoremanager.wranglers.Wrangler import Wrangler


class SegmentPackageWrangler(Wrangler):
    r'''Segment package wrangler.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager(is_test=True)
            >>> wrangler = score_manager._segment_package_wrangler
            >>> wrangler
            SegmentPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(SegmentPackageWrangler, self)
        superclass.__init__(session=session)
        self._asset_identifier = 'segment package'
        self._basic_breadcrumb = 'segments'
        self._manager_class = managers.SegmentPackageManager
        self._score_storehouse_path_infix_parts = ('segments',)

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(SegmentPackageWrangler, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'cp': self.copy_package,
            'de*': self.edit_every_definition_py,
            'no': self.open_init_py,
            'ns': self.write_stub_init_py,
            'mdpyls*': self.list_every_metadata_py,
            'mdo*': self.open_every_metadata_py,
            'mdw*': self.rewrite_every_metadata_py,
            'ki*': self.interpret_every_make_py,
            'new': self.make_package,
            'oli*': self.interpret_every_output_ly,
            'opo*': self.open_every_output_pdf,
            'ren': self.rename_package,
            'rm': self.remove_packages,
            'vr*': self.version_package,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_segments = False

    def _handle_numeric_user_input(self, result):
        manager = self._initialize_manager(result)
        manager._run()

    def _is_valid_directory_entry(self, expr):
        superclass = super(SegmentPackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _make_all_segments_menu_section(self, menu):
        commands = []
        commands.append(('segments - definition.py - edit', 'de*'))
        commands.append(('segments - make.py - interpret', 'ki*'))
        commands.append(('segments - __metadata__.py - open', 'mdo*'))
        commands.append(('segments - output.ly - interpret', 'oli*'))
        commands.append(('segments - output.pdf - open', 'opo*'))
        commands.append(('segments - version', 'vr*'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='segments 2',
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
        self._make_all_segments_menu_section(menu)
        self._make_init_py_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_metadata_py_menu_section(menu)
        self._make_segments_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    # TODO: migrate to SegmentPackageManager
    def _make_package(self, path, metadata=None):
        from scoremanager import managers
        assert os.path.sep in path
        metadata = collections.OrderedDict(metadata or {})
        assert not os.path.exists(path)
        os.mkdir(path)
        manager = self._initialize_manager(path)
        manager.write_stub_definition_py(confirm=False, display=False)
        manager.write_stub_make_py(confirm=False, display=False)

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
        self._session._is_navigating_to_score_segments = True

    ### PUBLIC METHODS ###

    def copy_package(self):
        r'''Copies segment package.

        Returns none.
        '''
        self._copy_asset()

    def edit_every_definition_py(self):
        r'''Edits ``definition.py`` in every segment.

        Returns none.
        '''
        self._open_in_each_package('definition.py', verb='edit')
        self._session._hide_next_redraw = True

    def interpret_every_make_py(self):
        r'''Interprets ``__make.py__`` in every segment.
        
        Makes ``output.ly`` and ``output.pdf`` in every segment.

        Returns none.
        '''
        with self._io_manager._make_interaction():
            managers = self._list_visible_asset_managers()
            make_py_paths = []
            output_ly_paths = []
            output_pdf_paths = []
            for manager in managers:
                make_py_paths.append(manager._make_py_path)
                output_ly_paths.append(manager._output_lilypond_file_path)
                output_pdf_paths.append(manager._output_pdf_file_path)
            # TODO: gather message with dry_run=True keyword
            messages = []
            messages.append('will interpret ...')
            triples = zip(make_py_paths, output_ly_paths, output_pdf_paths)
            for triple in triples:
                make_py_path = triple[0]
                output_ly_path = triple[1]
                output_pdf_path = triple[2]
                messages.append('  INPUT: {}'.format(make_py_path))
                messages.append(' OUTPUT: {}'.format(output_ly_path))
                messages.append(' OUTPUT: {}'.format(output_pdf_path))
            self._io_manager._display(messages)
            result = self._io_manager._confirm()
            if self._session.is_backtracking:
                return
            if not result:
                return
            for manager in managers:
                manager.interpret_make_py(confirm=False, display=False)
            if not managers:
                self._io_manager._display('')

    def interpret_every_output_ly(
        self,
        confirm=True,
        display=True,
        open_every_output_pdf=True,
        ):
        r'''Reinterprets all current LilyPond files.

        Returns none.
        '''
        segments_directory = self._get_current_directory()
        entries = sorted(os.listdir(segments_directory))
        if confirm:
            messages = []
            messages.append('')
            messages.append('will interpret ...')
            messages.append('')
            segment_paths = self._list_visible_asset_paths()
            for segment_path in segment_paths:
                input_path = os.path.join(segment_path, 'output.ly')
                output_path = os.path.join(segment_path, 'output.pdf')
                messages.append('  INPUT: {}'.format(input_path))
                messages.append(' OUTPUT: {}'.format(output_path))
                messages.append('')
            self._io_manager._display(messages)
            result = self._io_manager._confirm()
            if self._session.is_backtracking:
                return
            if not result:
                return
            self._io_manager._display('')
        for manager in self._list_visible_asset_managers():
            self._session._hide_next_redraw = False
            manager.interpret_output_ly(confirm=False, display=True)
        self._session._hide_next_redraw = True

    def list_every_metadata_py(self):
        r'''Lists ``__metadata__.py`` in every score.

        Returns none.
        '''
        self._list_every_metadata_py()

    def make_package(self):
        r'''Makes segment package.

        Returns none.
        '''
        if self._session.is_in_score:
            storehouse_path = self._current_storehouse_path
        else:
            storehouse_path = self._select_storehouse_path()
        prompt_string = 'enter segment package name'
        path = self._get_available_path(
            prompt_string=prompt_string,
            storehouse_path=storehouse_path,
            )
        if self._session.is_backtracking:
            return
        if not path:
            return
        self._make_package(path)
        manager = self._get_manager(path)
        manager._run()

    def open_every_metadata_py(self):
        r'''Opens ``__metadata__.py`` in every segment.

        Returns none.
        '''
        self._open_in_each_package('__metadata__.py')

    def open_every_output_pdf(self):
        r'''Opens output.pdf file in each segment.

        Returns none.
        '''
        self._open_in_each_package('output.pdf')
        self._session._hide_next_redraw = True

    def open_init_py(self):
        r'''Opens ``__init__.py``.

        Returns none.
        '''
        self._current_package_manager.open_init_py()

    def remove_packages(self):
        r'''Removes one or more segment packages.
        
        Returns none.
        '''
        self._remove_assets()

    def rename_package(self):
        r'''Renames segment package.

        Returns none.
        '''
        self._rename_asset()

    def rewrite_every_metadata_py(self, confirm=True, display=True):
        r'''Rewrites ``__metadata__.py`` in each segment.

        Returns none.
        '''
        self._rewrite_every_metadata_py(confirm=confirm, display=display)

    def version_package(self, confirm=True, display=True):
        r'''Versions every package.

        Returns none.
        '''
        self._version_package(confirm=confirm, display=display)

    def write_stub_init_py(self):
        r'''Writes stub ``__init__.py``.

        Returns none.
        '''
        self._current_package_manager.write_stub_init_py()