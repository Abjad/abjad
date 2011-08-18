from abjad.tools.importtools._get_public_names_in_module import _get_public_names_in_module
import os


def _import_contents_of_public_packages_in_path_into_namespace(
    path, namespace, package_root_name = 'abjad'):
    r'''Inspect the top level of path.

    Find public class packages and import class package contents into namespace.

    Do not inspect lower levels of path.
    '''

    parent_path = path[path.rindex(package_root_name):]
    parent_package = parent_path.replace(os.sep, '.')

    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path, name)):
            if name[0].isupper():
                class_package = '.'.join([parent_package, name])
                class_module = '.'.join([class_package, name])
                public_names = _get_public_names_in_module(class_module)
                for public_name in public_names:
                    namespace[public_name.__name__] = public_name

    try:
        del(namespace['_import_contents_of_public_packages_in_path_into_namespace'])
    except KeyError:
        pass
