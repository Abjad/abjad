from abjad.core import _ContextSettingHandler
from abjad.core import _GrobHandler
from abjad.interfaces._Interface import _Interface
import types


class MultiMeasureRestInterface(_Interface, _GrobHandler, _ContextSettingHandler):
   r'''Handle LilyPond MultiMeasureRest grob.
   
   ::

      abjad> staff = Staff([Note(0, (1, 4))])
      abjad> staff.multi_measure_rest.expand_limit = 12
      abjad> staff[0].multi_measure_rest.compress_full_bar_rests = True
      abjad> f(staff)
      \new Staff \with {
         \override MultiMeasureRest #'expand-limit = #12
      } {
         \compressFullBarRests
         c'4
      }
      abjad> staff[0].multi_measure_rest.compress_full_bar_rests = False
      abjad> f(staff)
      \new Staff \with {
         \override MultiMeasureRest #'expand-limit = #12
      } {
         \expandFullBarRests
         c'4
      }
   '''

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'MultiMeasureRest')
      self.compress_full_bar_rests = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def settings(self):
      r'''Read-only list of LilyPond context settings picked up
      at format-time.'''
      result = [ ] 
      if self.compress_full_bar_rests == True:
         result.append(r'\compressFullBarRests')
      elif self.compress_full_bar_rests == False:
         result.append(r'\expandFullBarRests')
      return result

   @apply
   def compress_full_bar_rests( ):
      def fget(self):
         r'''Read / write LilyPond ``compressFullBarRests`` /
         ``expandFullBarRests`` context setting.
         '''
         return self._compress_full_bar_rests
      def fset(self, arg):
         if not isinstance(arg, (bool, type(None))):
            raise TypeError('must be true, false or none.')
         self._compress_full_bar_rests = arg
      return property(**locals( ))
