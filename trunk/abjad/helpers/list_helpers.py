from abjad.cfg.abjad_version import _get_abjad_version


def list_helpers(search_string = '', scope = 'public'):
   '''Input parameters:
      
      search_string should be any Python string.
      scope should be 'public', 'private' or 'both'.

   List all Abjad helpers containing search_string.
   When scope is 'public' list only public Abjad helpers.
   When scope is 'private' list only private Abjad helpers.
   When scope is 'both' list both public and private Abjad helpers.


   Example with default public scope:

   abjad> list_helpers('are')   

   Abjad r1185 implements 1 public helper containing the string 'are':

      components_parentage_detach


   Example with private scope:

   abjad> list_helpers('are', scope = 'private')

   Abjad r1330 implements 14 private helpers containing the string 'are':

      _is_tie_chain_in_same_parent, _link_new_leaf_to_parent,
      _total_preprolated_duration_in_same_parent'''

   import abjad
   helpers = [x for x in dir(abjad) if x.islower( )]
   if scope == 'private':
      scope_string = 'private '
      helpers = [x for x in helpers if x.startswith('_')]
      helpers = [x for x in helpers if not x.startswith('__')]
   elif scope == 'public':
      scope_string = 'public '
      helpers = [x for x in helpers if not x.startswith('_')]
   elif scope == 'both':
      scope_string = ''
   else:
      raise ValueError("scope must be 'public', 'private' or 'both'.")

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
