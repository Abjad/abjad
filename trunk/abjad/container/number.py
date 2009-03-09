class _ContainerFormatterNumberInterface(object):

   def __init__(self, client):
      self._client = client
      self._leaves = None
      self._measures = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def leaves( ):
      def fget(self):
         return self._leaves
      def fset(self, arg):
         assert arg in ('comment', 'markup', None)
         self._leaves = arg
      return property(**locals( ))
         
   @apply
   def measures( ):
      def fget(self):
         return self._measures
      def fset(self, arg):
         assert arg in ('comment', None)
         self._measures = arg
      return property(**locals( ))
