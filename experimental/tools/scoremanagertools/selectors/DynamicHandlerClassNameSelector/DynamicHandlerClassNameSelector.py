from experimental.tools.scoremanagertools.selectors.HandlerClassNameSelector import HandlerClassNameSelector
import os


class DynamicHandlerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_importable_names = ['handlertools']
    asset_container_path_names = [os.environ.get('HANDLERS')]
    target_human_readable_name = 'dynamic handler class name'

    forbidden_names = (
        'DynamicHandler',
        )
