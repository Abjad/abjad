from abjad.tools.durtools._group import _group as durtools__group


def group_seconds(
   components, durations, fill = 'exact', cyclic = False, rump = False):
   '''Group ``component`` according to ``durations`` in seconds.
      When ``fill == exact``, parts must equal durations exactly.
      When ``fill == less``, parts must be less or equal to durations.
      When ``fill == greater``, parts must be greater or equal to durations.
      If ``cyclic`` is True, read *durations* cyclically.
      If ``rump`` is True and components remain, append as final part.
      If ``rump`` is False and components remain, do not append final part.'''

   duration_type = 'seconds'

   return durtools__group(duration_type, 
      components, durations, fill = fill, cyclic = cyclic, rump = rump)
