from abjad.components.Container._ContainerFormatterSlotsInterface import _ContainerFormatterSlotsInterface
from abjad.tools import durtools


class _TupletFormatterSlotsInterface(_ContainerFormatterSlotsInterface):
   '''Collect all tuplet format contributions and
   order by the seven canonical format slots.
   '''

   def __init__(self, _client):
      _ContainerFormatterSlotsInterface.__init__(self, _client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      r'''Read-only tuple of format contributions
      to appear before tuplet opening.

      There are four possible types of these and they appear
      in the following canonic order:

      *  User comments to come before tuplet opening
      *  User directives to come before tuplet opening
      *  Interface overrides
      *  Tuplet coloring

      Newly created, unmodified tuplets make no format
      contributions to slot 1. ::

         abjad> t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> import pprint
         abjad> pprint.pprint(t.formatter.slots.slot_1)
         ([(<CommentsInterface>, 'before'), [ ]],
          [(<DirectivesInterface>, 'before'), [ ]],
          [(<InterfaceAggregator>, 'overrides'), [ ]])
         abjad> print t.format
         \times 2/3 {
                 c'8
                 d'8
                 e'8
         }

      Modified tuplets, on the other hand, may make
      format contributions to slot 1. ::

         abjad> t.comments.append('This is a tuplet')
         abjad> t.override.note_head.color = 'red'
         abjad> t.override.dots.color = 'red'
         abjad> import pprint
         abjad> pprint.pprint(t.formatter.slots.slot_1)
         ([(<CommentsInterface>, 'before'), ['% This is a tuplet']],
          [(<DirectivesInterface>, 'before'), [ ]],
          [(<InterfaceAggregator>, 'overrides'),
           ["\\override Dots #'color = #red", "\\override NoteHead #'color = #red"]])
         abjad> print t.format
         % This is a tuplet
         \override Dots #'color = #red
         \override NoteHead #'color = #red
         \times 2/3 {
                 c'8
                 d'8
                 e'8
         }
         \revert Dots #'color
         \revert NoteHead #'color
      '''
      from abjad.tools.formattools._get_grob_override_format_contributions import \
         _get_grob_override_format_contributions

      result = [ ]
      tuplet = self.formatter.tuplet
      result.append(self.wrap(tuplet.comments, 'before'))
      result.append(self.wrap(tuplet.directives, 'before'))

      #result.append(self.wrap(tuplet.interfaces, 'overrides'))
      result.append([('overrides', 'overrides'),
         _get_grob_override_format_contributions(self._client._client)])

      if tuplet.duration.multiplier == 1 and \
         hasattr(tuplet.__class__, 'color'):
         contributor = (tuplet.__class__, 'color')
         contributions = [r"\tweak #'color #blue"]
         result.append([contributor, contributions])
      return tuple(result)

   @property
   def slot_2(self):
      r'''Read-only tuple of format contributions used
      to generate tuplet opening.

      Most tuplets open with the LilyPond ``\times`` command only. ::

         abjad> t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> print t.format
         \times 2/3 {
                 c'8
                 d'8
                 e'8
         }

      This is apparent in the contents of the slot 2. ::

         abjad> pprint.pprint(t.formatter.slots.slot_2)
         ([(<BracketsInterface>, 'open'), ['\\times 2/3 {']],)

      Trivial tuplets carry a ratio of ``1:1``. ::

         abjad> t = tuplettools.FixedDurationTuplet((3, 8), macros.scale(3)
         abjad> t.duration.multiplier
         Fraction(1, 1)

      Such tuplets output unscaled notes and rests. ::

         abjad> print t.format
                 c'8
                 d'8
                 e'8

      For this reason, trivial tuplets make no 
      format contributions to slot 2::

         abjad> pprint.pprint(t.formatter.slots.slot_2)
         ( )

      You can make trivial tuplets format as actual tuplets
      by setting ``color = True`` on the class of
      the tuplet in question.
      Colored trivial tuplets appear blue in printed output. ::

         abjad> t = tuplettools.FixedDurationTuplet((3, 8), macros.scale(3))
         abjad> FixedDurationTuplet.color = True
         abjad> print t.format
         \tweak #'color #blue
         \times 1/1 {
                 c'8
                 d'8
                 e'8
         }
         abjad> pprint.pprint(t.formatter.slots.slot_2)
         ([(<BracketsInterface>, 'open'), ['\\times 1/1 {']],)

      Note that ``color`` is a tuplet class attribute,
      not a tuplet instance attribute.
   
      Finally, settings ``t.is_invisible = True`` causes the tuplet
      to output with the LilyPond ``\scaleDurations`` command
      instead of the the Lilypond ``\times`` command. ::

         abjad> t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> t.is_invisible = True
         abjad> print t.format
         \scaleDurations #'(2 . 3) {
                 c'8
                 d'8
                 e'8
         }
         abjad> pprint.pprint(t.formatter.slots.slot_2)
         ([(tuplettools.FixedDurationTuplet(1/4, [c'8, d'8, e'8]), 'is_invisible'),
           ["\\scaleDurations #'(2 . 3) {"]],)

      Invisible tuplets carry neither tuplet bracket nor
      tuplet ratio in the printed output.
      '''
      result = [ ]
      formatter = self.formatter
      tuplet = formatter.tuplet
      if tuplet.duration.multiplier:
         if tuplet.is_invisible:
            multiplier = tuplet.duration.multiplier
            n, d = multiplier.numerator, multiplier.denominator
            contributor = (tuplet, 'is_invisible')
            contributions = [r"\scaleDurations #'(%s . %s) {" % (n, d)]
            result.append([contributor, contributions])
         else:
            #contributor = (tuplet.brackets, 'open')
            contributor = ('tuplet_brackets', 'open')
            if tuplet.duration.multiplier != 1 or \
               hasattr(tuplet.__class__, 'color'):
               contributions = [r'%s\times %s %s' % (
                  formatter._fraction, 
                  tuplet.duration._multiplier_fraction_string,
                  '{'
                  )]
            else:
               #contributions = [tuplet.brackets.open[0]]
               contributions = ['{']
            result.append([contributor, contributions])
      return tuple(result)

   @property
   def slot_3(self):
      '''Read-only tuple of format contributions to appear
      immediately after tuplet opening.'''
      from abjad.tools.formattools._get_opening_slot_format_contributions import \
         _get_opening_slot_format_contributions
      result = [ ]
      tuplet = self.formatter.tuplet
      result.append(self.wrap(tuplet.comments, 'opening'))
      result.append(self.wrap(tuplet.directives, 'opening'))

      #result.append(self.wrap(tuplet.interfaces, 'opening'))
      result.append([('opening', 'opening'),
         _get_opening_slot_format_contributions(self._client._client)])

      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_5(self):
      '''Read-only tuple of format contributions to appear
      immediately before tuplet closing.'''
      from abjad.tools.formattools._get_closing_slot_format_contributions import \
         _get_closing_slot_format_contributions
      result = [ ]
      tuplet = self.formatter.tuplet

      #result.append(self.wrap(tuplet.interfaces, 'closing'))
      result.append([('closing', 'closing'),
         _get_closing_slot_format_contributions(self._client._client)])

      result.append(self.wrap(tuplet.directives, 'closing'))
      result.append(self.wrap(tuplet.comments, 'closing'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_6(self):
      '''Read-only tuplet of format contributions used
      to generate tuplet closing.
      Usually just a single ``}`` close brace.'''
      result = [ ]
      tuplet = self.formatter.tuplet
      if tuplet.duration.multiplier:
         #result.append(self.wrap(tuplet.brackets, 'close'))
         result.append([('tuplet_brackets', 'close'), '}'])
      return tuple(result)

   @property
   def slot_7(self):
      '''Read-only tuple of format contributions
      to appear immediately after tuplet closing.'''
      from abjad.tools.formattools._get_grob_revert_format_contributions import \
         _get_grob_revert_format_contributions
      result = [ ]
      tuplet = self.formatter.tuplet
      result.append(self.wrap(tuplet.directives, 'after'))

      #result.append(self.wrap(tuplet.interfaces, 'reverts'))
      result.append([('reverts', 'reverts'),
         _get_grob_revert_format_contributions(self._client._client)])

      result.append(self.wrap(tuplet.comments, 'after'))
      return tuple(result)
