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

    def _format_right_of_leaf(self, leaf):
        result = []
        direction_string = ''
        if self.direction is not None:
            direction_string = '{} '.format(self.direction)
        if self._is_beamable_component(leaf):
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
                if self._is_my_first_leaf(leaf):
                    if next_leaf is not None:
                        if self._is_beamable_component(next_leaf):
                            string = '{}['.format(direction_string)
                            result.append(string)
                else:
                    if previous_leaf is not None:
                        if not self._is_beamable_component(previous_leaf):
                            if self._is_beamable_component(next_leaf):
                                string = '{}['.format(direction_string)
                                result.append(string)
                if self._is_my_last_leaf(leaf):
                    if previous_leaf is not None:
                        if self._is_beamable_component(previous_leaf):
                            result.append(']')
                else:
                    if self._is_beamable_component(previous_leaf):
                        next_leaf = leaf._get_leaf(1)
                        if next_leaf is not None:
                            if not self._is_beamable_component(next_leaf):
                                result.append(']')
        return result

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        lilypond_format_bundle.get('before').spanners.extend(
            self._format_before_leaf(leaf))
        lilypond_format_bundle.get('right').spanners.extend(
            self._format_right_of_leaf(leaf))
        lilypond_format_bundle.get('after').spanners.extend(
            self._format_after_leaf(leaf))
        return lilypond_format_bundle
