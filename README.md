# python-mockchroot
Python library for using Mock (the chroot-based build tool, not the mockup library)

## How do I use this?

Here is a quick example for building an EPEL7 RPM packge from a sources
dircetory and a spec file, where the build configuration comes from
Fedora Koji:

    out_dir = '/tmp/results'
    mock = MockChroot(config=mock_config.compose(
        mock_config.from_koji(target='epel7-build', koji_profile='koji'),
        mock_config.to['resultdir'].set(out_dir),
        mock_config.to['root_cache_enable'].set(True),
        mock_config.to['yum_cache_enable'].set(True)
    ))
    print('Building SRPM in Mock')
    mock.buildsrpm(
        spec='/path/to/package.spec',
        sources='/path/to/package/sources'
    )
    srpms = glob('{0}/*.src.rpm'.format(out_dir))
    if len(srpms) == 0:
        raise RuntimeError('no srpms found in {0}'.format(out_dir))
    elif len(srpms) > 1:
        raise RuntimeError('multiple srpms found in {0}'.format(out_dir))
    else:
        srpm = srpms[0]
    print('Building RPM in Mock')
    mock.rebuild(src_rpm=srpm, no_clean=True)

## Tell me more!

Please see the comprehensive documentation at [readthedocs][1]

[1]: http://python-mockchroot.readthedocs.org/

## How do I install this?

You can use *pip*:

    pip install mock-chroot

