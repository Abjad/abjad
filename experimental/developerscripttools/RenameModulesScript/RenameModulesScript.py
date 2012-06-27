from abc import abstractmethod
from abjad.cfg.cfg import ABJADPATH, ROOTPATH
from abjad.tools import documentationtools
from abjad.tools import iotools
from experimental.developerscripttools.DeveloperScript import DeveloperScript
from experimental.developerscripttools.ReplaceInFilesScript import ReplaceInFilesScript
import os


class RenameModulesScript(DeveloperScript):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'rename'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return None

    @property
    def short_description(self):
        return 'Rename public modules.'

    @property
    def version(self):
        return 1.0

    ### PRIVATE METHODS ###

    def _confirm_name_changes(self, kind, old_package_name, old_object_name, new_package_name, new_object_name):
        print ''
        print 'Is ...'
        print ''
        print '    {}.{}()'.format(old_package_name, old_object_name)
        print '    ===>'
        print '    {}.{}()'.format(new_package_name, new_object_name)
        print ''
        input = raw_input('... correct [Y(es)/n(o)]? ').lower()
        print ''
        if input in ('y', 'yes'):
            return
        else:
            raise SystemExit

    def _get_object_names(self, kind, tools_package_name):
        assert kind in ('class', 'function')
        path = os.path.join(ABJADPATH, 'tools', tools_package_name)
        if kind == 'class':
            crawler = documentationtools.ClassCrawler(path, include_private_objects=True)
        elif kind == 'function':
            crawler = documentationtools.FunctionCrawler(path, include_private_objects=True)
        objs = crawler()
        return tuple(sorted([x.__name__ for x in objs]))

    def _get_tools_package_names(self):
        tools_path = os.path.join(ABJADPATH, 'tools')
        names = []
        for x in os.listdir(tools_path):
            if os.path.isdir(os.path.join(ABJADPATH, 'tools', x)):
                if not x.startswith(('_', '.')):
                    names.append(x)
        return tuple(sorted(names))

    def _prompt_for_old_name(self, kind):
        assert kind in ('class', 'function')
        while True:
            message = 'Enter current tools package-qualified {} name: '.format(kind)
            qualified_object_name = raw_input(message)
            if qualified_object_name.count('.') != 1:
                print ''
                print 'Input not in toolspackage.{} format: {!r}'.format(kind, qualified_object_name)
                print ''
                continue
            qualified_object_name_parts = qualified_object_name.split('.')
            old_package_name = qualified_object_name_parts[0].lower()
            old_object_name = qualified_object_name_parts[1]
            if old_package_name not in self._get_tools_package_names():
                print ''
                print 'Error: can not find {!r} in Abjad tools.'.format(old_package_name)
                print ''
                continue
            print self._get_object_names(kind, old_package_name)
            if old_object_name not in self._get_object_names(kind, old_package_name):
                print ''
                print 'Error: can not find {!r} in {!r}.'.format(old_object_name, old_package_name)
                print ''
                continue
            return old_package_name, old_object_name

    def _prompt_for_new_name(self, kind):
        assert kind in ('class', 'function')
        while True:
            message = 'Enter new tools package-qualified {} name:     '.format(kind)
            qualified_object_name = raw_input(message)
            if qualified_object_name.count('.') != 1:
                print ''
                print 'Input not in toolspackage.{} format: {!r}'.format(kind, qualified_object_name)
                print ''
                continue
            qualified_object_name_parts = qualified_object_name.split('.')
            new_package_name = qualified_object_name_parts[0].lower()
            new_object_name = qualified_object_name_parts[1]
            if new_package_name not in self._get_tools_package_names():
                print ''
                print 'Error: can not find {!r} in Abjad packages.'.format(new_package_name)
                print ''
                continue
            if new_object_name in self._get_object_names(kind, new_package_name):
                print ''
                print 'Error: the {} {!r} already exists in {!r}.'.format(kind, new_object_name, new_package_name)
                print ''
                continue
            return new_package_name, new_object_name

    def _rename_old_api_page(self, kind, old_package_name, old_object_name, new_package_name, new_object_name):
        print 'Renaming old API page ...'

        api_path = os.path.join(ABJADPATH, 'docs', 'chapters', 'api')
        api_path = os.path.join(api_path, 'tools')

        old_rst_file_name = old_object_name + '.rst'
        new_rst_file_name = new_object_name + '.rst'

        if kind == 'function':
            old_api_path = os.path.join(api_path, old_package_name, old_rst_file_name)
            new_api_path = os.path.join(api_path, new_package_name, new_rst_file_name)
            command = 'svn --force mv {} {} > /dev/null'.format(old_api_path, new_api_path)
            iotools.spawn_subprocess(command)

        elif kind == 'class':
            # move the folder...
            old_api_path = os.path.join(api_path, old_package_name, old_object_name)
            new_api_path = os.path.join(api_path, new_package_name, new_object_name)
            command = 'svn --force mv {} {} > /dev/null'.format(old_api_path, new_api_path)
            iotools.spawn_subprocess(command)

            # ...then the file
            old_rst_file_name = os.path.join(new_api_path, old_rst_file_name)
            new_rst_file_name = os.path.join(new_api_path, new_rst_file_name)
            command = 'svn --force mv {} {} > /dev/null'.format(old_rst_file_name, new_rst_file_name)
            iotools.spawn_subprocess(command)

        print ''

    def _rename_old_module(self, kind, old_package, old_object_name, new_package, new_object_name):
        print 'Renaming old module ...'

        if kind == 'function':
            old_module = old_object_name + '.py'
            old_path = os.path.join(ABJADPATH, 'tools', old_package, old_module)
            new_module = new_object_name + '.py'
            new_path = os.path.join(ABJADPATH, 'tools', new_package, new_module)
            command = 'svn --force mv {} {} > /dev/null'.format(old_path, new_path)
            iotools.spawn_subprocess(command)

        elif kind == 'class':
            old_class_package = os.path.join(ABJADPATH, 'tools', old_package, old_object_name)
            new_class_package = os.path.join(ABJADPATH, 'tools', new_package, new_object_name)
            old_class_module = os.path.join(new_class_package, '{}.py'.format(old_object_name))
            new_class_module = os.path.join(new_class_package, '{}.py'.format(new_object_name))

            # move the folder...
            command = 'svn --force mv {} {} > /dev/null'.format(old_class_package, new_class_package)
            iotools.spawn_subprocess(command)

            # ...then the file
            command = 'svn --force mv {} {} > /dev/null'.format(old_class_module, new_class_module)
            iotools.spawn_subprocess(command)

        print ''

    def _rename_old_test_files(self, kind, old_package_name, old_object_name, new_package_name, new_object_name):
        print 'Renaming old test file(s) ...'

        if kind == 'function':
            old_test_file = 'test_{}_{}.py'.format(old_package, old_object_name)
            old_path = os.path.join(ABJADPATH, 'tools', old_package, 'test')
            old_path = os.path.join(old_path, old_test_file)
            new_test_file = 'test_{}_{}.py'.format(new_package, new_object_name)
            new_path = os.path.join(ABJADPATH, 'tools', new_package, 'test')
            new_path = os.path.join(new_path, new_test_file)
            command = 'svn --force mv {} {} > /dev/null'.format(old_path, new_path)
            iotools.spawn_subprocess(command)

        elif kind == 'class':
            test_path = os.path.join(ABJADPATH, 'tools', new_package_name, new_object_name, 'test')
            print test_path
            for x in os.listdir(test_path):
                if x.startswith('test_') and x.endswith('.py'):
                    old_path = os.path.join(test_path, x)

                    new_path = os.path.join(test_path,
                        x.replace('test_{}'.format(old_object_name), 'test_{}'.format(new_object_name)))

                    command = 'svn --force mv {} {} > /dev/null'.format(old_path, new_path)

                    print '\t{}'.format(old_path)
                    print '\t{}'.format(new_path)

                    iotools.spawn_subprocess(command)

        print ''

    def _update_codebase(self, kind, old_package_name, old_object_name, new_package_name, new_object_name):
        print 'Updating codebase ...'
        directory = ROOTPATH

        old_text = '{}.{}'.format(old_package_name, old_object_name)
        new_text = '{}.{}'.format(new_package_name, new_object_name)
        command = [directory, old_text, new_text, '--force', '--whole-words-only']
        ReplaceInFilesScript()(command)

        if kind == 'function':
            old_text = 'test_{}_{}_'.format(old_package_name, old_object_name)
            new_text = 'test_{}_{}_'.format(new_package_name, new_object_name)
        elif kind == 'class':
            old_text = 'test_{}_'.format(old_object_name)
            new_text = 'test_{}_'.format(new_object_name)
        command = [directory, old_text, new_text, '--force']
        ReplaceInFilesScript()(command)

        old_text = old_object_name
        new_text = new_object_name
        command = [directory, old_text, new_text, '--force', '--whole-words-only']
        ReplaceInFilesScript()(command)

        print ''

    ### PUBLIC METHODS ###

    def process_args(self, args):
        iotools.clear_terminal()

        kind = args.kind
        old_package_name, old_object_name = self._prompt_for_old_name(kind)
        new_package_name, new_object_name = self._prompt_for_new_name(kind)

        args = (kind, old_package_name, old_object_name, new_package_name, new_object_name)

        self._confirm_name_changes(*args)
        self._rename_old_module(*args)
        self._rename_old_test_files(*args)
        self._rename_old_api_page(*args)
        self._update_codebase(*args)

    def setup_argument_parser(self, parser):

        kind_group = parser.add_mutually_exclusive_group()

        kind_group.add_argument('-C', '--classes',
            action='store_const',
            const='class',
            dest='kind',
            help='rename classes',
            )

        kind_group.add_argument('-F', '--functions',
            action='store_const',
            const='function',
            dest='kind',
            help='rename functions',
            )

        parser.set_defaults(kind='function')
