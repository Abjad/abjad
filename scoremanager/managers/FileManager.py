# -*- encoding: utf-8 -*-
import os
import traceback
from abjad.tools import stringtools
from scoremanager.managers.Manager import Manager


class FileManager(Manager):
    r'''File manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(FileManager, self)
        superclass.__init__(path=path, session=session)

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_action(self):
        superlcass = super(FileManager, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            'cp': self.copy,
            'o': self.open,
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
        except:
            traceback.print_exc()
            self._io_manager.display('')
            return 'corrupt'
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
            name = stringtools.to_space_delimited_lowercase(name)
            return name

    def _handle_main_menu_result(self, result):
        if result in self._input_to_action:
            self._input_to_action[result]()
        elif result == 'user entered lone return':
            self._io_manager.edit(self._path)

    def _is_editable(self):
        if self._path.endswith(('.tex', '.py')):
            return True
        return False

    def _make_empty_asset(self, prompt=False):
        if not os.path.exists(self._path):
            with file(self._path, 'w') as file_pointer:
                file_pointer.write('')
        self._io_manager.proceed(prompt=prompt)

    def _make_file_menu_section(self, menu):
        commands = []
        if self._is_editable():
            commands.append(('file - edit', 'e'))
        commands.append(('file - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            )

    def _make_main_menu(self, name='file manager'):
        menu = self._io_manager.make_menu(name=name)
        self._main_menu = menu
        self._make_file_menu_section(self, menu)
        return menu

    def _read_lines(self):
        result = []
        if self._path:
            if os.path.exists(self._path):
                with file(self._path) as file_pointer:
                    result.extend(file_pointer.readlines())
        return result
    
    def _write(self, contents):
        with file(self._path, 'w') as file_pointer:
            file_pointer.write(contents)

    def _write_stub(self):
        self._write(self._unicode_directive)