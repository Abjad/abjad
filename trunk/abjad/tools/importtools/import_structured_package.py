# -*- encoding: utf-8 -*-
def import_structured_package(path, namespace, package_root_name='abjad'):
    r'''Import public names from `path` into `namespace`.

    This is the custom function that all Abjad packages use to import
    public classes and functions on startup.

    The function will work for any package laid out like Abjad packages.

    Set `package_root_name` to the root any Abjad-like package structure.

    Return none.
    '''
    from abjad.tools.importtools.import_public_names_from_filesystem_path_into_namespace import \
        import_public_names_from_filesystem_path_into_namespace

    import_public_names_from_filesystem_path_into_namespace(path, namespace, package_root_name)

    if 'importtools' in namespace:
        del(namespace['importtools'])
