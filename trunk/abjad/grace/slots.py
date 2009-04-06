from abjad.container.slots import _ContainerFormatterSlotsInterface


class _GraceFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   ## TODO: Rename Grace.type to a non-Python reserved word. ##

   @property
   def slot_2(self):
      result = [ ]
      grace = self.formatter.grace
      type = grace.type
      if type == 'after':
         result.append(grace.brackets.open)
      else:
         result.append(r'\%s %s' % (type, grace.brackets.open))
      return tuple(result)
