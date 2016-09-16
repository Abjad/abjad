# -*- coding: utf-8 -*-
import os
import shutil
from abjad.tools import commandlinetools
from abjad.tools import stringtools
from abjad.tools import systemtools
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib


class TestCase(systemtools.TestCase):

    test_path = pathlib.Path(__file__).parent
    doctest_path = test_path.joinpath('doctest_test')

    failing_module_path = doctest_path.joinpath('doctest_fail.py')
    failing_module_contents = stringtools.normalize(r'''
        def fail():
            """
            A failing module.

            ::

                >>> True is False
                True

            """
            return None
    ''')

    passing_module_path = doctest_path.joinpath('doctest_pass.py')
    passing_module_contents = stringtools.normalize(r'''
        def pass():
            """
            A passing module.

            ::

                >>> True is False
                False

            """
            return None
    ''')

    def setUp(self):
        super(TestCase, self).setUp()
        if not self.doctest_path.exists():
            self.doctest_path.mkdir()
        with open(str(self.failing_module_path), 'w') as file_pointer:
            file_pointer.write(self.failing_module_contents)
        with open(str(self.passing_module_path), 'w') as file_pointer:
            file_pointer.write(self.passing_module_contents)

    def tearDown(self):
        super(TestCase, self).tearDown()
        shutil.rmtree(str(self.doctest_path))

    def test_both(self):
        script = commandlinetools.DoctestScript()
        command = [str(self.doctest_path)]
        with systemtools.TemporaryDirectoryChange(str(self.test_path)):
            with systemtools.RedirectedStreams(stdout=self.string_io):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
        assert context_manager.exception.code == 1
        script_output = self.ansi_escape.sub('', self.string_io.getvalue())
        script_output = stringtools.normalize(script_output)
        expected = stringtools.normalize('''
        doctest_test/doctest_fail.py FAILED
        doctest_test/doctest_pass.py OK

        **********************************************************************
        File ".../doctest_test/doctest_fail.py", line 7, in doctest_fail.py
        Failed example:
            True is False
        Expected:
            True
        Got:
            False
        **********************************************************************
        1 items had failures:
            1 of   1 in doctest_fail.py
        ***Test Failed*** 1 failures.

        FAILED: doctest_test/doctest_fail.py

        1 passed, 1 failed out of 2 tests in 2 modules.
        '''.replace('/', os.path.sep))
        self.compare_strings(expected, script_output)

    def test_diff(self):
        script = commandlinetools.DoctestScript()
        command = ['--diff', str(self.failing_module_path)]
        with systemtools.TemporaryDirectoryChange(str(self.test_path)):
            with systemtools.RedirectedStreams(stdout=self.string_io):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
        assert context_manager.exception.code == 1
        script_output = self.ansi_escape.sub('', self.string_io.getvalue())
        script_output = stringtools.normalize(script_output)
        expected = stringtools.normalize('''
        doctest_test/doctest_fail.py FAILED

        **********************************************************************
        File ".../doctest_test/doctest_fail.py", line 7, in doctest_fail.py
        Failed example:
            True is False
        Differences (ndiff with -expected +actual):
            - True
            + False
        **********************************************************************
        1 items had failures:
            1 of   1 in doctest_fail.py
        ***Test Failed*** 1 failures.

        FAILED: doctest_test/doctest_fail.py

        0 passed, 1 failed out of 1 test in 1 module.
        '''.replace('/', os.path.sep))
        self.compare_strings(expected, script_output)

    def test_fail(self):
        script = commandlinetools.DoctestScript()
        command = [str(self.failing_module_path)]
        with systemtools.TemporaryDirectoryChange(str(self.test_path)):
            with systemtools.RedirectedStreams(stdout=self.string_io):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
        assert context_manager.exception.code == 1
        script_output = self.ansi_escape.sub('', self.string_io.getvalue())
        script_output = stringtools.normalize(script_output)
        expected = stringtools.normalize('''
        doctest_test/doctest_fail.py FAILED

        **********************************************************************
        File ".../doctest_test/doctest_fail.py", line 7, in doctest_fail.py
        Failed example:
            True is False
        Expected:
            True
        Got:
            False
        **********************************************************************
        1 items had failures:
            1 of   1 in doctest_fail.py
        ***Test Failed*** 1 failures.

        FAILED: doctest_test/doctest_fail.py

        0 passed, 1 failed out of 1 test in 1 module.
        '''.replace('/', os.path.sep))
        self.compare_strings(expected, script_output)

    def test_pass(self):
        script = commandlinetools.DoctestScript()
        command = [str(self.passing_module_path)]
        with systemtools.TemporaryDirectoryChange(str(self.test_path)):
            with systemtools.RedirectedStreams(stdout=self.string_io):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
        assert context_manager.exception.code == 0
        script_output = self.ansi_escape.sub('', self.string_io.getvalue())
        script_output = stringtools.normalize(script_output)
        expected = stringtools.normalize('''
        doctest_test/doctest_pass.py OK

        1 passed, 0 failed out of 1 test in 1 module.
        '''.replace('/', os.path.sep))
        self.compare_strings(expected, script_output)
