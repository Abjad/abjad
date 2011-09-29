from abjad import *
from abjad.exceptions import *
from abjad.tools.iotools._LilyPondToken._LilyPondToken import _LilyPondToken
from abjad.tools.sequencetools import flatten_sequence
from abjad.tools.iotools._LilyPondParserComponent._LilyPondParserComponent \
    import _LilyPondParserComponent


class _LilyPondSyntacticalAnalyzer(_LilyPondParserComponent):

    def __call__(self, tokens, lily_string = ''):
        # group sequential containers
        # group parallel containers
        # group directional marks (markup, articulations, etc.)
        # group non-directional marks (dynamics, context marks)
        objects = self._group_containers(tokens, lily_string, 'CONTAINER_OPEN', 'CONTAINER_CLOSE')
        objects = self._group_containers(objects, lily_string, 'PARALLEL_OPEN', 'PARALLEL_CLOSE')
        objects = self._group_scripts(objects, lily_string)
#        objects = self._group_context_marks(objects, lily_string)
#        objects = self._group_leaves(objects, lily_string)
        return objects

    ### PRIVATE METHODS ###

    def _group_containers(self, objects, lily_string, opening_token_kind, closing_token_kind):
        '''Recursively match opening and closing braces.'''
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
                            raise UnmatchedBraceLilyPondParserError(lily_string, token.line, token.column)
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
                raise UnmatchedBraceLilyPondParserError(lily_string, result[0].line, result[0].column)
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

    def _group_scripts(self, objects, lily_string):
        '''Recursively group script tokens (markup, dynamics, articulations etc.).'''

        def recurse(objects):
            result = [ ]
            idx = 0

            while idx < len(objects):
                this = objects[idx]

                if isinstance(this, list): # a container
                    result.append(recurse(this))

                elif isinstance(this, _LilyPondToken) and this.kind == 'ARTICULATION_SHORTCUT':
                    direction, value = this.value
                    result.append(marktools.Articulation(value, direction))

                # explicit direction
                elif isinstance(this, _LilyPondToken) and this.kind == 'DIRECTION':
                    direction = this.value
                    idx += 1
                    this = objects[idx]
                    if isinstance(this, _LilyPondToken) and this.kind in [
                    'ARTICULATION', 'DYNAMIC', 'MARKUP', 'STRING', 'SYMBOL']:
                        object, idx = self._handle_script(objects, idx, direction)
                        result.append(object)
                    else:
                        raise UnparseableTokenLilyPondParserError

                # implicit direction
                elif isinstance(this, _LilyPondToken) and this.kind in [
                    'ARTICULATION', 'DYNAMIC', 'MARKUP']:
                    object, idx = self._handle_script(objects, idx, direction = '-')
                    result.append(object)

                else: # unhandled token or object
                    result.append(this)

                idx += 1
            return result
        return recurse(objects)

    def _handle_script(self, objects, idx, direction = '-'):
        token = objects[idx]

        if token.kind == 'ARTICULATION':
            script = marktools.Articulation(token.value[1:], direction)

        # TODO: DynamicMark really should support a direction string (think piano music).
        elif token.kind == 'DYNAMIC':
            script = contexttools.DynamicMark(token.value[1:])

        elif token.kind == 'MARKUP':
            idx += 1
            next = objects[idx]

            if isinstance(next, _LilyPondToken) and next.kind in ['STRING', 'SYMBOL']:
                script = markuptools.Markup(next.value, direction)

            elif isinstance(next, list) and \
                isinstance(next[0], _LilyPondToken) and \
                next[0].kind == 'CONTAINER_OPEN': # normal markup block
                contents = ' '.join([x.value for x in flatten_sequence(next, klasses = (list,))])
                script = markuptools.Markup(contents, direction)

        elif token.kind == 'STRING':
            script = markuptools.Markup(token.value[1:-1], direction)

        elif token.kind == 'SYMBOL':
            script = markuptools.Markup(token.value, direction)

        else:
            raise UnparseableTokenLilyPondParserError

        return script, idx

    def _group_context_marks(self, objects, lily_string):
        '''Recursively group ContextMark tokens (key, tempo, time signature etc.).'''
        def recurse(objects):
            result = [ ]
            while idx < len(objects):
                this = objects[idx]
                if isinstance(this, list):
                    result.append(recurse(this))
                    idx += 1
                else:
                    result.append(this)
     
