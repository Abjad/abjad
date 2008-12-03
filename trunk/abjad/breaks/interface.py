from abjad.core.formatcarrier import _FormatCarrier
from abjad.core.interface import _Interface


class _BreaksInterface(_Interface, _FormatCarrier):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatCarrier.__init__(self)
      self._line = None
      self._page = None

   ### OVERLOADS ###

   def __nonzero__(self):
      return self.line is True or self.page is True

   ### PRIVATE ATTRIBUTES ###

   ### TODO: Is there a *PATTERN* that will generalize
   ###       this type of formatting information across
   ###       leaves and containers?
   ###       The _client inspection here is hackish.
   ###       [TB 2008-12-03]

   @property
   def _after(self):
      result = [ ]
      if self._client.kind('_Leaf'):
         if self.line:
            result.append(r'\break')
         if self.page:
            result.append(r'\pageBreak')
      return result

   @property
   def _closing(self):
      result = [ ]
      if self._client.kind('Container'):
         if self.line:
            result.append(r'\break')
         if self.page:
            result.append(r'\pageBreak')
      result = ['\t' + r for r in result]
      return result

   ### PUBLIC ATTRIBUTES ###

   @apply
   def line( ):
      def fget(self):
         return self._line
      def fset(self, arg):
         if arg is None:
            self._line = arg
         elif isinstance(arg, bool):
            self._line = arg
         else:
            raise ValueError('can not set line breaks.')
      return property(**locals( ))

   @apply
   def page( ):
      def fget(self):
         return self._page
      def fset(self, arg):
         if arg is None:
            self._page = arg
         elif isinstance(arg, bool):
            self._page = arg
         else:
            raise ValueError('can not set page breaks.')
      return property(**locals( ))

   ### PUBLIC METHODS ###

   def clear(self):
      self.line = None
      self.page = None
