from abjad.tools import gracetools
from abjad.tools import mathtools
from abjad.tools.spannertools.MetricGridSpanner._MetricGridSpannerFormatInterface import _MetricGridSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class MetricGridSpanner(Spanner):
    r'''Abjad metric grid spanner::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")

    ::

        abjad> spannertools.MetricGridSpanner(staff.leaves, meters = [(1, 8), (1, 4)])
        MetricGridSpanner(c'8, d'8, e'8, f'8, g'8, a'8, b'8, c'8)

    ::

        abjad> f(staff)
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

    def __init__(self, components = None, meters = None):
        Spanner.__init__(self, components)
        self._format = _MetricGridSpannerFormatInterface(self)
        self._meters = meters
        self.hide = False

    ### PRIVATE METHODS ###

    # DEPRECATED: DO NOT USE.
#   def _fuse_tied_leaves_within_measures(self):
#      from abjad.tools import leaftools
#      from abjad.tools import spannertools
#      from abjad.tools import tietools
#      # fuse tied notes
#      meters = self.meters
#      #meter = meters.next()
#      meter, moffset, temp_hide = meters.next()
#      leaves_in_meter = [[]]
#      leaf = self.leaves[0]
#      # group leaves by measure.
#      while leaf:
#         #if leaf._offset.start < meter._offset + meter.duration:
#         if leaf._offset.start < moffset + meter.duration:
#            leaves_in_meter[-1].append(leaf)
#            #leaf = leaf.next
#            leaf = leaftools.get_nth_leaf_in_thread_from_leaf(leaf, 1)
#         else:
#            try:
#               #meter = meters.next()
#               meter, moffset, temp_hide = meters.next()
#               leaves_in_meter.append([])
#            except StopIteration:
#               break
#      # group together leaves in same measure that are tied together.
#      for leaves in leaves_in_meter:
#         result = [[]]
#         if 0 < len(leaves):
#            #if leaves[0].tie.spanned:
#            if tietools.is_component_with_tie_spanner_attached(leaves[0]):
#               #sp = leaves[0].tie.spanner
#               sp = spannertools.get_the_only_spanner_attached_to_component(
#                  leaves[0], tietools.TieSpanner)
#            else:
#               sp = None
#         for l in leaves:
#            #if l.tie.spanned and l.tie.spanner == sp:
#            if tietools.is_component_with_tie_spanner_attached(l):
#               if spannertools.get_the_only_spanner_attached_to_component(
#                  l, tietools.TieSpanner) == sp:
#                  result[-1].append(l)
#            else:
#               #if l.tie.spanned:
#               if tietools.is_component_with_tie_spanner_attached(l):
#                  #sp = l.tie.spanner
#                  sp = spannertools.get_the_only_spanner_attached_to_component(
#                     l, tietools.TieSpanner)
#               else:
#                  sp = None
#               result.append([])
#         # fuse leaves
#         for r in result:
#            # keep last after graces, if any
#            # TODO: this is very hacky. Find better solution
#            if 0 < len(r):
#               #r[0].grace.after = r[-1].grace.after
#               #r[0].after_grace.extend(r[-1].after_grace)
#               gracetools.Grace([r[-1]], kind = 'after')(r[0])
#            leaftools.fuse_leaves_big_endian(r)

    def _matching_meter(self, leaf):
        '''Return the MetricStrip for which meter._offset == leaf._offset.
        '''
        #for m in self.meters:
        for m, moffset, temp_hide in self.meters:
            #if leaf._offset.start == m._offset:
            if leaf._offset.start == moffset:
                return m, temp_hide

    def _slicing_meters(self, leaf):
        '''Return the MetricStrip(s) that slices leaf, if any.
        '''
        #for m in self.meters:
        for m, moffset, temp_hide in self.meters:
            #if leaf._offset.start < m._offset:
            if leaf._offset.start < moffset:
                #if m._offset < leaf._offset.stop:
                if moffset < leaf._offset.stop:
                    yield m, moffset, temp_hide
                else:
                    break

    ### PUBLIC ATTRIBUTES ###

    @apply
    def meters():
        def fget(self):
            '''Get metric grid meters::

                abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")
                abjad> metric_grid_spanner = spannertools.MetricGridSpanner(staff.leaves, meters = [(1, 8), (1, 4)])
                abjad> list(metric_grid_spanner.meters)
                [(TimeSignatureMark((1, 8)), 0, False), (TimeSignatureMark((1, 4)), Duration(1, 8), False), (TimeSignatureMark((1, 8)), Duration(3, 8), False), (TimeSignatureMark((1, 4)), Duration(1, 2), False), (TimeSignatureMark((1, 8)), Duration(3, 4), False), (TimeSignatureMark((1, 4)), Duration(7, 8), False)]

            Set metric grid meters::

                abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c'8")
                abjad> metric_grid_spanner = spannertools.MetricGridSpanner(staff.leaves, meters = [(1, 8), (1, 4)])
                abjad> metric_grid_spanner.meters = [Duration(1, 4)]
                abjad> list(metric_grid_spanner.meters)
                [(TimeSignatureMark((1, 4)), 0, False), (TimeSignatureMark((1, 4)), Duration(1, 4), True), (TimeSignatureMark((1, 4)), Duration(1, 2), True), (TimeSignatureMark((1, 4)), Duration(3, 4), True)]

            Set iterable.
            '''
            from abjad.tools import contexttools
            i = 0
            moffset = 0
            prev_meter = None
            #while moffset < self.duration:
            while moffset < self.prolated_duration:
                m = self._meters[i % len(self._meters)]
                m = contexttools.TimeSignatureMark(m)
                # new attribute
                #m._offset = moffset
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

    def split_on_bar(self):
        '''Temporarily unavailable.
        '''
        from abjad.tools import componenttools
        leaves = [leaf for leaf in self.leaves if self.splitting_condition(leaf)]
        componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(
            leaves, [x[0].duration for x in self.meters], tie_after = True)
        #self._fuse_tied_leaves_within_measures()

    def splitting_condition(self, leaf):
        r'''User-definable boolean function to determine whether leaf should be split::

            abjad> voice = Voice("c'4 r4 c'4")

        ::

            abjad> f(voice)
            \new Voice {
                c'4
                r4
                c'4
            }

        ::

            abjad> def cond(leaf):
            ...   if not isinstance(leaf, Rest): return True
            ...   else: return False
            abjad> metric_grid_spanner = spannertools.MetricGridSpanner(voice.leaves, [Duration(1, 8)])
            abjad> metric_grid_spanner.splitting_condition = cond

        ::

            abjad> metric_grid_spanner.split_on_bar()

        ::

            abjad> f(voice)
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
