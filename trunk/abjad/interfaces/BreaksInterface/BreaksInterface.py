from abjad.core.formatcontributor import _FormatContributor
from abjad.interfaces._Interface import _Interface
from abjad.exceptions import LineBreakError
from abjad.exceptions import TypographicWhitespaceError
from abjad.rational import Rational
import types


class BreaksInterface(_Interface, _FormatContributor):
   r'''Interface to LilyPond ``\break`` and ``\pageBreak`` commands.

   Interface to LilyPond x- and y- system positioning.

   Handle no LilyPond grob. ::

      abjad> t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(t)
      abjad> t[0].formatter.number.self = 'comment'
      abjad> t[1].formatter.number.self = 'comment'

   ::

      abjad> t[0].breaks.page = True
      abjad> print t.format
      \new Staff {
              % start measure 1
                      \time 2/8
                      c'8
                      d'8
                      \pageBreak
              % stop measure 1
              % start measure 2
                      \time 2/8
                      e'8
                      f'8
              % stop measure 2
      }

   .. versionadded:: 1.1.1
      Affordance for nonstaff whitespace following client.

   .. versionadded:: 1.1.1
      Interface to LilyPond ``\adjustEOLMeterBarlineExtraOffset``.
   '''
   
   def __init__(self, _client):
      '''Bind to client and set line, page, eol_adjustment,
      whitespace, x and y to None.'''
      _Interface.__init__(self, _client)
      _FormatContributor.__init__(self)
      self._alignment_offsets = [ ]
      self._alignment_distances = [ ]
      self._eol_adjustment = None
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
      '''LilyPond ``Score.NonMusicalPaperColumn`` 
      ``#'line-break-system-details`` formatting contribution.

      Contribution appears **before** Abjad component.'''
      result = [ ]
      x = self.x
      y = self.y
      alignment_distances = self.alignment_distances
      alignment_offsets = self.alignment_offsets
      if x is not None or y is not None or alignment_distances or \
         alignment_offsets:
         result.append('\\overrideProperty #"Score.NonMusicalPaperColumn"')
         result.append("#'line-break-system-details")
         temp = [ ]
         if x is not None:
            temp.append('(X-offset . %s)' % x)
         if y is not None:
            temp.append('(Y-offset . %s)' % y)
         if alignment_distances:
            value_vector = ' '.join([str(x) for x in alignment_distances])
            temp.append('(alignment-distances . (%s))' % value_vector)
         if alignment_offsets:
            value_vector = ' '.join([str(x) for x in alignment_offsets])
            temp.append('(alignment-offsets . (%s))' % value_vector)
         temp_str = ' '.join(temp)
         result.append("#'(%s)" % temp_str)
      return result

   ## PUBLIC ATTRIBUTES ##

   @apply
   def alignment_distances( ):
      def fget(self):
         '''LilyPond ``alignment-distances`` list to format as
         ``NonMusicalPaperColumn``. 

         Contribution appears **before** Abjad component.

         ::

            abjad> t = Note(0, (1, 4))
            abjad> t.breaks.alignment_distances = [18, 18, 18]
            abjad> print t.format
            \overrideProperty #"Score.NonMusicalPaperColumn"
            #'line-break-system-details
            #'((alignment-distances . (18, 18, 18)))
            c'4

         .. note:: ``alignment-distances`` replaces ``alignment-offsets``
            in the vertical spacing improvements included in LilyPond
            versions 2.13 and greater.
         '''

         return self._alignment_distances
      def fset(self, expr):
         assert isinstance(expr, (tuple, list))
         self._alignment_distances = expr
      return property(**locals( ))

   @apply
   def alignment_offsets( ):
      def fget(self):
         '''LilyPond ``alignment-offsets`` list to format as
         ``NonMusicalPaperColumn``. 

         Contribution appears **before** Abjad component.

         ::

            abjad> t = Note(0, (1, 4))
            abjad> t.breaks.alignment_offsets = [0, -18, -54, -70]
            abjad> print t.format
            \overrideProperty #"Score.NonMusicalPaperColumn"
            #'line-break-system-details
            #'((alignment-offsets . (0 -18 -54 -70)))
            c'4
         '''

         return self._alignment_offsets
      def fset(self, expr):
         assert isinstance(expr, (tuple, list))
         self._alignment_offsets = expr
      return property(**locals( ))

   @property
   def _closing(self):
      r'''Format contribution at container closing or after leaf.'''
      result = [ ]
      whitespace = self.whitespace
      if whitespace:
         from abjad.tools.layouttools._rational_to_whitespace_measure_string import \
            _rational_to_whitespace_measure_string as \
            layout__rational_to_whitespace_measure_string
         string = layout__rational_to_whitespace_measure_string(whitespace)
         result.extend(string.split('\n'))
      if self.eol_adjustment:
         result.append(r'\adjustEOLMeterBarlineExtraOffset')
      if self.line == True:
         result.append(r'\break')
      elif self.line == False:
         result.append(r'\noBreak')
      if self.page == True:
         result.append(r'\pageBreak')
      elif self.page == False:
         result.append(r'\noPageBreak')
      return result

   @apply
   def eol_adjustment( ):
      def fget(self):
         '''.. versionadded:: 1.1.1
            Read / write boolean set. 

         Set to ``True`` to apply LilyPond ``extra-offset`` to 
         both LilyPond TimeSignature and LilyPond BarLine grobs. 
         
         Otherwise, apply no ``extra-offset``
   
         Raise ``LineBreakError`` when no line break is present.
         '''
         return self._eol_adjustment
      def fset(self, arg):
         assert isinstance(arg, (bool, types.NoneType))
         if arg == True and not self.line:
            raise LineBreakError('missing line break.')
         self._eol_adjustment = arg
      return property(**locals( ))

   @apply
   def line( ):
      def fget(self):
         r'''Boolean setting to contribute LilyPond ``\line`` break.

         Contribution appears **after** Abjad component.
         '''
         return self._line
      def fset(self, arg):
         assert isinstance(arg, bool) or arg is None
         self._line = arg
      return property(**locals( ))

   @property
   def _opening(self):
      '''Format contribution at container opening or before leaf.'''
      result = [ ]
      details = self._line_break_system_details
      if details:
         result.extend(details)
      return result

   @apply
   def page( ):
      def fget(self):
         r'''Boolean setting to contribute LilyPond ``\pageBreak``.
         
         Contribution appears **after** Abjad component.
         '''
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

         Fake measure between ``\stopStaff``, ``\startStaff`` commands.
         '''
         return self._whitespace
      def fset(self, arg):
         from abjad.leaf import _Leaf
         assert isinstance(arg, (int, Rational, types.NoneType))
         if isinstance(self._client, _Leaf):
            raise TypographicWhitespaceError
         self._whitespace = arg
      return property(**locals( ))

   @apply
   def x( ):
      def fget(self):
         '''X-value for ``line-break-system-details`` contribution.

         Contribution appears **before** Abjad component.
         '''
         return self._x
      def fset(self, arg):
         assert isinstance(arg, (int, long, float, types.NoneType))
         self._x = arg
      return property(**locals( ))

   @apply
   def y( ):
      def fget(self):
         '''Y-value for ``line-break-system-details`` contribution.

         Contribution appears **before** Abjad component.
         '''
         return self._y
      def fset(self, arg):
         assert isinstance(arg, (int, long, float, types.NoneType))
         self._y = arg
      return property(**locals( ))

   ## PUBLIC METHODS ##

   def clear(self):
      r'''Set ``line``, ``page``, ``eol_adjustment``, ``x`` and ``y`` 
      to ``None`` and empty ``alignment_distances`` and ``alignment_offsets``.

      ::

         abjad> t = Note(0, (1, 4))
         abjad> t.breaks.line = True
         abjad> t.breaks.eol_adjustment = True
         abjad> t.breaks.x = 20
         abjad> t.breaks.y = 40
         abjad> print t.format
         \overrideProperty #"Score.NonMusicalPaperColumn"
         #'line-break-system-details
         #'((X-offset . 20) (Y-offset . 40))
         c'4
         \adjustEOLMeterBarlineExtraOffset
         \break

      ::

         abjad> t.breaks.clear( )
         abjad> print t.format
         c'4
      '''

      self.__init__(self._client)
