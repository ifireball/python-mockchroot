mock_chroot tutorial
====================

`mock_chroot` lets you create *mock(1)* based chroot environemnts and run
operations inside them. `mock_chroot` supports running generic shell commands
as well as some higher-level operations supported by mock such as building an
*RPM* package.

Basic usage
-----------

To create a *chroot* environemnt you need to simply create a `MockChroot`
object::

    from mock_chroot import MockChroot

    mc = MockChroot(root='epel-6-x86_64')

The ``root`` argument is equivalent to the ``--root`` option of the *mock(1)*
command, it takes the name of a pre-packaged chroot configuration file or a path
to a custom configuration file.

Once you have a `MockChroot` object you can use it to perform operations
inside the *chroot* envoronment::

    output = mc.chroot('cat', '/etc/issue')


Custom configuration
--------------------

The power of the `mock_chroot` module lies with the ability it provides to
customize the *mock* environment from code. The most basic use is to create the
configuration from a string::

    # We read the configuration from a file here to avoid including an
    # unwieldy configuration string in the example
    with open('/etc/mock/epel-7-x86_64.cfg') as f:
        custom_cfg = f.read()

    mc = MockChroot(config=custom_cfg)

Just reading configuration from files is not very interesting, so
`mock_chroot` includes the `config` module which allows for programatically
creating configuration snippets and composing them together::

    import mock_chroot.config

    mc = MockChroot(config=mock_chroot.config.compose(
        custom_cfg,
        mock_chroot.config.bind_mount(
            ('/dir/outside/chroot', '/dir/inside/chroot')
        )
    ))

The `config` module supports configuring various aspects of the *chroot*
enviromnet including bind-mounts into it, creating files, setting environment
variables and setting up network connectivity.

We can also perform more fine-grained configuration using the
`mock_chroot.config.to` function::

    mc = MockChroot(config=mock_chroot.config.compose(
        custom_cfg,
        mock_chroot.config.to['resultdir'].set(out_dir),
        mock_chroot.config.to['root_cache_enable'].set(True),
        mock_chroot.config.to['yum_cache_enable'].set(True)
    ))

Koji-based configuration
------------------------

The (`koji <https://fedorahosted.org/koji/>`_) build system can generate
*mock(1)* configuration to allow one to imitate the build environments it
creates. We can leverage this functionality using the
`mock_chroot.config.from_koji` function::

    mc = MockChroot(config=mock_chroot.config.from_koji(
        tag='epel7-build',
        koji_profile='koji',
    ))

The function can be combined with other `config` finctions to further customize
the configuration::

    mc = MockChroot(config=mock_chroot.config.compose(
        mock_chroot.config.from_koji(tag='epel7-build', koji_profile='koji'),
        mock_chroot.config.to['resultdir'].set(out_dir),
    ))

