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
        command_section = main_menu.make_command_section()
        command_section.append(('output pdf - make', 'pdfm'))
        last_output_file_name = iotools.get_last_output_file_name(
            path=self.history_directory)
        command_section.append(('output pdf - write', 'pdfw'))
        if last_output_file_name is not None:
            command_section.append(('output pdf - view', 'pdfv'))
        return main_menu

    ### PUBLIC PROPERTIES ###

    @property
    def history_directory(self):
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

    def interactively_edit_asset_definition_module(
        self,
        pending_user_input=None,
        ):
        r'''Interactively edits asset definition module.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        self.segment_definition_module_proxy.interactively_edit()

    def interactively_make_asset_pdf(
        self,
        pending_user_input=None,
        ):
        r'''Interactively makes asset PDF.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        proxy = self.segment_definition_module_proxy
        proxy.interpret_in_external_process()
        iotools.pdf()

    def interactively_view_asset_pdf(
        self,
        pending_user_input=None,
        ):
        r'''Interactively views asset PDF.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        last_output_file_name = iotools.get_last_output_file_name(
            path=self.history_directory)
        if last_output_file_name is not None:
            result = os.path.splitext(last_output_file_name)
            file_name_without_extension, extension = result
            pdf_file_name = file_name_without_extension + '.pdf'
            pdf_path_name = os.path.join(self.history_directory, pdf_file_name)
            command = 'open {}'.format(pdf_path_name)
            iotools.spawn_subprocess(command)

    def interactively_write_asset_pdf(
        self,
        pending_user_input=None,
        ):
        r'''Interactively writes asset LilyPond file and PDF to disk.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        proxy = self.segment_definition_module_proxy
        proxy.interpret_in_external_process()
        history_directory = self.history_directory
        next_ly_file_name = iotools.get_next_output_file_name(
            path=history_directory)
        next_ly_path = os.path.join(history_directory, next_ly_file_name)
        iotools.save_last_ly_as(next_ly_path)
        next_pdf_file_name = next_ly_file_name.replace('.ly', '.pdf')
        next_pdf_path = os.path.join(history_directory, next_pdf_file_name)
        iotools.save_last_pdf_as(next_pdf_path)
        message = 'PDF & LilyPond source saved.'
        self.session.io_manager.proceed(message)

    def make_history_directory(self):
        r'''Makes history directory.

        Returns none.
        '''
        if not os.path.exists(self.history_directory):
            os.mkdir(self.history_directory)

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
        'sde': interactively_edit_asset_definition_module,
        'pdfm': interactively_make_asset_pdf,
        'pdfv': interactively_view_asset_pdf,
        'pdfw': interactively_write_asset_pdf,
        })
