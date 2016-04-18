mock_chroot.config Package reference
====================================

:mod:`mock_chroot.config` Package
---------------------------------

.. automodule:: mock_chroot.config
    :members: file, env_vars, use_host_resolv
    :member-order: bysource

    .. function:: compose([config_objects...])

        Compose configuration objects together to form *mock(1)* chroot
        configuration.

        :param list config_objects: Configuration objects can be
                                    strings, objects that have the
                                    `__str__()` method, or anything that
                                    is returned from one of the
                                    mock_chroot.config functions.

        :returns: An object representing the unified configuration.
                  The object is an instance of a `list` subclass, so
                  methods could be called on it to further add
                  configuration objects. Calling `__str__()` on that
                  object will return the composed configuration string.
                  The object could be passed as an argument to
                  sobsequent calls to `compose()`.

    .. function:: bind_mount([pairs...])

        Generate `mock(1)` bind mount configuration.

        :param list pairs: List of two-element tuples where the
                           fisrt element is a path on the host and the
                           secont element is the path within the chroot
                           where that path will be bind mounted

        :returns: A configuration object representing the bind mount
                  configuration

    .. function:: from_koji(tag=None, target=None, arch='x86_64', koji_profile='brew')

        Create a koji-based *mock(1)* configuration

        :param str tag: The Koji tag to pull configuration from
        :param str target: The Koji build target tag to pull configuration from
        :param str arch: The Koji build architecture
        :param str koji_profile: The koji configuration profile to use

        One and only one of 'tag' or 'target' must be specified

        :returns: A configuration object containing the requested configuration
