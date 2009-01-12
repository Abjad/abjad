from abjad.core.formatcarrier import _FormatCarrier
from abjad.core.interface import _Interface
import types


class _BreaksInterface(_Interface, _FormatCarrier):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatCarrier.__init__(self)
      self._line = None
      self._page = None
      self._x = None
      self._y = None

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
         details = self._line_break_system_details
         if details:
            result.append(details)
      return result

   @property
   def _closing(self):
      result = [ ]
      if self._client.kind('Container'):
         if self.line:
            result.append(r'\break')
         if self.page:
            result.append(r'\pageBreak')
         details = self._line_break_system_details
         if details:
            result.append(details)
      #result = ['\t' + r for r in result]
      return result

   @property
   def _line_break_system_details(self):
      result = ''
      x = self.x
      y = self.y
      if x is not None or y is not None:
         result += '\\overrideProperty #"Score.NonMusicalPaperColumn"\n'
         result += "#'line-break-system-details\n"
         temp = [ ]
         if x is not None:
            temp.append('(X-offset . %s)' % x)
         if y is not None:
            temp.append('(Y-offset . %s)' % y)
         temp_str = ' '.join(temp)
         result += "#'(%s)" % temp_str
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

   @apply
   def x( ):
      def fget(self):
         return self._x
      def fset(self, arg):
         assert isinstance(arg, (int, long, float, types.NoneType))
         self._x = arg
      return property(**locals( ))

   @apply
   def y( ):
      def fget(self):
         return self._y
      def fset(self, arg):
         assert isinstance(arg, (int, long, float, types.NoneType))
         self._y = arg
      return property(**locals( ))

   ### PUBLIC METHODS ###

   def clear(self):
      self.line = None
      self.page = None
