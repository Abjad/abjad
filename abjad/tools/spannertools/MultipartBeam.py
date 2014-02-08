# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.spannertools.Beam import Beam


class MultipartBeam(Beam):
    r'''A multipart beam.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'4 f'8 g'8 r4")
            >>> set_(staff).auto_beaming = False
            >>> show(staff) # doctest: +SKIP

        ::

            >>> beam = spannertools.MultipartBeam()
            >>> attach(beam, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                c'8 [
                d'8 ]
                e'4
                f'8 [
                g'8 ]
                r4
            }

    Avoids rests.

    Avoids large-duration notes.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        if not self._is_beamable_component(leaf):
            return lilypond_format_bundle
        direction_string = ''
        if self.direction is not None:
            direction_string = '{} '.format(self.direction)
        beamable_leaf_count = 0
        for _ in self._leaves:
            if self._is_beamable_component(_):
                beamable_leaf_count += 1
        if 2 <= beamable_leaf_count:
            previous_leaf = leaf._get_leaf(-1)
            if previous_leaf not in self._leaves:
                previous_leaf = None
            next_leaf = leaf._get_leaf(1)
            if next_leaf not in self._leaves:
                next_leaf = None
            start_piece = None
            stop_piece = None
            if self._is_my_first_leaf(leaf):
                if next_leaf is not None:
                    if self._is_beamable_component(next_leaf):
                        start_piece = '{}['.format(direction_string)
            else:
                if previous_leaf is not None:
                    if not self._is_beamable_component(previous_leaf):
                        if self._is_beamable_component(next_leaf):
                            start_piece = '{}['.format(direction_string)
            if self._is_my_last_leaf(leaf):
                if previous_leaf is not None:
                    if self._is_beamable_component(previous_leaf):
                        stop_piece = ']'
            else:
                if self._is_beamable_component(previous_leaf):
                    next_leaf = leaf._get_leaf(1)
                    if next_leaf is not None:
                        if not self._is_beamable_component(next_leaf):
                            stop_piece = ']'
            if start_piece and stop_piece:
                lilypond_format_bundle.right.spanner_starts.extend([
                    start_piece, stop_piece])
            elif start_piece:
                lilypond_format_bundle.right.spanner_starts.append(start_piece)
            elif stop_piece:
                lilypond_format_bundle.right.spanner_stops.append(stop_piece)
        return lilypond_format_bundle
