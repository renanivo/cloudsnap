import unittest
import datetime
from mock import MagicMock, Mock, patch

from ec2adapters import *

from settings import AWS


class EC2AccountTest(unittest.TestCase):


    def _get_instance_mock(self, id, name):
        instance_mock = MagicMock(spec='boto.ec2.instance.Instance')
        instance_mock.id = id
        instance_mock.tags = {'Name': name}

        return instance_mock

    @patch('ec2adapters.EC2Connection')
    def test_should_create_a_connection_when_not_given(self, connection_mock):
        a = EC2Account()
        connection_mock.assert_called_once_with(AWS['key'],
                                                AWS['secret'],
                                                is_secure=AWS['use_safe_connection'])

    @patch('ec2adapters.EC2Connection')
    def test_should_get_an_instance_list(self, connection_mock):

        reservation_mock1 = Mock(spec='boto.ec2.instance.Reservation')
        reservation_mock2 = Mock(spec='boto.ec2.instance.Reservation')

        instance_mock1 = Mock(spec='boto.ec2.instance.Instance')
        instance_mock2 = Mock(spec='boto.ec2.instance.Instance')

        reservation_mock1.instances = [instance_mock1]
        reservation_mock2.instances = [instance_mock2]

        connection_mock.get_all_instances.return_value = [reservation_mock1,
                                                          reservation_mock2]

        a = EC2Account(connection_mock)
        instances = a.get_instances()

        self.assertEqual(1, connection_mock.get_all_instances.call_count)
        self.assertEqual(2, len(instances))
        self.assertIn(instance_mock1, instances)
        self.assertIn(instance_mock2, instances)

    @patch('ec2adapters.AMI_NAME_TEMPLATE', '{{ today }}-{{ name }}')
    @patch('ec2adapters.EC2Connection')
    def test_should_backup_an_instance_and_get_the_AMI_id(self, connection_mock):
        connection_mock.create_image.return_value = 99
        instance_mock = self._get_instance_mock(11, "instance_name")

        account = EC2Account(connection_mock)

        self.assertEqual(99, account.backup_instance(instance_mock))

    @patch('ec2adapters.AMI_NAME_TEMPLATE', '{{ today }}-{{ name }}')
    @patch('ec2adapters.EC2Connection')
    def test_should_use_boto_to_backup_an_instance(self, connection_mock):
        instance_mock = self._get_instance_mock(11, "instance_name")

        account = EC2Account(connection_mock)

        account.backup_instance(instance_mock)
        connection_mock.create_image.assert_called_once_with(11, "%s-%s" % (datetime.date.today(),
                                                                          "instance_name"))

    @patch('ec2adapters.AMI_NAME_TEMPLATE', '{{ today }}-{{ name }}')
    @patch('ec2adapters.EC2Connection')
    def test_should_backup_an_instance_with_time_and_instance_id_on_tags(self, connection_mock):
        connection_mock.create_image.return_value = 99
        instance_mock = self._get_instance_mock(11, "instance_name")

        account = EC2Account(connection_mock)

        account.backup_instance(instance_mock)
        connection_mock.create_tags.assert_called_once_with([99], {"instance": 11,
                                                                   "created_at": datetime.date.today(),
                                                                   "created_by": "cloudsnap"})


if __name__ == '__main__':
    unittest.main()
