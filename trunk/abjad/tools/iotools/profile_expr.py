import os
import sys
import tempfile


def profile_expr(expr, sort_by='cum', line_count=12, strip_dirs=True, print_callers=False, 
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

    Function creates the file ``_tmp_abj_profile`` in the directory from which it is run.

    See the `Python docs <http://docs.python.org/library/profile.html>`_
    for more information on the Python profilers.
    '''

    class RedirectStdStreams(object):
        def __init__(self, stdout=None, stderr=None):
            self._stdout = stdout or sys.stdout
            self._stderr = stderr or sys.stderr
        def __enter__(self):
            self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
            self.old_stdout.flush(); self.old_stderr.flush()
            sys.stdout, sys.stderr = self._stdout, self._stderr
        def __exit__(self, exc_type, exc_value, traceback):
            self._stdout.flush(); self._stderr.flush()
            sys.stdout = self.old_stdout
            sys.stderr = self.old_stderr

    # NOTE: this try block was added because, for some strange reason,
    # Python 2.5.x doesn't come with 'pstats' installed in some Linux distros!
    try:
        import cProfile
        import pstats

        if global_context is None:
            cProfile.run(expr, '_tmp_abj_profile')
        else:
            cProfile.runctx(expr, global_context, local_context, '_tmp_abj_profile')

        with open('_tmp_abj_profile_print', 'w') as f:
            with RedirectStdStreams(stdout=f):
                p = pstats.Stats('_tmp_abj_profile')
                if strip_dirs:
                    p.strip_dirs().sort_stats(sort_by).print_stats(line_count)
                    if print_callers:
                        p.strip_dirs().sort_stats(sort_by).print_callers(line_count)
                else:
                    p.sort_stats(sort_by).print_stats(line_count)
                    if print_callers:
                        p.sort_stats(sort_by).print_callers(line_count)

        with open('_tmp_abj_profile_print', 'r') as f:
            result = f.read()

    except ImportError:
        print "Python 'pstats' package not installed in your system.\n" + \
            "Please install before running the profiler."

    finally:
        os.remove('_tmp_abj_profile')
        os.remove('_tmp_abj_profile_print')

    if print_to_terminal:
        print result
    else:
        return result
