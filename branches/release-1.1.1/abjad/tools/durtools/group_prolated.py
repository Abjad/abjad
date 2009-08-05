from abjad.tools.durtools._group import _group as durtools__group


def group_prolated(
   components, durations, fill = 'exact', cyclic = False, rump = False):
   '''Group ``component`` according to prolated ``durations``.

         * When ``fill == exact``, parts must equal durations exactly.
         * When ``fill == less``, parts must be <= durations.
         * When ``fill == greater``, parts must be >= durations.
         * If ``cyclic`` True, read *durations* cyclically.
         * If ``rump`` True and components remain, append final part.
         * If ``rump`` False and components remain, do not append final part.
   '''
   
   duration_type = 'prolated'

   return durtools__group(duration_type,
      components, durations, fill = fill, cyclic = cyclic, rump = rump)
