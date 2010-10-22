Timing code
===========

You can time code with Python's built-in ``timeit`` module::

   from abjad import *
   import timetime

   timer = timeit.Timer('Note(0, (1, 4))', 'from __main__ import Note')
   print timer.timeit(1000)

::

   3.97960996628
 
These results show that 1000 notes take 4 seconds to create.

Other Python timing modules are available for download on the public Internet.
