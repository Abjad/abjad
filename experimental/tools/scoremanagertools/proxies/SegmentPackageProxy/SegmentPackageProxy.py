# -*- encoding: utf-8 -*-
import os
from abjad.tools import iotools
from experimental.tools.scoremanagertools.proxies.PackageProxy \
    import PackageProxy


class SegmentPackageProxy(PackageProxy):

    ### INITIALIZER ###

    def __init__(
        self, 
        packagesystem_path=None, 
        score_template=None, 
        session=None,
        ):
        PackageProxy.__init__(
            self, 
            packagesystem_path=packagesystem_path, 
            session=session,
            )
        self.score_template = score_template

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self._space_delimited_lowercase_name

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)

    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        hidden_section = main_menu.make_command_section(is_hidden=True)
        hidden_section.append(('remove package', 'rm'))
        hidden_section.append(('list package', 'ls'))
        hidden_section.append(('rename package', 'ren'))
        hidden_section.append(('manage tags', 'tags'))
        command_section = main_menu.make_command_section()
        command_section.append(('segment definition - edit', 'sde'))
        command_section.append(('output pdf - make', 'pdfm'))
        command_section.append(('output pdf - view', 'pdfv'))
        return main_menu

    ### PUBLIC PROPERTIES ###

    @apply
    def score_template():
        def fget(self):
            return self._score_template
        def fset(self, score_template):
            from abjad.tools import scoretools
            assert isinstance(score_template, (scoretools.Score, type(None)))
            self._score_template = score_template
        return property(**locals())

    @property
    def segment_definition_module_file_name(self):
        return os.path.join(self.filesystem_path, 'segment_definition.py')

    @property
    def segment_definition_module_packagesystem_path(self):
        return '.'.join([
            self.package_path,
            'segment_definition',
            ])

    @property
    def segment_definition_module_proxy(self):
        from experimental.tools import scoremanagertools
        proxy = scoremanagertools.proxies.ModuleProxy(
            self.segment_definition_module_packagesystem_path,
            session=self.session,
            )
        return proxy

    ### PUBLIC METHODS ###

    def interactively_edit_segment_definition_module(self):
        r'''Interactively edits segment definition module.

        Returns none.
        '''
        self.segment_definition_module_proxy.interactively_edit()

    def interactively_make_asset(self, prompt=True):
        r'''Interactively makes asset.

        Returns none.
        '''
        self.session.io_manager.print_not_yet_implemented()

    def interactively_set_score_template(self):
        r'''Interactively sets score template.

        Returns none.
        '''
        self.session.io_manager.print_not_yet_implemented()

    def interactively_view_segment_pdf(self):
        r'''Interactively views segment PDF.

        Returns none.
        '''
        self.session.io_manager.print_not_yet_implemented()

    def make_asset(self):
        r'''Makes asset.

        Returns none.
        '''
        self.session.io_manager.print_not_yet_implemented()

    def make_history_directory(self):
        history_directory = os.path.join(self.filesystem_path, 'history')
        if not os.path.exists(history_directory):
            os.mkdir(history_directory)

    def write_initializer_to_disk(self):
        r'''Writes initializer to disk.

        Returns none.
        '''
        if not os.path.exists(self.initializer_file_name):
            file_pointer = file(self.initializer_file_name, 'w')
            file_pointer.write('')
            file_pointer.close()

    def write_segment_definition_module_to_disk(self):
        r'''Write segment definition module to disk.

        Returns none.
        '''
        if not os.path.exists(self.segment_definition_module_file_name):
            file_pointer = file(self.segment_definition_module_file_name, 'w')
            file_pointer.write('# -*- encoding: utf-8 -*-\n')
            file_pointer.write('from abjad import *\n')
            file_pointer.write('\n\n')
            file_pointer.close()

    def write_segment_ly_and_pdf_to_disk(self):
        r'''Writes segment LilyPond file and PDF to disk.

        Returns none.
        '''
        self.session.io_manager.print_not_yet_implemented()

    ### UI MANIFEST ###

    user_input_to_action = PackageProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'sde': interactively_edit_segment_definition_module,
        'pdfm': write_segment_ly_and_pdf_to_disk,
        'pdfv': interactively_view_segment_pdf,
        })
