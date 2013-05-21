from experimental.tools.scoremanagertools.selectors.HandlerClassNameSelector import HandlerClassNameSelector


class DynamicHandlerClassNameSelector(HandlerClassNameSelector):

    ### CLASS VARIABLES ###

    space_delimited_lowercase_target_name = 'dynamic handler class name'
    forbidden_directory_entries = (
        'Handler',
        'DynamicHandler',
        'test',
        )
