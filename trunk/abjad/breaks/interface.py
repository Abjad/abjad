from abjad.core.formatcontributor import _FormatContributor
from abjad.core.interface import _Interface
from abjad.exceptions.exceptions import TypographicWhitespaceError
from abjad.rational.rational import Rational
import types


class _BreaksInterface(_Interface, _FormatContributor):
   r'''Interface to LilyPond ``break`` and ``pageBreak`` commands.
      Affordance for nonstaff whitespace following client.
      Interface to *LilyPond* x- and y- system positioning.
      Handle no *LilyPond* grob.'''
   
   def __init__(self, client):
      '''Bind to client and set line, page, whitespace, x and y to None.'''
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      self._line = None
      self._page = None
      self._whitespace = None
      self._x = None
      self._y = None

   ## OVERLOADS ##

   def __nonzero__(self):
      '''True when line or page are set to True.'''
      return self.line is True or self.page is True

   ## PRIVATE ATTRIBUTES ##

   @property
   def _line_break_system_details(self):
      '''LilyPond Score.NonMusicalPaperColumn #'line-break-system-details
         formatting contribution.'''
      result = [ ]
      x = self.x
      y = self.y
      if x is not None or y is not None:
         result.append('\\overrideProperty #"Score.NonMusicalPaperColumn"')
         result.append("#'line-break-system-details")
         temp = [ ]
         if x is not None:
            temp.append('(X-offset . %s)' % x)
         if y is not None:
            temp.append('(Y-offset . %s)' % y)
         temp_str = ' '.join(temp)
         result.append("#'(%s)" % temp_str)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def closing(self):
      '''Format contribution at container closing or after leaf.'''
      result = [ ]
      whitespace = self.whitespace
      if whitespace:
         from abjad.tools.layout._rational_to_whitespace_measure_string import \
            _rational_to_whitespace_measure_string as \
            layout__rational_to_whitespace_measure_string
         string = layout__rational_to_whitespace_measure_string(whitespace)
         result.extend(string.split('\n'))
      if self.line:
         result.append(r'\break')
      if self.page:
         result.append(r'\pageBreak')
      return result

   @apply
   def line( ):
      def fget(self):
         r'''Boolean setting to contribute LilyPond \line break.'''
         return self._line
      def fset(self, arg):
         assert isinstance(arg, bool) or arg is None
         self._line = arg
      return property(**locals( ))

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      result = [ ]
      details = self._line_break_system_details
      if details:
         result.extend(details)
      return result

   @apply
   def page( ):
      def fget(self):
         r'''Boolean setting to contribute LilyPond \pageBreak.'''
         return self._page
      def fset(self, arg):
         assert isinstance(arg, bool) or arg is None
         self._page = arg
      return property(**locals( ))

   ## Client type-checking is a hack; find structural solution later. ##

   @apply
   def whitespace( ):
      def fget(self):
         r'''Rational-valued non-durative whitespace following client.
            Fake measure between \stopStaff, \startStaff commands.'''
         return self._whitespace
      def fset(self, arg):
         from abjad.leaf.leaf import _Leaf
         assert isinstance(arg, (int, Rational, types.NoneType))
         if isinstance(self._client, _Leaf):
            raise TypographicWhitespaceError
         self._whitespace = arg
      return property(**locals( ))

   @apply
   def x( ):
      def fget(self):
         '''X-value for line-break-system-details contribution.'''
         return self._x
      def fset(self, arg):
         assert isinstance(arg, (int, long, float, types.NoneType))
         self._x = arg
      return property(**locals( ))

   @apply
   def y( ):
      def fget(self):
         '''Y-value for line-break-system-details contribution.'''
         return self._y
      def fset(self, arg):
         assert isinstance(arg, (int, long, float, types.NoneType))
         self._y = arg
      return property(**locals( ))

   ## PUBLIC METHODS ##

   def clear(self):
      r'''Remove any LilyPond \line break contribution.
         Remove any LilyPond \pageBreak contribution.'''
      self.line = None
      self.page = None
