import abc
from abjad.tools import documentationtools
from abjad.tools import iotools
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript
from abjad.tools.developerscripttools.ReplaceInFilesScript import ReplaceInFilesScript
import os


class RenameModulesScript(DeveloperScript):
    '''Rename classes and functions.

    Handle renaming the module and package, as well as any tests, documentation or
    mentions of the class throughout the Abjad codebase:

    ::

        $ ajv rename -h
        usage: rename-modules [-h] [--version] (-C | -F)

        Rename public modules.

        optional arguments:
          -h, --help       show this help message and exit
          --version        show program's version number and exit
          -C, --classes    rename classes
          -F, --functions  rename functions

    Return `RenameModulesScript` instance.
    '''

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

    def _codebase_name_to_codebase_docs_path(self, codebase):
        from abjad import ABJCFG
        if codebase == 'mainline':
            return os.path.join(ABJCFG.ABJAD_PATH, 'docs', 'source', 'api', 'tools')
        elif codebase == 'experimental':
            return os.path.join(ABJCFG.ABJAD_EXPERIMENTAL_PATH, 'docs', 'source', 'experimental')
        raise Exception('Bad codebase name {!r}.'.format(codebase))

    def _codebase_name_to_codebase_tools_path(self, codebase):
        from abjad import ABJCFG
        if codebase == 'mainline':
            return os.path.join(ABJCFG.ABJAD_PATH, 'tools')
        elif codebase == 'experimental':
            return ABJCFG.ABJAD_EXPERIMENTAL_PATH
        raise Exception('Bad codebase name {!r}.'.format(codebase))

    def _confirm_name_changes(self, kind, old_codebase, old_package_name, old_object_name,
        new_codebase, new_package_name, new_object_name):

        max_codebase = max(len(old_codebase), len(new_codebase))
        old_codebase = old_codebase.ljust(max_codebase)
        new_codebase = new_codebase.ljust(max_codebase)

        print ''
        print 'Is ...'
        print ''
        print '    [{}] {}.{}()'.format(old_codebase, old_package_name, old_object_name)
        print '    ===>'
        print '    [{}] {}.{}()'.format(new_codebase, new_package_name, new_object_name)
        print ''
        input = raw_input('... correct [Y(es)/n(o)]? ').lower()
        print ''
        if input in ('y', 'yes'):
            return
        else:
            raise SystemExit

    def _get_object_names(self, kind, codebase, tools_package_name):
        assert kind in ('class', 'function')
        tools_path = self._codebase_name_to_codebase_tools_path(codebase)
        path = os.path.join(tools_path, tools_package_name)
        if kind == 'class':
            crawler = documentationtools.ClassCrawler(path, include_private_objects=True)
        elif kind == 'function':
            crawler = documentationtools.FunctionCrawler(path, include_private_objects=True)
        objs = crawler()
        return tuple(sorted([x.__name__ for x in objs]))

    def _get_tools_package_names(self, codebase):
        tools_path = self._codebase_name_to_codebase_tools_path(codebase)
        names = []
        for x in os.listdir(tools_path):
            if os.path.isdir(os.path.join(tools_path, x)):
                if not x.startswith(('_', '.')):
                    names.append(x)
        return tuple(sorted(names))

    def _prompt_for_new_name(self, kind):

        assert kind in ('class', 'function')

        while True:
            message = 'Select codebase ([m]ainline, e[x]perimental):     '
            if kind == 'function':
                message += '   '
            codebase = raw_input(message).lower()
            if codebase in ('mainline', 'experimental'):
                break
            elif codebase == 'm':
                codebase = 'mainline'
                break
            elif codebase == 'x':
                codebase = 'experimental'
                break
            print ''
            print 'Error: invalid codebase selection {!r}.'.format(codebase)
            print ''

        while True:
            message = 'Enter new tools package-qualified {} name:     '.format(kind)
            qualified_object_name = raw_input(message)
            if qualified_object_name.count('.') != 1:
                print ''
                print 'Input not in toolspackage.{} format: {!r}'.format(kind, qualified_object_name)
                print ''
                continue
            qualified_object_name_parts = qualified_object_name.split('.')
            package_name = qualified_object_name_parts[0].lower()
            object_name = qualified_object_name_parts[1]
            if package_name not in self._get_tools_package_names(codebase):
                print ''
                print 'Error: can not find {!r} in {!r} tools packages.'.format(package_name, codebase)
                print ''
                continue
            if object_name in self._get_object_names(kind, codebase, package_name):
                print ''
                print 'Error: the {} {!r} already exists in {!r}.'.format(kind, object_name, package_name)
                print ''
                continue
            return codebase, package_name, object_name

    def _prompt_for_old_name(self, kind):

        assert kind in ('class', 'function')

        while True:
            message = 'Select codebase ([m]ainline, e[x]perimental):     '
            if kind == 'function':
                message += '   '
            codebase = raw_input(message).lower()
            if codebase in ('mainline', 'experimental'):
                break
            elif codebase == 'm':
                codebase = 'mainline'
                break
            elif codebase == 'x':
                codebase = 'experimental'
                break
            print ''
            print 'Error: invalid codebase selection {!r}.'.format(codebase)
            print ''

        while True:
            message = 'Enter current tools package-qualified {} name: '.format(kind)
            qualified_object_name = raw_input(message)
            if qualified_object_name.count('.') != 1:
                print ''
                print 'Input not in toolspackage.{} format: {!r}'.format(kind, qualified_object_name)
                print ''
                continue
            qualified_object_name_parts = qualified_object_name.split('.')
            package_name = qualified_object_name_parts[0].lower()
            object_name = qualified_object_name_parts[1]
            if package_name not in self._get_tools_package_names(codebase):
                print ''
                print 'Error: can not find {!r} in {!r} tools packages.'.format(package_name, codebase)
                print ''
                continue
            if object_name not in self._get_object_names(kind, codebase, package_name):
                print ''
                print 'Error: can not find {!r} in {!r}.'.format(object_name, package_name)
                print ''
                continue
            return codebase, package_name, object_name

    def _rename_old_api_page(self, kind, old_codebase, old_package_name, old_object_name,
        new_codebase, new_package_name, new_object_name):

        print 'Renaming old API page ...'

        old_docs_path = self._codebase_name_to_codebase_docs_path(old_codebase)
        new_docs_path = self._codebase_name_to_codebase_docs_path(new_codebase)

        old_rst_file_name = old_object_name + '.rst'
        new_rst_file_name = new_object_name + '.rst'

        if kind == 'function':
            old_api_path = os.path.join(old_docs_path, old_package_name, old_rst_file_name)
            new_api_path = os.path.join(new_docs_path, new_package_name, new_rst_file_name)
            command = 'svn --force mv {} {} > /dev/null'.format(old_api_path, new_api_path)
            iotools.spawn_subprocess(command)

        elif kind == 'class':
            # move the folder...
            old_api_path = os.path.join(old_docs_path, old_package_name, old_object_name)
            new_api_path = os.path.join(new_docs_path, new_package_name, new_object_name)
            command = 'svn --force mv {} {} > /dev/null'.format(old_api_path, new_api_path)
            iotools.spawn_subprocess(command)

            # ...then the file
            old_rst_file_name = os.path.join(new_api_path, old_rst_file_name)
            new_rst_file_name = os.path.join(new_api_path, new_rst_file_name)
            command = 'svn --force mv {} {} > /dev/null'.format(old_rst_file_name, new_rst_file_name)
            iotools.spawn_subprocess(command)

        print ''

    def _rename_old_module(self, kind, old_codebase, old_package_name, old_object_name,
        new_codebase, new_package_name, new_object_name):

        print 'Renaming old module ...'

        old_tools_path = self._codebase_name_to_codebase_tools_path(old_codebase)
        new_tools_path = self._codebase_name_to_codebase_tools_path(new_codebase)

        if kind == 'function':
            old_module = old_object_name + '.py'
            old_path = os.path.join(old_tools_path, old_package_name, old_module)
            new_module = new_object_name + '.py'
            new_path = os.path.join(new_tools_path, new_package_name, new_module)
            command = 'svn --force mv {} {} > /dev/null'.format(old_path, new_path)
            iotools.spawn_subprocess(command)

        elif kind == 'class':
            # move the folder...
            old_class_package = os.path.join(old_tools_path, old_package_name, old_object_name)
            new_class_package = os.path.join(new_tools_path, new_package_name, new_object_name)
            command = 'svn --force mv {} {} > /dev/null'.format(old_class_package, new_class_package)
            iotools.spawn_subprocess(command)

            # ...then the file
            old_class_module = os.path.join(new_class_package, '{}.py'.format(old_object_name))
            new_class_module = os.path.join(new_class_package, '{}.py'.format(new_object_name))
            command = 'svn --force mv {} {} > /dev/null'.format(old_class_module, new_class_module)
            iotools.spawn_subprocess(command)

        print ''

    def _rename_old_test_files(self, kind, old_codebase, old_package_name, old_object_name,
        new_codebase, new_package_name, new_object_name):

        print 'Renaming old test file(s) ...'

        old_tools_path = self._codebase_name_to_codebase_tools_path(old_codebase)
        new_tools_path = self._codebase_name_to_codebase_tools_path(new_codebase)

        if kind == 'function':
            old_test_file = 'test_{}_{}.py'.format(old_package_name, old_object_name)
            old_path = os.path.join(old_tools_path, old_package_name, 'test')
            old_path = os.path.join(old_path, old_test_file)
            new_test_file = 'test_{}_{}.py'.format(new_package_name, new_object_name)
            new_path = os.path.join(new_tools_path, new_package_name, 'test')
            new_path = os.path.join(new_path, new_test_file)
            command = 'svn --force mv {} {} > /dev/null'.format(old_path, new_path)
            iotools.spawn_subprocess(command)

        elif kind == 'class':
            test_path = os.path.join(new_tools_path, new_package_name, new_object_name, 'test')
            for x in os.listdir(test_path):
                if x.startswith('test_') and x.endswith('.py'):
                    old_path = os.path.join(test_path, x)
                    new_path = os.path.join(test_path,
                        x.replace('test_{}'.format(old_object_name), 'test_{}'.format(new_object_name)))
                    command = 'svn --force mv {} {} > /dev/null'.format(old_path, new_path)
                    iotools.spawn_subprocess(command)

        print ''

    def _update_codebase(self, kind, old_codebase, old_package_name, old_object_name,
        new_codebase, new_package_name, new_object_name):

        from abjad import ABJCFG
        without_dirs = ['--without-dirs', 'build', '--without-dirs', '_build']

        directory = ABJCFG.ABJAD_ROOT_PATH

        print 'Updating codebase ...'
        print ''

        old_text = '{}.{}'.format(old_package_name, old_object_name)
        new_text = '{}.{}'.format(new_package_name, new_object_name)
        command = [directory, old_text, new_text, '--force', '--whole-words-only', '--verbose']
        command.extend(without_dirs)
        ReplaceInFilesScript()(command)

        print ''

        if kind == 'function':
            old_text = 'test_{}_{}_'.format(old_package_name, old_object_name)
            new_text = 'test_{}_{}_'.format(new_package_name, new_object_name)
        elif kind == 'class':
            old_text = 'test_{}_'.format(old_object_name)
            new_text = 'test_{}_'.format(new_object_name)
        command = [directory, old_text, new_text, '--force', '--verbose']
        command.extend(without_dirs)
        ReplaceInFilesScript()(command)

        print ''

        old_text = old_object_name
        new_text = new_object_name
        command = [directory, old_text, new_text, '--force', '--whole-words-only', '--verbose']
        command.extend(without_dirs)
        ReplaceInFilesScript()(command)

        print ''

    ### PUBLIC METHODS ###

    def process_args(self, args):
        iotools.clear_terminal()

        # print args

        kind = args.kind
        old_codebase, old_package_name, old_object_name = self._prompt_for_old_name(kind)
        new_codebase, new_package_name, new_object_name = self._prompt_for_new_name(kind)

        args = (kind, old_codebase, old_package_name, old_object_name,
            new_codebase, new_package_name, new_object_name)

        self._confirm_name_changes(*args)

        self._rename_old_module(*args)
        self._rename_old_test_files(*args)
        self._rename_old_api_page(*args)
        self._update_codebase(*args)

    def setup_argument_parser(self, parser):

        kind_group = parser.add_mutually_exclusive_group(required=True)

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

        #path_group = parser.add_mutually_exclusive_group(required=True)

        #path_group.add_argument('-X', '--experimental',
        #    action='store_const',
        #    const='experimental',
        #    dest='path',
        #    help='update Abjad abjad.tools directory',
        #    )

        #path_group.add_argument('-M', '--mainline',
        #    action='store_const',
        #    const='mainline',
        #    dest='path',
        #    help='update Abjad mainline directory',
        #    )

        parser.set_defaults(kind=False)
