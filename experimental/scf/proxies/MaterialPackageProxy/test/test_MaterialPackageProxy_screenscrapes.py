import py
import scf


def test_MaterialPackageProxy_screenscrapes_01():
    '''Score material run from studio.
    '''
    py.test.skip('TODO: add Example Score I time signatures.')


    studio = scf.studio.Studio()
    studio.run(user_input='all example_score_1 m black q')

    assert studio.transcript[-2] == \
    ['Example Score I (2013) - materials - time signatures',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     output material - make (omm)',
      '     output material - view (omv)',
      '',
      '     illustration builder - edit (ibe)',
      '     illustration builder - execute (ibx)',
      '     score stylesheet - select (sss)',
      '',
      '     output pdf - make (pdfm)',
      '     output pdf - view (pdfv)',
      '']


def test_MaterialPackageProxy_screenscrapes_02():
    '''Score material run independently.
    '''
    py.test.skip('TODO: add Example Score I time signatures.')

    material_proxy = scf.proxies.MaterialPackageProxy('example_score_1.mus.materials.time_signatures')
    material_proxy.run(user_input='q')

    assert material_proxy.transcript[-2] == \
    ['Time signatures',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     output material - make (omm)',
      '     output material - view (omv)',
      '',
      '     illustration builder - edit (ibe)',
      '     illustration builder - execute (ibx)',
      '     score stylesheet - select (sss)',
      '',
      '     output pdf - make (pdfm)',
      '     output pdf - view (pdfv)',
      '']
