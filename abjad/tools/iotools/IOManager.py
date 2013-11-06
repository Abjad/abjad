# -*- encoding: utf-8 -*-
import os


class IOManager(object):
    r'''Manages Abjad IO.
    '''

    ### PUBLIC METHODS ###

    @staticmethod
    def ensure_directory_existence(directory):
        r'''Ensures existence of `directory`.

        Returns none.
        '''
        if not os.path.isdir(directory):
            lines = []
            line = 'Attention: {!} does not exist on your system.'
            line = line.format(directory)
            lines.append(line)
            lines.append('Abjad will now create it to store all output files.')
            lines.append('Press any key to continue.')
            message = '\n'.join(lines)
            raw_input(message)
            os.makedirs(directory)

    @staticmethod
    def find_executable(name, flags=os.X_OK):
        r'''Finds executable `name`.

        Similar to Unix ``which`` command.

        ::

            >>> iotools.IOManager.find_executable('python2.7') # doctest: +SKIP
            ['/usr/bin/python2.7']

        Returns list of zero or more full paths to `name`.
        '''
        result = []
        extensions = [
            x
            for x in os.environ.get('PATHEXT', '').split(os.pathsep)
            if x
            ]
        path = os.environ.get('PATH', None)
        if path is None:
            return []
        for path in os.environ.get('PATH', '').split(os.pathsep):
            path = os.path.join(path, name)
            if os.access(path, flags):
                result.append(path)
            for extension in extensions:
                path_extension = path + extension
                if os.access(path_extension, flags):
                    result.append(path_extension)
        return result

