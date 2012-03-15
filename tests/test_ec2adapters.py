import unittest
import datetime
from mock import MagicMock, Mock, patch

from boto.ec2.connection import EC2Connection
from boto.ec2.instance import Instance, Reservation
from ec2adapters import *

from settings import AWS
import shortcuts


class EC2AccountTest(unittest.TestCase):

    @patch('ec2adapters.EC2Connection')
    def test_constructor_create_a_new_connection(self, connection_mock):
        a = EC2Account()
        connection_mock.assert_called_once_with(AWS['key'],
                                                AWS['secret'],
                                                is_secure=AWS['use_safe_connection'])

    @patch('ec2adapters.EC2Connection')
    def test_get_instances_should_return_an_instance_list(self, connection_mock):

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

    @patch('ec2adapters.EC2Connection')
    @patch('ec2adapters.create_AMI_name')
    def test_create_AMI_should_create_a_new_image_with_tags_from_a_given_instance(self,create_ami_name_mock, connection_mock):
        instance_name = "instance_name"
        ami_name = "%s-%s" % (datetime.date.today(), instance_name)
        create_ami_name_mock.return_value = ami_name

        instance_mock = MagicMock(spec='boto.ec2.instance.Instance')
        instance_mock.id = 11
        instance_mock.tags = {'Name': instance_name}

        connection_mock.create_AMI.return_value = 99 #image_id

        a = EC2Account(connection_mock)

        self.assertEqual(99, a.create_AMI(instance_mock))
        create_ami_name_mock.assert_called_once_with(instance_mock)
        connection_mock.create_AMI.assert_called_once_with(11, ami_name)

        connection_mock.create_tags.assert_called_once_with([99], {'instance': 11,
                                                                   'created_at': datetime.date.today(),
                                                                   'created_by': 'cloudsnap'})


if __name__ == '__main__':
    unittest.main()
