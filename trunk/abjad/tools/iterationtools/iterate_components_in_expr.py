from abjad.tools import componenttools


def iterate_components_in_expr(expr, klass=None, reverse=False, start=0, stop=None):
    r'''.. versionadded:: 2.10

    Iterate components forward in `expr`.
    '''

    klass = klass or componenttools.Component

    def subrange(iter, start=0, stop=None):
        # if start<0, then 'stop-start' gives a funny result
        # dont have to check stop>=start, as xrange(stop-start) already handles that
        assert 0 <= start

        try:
            # Skip the first few elements, up to 'start' of them:
            for i in xrange(start):
                iter.next()  # no 'yield' to swallow the results

            # Now generate (stop-start) elements (or all elements if stop is None)
            if stop is None:
                for x in iter:
                    yield x
            else:
                for i in xrange(stop-start):
                    yield iter.next()
        except StopIteration:
            # This happens if we exhaust the list before
            # we generate a total of 'stop' elements
            pass

    def component_iterator(expr, klass, reverse=False):
        if isinstance(expr, klass):
            yield expr
        if isinstance(expr, (list, tuple)) or hasattr(expr, '_music'):
            if hasattr(expr, '_music'):
                expr = expr._music 
            if reverse:
                expr = reversed(expr)
            for m in expr:
                for x in component_iterator(m, klass, reverse=reverse):
                    yield x
            
    return subrange(component_iterator(expr, klass, reverse=reverse), start, stop)
