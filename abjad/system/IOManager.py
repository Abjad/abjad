import cProfile
import datetime
import io
import os
import pathlib
import platform
import pstats
import re
import shutil
import subprocess
import sys
from abjad.system.AbjadObject import AbjadObject


class IOManager(AbjadObject):
    """
    Manages Abjad IO.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Managers'

    __slots__ = ()

    ### PRIVATE METHODS ###

    @staticmethod
    def _ensure_directory_existence(directory):
        if not directory:
            directory = '.'
        if not os.path.isdir(directory):
            lines = []
            line = 'Attention: {!r} does not exist on your system.'
            line = line.format(directory)
            lines.append(line)
            lines.append('Abjad will now create it to store all output files.')
            lines.append('Press any key to continue.')
            message = '\n'.join(lines)
            input(message)
            os.makedirs(directory)

    @staticmethod
    def _make_score_package(
        score_package_path,
        composer_email=None,
        composer_full_name=None,
        composer_last_name=None,
        composer_github_username=None,
        composer_library=None,
        score_title=None,
        year=None,
        ):
        import abjad
        configuration = abjad.AbjadConfiguration()
        score_package_name = os.path.basename(score_package_path)
        source_path = os.path.join(
            configuration.boilerplate_directory,
            'score',
            )
        target_path = score_package_path
        if not os.path.exists(target_path):
            shutil.copytree(source_path, target_path)
        else:
            for subentry in os.listdir(source_path):
                subentry_source = os.path.join(source_path, subentry)
                subentry_target = os.path.join(target_path, subentry)
                if os.path.isfile(subentry_source):
                    shutil.copy(subentry_source, subentry_target)
                elif os.path.isdir(subentry_source):
                    shutil.copytree(subentry_source, subentry_target)
                else:
                    raise ValueError(subentry_source)
        old_contents_directory = os.path.join(target_path, 'score')
        new_contents_directory = os.path.join(
            target_path,
            score_package_name,
            )
        shutil.move(old_contents_directory, new_contents_directory)
        suffixes = ('.py', '.tex', '.md', '.rst', '.ly', '.ily')
        for root, directory_name, file_names in os.walk(target_path):
            for file_name in file_names:
                if not file_name.endswith(suffixes):
                    continue
                file_ = os.path.join(root, file_name)
                with open(file_, 'r') as file_pointer:
                    template = file_pointer.read()
                try:
                    template = template.format(
                        composer_email=composer_email,
                        composer_full_name=composer_full_name,
                        composer_github_username=composer_github_username,
                        composer_last_name=composer_last_name,
                        composer_library=composer_library,
                        score_package_name=score_package_name,
                        score_title=score_title,
                        year=year,
                        )
                except (IndexError, KeyError):
                    lines = template.splitlines()
                    for i, line in enumerate(lines):
                        try:
                            lines[i] = line.format(
                                composer_email=composer_email,
                                composer_full_name=composer_full_name,
                                composer_github_username=composer_github_username,
                                composer_last_name=composer_last_name,
                                composer_library=composer_library,
                                score_package_name=score_package_name,
                                score_title=score_title,
                                year=year,
                                )
                        except (KeyError, IndexError, ValueError):
                            pass
                    template = '\n'.join(lines)
                with open(file_, 'w') as file_pointer:
                    file_pointer.write(template)

    @staticmethod
    def _read_from_pipe(pipe):
        lines = []
        string = pipe.read()
        for line in string.splitlines():
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                continue
            lines.append(line)
        return '\n'.join(lines)

    @staticmethod
    def _warn_when_output_directory_almost_full(last_number):
        import abjad
        abjad_output_directory = abjad.abjad_configuration[
            'abjad_output_directory']
        max_number = 10000
        lines = []
        lines.append('')
        lines.append('WARNING: Abjad output directory almost full!')
        line = 'Abjad output directory contains {} files '
        line += 'and only {} are allowed.'
        line = line.format(last_number, max_number)
        lines.append(line)
        line = 'Please empty {} soon!'.format(abjad_output_directory)
        lines.append(line)
        lines.append('')
        for line in lines:
            print(line.center(80))

    ### PUBLIC METHODS ###

    @staticmethod
    def clear_terminal():
        """
        Clears terminal.

        Runs ``clear`` if OS is POSIX-compliant (UNIX / Linux / MacOS).

        Runs ``cls`` if OS is not POSIX-compliant (Windows).

        Returns none.
        """
        if os.name == 'posix':
            command = 'clear'
        else:
            command = 'cls'
        IOManager.spawn_subprocess(command)

    @staticmethod
    def count_function_calls(
        argument,
        global_context=None,
        local_context=None,
        fixed_point=True,
        ):
        """
        Counts function calls required to execute ``argument``.

        Wraps ``IOManager.profile(argument)``.

        Returns nonnegative integer.
        """
        def extract_count(profile_output):
            return int(profile_output.splitlines()[2].split()[0])
        if fixed_point:
            # profile at least twice to ensure consist results from profiler;
            # not sure why but profiler eventually levels off to consistent
            # output
            last_result, current_result = 'foo', 'bar'
            while current_result != last_result:
                last_result = current_result
                current_result = IOManager.profile(
                    argument,
                    print_to_terminal=False,
                    global_context=global_context,
                    local_context=local_context,
                    )
                current_result = extract_count(current_result)
            return current_result
        result = IOManager.profile(
            argument,
            print_to_terminal=False,
            global_context=global_context,
            local_context=local_context,
            )
        result = extract_count(result)
        return result

    @staticmethod
    def execute_file(path=None, attribute_names=None):
        """
        Executes file ``path``.

        Returns ``attribute_names`` from file.
        """
        assert path is not None
        assert isinstance(attribute_names, tuple)
        path = pathlib.Path(path)
        if not path.is_file():
            return
        file_contents_string = path.read_text()
        try:
            result = IOManager.execute_string(
                file_contents_string,
                attribute_names,
                )
        except:
            message = 'Exception raised in {}.'.format(path)
            # use print instead of display
            # to force to terminal even when called in silent context
            print(message)
            traceback.print_exc()
            return 'corrupt'
        return result

    @staticmethod
    def execute_string(
        string,
        attribute_names=None,
        local_namespace=None,
        ):
        """
        Executes ``string``.

        ..  container:: example

            >>> string = 'foo = 23'
            >>> attribute_names = ('foo', 'bar')
            >>> abjad.IOManager.execute_string(string, attribute_names)
            (23, None)

        Returns ``attribute_names`` from executed string.
        """
        assert isinstance(string, str)
        assert isinstance(attribute_names, tuple)
        if local_namespace is None:
            local_namespace = {}
        assert isinstance(local_namespace, dict)
        local_namespace = {}
        try:
            exec(string, local_namespace, local_namespace)
        except SyntaxError:
            return
        result = []
        for name in attribute_names:
            if name in local_namespace:
                result.append(local_namespace[name])
            else:
                result.append(None)
        result = tuple(result)
        return result

    @staticmethod
    def find_executable(name, flags=os.X_OK):
        """
        Finds executable ``name``.

        Similar to Unix ``which`` command.

        ..  container:: example

            >>> abjad.IOManager.find_executable('python3.6') # doctest: +SKIP
            ['/usr/bin/python3.6']

        Returns list of zero or more full paths to ``name``.
        """
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
    def get_last_output_file_name(
        extension=None,
        output_directory=None,
        ):
        """
        Gets last output file name in ``output_directory``.

        ..  container:: example

            >>> abjad.IOManager.get_last_output_file_name() # doctest: +SKIP
            '6222.ly'

        Gets last output file name in Abjad output directory when
        ``output_directory`` is none.

        Returns none when output directory contains no output files.

        Returns string or none.
        """
        import abjad
        pattern = re.compile('\d{4,4}.[a-z]{2,3}')
        output_directory = output_directory or abjad.abjad_configuration[
            'abjad_output_directory']
        if not os.path.exists(output_directory):
            return
        all_file_names = os.listdir(output_directory)
        if extension:
            all_output = [
                x for x in all_file_names
                if pattern.match(x) and x.endswith(extension)
                ]
        else:
            all_output = [x for x in all_file_names if pattern.match(x)]
        if all_output == []:
            last_output_file_name = None
        else:
            last_output_file_name = sorted(all_output)[-1]
        return last_output_file_name

    @staticmethod
    def get_next_output_file_name(
        file_extension='ly',
        output_directory=None,
        ):
        """
        Gets next output file name with ``file_extension`` in
        ``output_directory``.

        ..  container:: example

            >>> abjad.IOManager.get_next_output_file_name() # doctest: +SKIP
            '6223.ly'

        Gets next output file name with ``file_extension`` in Abjad output
        directory when ``output_directory`` is none.

        Returns string.
        """
        assert file_extension.isalpha() and \
            0 < len(file_extension) < 4, repr(file_extension)
        last_output = IOManager.get_last_output_file_name(
            output_directory=output_directory,
            )
        if last_output is None:
            next_number = 1
            next_output_file_name = '0001.{}'.format(file_extension)
        else:
            last_number = int(last_output.split('.')[0])
            next_number = last_number + 1
            next_output_file_name = '{next_number:04d}.{file_extension}'
            next_output_file_name = next_output_file_name.format(
                next_number=next_number,
                file_extension=file_extension,
                )
        if 9000 < next_number:
            IOManager._warn_when_output_directory_almost_full(last_number)
        return next_output_file_name

    @staticmethod
    def make_subprocess(command):
        """
        Makes Popen instance.

        ..  container:: example

            >>> command = 'echo "hellow world"'
            >>> abjad.IOManager.make_subprocess(command)
            <subprocess.Popen object at 0x...>

        Defined equal to:

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                )

        Redirects stderr to stdout.
        """
        return subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )

    @staticmethod
    def open_file(file_path, application=None, line_number=None):
        """
        Opens ``file_path``.

        Uses ``application`` when ``application`` is not none.

        Uses Abjad configuration file ``text_editor`` when
        ``application`` is none.

        Takes best guess at operating system-specific file opener when both
        ``application`` and Abjad configuration file ``text_editor`` are none.

        Respects ``line_number`` when ``file_path`` can be opened with text
        editor.

        Returns none.
        """
        import abjad
        if sys.platform.lower().startswith('win'):
            os.startfile(file_path)
            return
        viewer = None
        if sys.platform.lower().startswith('linux'):
            viewer = application or 'xdg-open'
        elif file_path.endswith('.pdf'):
            viewer = application or abjad.abjad_configuration['pdf_viewer']
        elif file_path.endswith((
            '.log',
            '.py',
            '.rst',
            '.txt',
            )):
            viewer = application or abjad.abjad_configuration['text_editor']
        elif file_path.endswith((
            '.mid',
            '.midi',
            )):
            viewer = application or abjad.abjad_configuration['midi_player']
        viewer = viewer or 'open'
        if line_number:
            command = '{} +{} {}'.format(viewer, line_number, file_path)
        else:
            command = '{} {}'.format(viewer, file_path)
        IOManager.spawn_subprocess(command)

    @staticmethod
    def open_last_log():
        """
        Opens LilyPond log file in operating system-specific text editor.

        Returns none.
        """
        import abjad
        text_editor = abjad.abjad_configuration.get_text_editor()
        file_path = abjad.abjad_configuration.lilypond_log_file_path
        IOManager.open_file(file_path, application=text_editor)

    @staticmethod
    def open_last_ly(target=-1):
        """
        Opens last LilyPond output file produced by Abjad.

        Uses operating-specific text editor.

        Set ``target=-2`` to open the next-to-last LilyPond output file
        produced by Abjad, and so on.

        Returns none.
        """
        import abjad
        abjad_output_directory = abjad.abjad_configuration[
            'abjad_output_directory']
        text_editor = abjad.abjad_configuration.get_text_editor()
        if isinstance(target, int) and target < 0:
            last_lilypond = IOManager.get_last_output_file_name()
            if last_lilypond:
                last_number = last_lilypond
                last_number = last_number.replace('.ly', '')
                last_number = last_number.replace('.pdf', '')
                last_number = last_number.replace('.midi', '')
                last_number = last_number.replace('.mid', '')
                target_number = int(last_number) + (target + 1)
                target_str = '%04d' % target_number
                target_ly = os.path.join(
                    abjad_output_directory,
                    target_str + '.ly',
                    )
            else:
                print('Target LilyPond input file does not exist.')
        elif isinstance(target, int) and 0 <= target:
            target_str = '%04d' % target
            target_ly = os.path.join(
                abjad_output_directory,
                target_str + '.ly',
                )
        elif isinstance(target, str):
            target_ly = os.path.join(abjad_output_directory, target)
        else:
            message = 'can not get target LilyPond input from {}.'
            message = message.format(target)
            raise ValueError(message)
        if os.path.exists(target_ly):
            IOManager.open_file(target_ly, application=text_editor)
        else:
            message = 'Target LilyPond input file {} does not exist.'
            message = message.format(target_ly)
            print(message)

    @staticmethod
    def open_last_pdf(target=-1):
        """
        Opens last PDF generated by Abjad.

        Abjad writes PDFs to the ``~/.abjad/output`` directory by default.

        You may change this by setting the ``abjad_output_directory`` variable in
        the ``config.py`` file.

        Set ``target=-2`` to open the next-to-last PDF generated by Abjad.

        Returns none.
        """
        import abjad
        abjad_output_directory = abjad.abjad_configuration[
            'abjad_output_directory']
        if isinstance(target, int) and target < 0:
            last_lilypond_file_path = IOManager.get_last_output_file_name()
            if last_lilypond_file_path:
                result = os.path.splitext(last_lilypond_file_path)
                file_name_root, extension = result
                last_number = file_name_root
                target_number = int(last_number) + (target + 1)
                target_str = '%04d' % target_number
                target_pdf = os.path.join(
                    abjad_output_directory,
                    target_str + '.pdf',
                    )
            else:
                message = 'Target PDF does not exist.'
                print(message)
        elif isinstance(target, int) and 0 <= target:
            target_str = '%04d' % target
            target_pdf = os.path.join(
                abjad_output_directory,
                target_str + '.pdf',
                )
        elif isinstance(target, str):
            target_pdf = os.path.join(
                abjad_output_directory,
                target,
                )
        else:
            message = 'can not get target pdf name from {}.'
            message = message.format(target)
            raise ValueError(message)
        if os.stat(target_pdf):
            pdf_viewer = abjad.abjad_configuration['pdf_viewer']
            IOManager.open_file(target_pdf, pdf_viewer)
        else:
            message = 'target PDF {} does not exist.'
            message = message.format(target_pdf)
            print(message)

    @staticmethod
    def profile(
        argument,
        sort_by='cumulative',
        line_count=12, strip_dirs=True,
        print_callers=False,
        print_callees=False,
        global_context=None,
        local_context=None,
        print_to_terminal=True,
        ):
        """
        Profiles ``argument``.

        ..  container:: example

            ::

                >>> argument = 'abjad.Staff("c8 c8 c8 c8 c8 c8 c8 c8")'
                >>> abjad.IOManager.profile(
                ...     argument,
                ...     global_context=globals(),
                ...     ) # doctest: +SKIP
                Tue Apr  5 20:32:40 2011    _tmp_abj_profile

                        2852 function calls (2829 primitive calls) in 0.006 CPU seconds

                Ordered by: cumulative time
                List reduced from 118 to 12 due to restriction <12>

                ncalls  tottime  percall  cumtime  percall filename:lineno(function)
                        1    0.000    0.000    0.006    0.006 <string>:1(<module>)
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

        Set ``argument`` to any string of Abjad input.

        Set ``sort_by`` to ``'cumulative'``, ``'time'`` or ``'calls'``.

        Set ``line_count`` to any nonnegative integer.

        Set ``strip_dirs`` to true to strip directory names from output lines.

        See the `Python docs <http://docs.python.org/library/profile.html>`_
        for more information on the Python profilers.

        Returns none when ``print_to_terminal`` is false.

        Returns string when ``print_to_terminal`` is true.
        """
        now_string = datetime.datetime.today().strftime('%a %b %d %H:%M:%S %Y')
        profile = cProfile.Profile()
        if global_context is None:
            profile = profile.run(
                argument,
                )
        else:
            profile = profile.runctx(
                argument,
                global_context,
                local_context,
                )
        stats_stream = io.StringIO()
        stats = pstats.Stats(profile, stream=stats_stream)
        if sort_by == 'cum':
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
            print(result)
        else:
            return result

    @staticmethod
    def run_command(command):
        """
        Makes subprocess with ``command``.

        Runs command.

        Displays nothing.

        Returns stdout from subprocess.
        """
        process = IOManager.make_subprocess(command)
        lines = IOManager._read_from_pipe(process.stdout)
        lines = lines.splitlines()
        return lines

    @staticmethod
    def run_lilypond(ly_path, flags=None, lilypond_path=None):
        """
        Runs LilyPond on ``ly_path``.

        Writes redirected output of Unix ``date`` to top line of LilyPond log
        file.

        Then appends redirected output of LilyPond output to the LilyPond log
        file.

        Returns none.
        """
        import abjad
        ly_path = str(ly_path)
        lilypond_path = abjad.abjad_configuration.get('lilypond_path')
        if not lilypond_path:
            lilypond_path = abjad.IOManager.find_executable('lilypond')
            if lilypond_path:
                lilypond_path = lilypond_path[0]
            else:
                lilypond_path = 'lilypond'
        lilypond_base, extension = os.path.splitext(ly_path)
        flags = flags or ''
        date = datetime.datetime.now().strftime('%c')
        log_file_path = abjad.abjad_configuration.lilypond_log_file_path
        command = '{} {} -dno-point-and-click -o {} {}'.format(
            lilypond_path,
            flags,
            lilypond_base,
            ly_path,
            )
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
        subprocess_output, _ = process.communicate()
        subprocess_output = subprocess_output.decode('utf-8')
        exit_code = process.returncode
        with open(log_file_path, 'w') as file_pointer:
            file_pointer.write(date + '\n')
            file_pointer.write(subprocess_output)
        postscript_path = ly_path.replace('.ly', '.ps')
        try:
            os.remove(postscript_path)
        except OSError:
            pass
        # TODO: maybe just 'return exit_code'?
        if exit_code:
            return False
        return True

    @staticmethod
    def save_last_ly_as(file_path):
        """
        Saves last LilyPond file created by Abjad as ``file_path``.

        Returns none.
        """
        import abjad
        abjad_output_directory = abjad.abjad_configuration[
            'abjad_output_directory']
        last_output_file_name = IOManager.get_last_output_file_name(
            extension='.ly',
            )
        if last_output_file_name is None:
            return
        last_ly_full_name = os.path.join(
            abjad_output_directory,
            last_output_file_name,
            )
        with open(file_path, 'w') as new:
            with open(last_ly_full_name, 'r') as old:
                new.write(''.join(old.readlines()))

    @staticmethod
    def save_last_pdf_as(file_path):
        """
        Saves last PDF created by Abjad as ``file_path``.

        Returns none.
        """
        import abjad
        abjad_output_directory = abjad.abjad_configuration[
            'abjad_output_directory']
        last_output_file_name = IOManager.get_last_output_file_name(
            extension='.pdf',
            )
        last_pdf_full_name = os.path.join(
            abjad_output_directory,
            last_output_file_name,
            )
        with open(file_path, 'w') as new:
            with open(last_pdf_full_name, 'r') as old:
                new.write(''.join(old.readlines()))

    @staticmethod
    def spawn_subprocess(command):
        """
        Spawns subprocess and runs ``command``.

        The function is basically a reimplementation of the
        deprecated ``os.system()`` using Python's ``subprocess`` module.

        Redirects stderr to stdout.

        Returns integer exit code.
        """
        return subprocess.call(command, shell=True)
