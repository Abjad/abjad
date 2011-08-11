from abjad.checks._Check import _Check


class MispitchedTieCheck(_Check):

    def _run(self, expr):
        '''Check for mispitched notes.
        Do not check tied rests or skips.
        Implement chord-checking later.
        '''
        from abjad.tools.notetools.Note import Note
        from abjad.tools import componenttools
        from abjad.tools import spannertools
        from abjad.tools import tietools
        violators = [ ]
        total = 0
        for leaf in componenttools.iterate_components_forward_in_expr(expr, Note):
            total += 1
            spanners = spannertools.get_spanners_attached_to_component(
                leaf, tietools.TieSpanner)
            if spanners:
                spanner = spanners.pop( )
                if not spanner._is_my_last_leaf(leaf):
                    if leaf._navigator._next_bead:
                        if leaf.written_pitch != leaf._navigator._next_bead.written_pitch:
                            violators.append(leaf)
        return violators, total
