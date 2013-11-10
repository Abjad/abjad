# -*- encoding: utf-8 -*-
import StringIO
import datetime
import os
import platform
import subprocess
import sys


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
    def clear_terminal():
        '''Runs ``clear`` if OS is POSIX-compliant (UNIX / Linux / MacOS).

        Runs ``cls`` if OS is not POSIX-compliant (Windows).

        ::

            >>> IOManager.clear_terminal() # doctest: +SKIP

        Returns none.
        '''
        from abjad.tools import iotools
        if os.name == 'posix':
            command = 'clear'
        else:
            command = 'cls'
        IOManager.spawn_subprocess(command)

    @staticmethod
    def count_function_calls(
        expr,
        global_context=None,
        local_context=None,
        fixed_point=True,
        ):
        '''Counts function calls returned by ``IOManager.profile_expr(expr)``.

        ..  container:: example

            **Example 1.** Function calls required to initialize note
            from string:

            ::

                >>> IOManager.count_function_calls("Note('c4')", globals())
                10276

        ..  container:: example

            **Example 2.** Function calls required to initialize note
            from integers:

            ::

                >>> IOManager.count_function_calls(
                ...     "Note(-12, (1, 4))", globals())
                172

        Returns nonnegative integer.
        '''
        from abjad.tools import iotools

        def extract_count(profile_output):
            return int(profile_output.splitlines()[2].split()[0])

        if fixed_point:
            # profile at least twice to ensure consist results from profiler;
            # not sure why but profiler eventually levels off to consistent
            # output
            last_result, current_result = 'foo', 'bar'
            while current_result != last_result:
                last_result = current_result
                current_result = IOManager.profile_expr(
                    expr,
                    print_to_terminal=False,
                    global_context=global_context,
                    local_context=local_context,
                    )
                current_result = extract_count(current_result)
            return current_result

        result = IOManager.profile_expr(
            expr,
            print_to_terminal=False,
            global_context=global_context,
            local_context=local_context,
            )
        result = extract_count(result)
        return result

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

            >>> IOManager.find_executable('python2.7') # doctest: +SKIP
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
    def open_file(file_path, application=None):
        r'''Opens `file_path` with operating system-specific file-opener
        with `application` is none.

        Opens `file_path` with `application` when `application` is not none.

        Returns none.
        '''
        from abjad.tools import iotools
        if os.name == 'nt':
            os.startfile(file_path)
            return
        if sys.platform.lower() == 'linux2':
            viewer = application or 'xdg-open'
        else:
            viewer = application or 'open'
        command = '{} {} &'.format(viewer, file_path)
        IOManager.spawn_subprocess(command)

    @staticmethod
    def profile_expr(
        expr,
        sort_by='cum',
        line_count=12, strip_dirs=True,
        print_callers=False,
        print_callees=False,
        global_context=None,
        local_context=None,
        print_to_terminal=True,
        ):
        r'''Profiles `expr`.

        ::

            >>> expr = 'Staff(scoretools.make_repeated_notes(8))'
            >>> IOManager.profile_expr(expr) # doctest: +SKIP
            Tue Apr  5 20:32:40 2011    _tmp_abj_profile

                    2852 function calls (2829 primitive calls) in 0.006 CPU seconds

            Ordered by: cumulative time
            List reduced from 118 to 12 due to restriction <12>

            ncalls  tottime  percall  cumtime  percall filename:lineno(function)
                    1    0.000    0.000    0.006    0.006 <string>:1(<module>)
                    1    0.000    0.000    0.003    0.003 make_repeated_notes.py:5(
                    1    0.001    0.001    0.003    0.003 make_notes.py:12(make_not
                    1    0.000    0.000    0.003    0.003 Staff.py:21(__init__)
                    1    0.000    0.000    0.003    0.003 Context.py:11(__init__)
                    1    0.000    0.000    0.003    0.003 Container.py:23(__init__)
                    1    0.000    0.000    0.003    0.003 Container.py:271(_initial
                    2    0.000    0.000    0.002    0.001 all_are_logical_voice_con
                52    0.001    0.000    0.002    0.000 component_to_logical_voic
                    1    0.000    0.000    0.002    0.002 _construct_unprolated_not
                    8    0.000    0.000    0.002    0.000 make_tied_note.py:5(make_
                    8    0.000    0.000    0.002    0.000 make_tied_leaf.py:5(make_

        Wraps the built-in Python ``cProfile`` module.

        Set `expr` to any string of Abjad input.

        Set `sort_by` to `'cum'`, `'time'` or `'calls'`.

        Set `line_count` to any nonnegative integer.

        Set `strip_dirs` to true to strip directory names from output lines.

        See the `Python docs <http://docs.python.org/library/profile.html>`_
        for more information on the Python profilers.

        Returns none when `print_to_terminal` is false.

        Returns string when `print_to_terminal` is true.
        '''

        import cProfile
        import pstats
        from abjad.tools import iotools

        now_string = datetime.datetime.today().strftime('%a %b %d %H:%M:%S %Y')

        profile = cProfile.Profile()
        if global_context is None:
            profile = profile.run(
                expr,
                )
        else:
            profile = profile.runctx(
                expr,
                global_context,
                local_context,
                )

        stats_stream = StringIO.StringIO()
        stats = pstats.Stats(profile, stream=stats_stream)

        if sort_by == 'cum':
            if platform.python_version() == '2.7.5':
                sort_by = 'cumulative'

        if strip_dirs:
            stats.strip_dirs().sort_stats(sort_by).print_stats(line_count)
        else:
            stats.sort_stats(sort_by).print_stats(line_count)
        if print_callers:
            stats.sort_stats(sort_by).print_callers(line_count)
        if print_callees:
            stats.sort_stats(sort_by).print_callees(line_count)

        result = now_string + '\n\n' + stats_stream.getvalue()
        stats_stream.close()

        if print_to_terminal:
            print result
        else:
            return result

    @staticmethod
    def save_last_ly_as(file_path):
        r'''Saves last LilyPond file created in Abjad as `file_path`.

        ::

            >>> file_path = '/project/output/example-1.ly'
            >>> IOManager.save_last_ly_as(file_path) # doctest: +SKIP

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
            >>> IOManager.save_last_pdf_as(file_path) # doctest: +SKIP

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
            >>> IOManager.spawn_subprocess(command) # doctest: +SKIP
            hello world

        The function is basically a reimplementation of the
        deprecated ``os.system()`` using Python's ``subprocess`` module.

        Returns integer result code.
        '''
        return subprocess.call(command, shell=True)
