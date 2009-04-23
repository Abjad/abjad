from abjad.core.abjadcore import _Abjad


class _BacktrackingInterface(_Abjad):
   '''Interfaces with 'forced' and 'effective' attributes.'''

   def __init__(self, _interfaceName):
      self._interfaceName = _interfaceName

   ## PRIVATE METHODS ##

   def _getEffective(self):
      '''Works for any interface with 'forced' and 'effective' attributes.
         Most such interfaces are observers.'''
      myForced = self.forced
      if myForced is not None:
         return myForced
      prevComponent = self._client._navigator._prev 
      if prevComponent is not None:
         prevInterface = getattr(prevComponent, self._interfaceName, None)
         if prevInterface is not None:
            prevForced = prevInterface.forced
            if prevForced:
               return prevForced
            else:
               return prevInterface._effective
      for parent in self._client.parentage.parentage[1:]:
         parentInterface = getattr(parent, self._interfaceName, None)
         if parentInterface is not None:
            parentForced = parentInterface.forced
            if parentForced is not None:
               return parentForced
      default = getattr(self, 'default', None)
      return default
   
   def _update(self):
      '''Update my score-dependent core attributes.'''
      effective = self._getEffective( )
      self._effective = effective

   ## PUBLIC ATTRIBUTES ##

   @property
   def change(self):
      '''True when core attribute changes at client, otherwise False.'''
      prevLeaf = getattr(self._client, 'prev', None)
      if prevLeaf:
         prevInterface = getattr(prevLeaf, self._interfaceName)
         curInterface = getattr(self._client, self._interfaceName)
         return not prevInterface.effective == curInterface.effective
      return False

   @property
   def effective(self):
      '''Effective core attribute governing client.'''
      self._makeSubjectUpdateIfNecessary( )
      return self._effective

   @apply
   def forced( ):
      '''Read / write core attribute explicitly.'''
      def fget(self):
         return self._forced
      def fset(self, arg):
         assert isinstance(arg, self._acceptableTypes)
         self._forced = arg
         self._client._update._markForUpdateToRoot( )
      return property(**locals( ))
