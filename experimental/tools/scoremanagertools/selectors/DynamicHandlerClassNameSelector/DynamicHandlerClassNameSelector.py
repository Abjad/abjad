import os
from experimental.tools.scoremanagertools.selectors.HandlerClassNameSelector import HandlerClassNameSelector


class DynamicHandlerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_paths = ['handlertools']
    asset_container_paths = [HandlerClassNameSelector.configuration.HANDLER_TOOLS_DIRECTORY_PATH]
    target_human_readable_name = 'dynamic handler class name'

    forbidden_names = (
        'DynamicHandler',
        )
