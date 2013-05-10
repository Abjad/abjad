import os


def filesystem_path_to_package_path(filesystem_path):
    '''Change `filesystem_path` to package path.

    Return string.
    '''
    from experimental.tools.scoremanagertools import core

    configuration = core.ScoreManagerConfiguration()

    if filesystem_path is None:
        return

    filesystem_path = os.path.normpath(filesystem_path)

    if filesystem_path.endswith('.py'):
        filesystem_path = filesystem_path[:-3]
    if filesystem_path.startswith(configuration.score_manager_tools_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.score_manager_tools_directory_path)) + 1
    elif filesystem_path.startswith(configuration.system_materials_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.system_materials_directory_path)) + 1
    elif filesystem_path.startswith(configuration.user_sketches_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.user_sketches_directory_path)) + 1
    elif filesystem_path.startswith(configuration.system_specifiers_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.system_specifiers_directory_path)) + 1
    elif filesystem_path.startswith(configuration.user_scores_directory_path):
        prefix_length = len(configuration.user_scores_directory_path) + 1
    else:
        return

    package_path = filesystem_path[prefix_length:]
    package_path = package_path.replace(os.path.sep, '.')

    return package_path
