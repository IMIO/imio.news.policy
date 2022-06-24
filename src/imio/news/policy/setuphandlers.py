# -*- coding: utf-8 -*-

from imio.news.policy.utils import remove_unused_contents
from imio.news.policy.utils import setup_multilingual_site
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool import interfaces as quiskinstallinterfaces
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "imio.news.core:default",
            "imio.news.policy:uninstall",
        ]


@implementer(quiskinstallinterfaces.INonInstallable)
class HiddenProducts(object):
    def getNonInstallableProducts(self):
        """Hides profiles from QuickInstaller"""
        return [
            "imio.news.core",
        ]


def post_install(context):
    """Post install script"""
    portal = api.portal.get()
    remove_unused_contents(portal)
    setup_multilingual_site(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
