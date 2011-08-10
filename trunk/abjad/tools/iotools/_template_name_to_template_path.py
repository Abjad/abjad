from abjad.cfg.cfg import ABJADPATH
import os


def _template_name_to_template_path(template_name):
    '''Change `template_name` to template path.
    '''

    if not template_name.endswith('.ly'):
        template_name += '.ly'
    template_path = os.path.join(ABJADPATH, 'templates', template_name)
    return template_path
