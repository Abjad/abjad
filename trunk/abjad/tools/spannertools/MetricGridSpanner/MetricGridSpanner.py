from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import gracetools
from abjad.tools import mathtools
from abjad.tools import skiptools
from abjad.tools.spannertools.Spanner import Spanner


class MetricGridSpanner(Spanner):
    r'''Abjad metric grid spanner::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")

    ::

        >>> spannertools.MetricGridSpanner(staff.leaves, meters=[(1, 8), (1, 4)])
        MetricGridSpanner(c'8, d'8, e'8, f'8, g'8, a'8, b'8, c'8)

    ::

        >>> f(staff)
        \new Staff {
            \time 1/8
            c'8
            \time 1/4
            d'8
            e'8
            \time 1/8
            f'8
            \time 1/4
            g'8
            a'8
            \time 1/8
            b'8
            \time 1/4
            c'8
        }

    Format leaves in spanner cyclically with `meters`.

    Return metric grid spanner.
    '''

    def __init__(self, components=None, meters=None):
        Spanner.__init__(self, components)
        self._meters = meters
        self.hide = False

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._meters = self._meters
        new.hide = self.hide

    def _format_after_leaf(self, leaf):
        result = []
        if hasattr(self, '_slicing_metersFound'):
            delattr(self, '_slicing_metersFound')
            result.append('>>')
        return result

    #FIXME: formatting is ridiculously slow.
    #         find a way to make it faster.
    # Tue Jan 13 12:05:43 EST 2009 [VA] using _slicing_metersFound boolean
    # flag now to improve performance time. Better but still not perfect.

    def _format_before_leaf(self, leaf):
        result = []
        if not self.hide:
            #meter = self._matching_meter(leaf)
            matching_meter = self._matching_meter(leaf)
            if matching_meter is None:
                meter = None
            else:
                meter, temp_hide = matching_meter
            #if meter and not getattr(meter, '_temp_hide', False):
            if meter and not temp_hide:
                result.append(meter.lilypond_format)
            #m = self._slicing_meters(leaf)
            m = self._slicing_meters(leaf)
            #m = [meter for meter in m if not getattr(meter, '_temp_hide', False)]
            m = [triple for triple in m if not triple[-1]]
            if m:
                # set self._slicing_metersFound as temporary flag so that
                # self._after does not have to recompute _slicing_meters()
                self._slicing_metersFound = True
                result.append('<<')
                for meter, moffset, temp_hide in m:
                    s = skiptools.Skip(durationtools.Duration(1))
                    s.duration_multiplier = moffset - leaf.start_offset
                    numerator, denominator = meter.numerator, meter.denominator
                    mark = contexttools.TimeSignatureMark((numerator, denominator))(s)
                    mark._is_cosmetic_mark = True
                    container = containertools.Container([s])
                    result.append(container.lilypond_format)
        return result

    def _matching_meter(self, leaf):
        for m, moffset, temp_hide in self.meters:
            if leaf.start_offset == moffset:
                return m, temp_hide

    def _slicing_meters(self, leaf):
        '''Return the MetricStrip(s) that slices leaf, if any.
        '''
        for m, moffset, temp_hide in self.meters:
            if leaf.start_offset < moffset:
                if moffset < leaf.stop_offset:
                    yield m, moffset, temp_hide
                else:
                    break

    ### PUBLIC PROPERTIES ###

    @apply
    def meters():
        def fget(self):
            '''Get metric grid meters::

                >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")
                >>> metric_grid_spanner = spannertools.MetricGridSpanner(
                ...     staff.leaves, meters=[(1, 8), (1, 4)])

            Set metric grid meters::

                >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")
                >>> metric_grid_spanner = spannertools.MetricGridSpanner(
                ...     staff.leaves, meters=[(1, 8), (1, 4)])
                >>> metric_grid_spanner.meters = [Duration(1, 4)]

            Set iterable.
            '''
            i = 0
            moffset = 0
            prev_meter = None
            #while moffset < self.duration:
            while moffset < self.prolated_duration:
                m = self._meters[i % len(self._meters)]
                m = contexttools.TimeSignatureMark(m)
                # new attribute
                if prev_meter and prev_meter == m:
                    #m.hide = True
                    #m._temp_hide = True
                    temp_hide = True
                else:
                    temp_hide = False
                #yield m
                yield m, moffset, temp_hide
                moffset += m.duration
                i += 1
                prev_meter = m
        def fset(self, meters):
            assert isinstance(meters, list)
            self._meters = meters
        return property(**locals())

    ### PUBLIC METHODS ###

    # TODO: looks like these tests are working now?
    def split_on_bar(self):
        '''Temporarily unavailable.
        '''

        leaves = [leaf for leaf in self.leaves if self.splitting_condition(leaf)]
        #self._debug(leaves, 'leaves')
        componenttools.split_components_at_offsets(leaves, [x[0].duration for x in self.meters], 
            cyclic=True, fracture_spanners=False, tie_split_notes=True)
        #self._fuse_tied_leaves_within_measures()

    def splitting_condition(self, leaf):
        r'''User-definable boolean function to determine whether leaf should be split::

            >>> voice = Voice("c'4 r4 c'4")

        ::

            >>> f(voice)
            \new Voice {
                c'4
                r4
                c'4
            }

        ::

            >>> def cond(leaf):
            ...   if not isinstance(leaf, Rest): return True
            ...   else: return False
            >>> metric_grid_spanner = spannertools.MetricGridSpanner(
            ...     voice.leaves, [Duration(1, 8)])
            >>> metric_grid_spanner.splitting_condition = cond

        ::

            >>> metric_grid_spanner.split_on_bar()

        ::

            >>> f(voice)
            \new Voice {
                \time 1/8
                c'8 ~
                c'8
                r4
                c'8 ~
                c'8
            }

        Function defaults to return true.
        '''
        return True
