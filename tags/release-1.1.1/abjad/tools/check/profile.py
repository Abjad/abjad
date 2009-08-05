import cProfile
import pstats


def profile(expr, sort_by = 'cum', num_lines = 12, strip_dirs = True):
   '''Profile expr, sort stats, print 12 lines.
      Set strip_dirs to True to strip directory path names.
      Sort by values include 'cum', 'time', 'calls'.'''

   cProfile.run(expr, '_tmp_abj_profile')
   p = pstats.Stats('_tmp_abj_profile')
   if strip_dirs:
      p.strip_dirs( ).sort_stats(sort_by).print_stats(num_lines)
   else:
      p.sort_stats(sort_by).print_stats(num_lines)
