Profiling code
==============


Profile code with ``profile_expr()`` in the ``iotools`` package::

    abjad> iotools.profile_expr('Note(0, (1, 4))')
    Sun Aug 14 16:50:36 2011    _tmp_abj_profile

             327 function calls (312 primitive calls) in 0.001 CPU seconds

       Ordered by: cumulative time
       List reduced from 96 to 12 due to restriction <12>

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.001    0.001 <string>:1(<module>)
            1    0.000    0.000    0.001    0.001 Note.py:18(__init__)
            1    0.000    0.000    0.001    0.001 Note.py:133(fset)
            1    0.000    0.000    0.001    0.001 NoteHead.py:18(__init__)
            1    0.000    0.000    0.001    0.001 NoteHead.py:121(fset)
            1    0.000    0.000    0.001    0.001 NamedChromaticPitch.py:28(__new__)
            1    0.000    0.000    0.000    0.000 _Leaf.py:18(__init__)
            1    0.000    0.000    0.000    0.000 chromatic_pitch_name_to_diatonic_pitch_numbe
            1    0.000    0.000    0.000    0.000 octave_tick_string_to_octave_number.py:4(oct
            1    0.000    0.000    0.000    0.000 re.py:134(match)
            1    0.000    0.000    0.000    0.000 re.py:227(_compile)
            1    0.000    0.000    0.000    0.000 sre_compile.py:501(compile)

These results show 327 function calls to create a note.

The ``profile_expr()`` function wraps the Python ``cProfile`` and ``pstats`` modules.
