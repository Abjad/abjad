# -*- encoding: utf-8 -*-
import os
import shutil
import traceback
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.managers.Manager import Manager


class FileManager(Manager):
    r'''File manager.
    '''

    ### CLASS VARIABLES ###

    _temporary_asset_name = 'temporary-file.txt'

    extension = ''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(FileManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_class_name = 'file'

    ### PRIVATE PROPERTIES ###

    @property
    def _user_input_to_action(self):
        superlcass = super(FileManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'e': self.edit,
            'ts': self.typeset_tex_file,
            'v': self.view,
            })
        return result

    ### PRIVATE METHODS ###

    def _execute(self, path=None, attribute_names=None):
        assert isinstance(attribute_names, tuple)
        path = path or self._path
        if not os.path.isfile(path):
            return
        file_pointer = open(path, 'r')
        file_contents_string = file_pointer.read()
        file_pointer.close()
        try:
            exec(file_contents_string)
        except Exception:
            traceback.print_exc()
            return
        result = []
        for name in attribute_names:
            if name in locals():
                result.append(locals()[name])
            else:
                result.append(None)
        result = tuple(result)
        return result

    def _get_space_delimited_lowercase_name(self):
        if self._path:
            base_name = os.path.basename(self._path)
            name = base_name.strip('.py')
            name = stringtools.string_to_space_delimited_lowercase(name)
            return name

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            self.edit()

    # TODO: make public; add command alias
    def _interpret(self, prompt=True):
        command = 'python {}'.format(self._path)
        result = self._io_manager.spawn_subprocess(command)
        if result != 0:
            self._io_manager.display('')
            self._io_manager.proceed()
        elif prompt:
            message = 'file interpreted.'
            self._io_manager.proceed(message)

    def _is_editable(self):
        if self._path.endswith(('.tex', '.py')):
            return True
        return False

    def _make_empty_asset(self, prompt=False):
        if not os.path.exists(self._path):
            file_reference = file(self._path, 'w')
            file_reference.write('')
            file_reference.close()
        self._io_manager.proceed(prompt=prompt)

    def _make_file_menu_section(self, menu):
        section = menu.make_command_section(default_index=0)
        if self._is_editable():
            section.append(('file - edit', 'e'))
        section.append(('file - rename', 'ren'))
        section.append(('file - remove', 'rm'))
        if self._path.endswith('.py'):
            section.append(('file - run', 'run'))
        if self._path.endswith('.tex'):
            section.append(('file - typeset', 'ts'))
        if self._path.endswith('.pdf'):
            section.append(('file - view', 'v'))
        return section

    def _make_main_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        self._main_menu = menu
        self._make_file_menu_section(self, menu)
        return menu

    def _read_lines(self):
        result = []
        if self._path:
            if os.path.exists(self._path):
                file_pointer = file(self._path)
                result.extend(file_pointer.readlines())
                file_pointer.close()
        return result

    def _write(self, string):
        with file(self._path, 'w') as file_pointer:
            file_pointer.write(string)

    def _write_boilerplate(self, boilerplate_file_abjad_asset_name):
        if not os.path.exists(boilerplate_file_abjad_asset_name):
            boilerplate_file_abjad_asset_name = os.path.join(
                self._configuration.boilerplate_directory_path,
                boilerplate_file_abjad_asset_name,
                )
        if os.path.exists(boilerplate_file_abjad_asset_name):
            shutil.copyfile(
                boilerplate_file_abjad_asset_name,
                self._path,
                )
            return True

    def _write_stub(self):
        self._write(self._unicode_directive)

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
            self._path,
            )
        input_directory = os.path.dirname(self._path)
        with systemtools.TemporaryDirectoryChange(input_directory):
            self._io_manager.spawn_subprocess(command)
        self._io_manager.proceed('', prompt=prompt)

    def edit(self, line_number=None):
        r'''Edits file.

        Returns none.
        '''
        self._io_manager.edit(
            self._path,
            line_number=line_number,
            )

    def open(self):
        r'''Opens file.

        Returns none.
        '''
        self._io_manager.open_file(self._path)

    def typeset_tex_file(self, prompt=True):
        r'''Typesets TeX file.

        Returns none.
        '''
        input_directory = os.path.dirname(self._path)
        basename = os.path.basename(self._path)
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
        self._io_manager.view(self._path)

    def write_boilerplate(
        self, 
        pending_user_input=None,
        prompt=True,
        ):
        r'''Writes asset boilerplate.

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
