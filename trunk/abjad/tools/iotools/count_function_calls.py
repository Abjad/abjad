def count_function_calls(expr, global_context=None, local_context=None, fixed_point=True):
    '''.. versionadded:: 2.12

    Count function calls returned by ``iotools.profile_expr(expr)``.

    Example 1. Function calls required to initialize note from string:

    ::

        >>> iotools.count_function_calls("Note('c4')", globals())
        11267

    Example 2. Function calls required to initialize note from integers:

    ::

        >>> iotools.count_function_calls("Note(-12, (1, 4))", globals())
        138

    Return integer.
    '''
    from abjad.tools import iotools

    if fixed_point:
        # profile at least twice to ensure consist results from profiler;
        # not sure why but profiler eventually levels off to consistent output
        last_result, current_result = 'foo', 'bar'
        while current_result != last_result:
            last_result = current_result
            current_result = iotools.profile_expr(expr, print_to_terminal=False,
                global_context=global_context,
                local_context=local_context)
            current_result = int(current_result.split()[6])
        return current_result

    result = iotools.profile_expr(expr, print_to_terminal=False,
        global_context=global_context,
        local_context=local_context)
    result = int(result.split()[6])
    return result
