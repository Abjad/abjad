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
        self._score_storehouse_path_infix_parts = ('segments',)
        self._manager_class = managers.SegmentPackageManager

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            breadcrumb = 'segments'
        else:
            breadcrumb = 'segment library'
        view_name = self._read_view_name()
        if view_name:
            breadcrumb = '{} ({} view)'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _user_input_to_action(self):
        superclass = super(SegmentPackageWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            '>': self._navigate_to_next_asset,
            '<': self._navigate_to_previous_asset,
            'lyi': self.interpret_current_lilypond_files,
            'pdfs': self.version_segment_packages,
            'pdfo': self.view_segment_pdfs,
            'mmi': self.interpret_make_modules,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_segments = False

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            segment_package_manager = self._initialize_manager(result)
            segment_package_manager._run()

    def _is_valid_directory_entry(self, expr):
        superclass = super(SegmentPackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _make_all_segments_menu_section(self, menu):
        commands = []
        string = 'all segments - make module - interpret'
        commands.append((string, 'mmi'))
        string = 'all segments - lilypond file - interpret'
        commands.append((string, 'lyi'))
        commands.append(('all segments - pdf - version', 'pdfs'))
        commands.append(('all segments - pdf - open', 'pdfo'))
        menu.make_command_section(
            commands=commands,
            name='all segments',
            )

    def _make_asset(
        self,
        path,
        prompt=False,
        metadata=None,
        ):
        metadata = collections.OrderedDict(metadata or {})
        assert not os.path.exists(path)
        os.mkdir(path)
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        manager.write_initializer()
        manager.write_definition_module()
        manager.make_versions_directory()
        message = 'segment created: {!r}.'.format(path)
        self._io_manager.proceed(message=message, prompt=prompt)

    def _make_asset_menu_section(self, menu):
        include_annotation = not self._session.is_in_score
        entries = self._make_asset_menu_entries(
            include_annotation=include_annotation,
            )
        if not entries:
            return
        menu.make_asset_section(
            menu_entries=entries,
            )

    def _make_main_menu(self, name='segment wrangler'):
        superclass = super(SegmentPackageWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_all_segments_menu_section(menu)
        self._make_segments_menu_section(menu)
        self._make_directory_menu_section(menu, is_permanent=True)
        self._make_initializer_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_metadata_module_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _make_segments_menu_section(self, menu):
        commands = []
        commands.append(('segments - new', 'new'))
        menu.make_command_section(
            commands=commands,
            name='segments',
            )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_score_segments = True

    ### PUBLIC METHODS ###

    def interpret_current_lilypond_files(
        self,
        prompt=True,
        view_output_pdfs=True,
        ):
        r'''Reinterprets all current LilyPond files.

        Returns none.
        '''
        parts = (self._session.current_score_directory_path,)
        parts += self._score_storehouse_path_infix_parts
        segments_directory_path = os.path.join(*parts)
        for directory_entry in sorted(os.listdir(segments_directory_path)):
            if not directory_entry[0].isalpha():
                continue
            segment_package_name = directory_entry
            segment_package_directory_path = os.path.join(
                segments_directory_path,
                segment_package_name,
                )
            segment_package_path = \
                self._configuration.path_to_package_path(
                segment_package_directory_path)
            manager = self._manager_class(
                segment_package_path,
                session=self._session,
                )
            manager.interpret_current_lilypond_file(
                prompt=False,
                view_output_pdf=False,
                )
        message = 'press return to view PDF(s).'
        self._io_manager.proceed(message=message, prompt=prompt)
        if view_output_pdfs:
            self.view_segment_pdfs()

    def interpret_make_modules(self):
        r'''Makes asset PDFs.

        Returns none.
        '''
        parts = (self._session.current_score_directory_path,)
        parts += self._score_storehouse_path_infix_parts
        segments_directory_path = os.path.join(*parts)
        for directory_entry in sorted(os.listdir(segments_directory_path)):
            if not directory_entry[0].isalpha():
                continue
            segment_package_name = directory_entry
            segment_package_directory_path = os.path.join(
                segments_directory_path,
                segment_package_name,
                )
            manager = self._manager_class(
                path=segment_package_directory_path,
                session=self._session,
                )
            manager.interpret_make_module(
                prompt=False,
                )
            output_pdf_file_path = manager._output_pdf_file_path
            if os.path.isfile(output_pdf_file_path):
                message = 'segment {} PDF created.'
                message = message.format(segment_package_name)
                self._io_manager.display(message)
        self._io_manager.display('')
        self._io_manager.proceed()

    def remove_segment_package(self):
        r'''Removes one or more segment packages.
        
        Returns none.
        '''
        self._remove_asset(
            item_identifier='segment package',
            )

    def rename_segment_package(self):
        r'''Renames segment package.

        Returns none.
        '''
        self._rename_asset(
            item_identifier='segment package',
            )

    def version_segment_packages(self):
        r'''Versions all assets.

        Returns none.
        '''
        parts = (self._session.current_score_directory_path,)
        parts += self._score_storehouse_path_infix_parts
        segments_directory_path = os.path.join(*parts)
        for directory_entry in sorted(os.listdir(segments_directory_path)):
            if not directory_entry[0].isalpha():
                continue
            segment_package_name = directory_entry
            segment_package_directory_path = os.path.join(
                segments_directory_path,
                segment_package_name,
                )
            segment_package_path = \
                self._configuration.path_to_package_path(
                segment_package_directory_path)
            manager = self._manager_class(
                segment_package_path,
                session=self._session,
                )
            version_number = manager.save_to_versions_directory(
                prompt=False,
                )
            if version_number is not None:
                message = 'segment {} version {} written to disk.'
                message = message.format(segment_package_name, version_number)
                self._io_manager.display(message)
        self._io_manager.display('')
        self._io_manager.proceed()

    def view_segment_pdfs(self):
        r'''Views all asset PDFs.

        Returns none.
        '''
        parts = (self._session.current_score_directory_path,)
        parts += self._score_storehouse_path_infix_parts
        segments_directory_path = os.path.join(*parts)
        output_pdf_file_paths = []
        for directory_entry in sorted(os.listdir(segments_directory_path)):
            if not directory_entry[0].isalpha():
                continue
            segment_package_name = directory_entry
            output_pdf_file_path = os.path.join(
                segments_directory_path,
                segment_package_name,
                'output.pdf',
                )
            if os.path.isfile(output_pdf_file_path):
                output_pdf_file_paths.append(output_pdf_file_path)
        self._io_manager.view(output_pdf_file_paths)