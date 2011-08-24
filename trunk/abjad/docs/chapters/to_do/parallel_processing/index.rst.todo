Parallel processing
===================

Generating and acting upon score objects, especially large ones, can be very 
time consuming.  However, you can speed up your score generation greatly if
you can find ways to parallelize it!

Python provides a number of packages to handle parallel processing, using both
threads and processes.  Unfortunately, due to the Global Interpreter Lock 
(GIL), you won't see much performance improvement by multithreading your score
generation.  Luckily, the ``multiprocessing`` package gives us high level 
control over processes in a very similar manner to how one might manage
threads.

``multiprocessing`` provides a class, ``Pool``, which acts as a pool of
POSIX processes (just like the common thread-pool pattern).  ``Pool``, in 
turn, implements a parallelized ``map`` method, which works *basically* the 
same as Python's builtin ``map`` function.  If you don't provide ``Pool`` with
and arguments, it will create as many worker-processes as you have cores.

::

   from multiprocessing import Pool
   from abjad import *
   
   def proc(notes_to_make):
      con = Container([])
      con.extend(leaftools.make_repeated_notes(notes_to_make))
      return con
   
   def make(parallel = True):
      notes_per_fragment = range(1, 4)
      if parallel:
         pool = Pool()
         result = pool.map_async(proc, notes_per_fragment)
         pool.close() ## prevent the pool from accepting new work
         pool.join() ## wait for all child processes to return
         return result.get()
      else:
         return map(proc, notes_per_fragment)

::

   abjad> make(parallel = True)
   [{c'8}, {c'8, c'8}, {c'8, c'8, c'8}]

::

   abjad> make(parallel = False)
   [{c'8}, {c'8, c'8}, {c'8, c'8, c'8}]

A few words of caution about the above code fragment:

One, it's very useful to be able to turn the parallelization on and off, 
for debugging purposes, as errors encountered during processing may not
appear (especially if one process fails, while another continues, and
then the entire ``map_async`` simply hangs after the final process exits).
Just as annoying, when errors do appear, the offending line in your code
won't!

Two, do not use nested function definitions in your parallel procedure.
The code above will fail if you redefine ``proc`` inside ``make``.  Similarly,
if you pass a list of class instances to ``map_async`` which define another 
class inside themselves, it will also fail.  This is a quirk of how
``multiprocessing`` passes information around.

Three, if you're computing very large fragments in parallel, expect a wait
after your fragment generating procedures complete while the results are
returned to the main Python process.  If the function never returns, then
one of your processes failed, and you'll have to go find it.
