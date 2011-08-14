Timing code
===========

You can time code with Python's built-in ``timeit`` module::

    from abjad import *
    import timeit

    timer = timeit.Timer('Note(0, (1, 4))', 'from __main__ import Note')
    print timer.timeit(1000)

::

    0.225436925888
 
These results show that 1000 notes take 0.23 seconds to create.

Other Python timing modules are available for download on the public Internet.
