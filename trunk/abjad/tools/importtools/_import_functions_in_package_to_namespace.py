from abjad.tools.importtools._get_public_names_in_module import _get_public_names_in_module
from abjad.tools.importtools._remove_modules_from_namespace import _remove_modules_from_namespace
import os


def _import_functions_in_package_to_namespace(package, namespace, skip_dirs=['test', '.svn']):
    '''Import all the functions defined in the modules of the package given
        as a string path into the given namespace.

        Example:

        A package structure like so:
            package.mod1.mod1_func1()
            package.mod2.mod2_func1()
            package.mod2.mod2_func2()
            package.mod3.mod3_func1()
        Ends up as
            package.mod1_func1()
            package.mod2_func1()
            package.mod2_func2()
            package.mod3_func1()
    '''

    functions = []
    for root, dirs, files in os.walk(package):
        root = root[root.rindex('abjad'):]

        # remove directories of modules to skip
        for mod in skip_dirs:
            if mod in dirs:
                dirs.remove(mod)

        # get functions from module files
        for file in files:
            if file.endswith('py') and not file.startswith(('_', '.')):
                module = os.path.join(root, file[:-3])
                functions.extend(_get_public_names_in_module(module))

    # put functions retrieved into namespace
    for func in functions:
        namespace[func.__name__] = func

    # remove modules
    _remove_modules_from_namespace(namespace)

    # remove myself
    try:
        del(namespace['_import_functions_in_package_to_namespace'])
    # if we were importing into __builtins__, myself will raise KeyError
    except KeyError:
        pass
