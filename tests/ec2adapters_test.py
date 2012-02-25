import unittest
from mock import Mock, patch

from boto.ec2.connection import EC2Connection
from boto.ec2.instance import Instance, Reservation
from ec2adapters import *

from settings import AWS


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

        a = EC2Account()
        a._connection.get_all_instances.return_value = [reservation_mock1,
                                                        reservation_mock2]
        instances = a.get_instances()

        self.assertEqual(2, len(instances))
        self.assertIn(instance_mock1, instances)
        self.assertIn(instance_mock2, instances)


if __name__ == '__main__':
    unittest.main()
