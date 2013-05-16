import os
from experimental.tools.scoremanagertools.selectors.DirectoryContentSelector import DirectoryContentSelector


class HandlerClassNameSelector(DirectoryContentSelector):

    ### CLASS ATTRIBUTES ###

    handler_tools_directory_path = os.path.join(
        DirectoryContentSelector.configuration.abjad_configuration.abjad_experimental_directory_path, 
        'tools', 
        'handlertools')

    asset_container_filesystem_paths = [handler_tools_directory_path]
