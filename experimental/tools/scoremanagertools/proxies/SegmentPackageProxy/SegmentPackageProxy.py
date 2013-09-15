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

    def _get_output_lilypond_file_path(self):
        return os.path.join(self.filesystem_path, 'output.ly')
        
    def _get_output_pdf_file_path(self):
        return os.path.join(self.filesystem_path, 'output.pdf')
        
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
        command_section.append(('segment definition - edit', 'e'))
        command_section.append(('segment definition - execute', 'x'))
        command_section = main_menu.make_command_section()
        command_section.append(('output pdf - make', 'pdfm'))
        if os.path.isfile(self._get_output_pdf_file_path()):
            command_section.append(('output pdf - view', 'pdfv'))
        hidden_section = main_menu.make_command_section(is_hidden=True)
        if os.path.isfile(self._get_output_lilypond_file_path()):
            hidden_section.append(('output ly - view', 'lyv'))
        return main_menu

    ### PUBLIC PROPERTIES ###

    @property
    def history_directory_path(self):
        return os.path.join(self.filesystem_path, 'history')

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
        return os.path.join(self.filesystem_path, 'definition.py')

    @property
    def segment_definition_module_packagesystem_path(self):
        return '.'.join([
            self.package_path,
            'definition',
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

    def interactively_edit_asset_definition_module(
        self,
        pending_user_input=None,
        ):
        r'''Interactively edits asset definition module.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        self.segment_definition_module_proxy.interactively_edit()

    def interactively_execute_asset_definition_module(self):
        r'''Executes asset definition module.

        Returns none.
        '''
        proxy = self.segment_definition_module_proxy
        proxy.interpret_in_external_process()
        message = 'segment definition module executed.'
        self.session.io_manager.proceed(message)

    def interactively_make_asset_pdf(self):
        r'''Interactively makes asset PDF.

        Returns none.
        '''
        proxy = self.segment_definition_module_proxy
        proxy.interpret_in_external_process()
        self.view_output_pdf()

    def interactively_view_output_ly(self):
        r'''Interactively views output LilyPond file.

        Returns none.
        '''
        output_lilypond_file_path = self._get_output_lilypond_file_path()
        if os.path.isfile(output_lilypond_file_path):
            command = 'vim -R {}'.format(output_lilypond_file_path)
            iotools.spawn_subprocess(command)

#    def interactively_write_asset_pdf(
#        self,
#        is_interactive=True,
#        pending_user_input=None,
#        ):
#        r'''Interactively writes asset LilyPond file and PDF to disk.
#
#        Returns none.
#        '''
#        self.session.io_manager.assign_user_input(pending_user_input)
#        proxy = self.segment_definition_module_proxy
#        proxy.interpret_in_external_process()
#        history_directory_path = self.history_directory_path
#        next_ly_file_name = iotools.get_next_output_file_name(
#            output_directory_path=history_directory_path)
#        next_ly_path = os.path.join(history_directory_path, next_ly_file_name)
#        iotools.save_last_ly_as(next_ly_path)
#        next_pdf_file_name = next_ly_file_name.replace('.ly', '.pdf')
#        next_pdf_path = os.path.join(
#            history_directory_path, 
#            next_pdf_file_name,
#            )
#        iotools.save_last_pdf_as(next_pdf_path)
#        message = 'PDF & LilyPond source saved.'
#        self.session.io_manager.proceed(message, is_interactive=is_interactive)

    def make_history_directory(self):
        r'''Makes history directory.

        Returns none.
        '''
        if not os.path.exists(self.history_directory_path):
            os.mkdir(self.history_directory_path)

    def view_output_pdf(self):
        r'''Views output PDF.

        Returns none.
        '''
        output_pdf_file_path = self._get_output_pdf_file_path()
        if os.path.isfile(output_pdf_file_path):
            command = 'open {}'.format(output_pdf_file_path)
            iotools.spawn_subprocess(command)

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

    ### UI MANIFEST ###

    user_input_to_action = PackageProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'e': interactively_edit_asset_definition_module,
        'lyv': interactively_view_output_ly,
        'pdfm': interactively_make_asset_pdf,
        'pdfv': view_output_pdf,
        'x': interactively_execute_asset_definition_module,
        })
