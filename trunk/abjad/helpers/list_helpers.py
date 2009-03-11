from abjad.cfg.abjad_version import _get_abjad_version


## TODO: Would be nice to rename this function helpers( )
##       which will mean extending abjad/__init__.py

## TODO: Figure out how to write tests for this helper.

def list_helpers(search_string = '', private = False):
   '''List Abjad helpers containing search_string.

   Example:

   abjad> list_helpers('container')

   Abjad r1027 implements 8 helpers containing 'container':

      container_contents_scale, container_glom_by_count, container_hew,
      container_partition_by_count, container_rest_by_count, 
      container_rest_half, container_shatter, container_splinter'''

   import abjad
   helpers = [x for x in dir(abjad) if x.islower( )]
   if private == True:
      scope_string = 'private '
      helpers = [x for x in helpers if x.startswith('_')]
      helpers = [x for x in helpers if not x.startswith('__')]
   else:
      scope_string = ''
      helpers = [x for x in helpers if not x.startswith('_')]

   version = _get_abjad_version( )

   print ''

   if search_string == '':
      total = len(helpers)
      print 'Abjad r%s implements %s total %shelpers:' % (
         version, total, scope_string)
   else:
      helpers = [x for x in helpers if search_string in x]
      total = len(helpers)
      number_suffix = '' if total == 1 else 's'
      label_punctuation = ':' if total > 0 else '.'
      label = "Abjad r%s implements %s %shelper%s "
      label += "containing the string '%s'%s"
      label %= (version, total, scope_string, number_suffix, 
         search_string, label_punctuation)
      print label

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
