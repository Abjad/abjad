# -*- encoding: utf-8 -*-
import os
import subprocess


class IOManager(object):
    r'''Manages Abjad IO.
    '''

    ### PRIVATE METHODS ###

    @staticmethod
    def _warn_when_output_directory_almost_full(last_number):
        r'''Prints warning when Abjad output directory is almost full.

        Returns none.
        '''
        from abjad import abjad_configuration
        abjad_output = abjad_configuration['abjad_output']
        max_number = 10000
        lines = []
        lines.append('')
        lines.append('WARNING: Abjad output directory almost full!')
        line = 'Abjad output directory contains {} files '
        line += 'and only {} are allowed.'
        line = line.format(last_number, max_number)
        lines.append(line)
        line = 'Please empty {} soon!'.format(abjad_output)
        lines.append(line)
        lines.append('')
        for line in lines:
            print line.center(80)

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

    @staticmethod
    def save_last_ly_as(file_path):
        r'''Saves last LilyPond file created in Abjad as `file_path`.

        ::

            >>> file_path = '/project/output/example-1.ly'
            >>> iotools.IOManager.save_last_ly_as(file_path) # doctest: +SKIP

        Returns none.
        '''
        from abjad import abjad_configuration
        from abjad.tools import iotools
        ABJADOUTPUT = abjad_configuration['abjad_output']
        last_output_file_path = iotools.get_last_output_file_name()
        without_extension, extension = os.path.splitext(last_output_file_path)
        last_ly = without_extension + '.ly'
        last_ly_full_name = os.path.join(ABJADOUTPUT, last_ly)
        with open(file_path, 'w') as new:
            with open(last_ly_full_name, 'r') as old:
                new.write(''.join(old.readlines()))

    @staticmethod
    def save_last_pdf_as(file_path):
        r'''Saves last PDF created in Abjad as `file_path`.

        ::

            >>> file_path = '/project/output/example-1.pdf'
            >>> iotools.IOManager.save_last_pdf_as(file_path) # doctest: +SKIP

        Returns none.
        '''
        from abjad import abjad_configuration
        from abjad.tools import iotools
        ABJADOUTPUT = abjad_configuration['abjad_output']
        last_output_file_name = iotools.get_last_output_file_name()
        without_extension, extension = os.path.splitext(last_output_file_name)
        last_pdf = without_extension + '.pdf'
        last_pdf_full_name = os.path.join(ABJADOUTPUT, last_pdf)
        with open(file_path, 'w') as new:
            with open(last_pdf_full_name, 'r') as old:
                new.write(''.join(old.readlines()))

    @staticmethod
    def spawn_subprocess(command):
        r'''Spawns subprocess and runs `command`.

        Redirects stderr to stdout.

        ::

            >>> command = 'echo "hellow world"'
            >>> iotools.IOManager.spawn_subprocess(command) # doctest: +SKIP
            hello world

        The function is basically a reimplementation of the
        deprecated ``os.system()`` using Python's ``subprocess`` module.

        Returns integer result code.
        '''
        return subprocess.call(command, shell=True)
