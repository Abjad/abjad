# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.spannertools.Beam import Beam


class MultipartBeam(Beam):
    r'''A multipart beam.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'4 f'8 g'8 r4")
            >>> contextualize(staff).auto_beaming = False
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
            if 1 < len(self._leaves):
                previous_leaf = leaf._get_leaf(-1)
                if id(previous_leaf) not in [id(x) for x in self._leaves]:
                    previous_leaf = None
                next_leaf = leaf._get_leaf(1)
                if id(next_leaf) not in [id(x) for x in self._leaves]:
                    next_leaf = None
                if self._is_my_first_leaf(leaf):
                    if next_leaf is not None:
                        if self._is_beamable_component(next_leaf):
                            string = '{}['.format(direction_string)
                            result.append(string)
                else:
                    if previous_leaf is not None:
                        if not self._is_beamable_component(previous_leaf):
                            if next_leaf is not None:
                                string = '{}['.format(direction_string)
                                result.append(string)
                if self._is_my_last_leaf(leaf):
                    if previous_leaf is not None:
                        if self._is_beamable_component(previous_leaf):
                            result.append(']')
                else:
                    next_leaf = leaf._get_leaf(1)
                    if next_leaf is not None:
                        if not self._is_beamable_component(next_leaf):
                            result.append(']')
        return result
