def module_path_to_file_path(module_path, configuration):
    '''Change `module_path` to file path.

    Return none when `module_path` is none.

    Return string.
    '''
    from experimental.tools import packagepathtools

    if module_path is not None:
        file_path = packagepathtools.package_path_to_directory_path(module_path, configuration)
        file_path += '.py'
        return file_path
