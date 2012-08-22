from abjad.tools import documentationtools
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript
import os


class MakeNewClassTemplateScript(DeveloperScript):
    '''Create class stubs, complete with test subdirectory:

    ::

        bash$ ajv new class -h
        usage: make-new-class-template [-h] [--version] (-X | -M) name

        Make a new class template file.

        positional arguments:
          name                tools package qualified class name

        optional arguments:
          -h, --help          show this help message and exit
          --version           show program's version number and exit
          -X, --abjad.tools  use the Abjad abjad.tools path
          -M, --mainline      use the Abjad mainline tools path

    Return `MakeNewClassTemplateScript` instance.
    '''

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def alias(self):
        return 'class'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'new'

    @property
    def short_description(self):
        return 'Make a new class template file.'

    @property
    def version(self):
        return 1.0

    ### PRIVATE METHODS ###

    def _get___init___text(self, package_root_name):
        return [
            'from abjad.tools import importtools',
            '',
            "importtools.import_structured_package(__path__[0], globals(), package_root_name={!r})".format(package_root_name),
        ]

    def _get_class_text(self, class_name):
        return [
            'from abjad.tools import abctools',
            '',
            '',
            'class {}(abctools.AbjadObject):'.format(class_name),
            '    pass'
        ]

    def _get_class_names_in_tools_package(self, root, tools_package_name):
        path = os.path.join(root, tools_package_name)
        crawler = documentationtools.ClassCrawler(path, include_private_objects=True)
        objs = crawler()
        return tuple(sorted([x.__name__ for x in objs]))

    def _get_tools_package_names(self, root):
        names = []
        for x in os.listdir(root):
            if os.path.isdir(os.path.join(root, x)):
                if not x.startswith(('_', '.')):
                    names.append(x)
        return tuple(sorted(names))

    ### PUBLIC METHODS ###

    def process_args(self, args):

        if args.name.count('.') != 1:
            print 'Error: {!r} not in tools_package.class_name format.'.format(args.name)
            return

        root = args.path
        tools_package_name, class_name = args.name.split('.')

        if tools_package_name not in self._get_tools_package_names(root):
            print 'Error: {!r} is not a valid tools package.'.format(tools_package_name)
            return

        if class_name in self._get_class_names_in_tools_package(root, tools_package_name):
            print 'Error: {!r} already exists in {!r}'.format(class_name, tools_package_name)
            return

        package_path = os.path.join(root, tools_package_name, class_name)

        os.mkdir(package_path)
        os.mkdir(os.path.join(package_path, 'test'))

        if args.path.endswith('experimental'):
            package_root_name = 'experimental'
        else:
            package_root_name = 'abjad'

        module_path = os.path.join(package_path, '{}.py'.format(class_name))
        module_text = '\n'.join(self._get_class_text(class_name)) + '\n'

        init_path = os.path.join(package_path, '__init__.py')
        init_text = '\n'.join(self._get___init___text(package_root_name)) + '\n'
        
        with open(module_path, 'w') as f:
            f.write(module_text)

        with open(init_path, 'w') as f:
            f.write(init_text)

    def setup_argument_parser(self, parser):

        from abjad import ABJCFG

        parser.add_argument('name',
            help='tools package qualified class name'
            )

        path_group = parser.add_mutually_exclusive_group(required=True)

        path_group.add_argument('-X', '--experimental',
            action='store_const',
            const=ABJCFG.ABJAD_EXPERIMENTAL_PATH,
            dest='path',
            help='use the Abjad abjad.tools path',
            )

        path_group.add_argument('-M', '--mainline',
            action='store_const',
            const=os.path.join(ABJCFG.ABJAD_PATH, 'tools'),
            dest='path',
            help='use the Abjad mainline tools path',
            )
