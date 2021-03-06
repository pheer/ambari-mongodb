import os
import sys
from time import sleep

# Ambari includes
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.libraries.script import Script

# Custom service test classes includes
from integrated_base_test import IntegratedBaseTestCase

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.join(SCRIPT_DIR, '../scripts/')
SERVICE_DIR = os.path.join(SCRIPT_DIR, '../')
sys.path.append(PACKAGE_DIR)
sys.path.append(SERVICE_DIR)

# Custom service scripts includes
import params
from mongo_db import MongoDBServer
from mongo_base import InstanceConfig
from mongo_base import InstanceStatus

class IntegratedReplicaMongodTestCase(IntegratedBaseTestCase):

    def setUp(self):
        self.as_super = super(IntegratedReplicaMongodTestCase, self)
        self.as_super.setUp()
        params.try_interval = 4
        params.times_to_try = 10
        # Configuring and Installing mongod dependencies
        server = MongoDBServer()
        server.my_hostname = 'node1.test.com'
        server.configure(self.env)
        server.install(self.env)

    def several_hosts_setup(self):
        Script.config['clusterHostInfo'] = {
            'mongos_hosts': [],
            'mongodb_hosts': ['node1.test.com','node2.test.com','node3.test.com'],
            'mongodc_hosts': []
        }

        params.mongod_cluster_definition = 'node1.test.com,node2.test.com/arbiter,node3.test.com,node2.test.com'

    expected_cluster_status_for_several_hosts_stopped = [
        ('shard0',['node1.test.com','node2.test.com/arbiter','node3.test.com','node2.test.com'], [
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node1_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node1_shard0_0',
                           log_file='/var/log/mongodb/node1_shard0_0.log',
                           db_port='27025',
                           host_name='node1.test.com',
                           is_arbiter=False,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node2_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node2_shard0_0',
                           log_file='/var/log/mongodb/node2_shard0_0.log',
                           db_port='27025',
                           host_name='node2.test.com',
                           is_arbiter=True,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node3_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node3_shard0_0',
                           log_file='/var/log/mongodb/node3_shard0_0.log',
                           db_port='27025',
                           host_name='node3.test.com',
                           is_arbiter=False,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node2_shard0_1.pid',
                           final_db_path='/var/lib/mongodb/node2_shard0_1',
                           log_file='/var/log/mongodb/node2_shard0_1.log',
                           db_port='27030',
                           host_name='node2.test.com',
                           is_arbiter=False,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None)])]

    def one_host_setup(self):
        Script.config['clusterHostInfo'] = {
            'mongos_hosts': [],
            'mongodb_hosts': ['node1.test.com'],
            'mongodc_hosts': []
        }

        params.mongod_cluster_definition = 'node1.test.com,node1.test.com/arbiter,node1.test.com'

    expected_cluster_status_for_one_host_stopped = [
        ('shard0',['node1.test.com','node1.test.com/arbiter','node1.test.com'], [
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node1_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node1_shard0_0',
                           log_file='/var/log/mongodb/node1_shard0_0.log',
                           db_port='27025',
                           host_name='node1.test.com',
                           is_arbiter=False,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node1_shard0_1.pid',
                           final_db_path='/var/lib/mongodb/node1_shard0_1',
                           log_file='/var/log/mongodb/node1_shard0_1.log',
                           db_port='27030',
                           host_name='node1.test.com',
                           is_arbiter=True,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node1_shard0_2.pid',
                           final_db_path='/var/lib/mongodb/node1_shard0_2',
                           log_file='/var/log/mongodb/node1_shard0_2.log',
                           db_port='27031',
                           host_name='node1.test.com',
                           is_arbiter=False,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None)])]

    def test_get_cluster_data_with_one_host(self):
        self.one_host_setup()
        server = MongoDBServer()
        server.my_hostname = 'node1.test.com'

        expectedClusterData = [('shard0', ['node1.test.com', 'node1.test.com/arbiter', 'node1.test.com'],
                                [InstanceConfig(shard_name='shard0',
                                                pid_file_name='/var/run/mongodb/node1_shard0_0.pid',
                                                final_db_path='/var/lib/mongodb/node1_shard0_0',
                                                log_file='/var/log/mongodb/node1_shard0_0.log',
                                                db_port='27025',
                                                host_name='node1.test.com',
                                                is_arbiter=False),
                                 InstanceConfig(shard_name='shard0',
                                                pid_file_name='/var/run/mongodb/node1_shard0_1.pid',
                                                final_db_path='/var/lib/mongodb/node1_shard0_1',
                                                log_file='/var/log/mongodb/node1_shard0_1.log',
                                                db_port='27030',
                                                host_name='node1.test.com',
                                                is_arbiter=True),
                                 InstanceConfig(shard_name='shard0',
                                                pid_file_name='/var/run/mongodb/node1_shard0_2.pid',
                                                final_db_path='/var/lib/mongodb/node1_shard0_2',
                                                log_file='/var/log/mongodb/node1_shard0_2.log',
                                                db_port='27031',
                                                host_name='node1.test.com',
                                                is_arbiter=False)])]
        clusterData = server.getClusterData()
        self.assertEqual(clusterData,expectedClusterData,"The cluster data for the replicaset is not right")

    def test_get_cluster_status_with_one_host(self):
        self.one_host_setup()
        server = MongoDBServer()
        server.my_hostname = 'node1.test.com'

        clusterStatus = server.getClusterStatus(server.getClusterData())
        self.assertEqual(clusterStatus,self.expected_cluster_status_for_one_host_stopped,
                         "The cluster status result before stating the replicaset is not right")

    def test_stopping_an_already_stopped_cluster(self):
        self.one_host_setup()
        server = MongoDBServer()
        server.my_hostname = 'node1.test.com'
        clusterStatus = server.getClusterStatus(server.getClusterData())
        self.assertEqual(clusterStatus,self.expected_cluster_status_for_one_host_stopped,
                         "The cluster status result before stating the replicaset is not right")
        server.stop(self.env)
        clusterStatus = server.getClusterStatus(server.getClusterData())
        self.assertEqual(clusterStatus, self.expected_cluster_status_for_one_host_stopped,
                         "The cluster status result after stopping the replicaset is not right")

    def test_replicaset_in_one_host(self):
        self.one_host_setup()

        server = MongoDBServer()
        server.my_hostname = 'node1.test.com'

        with self.assertRaises(ComponentIsNotRunning):
            server.status(self.env)

        clusterStatus = server.getClusterStatus(server.getClusterData())
        self.assertEqual(clusterStatus, self.expected_cluster_status_for_one_host_stopped,
                         "The cluster status result before stating the replicaset is not right")

        server.start(self.env)
        sleep(self.SLEEP_INTERVAL_AFTER_START_A_INSTANCE)
        server.status(self.env)

        expectedClusterStatus = [('shard0', ['node1.test.com', 'node1.test.com/arbiter', 'node1.test.com'], [
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node1_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node1_shard0_0',
                           log_file='/var/log/mongodb/node1_shard0_0.log',
                           db_port='27025',
                           host_name='node1.test.com',
                           is_arbiter=False,
                           is_started=True,
                           is_repl_configurated=True,
                           repl_role="PRIMARY"),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node1_shard0_1.pid',
                           final_db_path='/var/lib/mongodb/node1_shard0_1',
                           log_file='/var/log/mongodb/node1_shard0_1.log',
                           db_port='27030',
                           host_name='node1.test.com',
                           is_arbiter=True,
                           is_started=True,
                           is_repl_configurated=True,
                           repl_role="SECONDARY"),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node1_shard0_2.pid',
                           final_db_path='/var/lib/mongodb/node1_shard0_2',
                           log_file='/var/log/mongodb/node1_shard0_2.log',
                           db_port='27031',
                           host_name='node1.test.com',
                           is_arbiter=False,
                           is_started=True,
                           is_repl_configurated=True,
                           repl_role="SECONDARY")])]
        clusterStatus = server.getClusterStatus(server.getClusterData())
        self.assertEqual(clusterStatus, expectedClusterStatus,"The cluster status result for a started replicaset is "
                                                              "not right")

        server.stop(self.env)

        with self.assertRaises(ComponentIsNotRunning):
            server.status(self.env)

        clusterStatus = server.getClusterStatus(server.getClusterData())
        self.assertEqual(clusterStatus, self.expected_cluster_status_for_one_host_stopped,
                         "The cluster status result after stopping the replicaset is not right")

    def test_get_cluster_status_with_several_hosts(self):
        self.several_hosts_setup()
        server = MongoDBServer()
        server.my_hostname = 'node1.test.com'

        clusterStatus = server.getClusterStatus(server.getClusterData())
        self.assertEqual(clusterStatus, self.expected_cluster_status_for_several_hosts_stopped,
                         "The cluster status result before stating the replicaset is not right")


    def test_replicaset_with_several_hosts(self):
        self.several_hosts_setup()

        server3 = MongoDBServer()
        server3.my_hostname = 'node3.test.com'
        server2 = MongoDBServer()
        server2.my_hostname = 'node2.test.com'
        server1 = MongoDBServer()
        server1.my_hostname = 'node1.test.com'

        clusterStatus = server3.getClusterStatus(server3.getClusterData())
        self.assertEqual(clusterStatus, self.expected_cluster_status_for_several_hosts_stopped,
                         "The cluster status result before stating the replicaset is not right")

        server3.start(self.env)
        sleep(self.SLEEP_INTERVAL_AFTER_START_A_INSTANCE)
        server3.status(self.env)

        expectedClusterStatusServer3On = [
        ('shard0',['node1.test.com','node2.test.com/arbiter','node3.test.com','node2.test.com'], [
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node1_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node1_shard0_0',
                           log_file='/var/log/mongodb/node1_shard0_0.log',
                           db_port='27025',
                           host_name='node1.test.com',
                           is_arbiter=False,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node2_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node2_shard0_0',
                           log_file='/var/log/mongodb/node2_shard0_0.log',
                           db_port='27025',
                           host_name='node2.test.com',
                           is_arbiter=True,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node3_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node3_shard0_0',
                           log_file='/var/log/mongodb/node3_shard0_0.log',
                           db_port='27025',
                           host_name='node3.test.com',
                           is_arbiter=False,
                           is_started=True,
                           is_repl_configurated=False,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node2_shard0_1.pid',
                           final_db_path='/var/lib/mongodb/node2_shard0_1',
                           log_file='/var/log/mongodb/node2_shard0_1.log',
                           db_port='27030',
                           host_name='node2.test.com',
                           is_arbiter=False,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None)])]

        clusterStatus = server3.getClusterStatus(server3.getClusterData())
        self.assertEqual(clusterStatus, expectedClusterStatusServer3On, "The cluster status result for a started node3 "
                                                                        "in the replicaset is not right")
        server2.start(self.env)
        sleep(self.SLEEP_INTERVAL_AFTER_START_A_INSTANCE)
        server2.status(self.env)

        expectedClusterStatusServer2On = [
        ('shard0',['node1.test.com','node2.test.com/arbiter','node3.test.com','node2.test.com'], [
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node1_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node1_shard0_0',
                           log_file='/var/log/mongodb/node1_shard0_0.log',
                           db_port='27025',
                           host_name='node1.test.com',
                           is_arbiter=False,
                           is_started=False,
                           is_repl_configurated=None,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node2_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node2_shard0_0',
                           log_file='/var/log/mongodb/node2_shard0_0.log',
                           db_port='27025',
                           host_name='node2.test.com',
                           is_arbiter=True,
                           is_started=True,
                           is_repl_configurated=False,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node3_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node3_shard0_0',
                           log_file='/var/log/mongodb/node3_shard0_0.log',
                           db_port='27025',
                           host_name='node3.test.com',
                           is_arbiter=False,
                           is_started=True,
                           is_repl_configurated=False,
                           repl_role=None),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node2_shard0_1.pid',
                           final_db_path='/var/lib/mongodb/node2_shard0_1',
                           log_file='/var/log/mongodb/node2_shard0_1.log',
                           db_port='27030',
                           host_name='node2.test.com',
                           is_arbiter=False,
                           is_started=True,
                           is_repl_configurated=False,
                           repl_role=None)])]

        clusterStatus = server2.getClusterStatus(server2.getClusterData())
        self.assertEqual(clusterStatus, expectedClusterStatusServer2On, "The cluster status result for a started node2"
                                                                        " in the replicaset is not right")
        server1.start(self.env)
        sleep(self.SLEEP_INTERVAL_AFTER_START_A_INSTANCE)
        server1.status(self.env)

        expectedClusterStatusServer1On = [
        ('shard0',['node1.test.com','node2.test.com/arbiter','node3.test.com','node2.test.com'], [
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node1_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node1_shard0_0',
                           log_file='/var/log/mongodb/node1_shard0_0.log',
                           db_port='27025',
                           host_name='node1.test.com',
                           is_arbiter=False,
                           is_started=True,
                           is_repl_configurated=True,
                           repl_role="PRIMARY"),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node2_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node2_shard0_0',
                           log_file='/var/log/mongodb/node2_shard0_0.log',
                           db_port='27025',
                           host_name='node2.test.com',
                           is_arbiter=True,
                           is_started=True,
                           is_repl_configurated=True,
                           repl_role="SECONDARY"),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node3_shard0_0.pid',
                           final_db_path='/var/lib/mongodb/node3_shard0_0',
                           log_file='/var/log/mongodb/node3_shard0_0.log',
                           db_port='27025',
                           host_name='node3.test.com',
                           is_arbiter=False,
                           is_started=True,
                           is_repl_configurated=True,
                           repl_role="SECONDARY"),
            InstanceStatus(shard_name='shard0',
                           pid_file_name='/var/run/mongodb/node2_shard0_1.pid',
                           final_db_path='/var/lib/mongodb/node2_shard0_1',
                           log_file='/var/log/mongodb/node2_shard0_1.log',
                           db_port='27030',
                           host_name='node2.test.com',
                           is_arbiter=False,
                           is_started=True,
                           is_repl_configurated=True,
                           repl_role="SECONDARY")])]

        clusterStatus = server1.getClusterStatus(server1.getClusterData())
        print "\n\n\n\n\n clusterStatus: " + str(clusterStatus) + '\n\n\n\n\n\n'
        print "\n\n\n\n\n expectedClusterStatusServer1On: " + str(expectedClusterStatusServer1On) + '\n\n\n\n\n\n'

        self.assertEqual(clusterStatus, expectedClusterStatusServer1On, "The cluster status result for a started node1"
                                                                        " in the replicaset is not right")

        server2.stop(self.env)
        with self.assertRaises(ComponentIsNotRunning):
            server2.status(self.env)

        server1.stop(self.env)
        with self.assertRaises(ComponentIsNotRunning):
            server1.status(self.env)

        server3.stop(self.env)
        with self.assertRaises(ComponentIsNotRunning):
            server3.status(self.env)


        clusterStatus = server3.getClusterStatus(server3.getClusterData())
        self.assertEqual(clusterStatus, self.expected_cluster_status_for_several_hosts_stopped,
                         "The cluster status result after stopping the replicaset is not right")
