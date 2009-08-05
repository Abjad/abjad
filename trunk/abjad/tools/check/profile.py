def profile(expr, sort_by = 'cum', num_lines = 12, strip_dirs = True):
   '''Profile expr, sort stats, print 12 lines.
      Set strip_dirs to True to strip directory path names.
      Sort by values include 'cum', 'time', 'calls'.'''

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
