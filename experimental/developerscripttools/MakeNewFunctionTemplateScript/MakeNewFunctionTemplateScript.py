from abjad.cfg.cfg import ABJADPATH, EXPERIMENTALPATH
from experimental.developerscripttools.DeveloperScript import DeveloperScript
import os


class MakeNewFunctionTemplateScript(DeveloperScript):

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

        parser.add_argument('name',
            help='tools package qualified function name'
            )

        path_group = parser.add_mutually_exclusive_group(required=True)

        path_group.add_argument('-X', '--experimental',
            action='store_const',
            const=EXPERIMENTALPATH,
            dest='path',
            help='use the Abjad experimental path',
            )

        path_group.add_argument('-M', '--mainline',
            action='store_const',
            const=os.path.join(ABJADPATH, 'tools'),
            dest='path',
            help='use the Abjad mainline tools path',
            )
