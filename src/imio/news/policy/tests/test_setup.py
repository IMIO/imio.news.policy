# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from imio.news.policy.testing import IMIO_NEWS_POLICY_INTEGRATION_TESTING
from imio.news.policy.utils import setup_multilingual_site
from plone import api
from plone.app.multilingual.api import is_translatable
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFPlone.interfaces import ILanguage
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that imio.news.policy is properly installed."""

    layer = IMIO_NEWS_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if imio.news.policy is installed."""
        self.assertTrue(self.installer.is_product_installed("imio.news.policy"))

    def test_browserlayer(self):
        """Test that IImioNewsPolicyLayer is registered."""
        from imio.news.policy.interfaces import IImioNewsPolicyLayer
        from plone.browserlayer import utils

        self.assertIn(IImioNewsPolicyLayer, utils.registered_layers())

    def test_multilingual(self):
        self.assertIn("fr", self.portal.objectIds())
        self.assertIn("nl", self.portal.objectIds())

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        entity = api.content.create(
            container=self.portal,
            type="imio.news.Entity",
            id="entity",
        )
        newsfolder = api.content.create(
            container=entity,
            type="imio.news.NewsFolder",
            id="newsfolder",
        )
        folder = api.content.create(
            container=newsfolder,
            type="imio.news.Folder",
            id="folder",
        )
        api.content.create(
            container=folder,
            type="imio.news.NewsItem",
            id="newsitem",
        )
        setup_multilingual_site(self.portal)
        self.assertNotIn("entity", self.portal.objectIds())
        self.assertIn("entity", self.portal.fr.objectIds())
        entity = self.portal.fr.entity
        self.assertIn("newsfolder", entity.objectIds())
        newsfolder = entity.newsfolder
        self.assertIn("folder", newsfolder.objectIds())
        folder = newsfolder.folder
        self.assertIn("newsitem", folder.objectIds())
        newsitem = folder.newsitem
        self.assertTrue(is_translatable(newsitem))
        self.assertEquals(ILanguage(newsitem).get_language(), "fr")


class TestUninstall(unittest.TestCase):

    layer = IMIO_NEWS_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("imio.news.policy")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if imio.news.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("imio.news.policy"))

    def test_browserlayer_removed(self):
        """Test that IImioNewsPolicyLayer is removed."""
        from imio.news.policy.interfaces import IImioNewsPolicyLayer
        from plone.browserlayer import utils

        self.assertNotIn(IImioNewsPolicyLayer, utils.registered_layers())
