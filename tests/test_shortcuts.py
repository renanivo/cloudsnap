# -*- coding: utf-8 -*-
import unittest
import datetime
from mock import Mock, patch

from boto.ec2.connection import EC2Connection
from boto.ec2.instance import Instance, Reservation
from boto.ec2.tag import TagSet

from shortcuts import *


class ShortcutsTest(unittest.TestCase):

    @patch('shortcuts.AMI_NAME_TEMPLATE', "{{ today }}-{{ name }}-{{ instance_id }}")
    def test_create_AMI_name_should_return_a_string_rendered_from_template(self):
        expected = "%s-%s-%s" % (datetime.date.today(), "name", "id")

        instance = Mock(Instance)

        instance.id = "id"
        instance.tags = {
            "Name": "name",
            }

        actual = create_AMI_name(instance)
        self.assertEqual(expected, actual)

    @patch('shortcuts.AMI_NAME_TEMPLATE', "{{ today }}-{{ name }}")
    def test_create_AMI_name_should_fallback_to_instance_id_when_template_has_name_and_instance_didnt(self):
        expected = "%s-%s" % (datetime.date.today(), "id")

        instance = Mock(Instance)
        instance.id = "id"

        tags_mock = Mock(TagSet)
        tags_mock.has_key.return_value = False
        instance.tags = tags_mock

        actual = create_AMI_name(instance)

        self.assertEqual(expected, actual)
        self.assertTrue(tags_mock.has_key.called)
        tags_mock.has_key.assert_called_with("Name")


if __name__ == '__main__':
    unittest.main()
