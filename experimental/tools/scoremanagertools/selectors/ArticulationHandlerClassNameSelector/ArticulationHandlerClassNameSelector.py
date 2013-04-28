import os
from experimental.tools.scoremanagertools.selectors.HandlerClassNameSelector import HandlerClassNameSelector


class ArticulationHandlerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_paths = ['handlertools']
    asset_container_paths = [HandlerClassNameSelector.configuration.handler_tools_directory_path]
    target_human_readable_name = 'articulation handler class name'

    forbidden_directory_content_names = (
        'ArticulationHandler',
        )
