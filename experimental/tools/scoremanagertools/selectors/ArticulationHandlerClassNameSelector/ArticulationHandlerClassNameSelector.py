from experimental.tools.scoremanagertools.selectors.HandlerClassNameSelector import HandlerClassNameSelector


class ArticulationHandlerClassNameSelector(HandlerClassNameSelector):

    ### CLASS ATTRIBUTES ###

    space_delimited_lowercase_target_name = 'articulation handler class name'
    forbidden_directory_entries = (
        'ArticulationHandler',
        )
