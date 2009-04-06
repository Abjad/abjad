from abjad.core.interface import _Interface
from abjad.comments.comments import _UserComments
from abjad.directives.interface import _UserDirectivesInterface


class _ComponentFormatterSlotsInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      
   ## PRIVATE METHODS ##

   def _format_contributor_name(self, contributor):
      '''Formater contributor name.'''
      result = [ ]
      for part in contributor:
         if isinstance(part, str):
            result.append(part)
         else:
            result.append(part.__class__.__name__)
      result = '.'.join(result)
      return result

   def _format_slot(self, label, slot, 
      verbose = False, output = 'screen'):
      '''Format slot.'''
      result = label + '\n'
      for (contributor, contributions) in slot:
         if contributions or verbose:
            result += '\t%s\n' % self._format_contributor_name(contributor)
            for contribution in contributions:
               result += '\t\t%s\n' % contribution
      if output == 'screen':
         print result
      else:
         return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def formatter(self):
      return self._client

   @property
   def slot_1(self):
      '''Format contributions immediately before open brackets.'''
      return ( )

   @property
   def slot_2(self):
      '''Open brackets, possibly including with-block.'''
      return ( )

   @property
   def slot_3(self):
      '''Format contributions immediately after open brackets.'''
      return ( )

   @property
   def slot_4(self):
      '''Formatted container contents or formatted leaf body.'''
      return ( )

   @property
   def slot_5(self):
      '''Format contributions immediately before close brackets.'''
      return ( )

   @property
   def slot_6(self):
      '''Close brackets.'''
      return ( )

   @property
   def slot_7(self):
      '''Format contributions immediately after close brackets.'''
      return ( )

   ## PUBLIC METHODS ##

   def contributions(self, attr):
      result = [ ]
      for contributor, contributions in getattr(self, attr):
         result.extend(contributions)
      return result

#   def report(self):
#      print '%s: %s' % ('slot_1', self.slot_1)
#      print '%s: %s' % ('slot_2', self.slot_2)
#      print '%s: %s' % ('slot_3', self.slot_3)
#      print '%s: %s' % ('slot_4', self.slot_4)
#      print '%s: %s' % ('slot_5', self.slot_5)
#      print '%s: %s' % ('slot_6', self.slot_6)
#      print '%s: %s' % ('slot_7', self.slot_7)

#   def report(self, verbose = False, output = 'screen'):
#      '''Report format contributions.'''
#      result = ''
#      for i in range(1, 7 + 1):
#         label = 'slot_%s' % i
#         attr = label
#         result += self._format_slot(
#            label, getattr(self, attr), verbose, output = 'string')
#      if output == 'screen':
#         print result
#      else:
#         return result

   def wrap(self, contributor, attr):
      '''Wrap format contribution with format source.'''
      if isinstance(contributor, _UserComments) and \
         not isinstance(contributor, _UserDirectivesInterface):
         return [(contributor, attr), 
            ['% ' + x for x in getattr(contributor, attr)]]
      else:
         return [(contributor, attr), getattr(contributor, attr)]
