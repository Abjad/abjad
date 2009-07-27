from abjad.container.slots import _ContainerFormatterSlotsInterface
from abjad.tools import durtools


class _TupletFormatterSlotsInterface(_ContainerFormatterSlotsInterface):
   '''Collect all tuplet format contributions and \
      order by the seven canonical format slots.

      *  Every slots interface binds to a formatter.
      *  The :class:`_TupletFormatterSlotsInterface \
         <abjad.tuplet.slots._TupletFormatterSlotsInterface>`
         described here binds to the :class:`_TupletFormatter \
         <abjad.tuplet.formatter._TupletFormatter>`.

      ::

         
         abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
         abjad> t.formatter
         <_TupletFormatter>

      ::

         abjad> t.formatter.slots
         <_TupletFormatterSlotsInterface>'''

   def __init__(self, _client):
      '''Init as type of :class:`_ContainerFormatterSlotsInterface \
         <abjad.container.slots._ContainerFormatterSlotsInterface>`.'''

      _ContainerFormatterSlotsInterface.__init__(self, _client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      r'''Read-only tuple of format contributions \
         to appear before tuplet opening.

         There are four possible types of these and they appear \
         in the following canonic order:

         *  User comments to come before tuplet opening
         *  User directives to come before tuplet opening
         *  Interface overrides
         *  Tuplet coloring

         Newly created, unmodified tuplets make no format \
         contributions to slot 1::

            abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))

         ::

            abjad> import pprint
            abjad> pprint.pprint(t.formatter.slots.slot_1)
            ([(<UserComments>, 'before'), []],
             [(<UserDirectivesInterface>, 'before'), []],
             [(<InterfaceAggregator>, 'overrides'), []])

         ::

            abjad> print t.format
            \times 2/3 {
                    c'8
                    d'8
                    e'8
            }

         Modified tuplets, on the other hand, may make \
         format contributions to slot 1::

            abjad> t.comments.append('This is a tuplet')
            abjad> t.notehead.color = 'red'
            abjad> t.dots.color = 'red'
     
         ::

            abjad> import pprint
            abjad> pprint.pprint(t.formatter.slots.slot_1)
            ([(<UserComments>, 'before'), ['% This is a tuplet']],
             [(<UserDirectivesInterface>, 'before'), []],
             [(<InterfaceAggregator>, 'overrides'),
              ["\\override Dots #'color = #red", "\\override NoteHead #'color = #red"]])
   
         ::

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
            \revert NoteHead #'color'''

      result = [ ]
      tuplet = self.formatter.tuplet
      result.append(self.wrap(tuplet.comments, 'before'))
      result.append(self.wrap(tuplet.directives, 'before'))
      result.append(self.wrap(tuplet.interfaces, 'overrides'))
      if tuplet.duration.multiplier == 1 and \
         hasattr(tuplet.__class__, 'color'):
         contributor = (tuplet.__class__, 'color')
         contributions = [r"\tweak #'color #blue"]
         result.append([contributor, contributions])
      return tuple(result)

   @property
   def slot_2(self):
      r'''Read-only tuple of format contributions used \
         to generate tuplet opening.

         Most tuplets open with the *LilyPond* ``\times`` command only::

            abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))

         ::

            abjad> print t.format
            \times 2/3 {
                    c'8
                    d'8
                    e'8
            }

         This is apparent in the contents of the slot 2::

            abjad> pprint.pprint(t.formatter.slots.slot_2)
            ([(<BracketsInterface>, 'open'), ['\\times 2/3 {']],)

         Trivial tuplets carry a ratio of ``1:1``::

            abjad> t = FixedDurationTuplet((3, 8), construct.scale(3)
            abjad> t.duration.multiplier
            Rational(1, 1)

         Such tuplets output unscaled notes and rests::

            abjad> print t.format
                    c'8
                    d'8
                    e'8

         For this reason, trivial tuplets make no \
         format contributions to slot 2::

            abjad> pprint.pprint(t.formatter.slots.slot_2)
            ()

         You can make trivial tuplets format as actual tuplets \
         by setting ``color = True`` on the class of \
         the tuplet in question. \
         Colored trivial tuplets appear blue in printed output::

            abjad> t = FixedDurationTuplet((3, 8), construct.scale(3))
            abjad> FixedDurationTuplet.color = True

         ::

            abjad> print t.format
            \tweak #'color #blue
            \times 1/1 {
                    c'8
                    d'8
                    e'8
            }

         ::

            abjad> pprint.pprint(t.formatter.slots.slot_2)
            ([(<BracketsInterface>, 'open'), ['\\times 1/1 {']],)

         Note that ``color`` is a tuplet class attribute, \
         not a tuplet instance attribute.
      
         Finally, settings ``t.invisible = True`` causes the tuplet \
         to output with the *LilyPond* ``\scaleDurations`` command \
         instead of the the *Lilypond* ``\times`` command::

            abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
            abjad> t.invisible = True

         ::

            abjad> print t.format
            \scaleDurations #'(2 . 3) {
                    c'8
                    d'8
                    e'8
            }

         ::

            abjad> pprint.pprint(t.formatter.slots.slot_2)
            ([(FixedDurationTuplet(1/4, [c'8, d'8, e'8]), 'invisible'),
              ["\\scaleDurations #'(2 . 3) {"]],)

         Invisible tuplets carry neither tuplet bracket nor \
         tuplet ratio in the printed output.'''

      result = [ ]
      formatter = self.formatter
      tuplet = formatter.tuplet
      if tuplet.duration.multiplier:
         if tuplet.duration.multiplier != 1 or \
            hasattr(tuplet.__class__, 'color'):
            if tuplet.invisible:
               multiplier = tuplet.duration.multiplier
               n, d = multiplier._n, multiplier._d
               contributor = (tuplet, 'invisible')
               contributions = [r"\scaleDurations #'(%s . %s) {" % (n, d)]
               result.append([contributor, contributions])
            else:
               contributor = (tuplet.brackets, 'open')
               contributions = [r'%s\times %s %s' % (
                  formatter._fraction, 
                  durtools.to_fraction(tuplet.duration.multiplier), 
                  tuplet.brackets.open[0])]
               result.append([contributor, contributions])
      return tuple(result)

   @property
   def slot_3(self):
      '''Read-only tuple of format contributions to appear \
         immediately after tuplet opening.'''

      result = [ ]
      tuplet = self.formatter.tuplet
      result.append(self.wrap(tuplet.comments, 'opening'))
      result.append(self.wrap(tuplet.directives, 'opening'))
      result.append(self.wrap(tuplet.interfaces, 'opening'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_5(self):
      '''Read-only tuple of format contributions to appear \
         immediately before tuplet closing.'''

      result = [ ]
      tuplet = self.formatter.tuplet
      result.append(self.wrap(tuplet.interfaces, 'closing'))
      result.append(self.wrap(tuplet.directives, 'closing'))
      result.append(self.wrap(tuplet.comments, 'closing'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_6(self):
      '''Read-only tuplet of format contributions used \
         to generate tuplet closing. \
         Usually just a single ``}`` close brace.'''
   
      result = [ ]
      tuplet = self.formatter.tuplet
      if tuplet.duration.multiplier:
         if tuplet.duration.multiplier != 1 or \
            hasattr(tuplet.__class__, 'color'):
            result.append(self.wrap(tuplet.brackets, 'close'))
      return tuple(result)

   @property
   def slot_7(self):
      '''Read-only tuple of format contributions \
         to appear immediately after tuplet closing.'''

      result = [ ]
      tuplet = self.formatter.tuplet
      result.append(self.wrap(tuplet.directives, 'after'))
      result.append(self.wrap(tuplet.interfaces, 'reverts'))
      result.append(self.wrap(tuplet.comments, 'after'))
      return tuple(result)
