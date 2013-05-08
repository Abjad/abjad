import os


def package_path_to_directory_path(package_path, configuration=None):
    '''Change `package_path` to directory path.
    
    When score manager configuration variables when `configuration` is none.

    Return string.
    '''
    from experimental.tools.scoremanagertools import core

    configuration = configuration or core.ScoreManagerConfiguration()
    
    if package_path is None:
        return
    package_path_parts = package_path.split('.')
    if package_path_parts[0] == \
        configuration.score_manager_tools_package_name:
        directory_parts = [configuration.score_manager_tools_directory_path] + \
            package_path_parts[1:]
    elif package_path_parts[0] == \
        configuration.system_materials_package_path:
        directory_parts = \
            [configuration.system_materials_directory_path] + \
            package_path_parts[1:]
    elif package_path_parts[0] == \
        configuration.user_sketches_package_path:
        directory_parts = \
            [configuration.user_sketches_directory_path] + \
            package_path_parts[1:]
    elif package_path_parts[0] == \
        configuration.system_specifiers_package_path:
        directory_parts = \
            [configuration.system_specifiers_directory_path] + \
            package_path_parts[1:]
    else:
        directory_parts = [configuration.user_scores_directory_path] + package_path_parts[:]
    directory_path = os.path.join(*directory_parts)
    return directory_path
