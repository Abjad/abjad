# -*- encoding: utf-8 -*-
import os
from abjad.tools import documentationtools
from abjad.tools import systemtools
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript
from abjad.tools.developerscripttools.ReplaceInFilesScript \
    import ReplaceInFilesScript


class RenameModulesScript(DeveloperScript):
    r'''Renames classes and functions.

    Handle renaming the module and package, as well as any tests,
    documentation or mentions of the class throughout the Abjad codebase:

    ..  shell::

        ajv rename --help

    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.

        Returns ``'rename'``.
        '''
        return 'rename'

    @property
    def long_description(self):
        r'''Long description of script.

        Returns string or none.
        '''
        return None

    @property
    def scripting_group(self):
        r'''Scripting group of script.

        Returns none.
        '''
        return None

    @property
    def short_description(self):
        r'''Short description of script.

        Returns string.
        '''
        return 'Rename public modules.'

    @property
    def version(self):
        r'''Version of script.

        Returns float.
        '''
        return 1.0

    ### PRIVATE METHODS ###

    def _codebase_name_to_codebase_docs_path(self, codebase):
        from abjad import abjad_configuration
        if codebase == 'mainline':
            return os.path.join(
                abjad_configuration.abjad_directory,
                'docs',
                'source',
                'api',
                'tools',
                )
        elif codebase == 'experimental':
            return os.path.join(
                abjad_configuration.abjad_experimental_directory,
                'docs',
                'source',
                'tools',
                )
        message = 'bad codebase name: {!r}.'
        message = message.format(codebase)
        raise Exception(message)

    def _codebase_name_to_codebase_tools_path(self, codebase):
        from abjad import abjad_configuration
        if codebase == 'mainline':
            return os.path.join(
                abjad_configuration.abjad_directory, 'tools')
        elif codebase == 'experimental':
            return os.path.join(
                abjad_configuration.abjad_experimental_directory, 'tools')
        message = 'bad codebase name: {!r}.'
        message = message.format(codebase)
        raise Exception(message)

    def _confirm_name_changes(self,
        old_codebase,
        old_tools_package_name,
        old_module_name,
        new_codebase,
        new_tools_package_name,
        new_module_name,
        ):
        max_codebase = max(len(old_codebase), len(new_codebase))
        old_codebase = old_codebase.ljust(max_codebase)
        new_codebase = new_codebase.ljust(max_codebase)
        print('')
        print('Is ...')
        print('')
        print('    [{}] {}.{}()'.format(
            old_codebase, old_tools_package_name, old_module_name))
        print('    ===>')
        print('    [{}] {}.{}()'.format(
            new_codebase, new_tools_package_name, new_module_name))
        print('')
        string = raw_input('... correct [yes, no, abort]? ').lower()
        print('')
        if string in ('y', 'yes'):
            return True
        elif string in ('a', 'abort', 'q', 'quit'):
            raise SystemExit
        elif string in ('n', 'no'):
            return False

    def _get_object_names(self, kind, codebase, tools_package_name):
        assert kind in ('class', 'function')
        tools_path = self._codebase_name_to_codebase_tools_path(codebase)
        path = os.path.join(tools_path, tools_package_name)
        if kind == 'class':
            generator = documentationtools.yield_all_classes(
                code_root=path,
                include_private_objects=True,
                )
        elif kind == 'function':
            generator = documentationtools.yield_all_functions(
                code_root=path,
                include_private_objects=True,
                )
        return tuple(sorted(generator, key=lambda x: x.__name__))

    def _get_tools_package_names(self, codebase):
        tools_path = self._codebase_name_to_codebase_tools_path(codebase)
        names = []
        for x in os.listdir(tools_path):
            if os.path.isdir(os.path.join(tools_path, x)):
                if not x.startswith(('_', '.')):
                    names.append(x)
        return tuple(sorted(names))

    def _parse_tools_package_path(self, path):
        from abjad import abjad_configuration
        if '.' not in path:
            raise SystemExit
        tools_package_name, module_name = path.split('.')
        mainline_tools_directory = os.path.join(
            abjad_configuration.abjad_directory,
            'tools',
            )
        for directory_name in os.listdir(mainline_tools_directory):
            directory = os.path.join(
                mainline_tools_directory, directory_name)
            if not os.path.isdir(directory):
                continue
            elif directory_name != tools_package_name:
                continue
            return 'mainline', tools_package_name, module_name
        experimental_tools_directory = os.path.join(
            abjad_configuration.abjad_experimental_directory,
            'tools',
            )
        for directory_name in os.listdir(mainline_tools_directory):
            directory = os.path.join(
                experimental_tools_directory, directory_name)
            if not os.path.isdir(directory):
                continue
            elif directory_name != tools_package_name:
                continue
            return 'experimental', tools_package_name, module_name
        raise SystemExit

    def _rename_old_api_page(self,
        old_codebase,
        old_tools_package_name,
        old_module_name,
        new_codebase,
        new_tools_package_name,
        new_module_name,
        ):
        print('Renaming old API page ...')
        old_docs_path = self._codebase_name_to_codebase_docs_path(old_codebase)
        new_docs_path = self._codebase_name_to_codebase_docs_path(new_codebase)
        old_rst_file_name = old_module_name + '.rst'
        new_rst_file_name = new_module_name + '.rst'
        old_api_path = os.path.join(
            old_docs_path, old_tools_package_name, old_rst_file_name)
        new_api_path = os.path.join(
            new_docs_path, new_tools_package_name, new_rst_file_name)
        command = 'mv {} {}'.format(
            old_api_path, new_api_path)
        systemtools.IOManager.spawn_subprocess(command)
        print('')

    def _rename_old_module(self,
        old_codebase,
        old_tools_package_name,
        old_module_name,
        new_codebase,
        new_tools_package_name,
        new_module_name,
        ):
        print('Renaming old module ...')
        old_tools_path = self._codebase_name_to_codebase_tools_path(
            old_codebase)
        new_tools_path = self._codebase_name_to_codebase_tools_path(
            new_codebase)
        old_module = old_module_name + '.py'
        old_path = os.path.join(
            old_tools_path, old_tools_package_name, old_module)
        new_module = new_module_name + '.py'
        new_path = os.path.join(
            new_tools_path, new_tools_package_name, new_module)
        command = 'git mv -f {} {}'.format(
            old_path, new_path)
        systemtools.IOManager.spawn_subprocess(command)
        print('')

    def _rename_old_test_files(self,
        old_codebase,
        old_tools_package_name,
        old_module_name,
        new_codebase,
        new_tools_package_name,
        new_module_name,
        ):
        print('Renaming old test file(s) ...')
        old_tools_path = self._codebase_name_to_codebase_tools_path(
            old_codebase)
        old_test_path = os.path.join(
            old_tools_path, old_tools_package_name, 'test')
        if not os.path.exists(old_test_path):
            return
        new_tools_path = self._codebase_name_to_codebase_tools_path(
            new_codebase)
        new_test_path = os.path.join(
            new_tools_path, new_tools_package_name, 'test')
        old_test_file_prefix = 'test_{}_{}'.format(
            old_tools_package_name, old_module_name)
        old_test_file_names = [x for x in os.listdir(old_test_path)
            if x.startswith(old_test_file_prefix) and x.endswith('.py')]
        for old_test_file_name in old_test_file_names:
            old_test_file_path = os.path.join(
                old_test_path, old_test_file_name)
            old_test_file_suffix = old_test_file_name[
                len(old_test_file_prefix):]
            new_test_file_name = 'test_{}_{}{}'.format(
                new_tools_package_name, new_module_name, old_test_file_suffix)
            new_test_file_path = os.path.join(
                new_test_path, new_test_file_name)
            command = 'git mv -f {} {}'.format(
                old_test_file_path, new_test_file_path)
            systemtools.IOManager.spawn_subprocess(command)
        print('')

    def _update_codebase(self,
        old_codebase,
        old_tools_package_name,
        old_module_name,
        new_codebase,
        new_tools_package_name,
        new_module_name,
        ):
        from abjad import abjad_configuration
        without_dirs = ['--without-dirs', 'build', '--without-dirs', '_build']
        directory = abjad_configuration.abjad_root_directory
        print('Updating codebase ...')
        print('')
        old_text = '{}.{}'.format(old_tools_package_name, old_module_name)
        new_text = '{}.{}'.format(new_tools_package_name, new_module_name)
        command = [
            directory,
            old_text,
            new_text,
            '--force',
            '--whole-words-only',
            #'--verbose',
            ]
        command.extend(without_dirs)
        ReplaceInFilesScript()(command)
        print('')
        old_text = 'test_{}_{}_'.format(
            old_tools_package_name, old_module_name)
        new_text = 'test_{}_{}_'.format(
            new_tools_package_name, new_module_name)
        command = [directory, old_text, new_text, '--force', '--verbose']
        command.extend(without_dirs)
        ReplaceInFilesScript()(command)
        print('')
        old_text = old_module_name
        new_text = new_module_name
        command = [
            directory,
            old_text,
            new_text,
            '--force',
            '--whole-words-only',
            #'--verbose',
            ]
        command.extend(without_dirs)
        ReplaceInFilesScript()(command)
        print('')

    ### PUBLIC METHODS ###

    def process_args(self, args):
        r'''Processes `args`.

        Returns none.
        '''
        systemtools.IOManager.clear_terminal()
        # Handle source path:
        old_codebase, old_tools_package_name, old_module_name = \
            self._parse_tools_package_path(args.source)
        old_codebase_tools_path = self._codebase_name_to_codebase_tools_path(
            old_codebase)
        old_module_path = os.path.join(
            old_codebase_tools_path,
            old_tools_package_name,
            old_module_name + '.py',
            )
        if not os.path.exists(old_module_path):
            message = 'source does not exist: {}'
            message = message.format(old_module_path)
            raise SystemExit(message)
        # Handle destination path:
        new_codebase, new_tools_package_name, new_module_name = \
            self._parse_tools_package_path(args.destination)
        new_codebase_tools_path = self._codebase_name_to_codebase_tools_path(
            new_codebase)
        new_module_path = os.path.join(
            new_codebase_tools_path,
            new_tools_package_name,
            new_module_name + '.py',
            )
        if os.path.exists(new_module_path):
            message = 'destination already exists: {}'
            message = message.format(old_module_path)
            raise SystemExit(message)
        # Process changes:
        new_args = (
            old_codebase, old_tools_package_name, old_module_name,
            new_codebase, new_tools_package_name, new_module_name,
            )
        if not self._confirm_name_changes(*new_args):
            raise SystemExit
        self._rename_old_test_files(*new_args)
        self._rename_old_api_page(*new_args)
        self._rename_old_module(*new_args)
        self._update_codebase(*new_args)
        raise SystemExit

    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''
        parser.add_argument(
            'source',
            help='toolspackage path of source module',
            )
        parser.add_argument(
            'destination',
            help='toolspackage path of destination module',
            )