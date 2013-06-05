import datetime
import StringIO
import sys


def profile_expr(expr, sort_by='cum', line_count=12, strip_dirs=True,
    print_callers=False, print_callees=False,
    global_context=None, local_context=None, print_to_terminal=True):
    '''Profile `expr`:

    ::

        >>> iotools.profile_expr('Staff(notetools.make_repeated_notes(8))') # doctest: +SKIP
        Tue Apr  5 20:32:40 2011    _tmp_abj_profile

                 2852 function calls (2829 primitive calls) in 0.006 CPU seconds

        Ordered by: cumulative time
        List reduced from 118 to 12 due to restriction <12>

        ncalls  tottime  percall  cumtime  percall filename:lineno(function)
                1    0.000    0.000    0.006    0.006 <string>:1(<module>)
                1    0.000    0.000    0.003    0.003 make_repeated_notes.py:5(make_repeated
                1    0.001    0.001    0.003    0.003 make_notes.py:12(make_notes)
                1    0.000    0.000    0.003    0.003 Staff.py:21(__init__)
                1    0.000    0.000    0.003    0.003 Context.py:11(__init__)
                1    0.000    0.000    0.003    0.003 Container.py:23(__init__)
                1    0.000    0.000    0.003    0.003 Container.py:271(_initialize_music)
                2    0.000    0.000    0.002    0.001 all_are_thread_contiguous_components.p
               52    0.001    0.000    0.002    0.000 component_to_thread_signature.py:5(com
                1    0.000    0.000    0.002    0.002 _construct_unprolated_notes.py:4(_cons
                8    0.000    0.000    0.002    0.000 make_tied_note.py:5(make_tied_note)
                8    0.000    0.000    0.002    0.000 make_tied_leaf.py:5(make_tied_leaf)

    Function wraps the built-in Python ``cProfile`` module.

    Set `expr` to any string of Abjad input.

    Set `sort_by` to `'cum'`, `'time'` or `'calls'`.

    Set `line_count` to any nonnegative integer.

    Set `strip_dirs` to true to strip directory names from output lines.

    See the `Python docs <http://docs.python.org/library/profile.html>`_
    for more information on the Python profilers.
    '''

    import cProfile
    import pstats
    from abjad.tools import iotools

    now_string = datetime.datetime.today().strftime('%a %b %d %H:%M:%S %Y')

    profile = cProfile.Profile()
    if global_context is None:
        profile = profile.run(
            expr,
            )
    else:
        profile = profile.runctx(
            expr,
            global_context,
            local_context,
            )

    stats_stream = StringIO.StringIO()
    stats = pstats.Stats(profile, stream=stats_stream)

    if strip_dirs:
        stats.strip_dirs().sort_stats(sort_by).print_stats(line_count)
    else:
        stats.sort_stats(sort_by).print_stats(line_count)
    if print_callers:
        stats.sort_stats(sort_by).print_callers(line_count)
    if print_callees:
        stats.sort_stats(sort_by).print_callees(line_count)

    result = now_string + '\n\n' + stats_stream.getvalue()
    stats_stream.close()

    if print_to_terminal:
        print result
    else:
        return result
