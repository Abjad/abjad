from abjad.cfg.abjad_version import _get_abjad_version


## TODO: Would be nice to rename this function helpers( )
##       which will mean extending abjad/__init__.py

def list_helpers(start_string = ''):
   '''List Abjad helpers starting with start_string.

   Example:

   abjad> list_helpers('container')

   Abjad r1027 implements 8 helpers starting in 'container':

      container_contents_scale, container_glom_by_count, container_hew,
      container_partition_by_count, container_rest_by_count, 
      container_rest_half, container_shatter, container_splinter'''

   import abjad
   helpers = [x for x in dir(abjad) if x.islower( )]
   helpers = [x for x in helpers if not x.startswith('_')]
   version = _get_abjad_version( )

   print ''

   if start_string == '':
      total = len(helpers)
      print 'Abjad r%s implements %s total helpers:' % (
         version, total)
   else:
      helpers = [x for x in helpers if x.startswith(start_string)]
      total = len(helpers)
      number_suffix = '' if total == 1 else 's'
      print "Abjad r%s implements %s helper%s starting in '%s':" % (
         version, total, number_suffix, start_string)

   if total > 0:
      print ''

   line_width = 80
   indent = '   '
   output_line = indent + helpers[0]
   for helper in helpers[1:]:
      if len(output_line) + len(helper) > (line_width - 5):
         print output_line + ','
         output_line = indent + helper
      else:
         output_line += ', ' + helper
   print output_line

   print ''
