from abjad.marks import Markup
from abjad.components.Staff import Staff
from abjad.tools import iterate
from abjad.tools import lilyfiletools
from abjad.tools.scoretools.make_piano_score_from_leaves import make_piano_score_from_leaves


def make_piano_sketch_score_from_leaves(leaves):
   r""".. versionadded:: 1.1.2

   Create a two-staff, treble / bass score of `leaves`.

      * Make time signatures and bar numbers transparent.
      * Do not print bar lines or span bars.
      * Set all staff accidental styles to forget.
   """

   score, treble_staff, bass_staff = make_piano_score_from_leaves(leaves)
   lily_file = lilyfiletools.make_basic_lily_file(score)
   score._lily_file = lily_file
   lily_file.layout.indent = 0
   lily_file.paper.tagline = Markup('')

   score.meter.transparent = True
   score.bar_number.transparent = True
   score.bar_line.stencil = False
   score.span_bar.stencil = False

   for staff in iterate.naive_forward_in_expr(score, klass = Staff):
      staff.accidental.style = 'forget'

   return score, treble_staff, bass_staff
