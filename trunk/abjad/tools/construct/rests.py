from abjad.tools import durtools
from abjad.tools.construct._construct_tied_rest import _construct_tied_rest


def rests(durations, direction='big-endian', tied=False):
   '''Return a list of rests.

   * `durations` can be a sinlge duration token or a list of durations.
   * `direction`, a string that may be ``'big-endian'`` or \
      ``'little-endian'``.  When `durations` are not \
      :term:`assignable`, ``'big-endian'`` returns a list of rests \
         in decreasing duration, while ``'little-endian'`` returns a \
         list of rests in increasing duration.
   * `tied`, set to ``True`` to return tied rests, otherwise set to \
      ``False``. Default is ``False``.

   ::

      abjad> construct.rests([(1, 16), (5, 16), (1, 4)])
      [Rest(16), Rest(4), Rest(16), Rest(4)]

   ::

      abjad> construct.rests([(1, 16), (5, 16), (1, 4)], 'little-endian')
      [Rest(16), Rest(16), Rest(4), Rest(4)]

   ::

      abjad> durs = [(1, 16), (5, 16), (1, 4)]
      abjad> construct.rests(durs, 'little-endian', tied = True)
      [Rest(16), Rest(16), Rest(4), Rest(4)]
      abjad> for r in _:
      ...     print r.tie.spanners
      ... 
      set([])
      set([Tie(r16, r4)])
      set([Tie(r16, r4)])
      set([]) '''

   if durtools.is_duration_token(durations):
      durations = [durations]

   result = [ ]
   for d in durations:
      result.extend(_construct_tied_rest(d, direction, tied))
   return result
