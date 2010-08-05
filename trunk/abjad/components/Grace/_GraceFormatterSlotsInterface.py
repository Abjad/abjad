from abjad.components.Container._ContainerFormatterSlotsInterface import \
   _ContainerFormatterSlotsInterface


class _GraceFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_2(self):
      result = [ ]
      grace = self.formatter.grace
      kind = grace.kind
      if kind == 'after':
         result.append(self.wrap(grace.brackets, 'open'))
      else:
         contributor = (grace.brackets, 'open')
         contributions = [r'\%s %s' % (kind, grace.brackets.open[0])]
         result.append([contributor, contributions])
      return tuple(result)
