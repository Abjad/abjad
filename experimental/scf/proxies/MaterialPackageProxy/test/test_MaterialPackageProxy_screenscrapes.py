import scf


def test_MaterialPackageProxy_screenscrapes_01():
    '''Score material run from studio.
    '''


    studio = scf.studio.Studio()
    studio.run(user_input='all las m black q')

    assert studio.transcript[-2] == \
    ['Las manos m\xc3\xa1gicas - materials - black pcs',
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

    material_proxy = scf.proxies.MaterialPackageProxy('manos.mus.materials.black_pcs')
    material_proxy.run(user_input='q')

    assert material_proxy.transcript[-2] == \
    ['Black pcs',
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
