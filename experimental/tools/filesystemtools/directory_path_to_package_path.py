import os


def directory_path_to_package_path(directory_path):
    '''Change `directory_path` to package path.

    Return string.
    '''
    from experimental.tools.scoremanagertools import core
    
    configuration = core.ScoreManagerConfiguration()
    
    if directory_path is None:
        return

    directory_path = os.path.normpath(directory_path)

    if directory_path.endswith('.py'):
        directory_path = directory_path[:-3]
    if directory_path.startswith(configuration.score_manager_tools_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.score_manager_tools_directory_path)) + 1
    elif directory_path.startswith(configuration.score_external_materials_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.score_external_materials_directory_path)) + 1
    elif directory_path.startswith(configuration.score_external_segments_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.score_external_segments_directory_path)) + 1
    elif directory_path.startswith(configuration.score_external_specifiers_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.score_external_specifiers_directory_path)) + 1
    elif directory_path.startswith(configuration.scores_directory_path):
        prefix_length = len(configuration.scores_directory_path) + 1
    else:
        return

    package_path = directory_path[prefix_length:]
    package_path = package_path.replace(os.path.sep, '.')

    return package_path
