def import_structured_package(path, namespace, package_root_name='abjad'):
    r'''.. versionadded:: 2.9

    Import public names from `path` into `namespace`.

    This is the custom function that all Abjad packages use to import 
    public classes and functions on startup.

    The function will work for any package laid out like Abjad packages.

    Set `package_root_name` to the root any Abjad-like package structure.
    
    Return none.
    '''
    from abjad.tools.importtools._import_public_names_from_path_into_namespace import \
        _import_public_names_from_path_into_namespace

    _import_public_names_from_path_into_namespace(path, namespace, package_root_name)
