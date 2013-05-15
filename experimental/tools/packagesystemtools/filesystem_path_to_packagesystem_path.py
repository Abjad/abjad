import os


def filesystem_path_to_packagesystem_path(filesystem_path, configuration):
    '''Change `filesystem_path` to package path.

    Return string.
    '''
    #from experimental.tools import scoremanagertools
    #configuration = scoremanagertools.core.ScoreManagerConfiguration()

    if filesystem_path is None:
        return

    filesystem_path = os.path.normpath(filesystem_path)

    if filesystem_path.endswith('.py'):
        filesystem_path = filesystem_path[:-3]
    # TODO: maybe elif here instead of if?
    if filesystem_path.startswith(configuration.built_in_scores_directory_path):
        prefix_length = len(configuration.abjad_configuration.abjad_root_directory_path) + 1
    elif filesystem_path.startswith(configuration.built_in_specifiers_directory_path):
        prefix_length = len(configuration.abjad_configuration.abjad_root_directory_path) + 1
    elif filesystem_path.startswith(configuration.built_in_materials_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.built_in_materials_directory_path)) + 1
    elif filesystem_path.startswith(configuration.score_manager_tools_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.score_manager_tools_directory_path)) + 1
    elif filesystem_path.startswith(configuration.user_sketches_directory_path):
        prefix_length = \
            len(os.path.dirname(configuration.user_sketches_directory_path)) + 1
    elif filesystem_path.startswith(configuration.user_scores_directory_path):
        prefix_length = len(configuration.user_scores_directory_path) + 1
    elif filesystem_path.startswith(configuration.user_material_package_makers_directory_path):
        return configuration.user_material_package_makers_package_path
    else:
        raise Exception('can not change to package path: {!r}'.format(filesystem_path))

    package_path = filesystem_path[prefix_length:]
    package_path = package_path.replace(os.path.sep, '.')

    return package_path
