from .. containers.formatter import ContainerFormatter

class GraceFormatter(ContainerFormatter):

   def __init__(self, client):
      ContainerFormatter.__init__(self, client)

   @property
   def _opening(self):
      result = [ ]
      result.append(r'\grace {')
      result.extend(ContainerFormatter._opening.fget(self))
      return result

   @property
   def _closing(self):
      result = [ ]
      result.extend(ContainerFormatter._closing.fget(self))
      result.append('}')
      return result
