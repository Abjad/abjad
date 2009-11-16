from abjad.markup import Markup
from abjad.tools import iterate
from abjad.tools import lilytools
from abjad.staff import Staff
from make_piano_score import make_piano_score


def make_piano_sketch_score(leaves):
   r""".. versionadded:: 1.1.2

   Create a two-staff, treble / bass score of `leaves`.

      * Make time signatures and bar numbers transparent.
      * Do not print bar lines or span bars.
      * Set all staff accidental styles to forget.
   """

   score, treble_staff, bass_staff = make_piano_score(leaves)
   lily_file = lilytools.make_basic_lily_file(score)
   score._lily_file = lily_file
   lily_file.layout.indent = 0
   lily_file.paper.tagline = Markup('')

   score.meter.transparent = True
   score.bar_number.transparent = True
   score.bar_line.stencil = False
   score.span_bar.stencil = False

   for staff in iterate.naive_forward_in(score, klass = Staff):
      staff.accidental.style = 'forget'

   return score, treble_staff, bass_staff
