import os


def profile_expr(expr, sort_by = 'cum', num_lines = 12, strip_dirs = True):
    '''Profile `expr`::

        abjad> iotools.profile_expr('Staff(notetools.make_repeated_notes(8))') # doctest: +SKIP
        Tue Apr  5 20:32:40 2011    _tmp_abj_profile

                 2852 function calls (2829 primitive calls) in 0.006 CPU seconds

           Ordered by: cumulative time
           List reduced from 118 to 12 due to restriction <12>

           ncalls  tottime  percall  cumtime  percall filename:lineno(function)
                1    0.000    0.000    0.006    0.006 <string>:1(<module>)
                1    0.000    0.000    0.003    0.003 make_repeated_notes.py:5(make_repeated_notes)
                1    0.001    0.001    0.003    0.003 make_notes.py:12(make_notes)
                1    0.000    0.000    0.003    0.003 Staff.py:21(__init__)
                1    0.000    0.000    0.003    0.003 _Context.py:11(__init__)
                1    0.000    0.000    0.003    0.003 Container.py:23(__init__)
                1    0.000    0.000    0.003    0.003 Container.py:271(_initialize_music)
                2    0.000    0.000    0.002    0.001 all_are_thread_contiguous_components.py:9(all_are_thread_contiguous_components)
               52    0.001    0.000    0.002    0.000 component_to_thread_signature.py:5(component_to_thread_signature)
                1    0.000    0.000    0.002    0.002 _construct_unprolated_notes.py:4(_construct_unprolated_notes)
                8    0.000    0.000    0.002    0.000 _construct_tied_note.py:5(_construct_tied_note)
                8    0.000    0.000    0.002    0.000 _construct_tied_leaf.py:5(_construct_tied_leaf)

    Function wraps the built-in Python ``cProfile`` module.

    Set `expr` to any string of Abjad input.

    Set `sort_by` to `'cum'`, `'time'` or `'calls'`.

    Set `num_lines` to any positive integer.

    Set `strip_dirs` to ``True`` to strip directory names from output lines.

    .. note:: This function fails on some Linux distros. Some Linux
       distributions do not include the Python ``pstats`` module.

    .. note:: This function creates the file ``_tmp_abj_profile`` in
       the directory from which it is run.

    .. note:: For information on reading the output of the different
       Python profilers, see `the Python docs
       <http://docs.python.org/library/profile.html>`_.

    .. versionchanged:: 2.0
       renamed ``check.profile()`` to
       ``iotools.profile_expr()``.
    '''

    # NOTE: this try block was added because, for some strange reason,
    # Python 2.5.x doesn't come with 'pstats' installed in some Linux distros!
    try:
        import cProfile
        import pstats

        cProfile.run(expr, '_tmp_abj_profile')
        p = pstats.Stats('_tmp_abj_profile')
        if strip_dirs:
            p.strip_dirs().sort_stats(sort_by).print_stats(num_lines)
        else:
            p.sort_stats(sort_by).print_stats(num_lines)

        os.remove('_tmp_abj_profile')

    except ImportError:
        msg = "Python 'pstats' package not installed in your system.\n"
        msg +="Please install before running the profiler."
        print msg
