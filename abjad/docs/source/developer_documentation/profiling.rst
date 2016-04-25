Profiling code
==============


Profile code with ``profile_expr()`` in the ``systemtools`` package:

::

    >>> systemtools.IOManager.profile_expr(
    ...     'Note(0, (1, 4))',
    ...     global_context=globals(),
    ...     )
    Fri Oct 18 14:24:16 2013

            1242 function calls (1121 primitive calls) in 0.003 seconds

    Ordered by: cumulative time
    List reduced from 83 to 12 due to restriction <12>

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.003    0.003 <string>:1(<module>)
         1    0.000    0.000    0.003    0.003 Note.py:45(__init__)
        18    0.000    0.000    0.002    0.000 abc.py:128(__instancecheck__)
        27    0.000    0.000    0.002    0.000 {isinstance}
     68/11    0.001    0.000    0.002    0.000 abc.py:148(__subclasscheck__)
         1    0.000    0.000    0.002    0.002 NoteHead.py:33(__init__)
         1    0.000    0.000    0.002    0.002 NoteHead.py:237(fset)
         1    0.000    0.000    0.002    0.002 NamedPitch.py:29(__init__)
     75/11    0.000    0.000    0.001    0.000 {issubclass}
         1    0.000    0.000    0.001    0.001 Leaf.py:36(__init__)
        85    0.000    0.000    0.001    0.000 _weakrefset.py:58(__iter__)
         1    0.000    0.000    0.000    0.000 NamedPitch.py:232(_initialize_by_pitch_number)

These results show 1242 function calls to create a note.
