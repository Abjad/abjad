from abjad.tools import leaftools
from abjad.tools import sequencetools


def split_container_by_counts(components, counts, fracture_spanners=False, cyclic=False):
    r'''.. versionadded:: 1.1

    Partition Python list of zero or more Abjad components.
    Partition by zero or more positive integers in counts list.
    Fracture spanners or not according to keyword.
    Read counts in list cyclically or not according to keyword.
    Return list of component lists.

    Example 1. Split container cyclically by counts and do not fracture 
    crossing spanners::

        >>> container = Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> voice = Voice([container])
        >>> beam = beamtools.BeamSpanner(voice)
        >>> slur = spannertools.SlurSpanner(container)

    ::

        >>> f(voice)
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }

    ::

        >>> containertools.split_container_by_counts(
        ...     container, [1, 3], cyclic=True, fracture_spanners=False)
        [[{c'8}], [{d'8, e'8, f'8}], [{g'8}], [{a'8, b'8, c''8}]]

    ::

        >>> f(voice)
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
            }
            {
                a'8
                b'8
                c''8 ] )
            }
        }

    Example 2. Split container cyclically by counts and fracture crossing spanners::

        >>> container = Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> voice = Voice([container])
        >>> beam = beamtools.BeamSpanner(voice)
        >>> slur = spannertools.SlurSpanner(container)

    ::

        >>> f(voice)
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }

    ::

        >>> containertools.split_container_by_counts(
        ...     container, [1, 3], cyclic=True, fracture_spanners=True)
        [[{c'8}], [{d'8, e'8, f'8}], [{g'8}], [{a'8, b'8, c''8}]]

    ::

        >>> f(voice)
        \new Voice {
            {
                c'8 ( ) [
            }
            {
                d'8 (
                e'8
                f'8 )
            }
            {
                g'8 ( )
            }
            {
                a'8 (
                b'8
                c''8 ] )
            }
        }

    Example 3. Split container once by counts and do not fracture crossing spanners::

        >>> container = Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> voice = Voice([container])
        >>> beam = beamtools.BeamSpanner(voice)
        >>> slur = spannertools.SlurSpanner(container)

    ::

        >>> f(voice)
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }

    ::

        >>> containertools.split_container_by_counts(
        ...     container, [1, 3], cyclic=False, fracture_spanners=False)
        [[{c'8}], [{d'8, e'8, f'8}], [{g'8, a'8, b'8, c''8}]]

    ::

        >>> f(voice)
        \new Voice {
            {
                c'8 [ (
            }
            {
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }


    Example 4. Split container once by counts and fracture crossing spanners::

        >>> container = Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> voice = Voice([container])
        >>> beam = beamtools.BeamSpanner(voice)
        >>> slur = spannertools.SlurSpanner(container)

    ::

        >>> f(voice)
        \new Voice {
            {
                c'8 [ (
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8 ] )
            }
        }

    ::

        >>> containertools.split_container_by_counts(
        ...     container, [1, 3], cyclic=False, fracture_spanners=True)
        [[{c'8}], [{d'8, e'8, f'8}], [{g'8, a'8, b'8, c''8}]]

    ::

        >>> f(voice)
        \new Voice {
            {
                c'8 ( ) [
            }
            {
                d'8 (
                e'8
                f'8 )
            }
            {
                g'8 (
                a'8
                b'8
                c''8 ] )
            }
        }

    Return list of split parts.
    '''
    from abjad.tools import containertools

    # check input
    assert isinstance(components, containertools.Container)
    components = [components]

    assert sequencetools.all_are_positive_integers(counts)

    # handle empty counts boundary case
    if counts == []:
        return [components[:]]

    # initialize loop variables
    result = []
    part = []
    i = 0
    len_counts = len(counts)
    cum_comp_in_this_part = 0
    xx = components[:]

    # grab one component per loop, but grab new part size only as needed
    while True:
        # get size of next part only if time to fill next part
        if cum_comp_in_this_part == 0:
            # find size of part and store as 'count'
            try:
                if cyclic:
                    count = counts[i % len_counts]
                else:
                    count = counts[i]
            except IndexError:
                break
        # grab new component from list every time through loop
        try:
            x = xx.pop(0)
        except IndexError:
            break
        # if current component is a leaf, add to part
        if isinstance(x, leaftools.Leaf):
            part.append(x)
            cum_comp_in_this_part += 1
            comp_still_needed = count - cum_comp_in_this_part
            # if part is now full, fracture spanners right of leaf
            if comp_still_needed == 0:
                containertools.split_container_at_index(x, 100, fracture_spanners=fracture_spanners)
        # if current component is container
        else:
            # try to grab enough container contents to fill current part
            comp_still_needed = count - cum_comp_in_this_part
            left, right = containertools.split_container_at_index(
                x, comp_still_needed, fracture_spanners=fracture_spanners)
            # accept whatever num of container contents came back and append
            part.append(left)
            cum_comp_in_this_part += len(left)
            # put unused (right) half of partition back on stack
            if len(right):
                xx.insert(0, right)
            comp_still_needed = count - cum_comp_in_this_part
        # if part is now full, appent part and reset loop variables
        if comp_still_needed == 0:
            result.append(part)
            i += 1
            cum_comp_in_this_part = 0
            part = []

    # append stub part, if any
    if len(part):
        result.append(part)

    # append unexamined components, if any
    if len(xx):
        result.append(xx)

    # return list of parts, each of which is, in turn, a list
    return result
