# -*- encoding: utf-8 -*-
import os
import types


class ImportManager(object):
    r'''Imports structured packages.
    '''

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_public_function_names_in_module(module_file):
        r'''Collects and returns all public functions defined in module_file.'''
        result = []
        module_file = module_file.replace(os.sep, '.')
        mod = __import__(module_file, fromlist=['*'])
        for key, value in vars(mod).items():
            if not key.startswith('_'):
                # handle public function decorated with @require
                if getattr(value, 'func_closure', None):
                    module_name = getattr(value.func_closure[1].cell_contents, 
                        '__module__', None)
                # handle plain old function
                else:
                    module_name = getattr(value, '__module__', None)
                if module_name == module_file:
                    result.append(value)
        return result

    @staticmethod
    def _import_contents_of_public_packages_in_path_into_namespace(
        path, namespace, package_root_name = 'abjad'):
        r'''Inspect the top level of path.

        Find public class packages and import class package contents into namespace.

        Do not inspect lower levels of path.
        '''

        parent_path = path[path.rindex(package_root_name):]
        parent_package = parent_path.replace(os.sep, '.')

        for name in os.listdir(path):
            fullname = os.path.join(path, name)
            if os.path.isdir(fullname):
                if name[0].isupper() and \
                    os.path.exists(os.path.join(fullname, '__init__.py')) and \
                    os.path.exists(os.path.join(fullname, '%s.py' % name)):
                    class_package = '.'.join([parent_package, name])
                    class_module = '.'.join([class_package, name])
                    public_names = ImportManager._get_public_function_names_in_module(
                        class_module)
                    for public_name in public_names:
                        namespace[public_name.__name__] = public_name

    ### PUBLIC METHODS ###

    @staticmethod
    def import_public_names_from_filesystem_path_into_namespace(
        path, namespace, package_root_name='abjad'):
        r'''Inspect the top level of `path`.

        Find .py modules in path and import public functions from .py modules 
        into namespace.

        Find packages in path and import package names into namespace.

        Do not import package content into namespace.

        Do not inspect lower levels of path.
        '''

        package_root_name += os.sep
        module = path[path.rindex(package_root_name):]
        module = module.replace(os.sep, '.')

        for element in os.listdir(path):
            if os.path.isfile(os.path.join(path, element)):
                if not element.startswith('_') and element.endswith('.py'):
                    # import function inside module
                    submod = os.path.join(module, element[:-3])
                    functions = ImportManager._get_public_function_names_in_module(
                        submod)
                    for f in functions:
                        # handle public function decorated with @require
                        if f.__name__ == 'wrapper':
                            name = f.func_closure[1].cell_contents.__name__
                        else:
                            name = f.__name__
                        namespace[name] = f
            elif os.path.isdir(os.path.join(path, element)):
                if not element in ('.svn', 'test', '__pycache__'):
                    if os.path.exists(os.path.join(path, element, '__init__.py')):
                        submod = '.'.join([module, element])
                        namespace[element] = __import__(submod, fromlist=['*'])
            else:
                raise ImportError('Not a dir, not a file, what is %s?' % element)

        ImportManager._import_contents_of_public_packages_in_path_into_namespace(
            path, namespace, package_root_name)

        if 'importtools' in namespace:
            del(namespace['importtools'])
        if ImportManager.__name__ in namespace:
            del(namespace[ImportManager.__name__])

    @staticmethod
    def import_structured_package(
        path, 
        namespace, 
        package_root_name='abjad'):
        r'''Import public names from `path` into `namespace`.

        This is the custom function that all Abjad packages use to import
        public classes and functions on startup.

        The function will work for any package laid out like Abjad packages.

        Set `package_root_name` to the root any Abjad-like package structure.

        Return none.
        '''
        ImportManager.import_public_names_from_filesystem_path_into_namespace(
            path, namespace, package_root_name)
        if 'importtools' in namespace:
            del(namespace['importtools'])
        if ImportManager.__name__ in namespace:
            del(namespace[ImportManager.__name__])
