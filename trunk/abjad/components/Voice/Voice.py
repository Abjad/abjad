from abjad.components._Context import _Context


class Voice(_Context):
   r'''Abjad model of a voice:

   ::

      abjad> voice = Voice(macros.scale(4))
      abjad> f(voice)
      \new Voice {
         c'8
         d'8
         e'8
         f'8
      }
   '''

   __slots__ = ('_is_nonsemantic', )

   def __init__(self, music = None, **kwargs):
      _Context.__init__(self, music)
      self.context = 'Voice'
      self._initialize_keyword_values(**kwargs)
      self.is_nonsemantic = False

   ## PUBLIC ATTRIBUTES ##

   @apply
   def is_nonsemantic( ):
      def fget(self):
         r'''Set indicator of nonsemantic voice::

            abjad> measures = measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (5, 16), (5, 16))
            abjad> voice = Voice(measures)
            abjad> voice.name = 'HiddenTimeSignatureVoice'

         ::

            abjad> voice.is_nonsemantic = True

         ::

            abjad> f(voice)
            \context Voice = "HiddenTimeSignatureVoice" {
               {
                  \time 1/8
                  s1 * 1/8
               }
               {
                  \time 5/16
                  s1 * 5/16
               }
               {
                  \time 5/16
                  s1 * 5/16
               }
            }
      
         ::

            abjad> voice.is_nonsemantic
            True

         Get indicator of nonsemantic voice::

            abjad> voice = Voice([ ])

         ::

            abjad> voice.is_nonsemantic
            False

         Return boolean.

         The intent of this read / write attribute is to allow composers to tag invisible
         voices used to house time signatures indications, bar number directives or other 
         pieces of score-global non-musical information. Such nonsemantic voices can then
         be omitted from voice interation and other functions.
         '''
         return self._is_nonsemantic
      def fset(self, arg):
         if not isinstance(arg, type(True)):
            raise TypeError
         self._is_nonsemantic = arg
      return property(**locals( ))
