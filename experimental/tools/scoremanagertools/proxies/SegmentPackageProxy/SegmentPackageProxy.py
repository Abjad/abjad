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

    ### PUBLIC METHODS ###

    def interactively_edit_segment_definition_module(self):
        r'''Interactively edits segment definition module.

        Returns none.
        '''
        self.session.io_manager.print_not_yet_implemented()

    def interactively_make_asset(self, prompt=True):
        r'''Interactively makes asset.

        Returns none.
        '''
        self.session.io_manager.print_not_yet_implemented()

    def interactively_rename_segment(self):
        r'''Interactively renames segment.

        Returns none.
        '''
        #self.session.io_manager.print_not_yet_implemented()
        line = 'current name: {}'.format(self.filesystem_basename)
        self.session.io_manager.display(line)
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_snake_case_package_name('new name')
        new_package_name = getter._run()
        if self.session.backtrack():
            return
        lines = []
        line = 'current name: {}'.format(self.filesystem_basename)
        lines.append(line)
        line = 'new name:     {}'.format(new_package_name)
        lines.append(line)
        lines.append('')
        self.session.io_manager.display(lines)
        if not self.session.io_manager.confirm():
            return
        new_directory_path = self.filesystem_path.replace(
            self.filesystem_basename,
            new_package_name,
            )
        if self.is_versioned():
            # rename package directory
            command = 'svn mv {} {}'
            command = command.format(self.filesystem_path, new_directory_path)
            os.system(command)
            # commit
            commit_message = 'renamed {} to {}.'
            commit_message = commit_message.format(
                self.filesystem_basename,
                new_package_name,
                )
            commit_message = commit_message.replace('_', ' ')
            command = 'svn commit -m {!r} {}'
            command = command.format(
                commit_message,
                self.parent_directory_filesystem_path,
                )
            os.system(command)
        else:
            command = 'mv {} {}'
            command = command.format(self.filesystem_path, new_directory_path)
            os.system(command)
        # update path name to reflect change
        self._path = new_directory_path
        self.session.is_backtracking_locally = True

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

    # hoist to superclass
    def remove_segment_package(self):
        r'''Removes segment package.

        Returns none.
        '''
        self.remove()
        self.session.is_backtracking_locally = True

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
        # maybe generalize to interactively_rename_package 
        'ren': interactively_rename_segment,
        # maybe generalize to remove_package
        'rm': remove_segment_package,
        'sde': interactively_edit_segment_definition_module,
        'pdfm': write_segment_ly_and_pdf_to_disk,
        'pdfv': interactively_view_segment_pdf,
        })
