from abjad.tools.containertools.Container import Container
from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools import sequencetools
from abjad.tools.componenttools._split_component_at_index import _split_component_at_index
from abjad.tools.componenttools.all_are_components import all_are_components


def _split_container_by_counts(components, counts, spanners = 'unfractured', cyclic = False):
    '''Partition Python list of zero or more Abjad components.
    Partition by zero or more positive integers in counts list.
    Fracture spanners or not according to keyword.
    Read counts in list cyclically or not according to keyword.
    Return list of component lists.
    # QUESTION: is there any component copying in this function? #
    '''

    # check input
    #assert all_are_components(components, klasses = Container)
    assert isinstance(components, Container)
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
        if isinstance(x, _Leaf):
            part.append(x)
            cum_comp_in_this_part += 1
            comp_still_needed = count - cum_comp_in_this_part
            # if part is now full, fracture spanners right of leaf
            if comp_still_needed == 0:
                _split_component_at_index(x, 100, spanners = spanners)
        # if current component is container
        else:
            # try to grab enough container contents to fill current part
            comp_still_needed = count - cum_comp_in_this_part
            left, right = _split_component_at_index(x, comp_still_needed, spanners = spanners)
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
