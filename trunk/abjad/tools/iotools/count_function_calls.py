# -*- encoding: utf-8 -*-


def count_function_calls(
    expr,
    global_context=None,
    local_context=None,
    fixed_point=True,
    ):
    '''Count function calls returned by ``iotools.profile_expr(expr)``.

    ..  container:: example

        **Example 1.** Function calls required to initialize note from string:

        ::

            >>> iotools.count_function_calls("Note('c4')", globals())
            10429
        
    ..  container:: example

        **Example 2.** Function calls required to initialize note from integers:

        ::

            >>> iotools.count_function_calls("Note(-12, (1, 4))", globals())
            131

    Return integer.
    '''
    from abjad.tools import iotools

    def extract_count(profile_output):
        return int(profile_output.splitlines()[2].split()[0])

    if fixed_point:
        # profile at least twice to ensure consist results from profiler;
        # not sure why but profiler eventually levels off to consistent output
        last_result, current_result = 'foo', 'bar'
        while current_result != last_result:
            last_result = current_result
            current_result = iotools.profile_expr(
                expr,
                print_to_terminal=False,
                global_context=global_context,
                local_context=local_context,
                )
            current_result = extract_count(current_result)
        return current_result

    result = iotools.profile_expr(
        expr,
        print_to_terminal=False,
        global_context=global_context,
        local_context=local_context,
        )
    result = extract_count(result)
    return result
