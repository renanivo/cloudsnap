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

    def test_get_all_instances_should_return_an_instance_list(self):
        connection = self.mox.CreateMock(EC2Connection)

        reservation1 = self.mox.CreateMock(Reservation)
        reservation2 = self.mox.CreateMock(Reservation)

        instance1 = self.mox.CreateMock(Instance)
        instance2 = self.mox.CreateMock(Instance)

        connection.get_all_instances().AndReturn([reservation1, reservation2])

        reservation1.instances = [instance1]
        reservation2.instances = [instance2]

        self.mox.ReplayAll()

        instances = get_all_instances(connection)

        self.mox.VerifyAll()

        self.assertEqual(2, len(instances))
        self.assertIn(instance1, instances)
        self.assertIn(instance2, instances)

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
