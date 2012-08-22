from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript
import os


class MakeNewFunctionTemplateScript(DeveloperScript):
    '''Create function stub files:

    ::

        bash$ ajv new function -h
        usage: make-new-function-template [-h] [--version] (-X | -M) name

        Make a new function template file.

        positional arguments:
          name                tools package qualified function name

        optional arguments:
          -h, --help          show this help message and exit
          --version           show program's version number and exit
          -X, --abjad.tools  use the Abjad abjad.tools path
          -M, --mainline      use the Abjad mainline tools path

    Return `MakeNewFunctionTemplateScript` instance.
    '''

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def alias(self):
        return 'function'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'new'

    @property
    def short_description(self):
        return 'Make a new function template file.'

    @property
    def version(self):
        return 1.0

    ### PRIVATE METHODS ###

    def _get_function_text(self, function_name):
        return [
            'def {}():'.format(function_name),
            '    pass'
        ]

    def _get_function_names_in_tools_package(self, root, tools_package_name):
        path = os.path.join(root, tools_package_name)
        return tuple(sorted([x[:-3] for x in os.listdir(path)
            if x.endswith('.py') and not x.startswith('__')]))

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
            print 'Error: {!r} not in tools_package.function format.'.format(args.name)
            return

        root = args.path
        tools_package_name, function_name = args.name.split('.')

        if tools_package_name not in self._get_tools_package_names(root):
            print 'Error: {!r} is not a valid tools package.'.format(tools_package_name)
            return

        if function_name in self._get_function_names_in_tools_package(root, tools_package_name):
            print 'Error: {!r} already exists in {!r}'.format(function_name, tools_package_name)
            return

        package_path = os.path.join(root, tools_package_name)

        module_path = os.path.join(package_path, '{}.py'.format(function_name))
        module_text = '\n'.join(self._get_function_text(function_name)) + '\n'

        with open(module_path, 'w') as f:
            f.write(module_text)

    def setup_argument_parser(self, parser):

        from abjad import ABJCFG

        parser.add_argument('name',
            help='tools package qualified function name'
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
