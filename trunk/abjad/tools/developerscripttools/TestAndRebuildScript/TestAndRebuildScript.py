import doctest
import importlib
import os
import pytest
from abjad.tools import iotools
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript


class TestAndRebuildScript(DeveloperScript):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 're'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return None

    @property
    def short_description(self):
        return 'Run py.test -x, doctest -x and then rebuild the API.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC PROPERTIES ###

    def get_terminal_width(self):
        """Borrowed from the py lib."""
        try:
            import termios, fcntl, struct
            call = fcntl.ioctl(0, termios.TIOCGWINSZ,
                               struct.pack('hhhh', 0, 0, 0, 0))
            height, width = struct.unpack('hhhh', call)[:2]
            terminal_width = width
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            # FALLBACK
            terminal_width = int(os.environ.get('COLUMNS', 80)) - 1
        return terminal_width

    def rebuild_docs(self, args):
        from abjad.tools import developerscripttools
        developerscripttools.BuildApiScript()(['-X', '-M'])

    def run_pytest(self, args):
        options = ['-x', '-rf', '.']
        return pytest.main(options)        

    def run_doctest(self, args):
        start_message = ' doctest session starts '
        stop_message = ' {} of {} tests passed, in {} modules '

        print start_message.center(self.get_terminal_width(), '=')
        print

        globs = importlib.import_module('abjad').__dict__.copy()
        try:
            globs.update(importlib.import_module('experimental.tools').__dict__)
            globs.update(importlib.import_module('experimental.demos').__dict__)
        except ImportError:
            pass
        failed_tests = 0
        passed_tests = 0
        passed_modules = 0
        optionflags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS|doctest.REPORT_NDIFF|doctest.REPORT_ONLY_FIRST_FAILURE
        for dir_path, dir_names, file_names in os.walk('.'):
            for file_name in file_names:
                if file_name.endswith('.py') and \
                    not file_name.startswith('test_') and \
                    not file_name == '__init__.py':
                    full_file_name = os.path.abspath(os.path.join(dir_path, file_name))
                    print os.path.relpath(full_file_name)
                    failure_count, test_count = doctest.testfile(
                        full_file_name,
                        module_relative=False,
                        globs=globs,
                        optionflags=optionflags
                        )
                    if failure_count:
                        failed_tests += failure_count
                        return True
                    passed_modules += 1
                    passed_tests += test_count

        print
        print stop_message.format(
            passed_tests - failed_tests,
            passed_tests,
            passed_modules).center(self.get_terminal_width(), '=')

        return False

    def process_args(self, args):
        iotools.clear_terminal()
        if not self.run_pytest(args):
            print
            if not self.run_doctest(args):
                print
                self.rebuild_docs(args)

    def setup_argument_parser(self, parser):
        pass
