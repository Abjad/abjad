from abjad.core.formatcontributor import _FormatContributor
from abjad.core.interface import _Interface
import types


class _BreaksInterface(_Interface, _FormatContributor):
   r'''Handle no LilyPond grob.
      Interface to LilyPond \break and \pageBreak commands.
      Interface to LilyPond x- and y- system positioning.'''
   
   def __init__(self, client):
      '''Bind to client and set line, page, x and y to None.'''
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      self._line = None
      self._page = None
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
      #result = ''
      result = [ ]
      x = self.x
      y = self.y
      if x is not None or y is not None:
         #result += '\\overrideProperty #"Score.NonMusicalPaperColumn"\n'
         #result += "#'line-break-system-details\n"
         result.append('\\overrideProperty #"Score.NonMusicalPaperColumn"')
         result.append("#'line-break-system-details")
         temp = [ ]
         if x is not None:
            temp.append('(X-offset . %s)' % x)
         if y is not None:
            temp.append('(Y-offset . %s)' % y)
         temp_str = ' '.join(temp)
         #result += "#'(%s)" % temp_str
         result.append("#'(%s)" % temp_str)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def closing(self):
      '''Format contribution at container closing or after leaf.'''
      result = [ ]
      if self.line:
         result.append(r'\break')
      if self.page:
         result.append(r'\pageBreak')
#      details = self._line_break_system_details
#      if details:
#         #result.append(details)
#         result.extend(details)
      return result

   @apply
   def line( ):
      r'''Boolean setting to contribute LilyPond \line break.'''
      def fget(self):
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
      r'''Boolean setting to contribute LilyPond \pageBreak.'''
      def fget(self):
         return self._page
      def fset(self, arg):
         assert isinstance(arg, bool) or arg is None
         self._page = arg
      return property(**locals( ))

   @apply
   def x( ):
      '''X-value for line-break-system-details contribution.'''
      def fget(self):
         return self._x
      def fset(self, arg):
         assert isinstance(arg, (int, long, float, types.NoneType))
         self._x = arg
      return property(**locals( ))

   @apply
   def y( ):
      '''Y-value for line-break-system-details contribution.'''
      def fget(self):
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
