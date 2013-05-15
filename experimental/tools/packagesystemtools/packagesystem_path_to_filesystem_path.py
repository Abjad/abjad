import os


def packagesystem_path_to_filesystem_path(package_path, is_module=False):
    '''Change `package_path` to directory path.
    
    When score manager configuration variables when `configuration` is none.

    Return string.
    '''
    from experimental.tools import scoremanagertools

    configuration = scoremanagertools.core.ScoreManagerConfiguration()
    
    if package_path is None:
        return
    package_path_parts = package_path.split('.')
    if package_path_parts[0] == 'scoremanagertools':
        directory_parts = [configuration.score_manager_tools_directory_path] + \
            package_path_parts[1:]
    elif package_path_parts[:3] == ['experimental', 'tools', 'scoremanagertools']:
        directory_parts = [configuration.score_manager_tools_directory_path] + \
            package_path_parts[3:]
    elif package_path_parts[0] == \
        configuration.built_in_materials_package_path:
        directory_parts = \
            [configuration.built_in_materials_directory_path] + \
            package_path_parts[1:]
    elif package_path_parts[0] == \
        configuration.user_sketches_package_path:
        directory_parts = \
            [configuration.user_sketches_directory_path] + \
            package_path_parts[1:]
    elif package_path_parts[0] == \
        configuration.built_in_specifiers_package_path:
        directory_parts = \
            [configuration.built_in_specifiers_directory_path] + \
            package_path_parts[1:]
    else:
        directory_parts = [configuration.user_scores_directory_path] + package_path_parts[:]
    directory_path = os.path.join(*directory_parts)
    
    if is_module:
        directory_path += '.py'

    return directory_path
