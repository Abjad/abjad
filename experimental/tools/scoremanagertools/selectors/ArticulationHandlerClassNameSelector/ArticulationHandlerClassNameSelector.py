from experimental.tools.scoremanagertools.selectors.HandlerClassNameSelector import HandlerClassNameSelector
import os


class ArticulationHandlerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_importable_names = ['handlertools']
    asset_container_path_names = [os.environ.get('HANDLERS')]
    target_human_readable_name = 'articulation handler class name'

    forbidden_names = (
        'ArticulationHandler',
        )
