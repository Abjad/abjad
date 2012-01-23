from abjad.tools.importtools._get_public_names_in_module import _get_public_names_in_module
from abjad.tools.importtools._import_contents_of_public_packages_in_path_into_namespace import _import_contents_of_public_packages_in_path_into_namespace
import os


def _import_public_names_from_path_into_namespace(path, namespace, package_root_name = 'abjad'):
    r'''Inspect the top level of path.

    Find .py modules in path and import public functions from .py modules into namespace.

    Find packages in path and import package names into namespace.

    Do not import package content into namespace.

    Do not inspect lower levels of path.
    '''

    module = path[path.rindex(package_root_name):]
    module = module.replace(os.sep, '.')

    for element in os.listdir(path):
        if os.path.isfile(os.path.join(path, element)):
            if not element.startswith('_') and element.endswith('.py'):
                # import function inside module
                submod = os.path.join(module, element[:-3])
                functions = _get_public_names_in_module(submod)
                for f in functions:
                    #namespace[f.__name__] = f
                    # handle public function decorated with @require
                    if f.__name__ == 'wrapper':
                        name = f.func_closure[1].cell_contents.__name__
                    else:
                        name = f.__name__
                    namespace[name] = f
        elif os.path.isdir(os.path.join(path, element)):
            if not element in ('.svn', 'test', '__pycache__'):
                #exec('from %s import %s' % (module, element))
                submod = '.'.join([module, element])
                namespace[element] = __import__(submod, fromlist =['*'])
        else:
            raise ImportError('Not a dir, not a file, what is %s?' % element)

    _import_contents_of_public_packages_in_path_into_namespace(path, namespace, package_root_name)

    try:
        del(namespace['_import_public_names_from_path_into_namespace'])
    except KeyError:
        pass
