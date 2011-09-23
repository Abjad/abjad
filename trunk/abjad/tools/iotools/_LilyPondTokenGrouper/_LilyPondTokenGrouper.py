from abjad.exceptions import *
from abjad.tools.iotools._LilyPondToken._LilyPondToken import _LilyPondToken


class _LilyPondTokenGrouper(object):

    def __call__(self, tokens, lily_string = ''):
        # group sequential containers
        # group parallel containers
        # group directional marks (markup, articulations, etc.)
        # group non-directional marks (dynamics, context marks)
        objects = self._group_containers(tokens, lily_string, 'CONTAINER_OPEN', 'CONTAINER_CLOSE')
        objects = self._group_containers(objects, lily_string, 'PARALLEL_OPEN', 'PARALLEL_CLOSE')
#        objects = self._group_marks(objects, lily_string)
#        objects = self._group_leaves(objects, lily_string)
        return objects

    ### PRIVATE METHODS ###

    def _group_containers(self, objects, lily_string, opening_token_kind, closing_token_kind):
        def recurse(objects, idx = 0, depth = 0):
            result = [ ]
            level = 0
            while idx < len(objects):
                if isinstance(objects[idx], _LilyPondToken):
                    token = objects[idx]

                    if token.kind == opening_token_kind:
                        if not result and 0 < depth:
                            result.append(token)
                            level += 1
                            idx += 1
                        else:
                            subresult, idx = recurse(objects, idx = idx, depth = depth + 1)
                            result.append(subresult)

                    elif token.kind == closing_token_kind:
                        if level != 1:
                            raise UnmatchedBraceLilyPondParserError(token.position, lily_string)
                        level -= 1
                        result.append(token)
                        idx += 1
                        return result, idx

                    else:
                        result.append(token)
                        idx += 1

                elif isinstance(objects[idx], list):
                    subresult, subidx = recurse(objects[idx], idx = 0, depth = 0)
                    result.append(subresult)
                    idx += 1

                else:
                    result.append(objects[idx])
                    idx += 1

            if level != 0:
                raise UnmatchedBraceLilyPondParserError(result[0].position, lily_string)
            return result, idx

        objects = recurse(objects)[0]
        if 1 == len(objects) and isinstance(objects[0], list):
            return objects[0]
        return objects

    def _group_leaves(self, objects, lily_string):
        def recurse(objects):
            result = [ ]
            while idx < len(objects):
                this = objects[idx]
                if isinstance(this, list):
                    result.append(recurse(this))
                    idx += 1
                elif isinstance(this, _LilyPondToken) and \
                    this.kind in ['CHORD_OPEN', 'PITCH_CLASS', 'REST', 'SKIP']:
                    # what happens if this runs into a pitch class sitting in a key-sig block?
                    # or an identifier in a markup block?
                    result.append(this)
                    idx += 1
                else:
                    result.append(this)
                    idx += 1
            return result
        return objects

    def _group_marks(self, objects, lily_string):
        def recurse(objects):
            result = [ ]
            while idx < len(objects):
                this = objects[idx]
            return result
        return result
