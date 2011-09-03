import os
import re


class _CodeBlock(object):
    '''Class that handles code-block processing for abjad-book.'''

    def __init__(self):
        self.type = None
        self.images = [ ]
        self.preProcessedCode = [ ] # raw code block
        self.postProcessedCode = [ ]# processed code + code output

        self.filterFromOutput = ['LilyPond input']

    @property
    def final_output_code(self):
        out = _recover_commented_show_directives(self.postProcessedCode)
        out = _remove_hidden_directives(out)
        out = _remove_lines_starting_with(out, self.filterFromOutput)
        out = _insert_abjad_prompt(out, self.preProcessedCode)
        # TODO os.linesep here inserts a white space between every line in
        # Windowz. Using '\r' instead seems to work on both Linux and
        # Windowz. use '\r' instead?
        out = ['\t%s%s' % (line, os.linesep) for line in out]
        return out

    @property
    def to_process_code(self):
        '''Parses pre-processed code and return massaged raw code before
        processing.'''

        result = [ ]
        result.append('print "# START #"')

        codelines = self.preProcessedCode

        # handle code block type
        if self.type == 'hide':
            for i in range(len(codelines)):
                codelines[i] += '<hide'

        for line in codelines:
            # get indentation
            indent = re.search('^ +', line)
            if indent:
                indent = indent.group( )

            # get abjad directive
            if '<hide' in line:
                abj_directive = line.replace('<hide', '#<hide')
            else:
                abj_directive = line

            # handle abjad directive
            if 'show(' in abj_directive:
                abj_directive = '%s#abjad_comment#%s' % ((indent or ''),
                    abj_directive)

            result.append("%sprint '''%s '''" % ((indent or ''), abj_directive))
            result.append(abj_directive)

        return result

    def _collect_images(self):
        for line in self.preProcessedCode:
            if line.startswith('iotools.write'):
                self.images.append(_get_image_name(line))


# HELPERS #

def _insert_abjad_prompt(output_lines, input_lines):
    result = [ ]
    for oline in output_lines:
        oline = oline.rstrip( )
        if oline in input_lines:
            oline = 'abjad> ' + oline
        result.append(oline)
    return result


def _get_image_name(directive):
    try:
        image_name = directive.split(',')[1].split(')')[0]
        image_name = image_name.strip(' ').strip("'").strip('"')
        return image_name
    except IndexError:
        print "Problem parsing 'write( )'. Did you forget to add a file name?"


def _remove_hidden_directives(lines):
    '''remove hidden lines'''
    for line in lines[:]:
        if '#<hide' in line:
            lines.remove(line)
    return lines


def _recover_commented_show_directives(lines):
    ''' remove #abjad_comments# from temporarily commented show( ).'''
    for i, line in enumerate(lines):
        if line.startswith('#abjad_comment#'):
            lines[i] = line.strip('#abjad_comment#')
    return lines


def _remove_lines_starting_with(lines, filters):
    '''Removes all lines starting with strings given in `filters` .'''

    result = [ ]
    for line in lines:
        for f in filters:
            if not line.startswith(f):
                result.append(line)

    return result
