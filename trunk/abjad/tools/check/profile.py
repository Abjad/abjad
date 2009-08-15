def profile(expr, sort_by = 'cum', num_lines = 12, strip_dirs = True):
   '''Profile `expr` with the built-in Python ``cProfile`` module.

   Set `expr` to any string of Abjad input.

   Set `sort_by` to `'cum'`, `'time'` or `'calls'`.

   Set `num_lines` to any positive integer.

   Set `strip_dirs` to ``True`` to strip directory names from output lines. ::

      abjad> check.profile('Staff(construct.run(8))')
      Sat Aug 15 15:29:14 2009    _tmp_abj_profile

               147262 function calls (123144 primitive calls) in 0.237 CPU seconds

         Ordered by: cumulative time
         List reduced from 155 to 12 due to restriction <12>

         ncalls  tottime  percall  cumtime  percall filename:lineno(function)
              1    0.000    0.000    0.237    0.237 <string>:1(<module>)
              1    0.000    0.000    0.231    0.231 run.py:5(run)
              1    0.000    0.000    0.224    0.224 component.py:110(__mul__)
            8/1    0.001    0.000    0.224    0.224 unspan.py:8(unspan)
        19680/8    0.069    0.000    0.221    0.028 copy.py:144(deepcopy)
          400/8    0.002    0.000    0.221    0.028 copy.py:223(_deepcopy_list)
         2040/8    0.020    0.000    0.220    0.028 copy.py:299(_reconstruct)
         2008/8    0.016    0.000    0.220    0.027 copy.py:250(_deepcopy_dict)
           2408    0.029    0.000    0.044    0.000 copy.py:231(_deepcopy_tuple)
           2040    0.024    0.000    0.024    0.000 {method '__reduce_ex__' of 'object' objects}
           8728    0.015    0.000    0.019    0.000 copy.py:260(_keep_alive)
          30448    0.010    0.000    0.010    0.000 {method 'get' of 'dict' objects}

   .. note:: This function fails on some Linux distros. Some Linux
      distributions do not include the Python ``pstats`` module.

   .. note:: This function creates the file ``_tmp_abj_profile`` in
      the directory from which it is run.

   .. note:: For information on reading the output of the different
      Python profilers, see `the Python docs 
      <http://docs.python.org/library/profile.html>`_.
   '''

   ## NOTE: this try block was added because, for some strange reason, 
   ## Python 2.5.x doesn't come with 'pstats' installed in some Linux distros!
   try:
      import cProfile
      import pstats

      cProfile.run(expr, '_tmp_abj_profile')
      p = pstats.Stats('_tmp_abj_profile')
      if strip_dirs:
         p.strip_dirs( ).sort_stats(sort_by).print_stats(num_lines)
      else:
         p.sort_stats(sort_by).print_stats(num_lines)

   except ImportError:
      msg = "Python 'pstats' package not installed in your system.\n"
      msg +="Please install before running the profiler."
      print msg
      

#import cProfile
#import pstats
#
#
#def profile(expr, sort_by = 'cum', num_lines = 12, strip_dirs = True):
#   '''Profile expr, sort stats, print 12 lines.
#      Set strip_dirs to True to strip directory path names.
#      Sort by values include 'cum', 'time', 'calls'.'''
#
#   cProfile.run(expr, '_tmp_abj_profile')
#   p = pstats.Stats('_tmp_abj_profile')
#   if strip_dirs:
#      p.strip_dirs( ).sort_stats(sort_by).print_stats(num_lines)
#   else:
#      p.sort_stats(sort_by).print_stats(num_lines)
