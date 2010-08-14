Profiling code
==============


Profile code with ``profile_expr( )`` in the ``iotools`` package::

   abjad> iotools.profile_expr('Note(0, (1, 4))')

   Sat Aug 14 13:03:16 2010    _tmp_abj_profile

            2214 function calls (2187 primitive calls) in 0.010 CPU seconds

      Ordered by: cumulative time
      List reduced from 157 to 12 due to restriction <12>

      ncalls  tottime  percall  cumtime  percall filename:lineno(function)
           1    0.000    0.000    0.010    0.010 <string>:1(<module>)
           1    0.000    0.000    0.010    0.010 Note.py:9(__init__)
           1    0.000    0.000    0.010    0.010 _NoteInitializer.py:8(__init__)
           1    0.000    0.000    0.009    0.009 _Leaf.py:19(__init__)
           3    0.000    0.000    0.008    0.003 _Component.py:80(__init__)
           1    0.000    0.000    0.007    0.007 GraceInterface.py:6(__init__)
           2    0.000    0.000    0.007    0.003 Grace.py:8(__init__)
           2    0.000    0.000    0.006    0.003 Container.py:12(__init__)
           3    0.003    0.001    0.003    0.001 MeterInterface.py:16(__init__)
          79    0.000    0.000    0.002    0.000 _GrobHandler.py:13(__init__)
     412/393    0.001    0.000    0.002    0.000 _GrobHandler.py:27(__setattr__)
          90    0.000    0.000    0.001    0.000 _FormatContributor.py:6(__init__)

These results show 2214 function calls to create a note.

The ``profile_expr( )`` function wraps the Python ``cProfile`` and ``pstats`` modules.
