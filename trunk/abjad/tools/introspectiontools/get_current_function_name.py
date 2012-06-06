import inspect


def get_current_function_name():
    r'''.. versionadded:: 2.10

    Get current function name::

        >>> from abjad.tools import introspectiontools

    ::

        >>> def foo():
        ...        function_name = introspectiontools.get_current_function_name()
        ...        print 'Function name is {!r}.'.format(function_name)

    ::

        >>> foo()
        Function name is 'foo'.

    Call this function within the implementation of any ofther function.

    Returns enclosing function name as a string or else none.
    '''
    
    stack = inspect.stack()

    # per the inspect module doc page ...
    try:
        parent_frame_record = stack[1]
        parent_frame = parent_frame_record[0]
        parent_frame_info = inspect.getframeinfo(parent_frame)
        parent_frame_function_name = parent_frame_info.function
        return parent_frame_function_name
    # ... destroy frame to avoid reference cycle
    finally:
        del stack
