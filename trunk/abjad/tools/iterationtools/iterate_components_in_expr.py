# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def iterate_components_in_expr(
    expr,
    component_class=None,
    reverse=False,
    start=0,
    stop=None,
    ):
    r'''Iterate components forward in `expr`.
    '''
    from abjad.tools import spannertools

    component_class = component_class or componenttools.Component

    def component_iterator(expr, component_class, reverse=False):
        if isinstance(expr, component_class):
            yield expr
        if isinstance(expr, (list, tuple, spannertools.Spanner)) or \
            hasattr(expr, '_music'):
            if hasattr(expr, '_music'):
                expr = expr._music
            if reverse:
                expr = reversed(expr)
            for m in expr:
                for x in component_iterator(
                    m, component_class, reverse=reverse):
                    yield x

    def subrange(iter, start=0, stop=None):
        # if start<0, then 'stop-start' gives a funny result
        # don not have to check stop>=start
        # because xrange(stop-start) already handles that
        assert 0 <= start

        try:
            # skip the first few elements, up to 'start' of them:
            for i in xrange(start):
                # no yield to swallow the results
                iter.next()

            # now generate (stop-start) elements
            # (or all elements if stop is none)
            if stop is None:
                for x in iter:
                    yield x
            else:
                for i in xrange(stop-start):
                    yield iter.next()
        except StopIteration:
            # this happens if we exhaust the list before
            # we generate a total of 'stop' elements
            pass

    return subrange(
        component_iterator(
            expr,
            component_class,
            reverse=reverse),
        start,
        stop,
        )
