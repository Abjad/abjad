# -*- encoding: utf-8 -*-
import os
import shutil
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.managers.Manager import Manager


class FileManager(Manager):
    r'''File manager.
    '''

    ### CLASS VARIABLES ###

    _temporary_asset_name = 'temporary_file.txt'

    extension = ''

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        superclass = super(FileManager, self)
        superclass.__init__(filesystem_path=filesystem_path, session=session)
        self._generic_class_name = 'file'

    ### PRIVATE PROPERTIES ###

    @property
    def _user_input_to_action(self):
        superlcass = super(FileManager, self)
        _user_input_to_action = superclass._user_input_to_action
        _user_input_to_action = _user_input_to_action.copy()
        _user_input_to_action.update({
            'e': self.edit,
            'ts': self.typeset_tex_file,
            'v': self.view,
            })
        return _user_input_to_action

    ### PRIVATE METHODS ###

    def _get_space_delimited_lowercase_name(self):
        if self._filesystem_path:
            base_name = os.path.basename(self._filesystem_path)
            name = base_name.strip('.py')
            name = stringtools.string_to_space_delimited_lowercase(name)
            return name

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            self.edit()

    def _execute(self, file_path=None, return_attribute_name=None):
        file_path = file_path or self._filesystem_path
        if os.path.isfile(file_path):
            file_pointer = open(file_path, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            try:
                exec(file_contents_string)
            except Exception:
                return
            if isinstance(return_attribute_name, str):
                if return_attribute_name in locals():
                    return locals()[return_attribute_name]
            elif isinstance(return_attribute_name, (list, tuple)):
                result = []
                for name in return_attribute_name:
                    if name in locals():
                        result.append(locals()[name])
                    else:
                        result.append(None)
                result = tuple(result)
                return result

    def _interpret(self, prompt=True):
        command = 'python {}'.format(self._filesystem_path)
        self._io_manager.spawn_subprocess(command)
        message = 'file interpreted.'
        self._io_manager.proceed(message, prompt=prompt)

    def _interpret_in_external_process(self):
        command = 'python {}'.format(self._filesystem_path)
        result = self._io_manager.spawn_subprocess(command)
        if result != 0:
            self._io_manager.display('')
            self._io_manager.proceed()

    def _is_editable(self):
        if self._filesystem_path.endswith(('.tex', '.py')):
            return True
        return False

    def _make_empty_asset(self, prompt=False):
        if not os.path.exists(self._filesystem_path):
            file_reference = file(self._filesystem_path, 'w')
            file_reference.write('')
            file_reference.close()
        self._io_manager.proceed(prompt=prompt)

    def _make_main_menu(self):
        main_menu = self._io_manager.make_menu(where=self._where)
        self._main_menu = main_menu
        command_section = main_menu.make_command_section()
        if self._is_editable():
            command_section.append(('edit', 'e'))
            command_section.default_index = len(command_section) - 1
        command_section.append(('rename', 'ren'))
        command_section.append(('remove', 'rm'))
        if self._filesystem_path.endswith('.py'):
            command_section.append(('run', 'run'))
        if self._filesystem_path.endswith('.tex'):
            command_section.append(('typeset', 'ts'))
        if self._filesystem_path.endswith('.pdf'):
            command_section.append(('view', 'v'))
        return main_menu

    def _read_lines(self):
        result = []
        if self._filesystem_path:
            if os.path.exists(self._filesystem_path):
                file_pointer = file(self._filesystem_path)
                result.extend(file_pointer.readlines())
                file_pointer.close()
        return result

    def _write_boilerplate(self, boilerplate_file_abjad_asset_name):
        if not os.path.exists(boilerplate_file_abjad_asset_name):
            boilerplate_file_abjad_asset_name = os.path.join(
                self._configuration.boilerplate_directory_path,
                boilerplate_file_abjad_asset_name,
                )
        if os.path.exists(boilerplate_file_abjad_asset_name):
            shutil.copyfile(
                boilerplate_file_abjad_asset_name,
                self._filesystem_path,
                )
            return True

    def _write_stub(self):
        file_pointer = open(self._filesystem_path, 'w')
        file_pointer.write('# -*- encoding: utf-8 -*-')
        file_pointer.close()

    ### PUBLIC METHODS ###

    def call_lilypond(self, prompt=True):
        r'''Calls LilyPond on file.

        Returns none.
        '''
        if self._io_manager.find_executable('lily'):
            executable = 'lily'
        elif self._io_manager.find_executable('lilypond'):
            executable = 'lilypond'
        else:
            message = 'Cannot find LilyPond executable.'
            raise ValueError(message)
        command = '{} {}'.format(
            executable,
            self._filesystem_path,
            )
        input_directory = os.path.dirname(self._filesystem_path)
        with systemtools.TemporaryDirectoryChange(input_directory):
            self._io_manager.spawn_subprocess(command)
        self._io_manager.proceed('', prompt=prompt)

    def edit(self, line_number=None):
        r'''Edits file.

        Returns none.
        '''
        self._io_manager.edit(
            self._filesystem_path,
            line_number=line_number,
            )

    def open(self):
        r'''Opens file.

        Returns none.
        '''
        self._io_manager.open_file(self._filesystem_path)

    def typeset_tex_file(self, prompt=True):
        r'''Typesets TeX file.

        Returns none.
        '''
        input_directory = os.path.dirname(self._filesystem_path)
        basename = os.path.basename(self._filesystem_path)
        input_file_name_stem, extension = os.path.splitext(basename)
        output_directory = input_directory
        command = 'pdflatex --jobname={} -output-directory={} {}/{}.tex'
        command = command.format(
            input_file_name_stem,
            output_directory,
            input_directory,
            input_file_name_stem,
            )
        with systemtools.TemporaryDirectoryChange(input_directory):
            self._io_manager.spawn_subprocess(command)
            command = 'rm {}/*.aux'.format(output_directory)
            self._io_manager.spawn_subprocess(command)
            command = 'rm {}/*.log'.format(output_directory)
            self._io_manager.spawn_subprocess(command)
        self._io_manager.proceed('', prompt=prompt)

    def view(self):
        r'''Views file.

        Returns none.
        '''
        self._io_manager.view(self._filesystem_path)

    def write_boilerplate(
        self, 
        pending_user_input=None,
        prompt=True,
        ):
        r'''Writes filesystem asset boilerplate.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_snake_case_file_name('name of boilerplate asset')
        with self._backtracking:
            boilerplate_file_abjad_asset_name = getter._run()
        if self._session._backtrack():
            return
        if self._write_boilerplate(boilerplate_file_abjad_asset_name):
            self._io_manager.proceed('boilerplate asset copied.')
        else:
            message = 'boilerplate asset {!r} does not exist.'
            message = message.format(boilerplate_file_abjad_asset_name)
            self._io_manager.proceed(message)
