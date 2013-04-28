import os
from experimental.tools.scoremanagertools.selectors.HandlerClassNameSelector import HandlerClassNameSelector


class DynamicHandlerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_paths = ['handlertools']
    asset_container_paths = [HandlerClassNameSelector.configuration.handler_tools_directory_path]
    target_human_readable_name = 'dynamic handler class name'

    forbidden_directory_content_names = (
        'DynamicHandler',
        )
