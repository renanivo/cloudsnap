# -*- coding: utf-8 -*-
import unittest
import datetime
import mox

from boto.ec2.connection import EC2Connection
from boto.ec2.instance import Instance, Reservation
from boto.ec2.tag import TagSet

from shortcuts import *


class ShortcutsTest(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_create_instance_backup_name_should_return_a_string_rendered_from_template(self):
        expected = "%s-%s-%s" % (datetime.date.today(), "name", "id")

        instance = self.mox.CreateMock(Instance)

        instance.id = "id"
        instance.tags = {
            "Name": "name",
            }

        actual = create_instance_backup_name("{{ today }}-{{ name }}-{{ instance_id }}", instance)
        self.assertEqual(expected, actual)

    def test_create_instance_backup_name_should_fallback_to_instance_id_when_template_has_name_and_instance_didnt(self):
        expected = "%s-%s" % (datetime.date.today(), "id")

        instance = self.mox.CreateMock(Instance)
        instance.id = "id"

        tags = self.mox.CreateMock(TagSet)
        tags.has_key("Name").AndReturn(False)
        instance.tags = tags

        self.mox.ReplayAll()

        actual = create_instance_backup_name("{{ today }}-{{ name }}", instance)

        self.mox.VerifyAll()

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
