import os
from time import sleep
from resource_management import *
from mongo_base import MongoBase
from resource_management.core.logger import Logger

class MongoMaster(MongoBase):
    mongo_packages = ['mongodb-org']

    def install(self, env):
        import params
        env.set_params(params)
        self.installMongo(env)

    def configure(self, env):
        import params
        env.set_params(params)
        self.configureMongo(env)

    def start(self, env):
        import params
        self.configure(env)
        print "start mongodb"
        
        import socket
        current_host_name=socket.getfqdn(socket.gethostname())
        
        config = Script.get_config()
        shard_prefix = params.shard_prefix
        
        db_hosts = config['clusterHostInfo']['mongodb_hosts']
        #if params.node_group =='':
        #    db_hosts = config['clusterHostInfo']['mongodb_hosts']
        #else:
        #    groups = params.node_group.split(';')
        #    db_hosts = []
        #    for index,item in enumerate(groups,start=0):                
        #        if current_host_name in item and index ==0:
        #           db_hosts = item.split(',')
                                 
        len_host=len(db_hosts)
        len_port=len(params.db_ports)
        print "hostname :" + current_host_name
        print "db nodes list"
        print db_hosts
        #get shard_name
        for index,item in enumerate(db_hosts,start=0):
            if item ==current_host_name:
                #foreach db_ports
                for index_p,p in enumerate(params.db_ports,start=0):
                   #rm mongo_*.sock
                   Execute(format('rm -rf /tmp/mongodb-{p}.sock'),logoutput=True)
                   #get shard_name
                   shard_name = shard_prefix + str((index-index_p)%len_host)
                   pid_file_name = params.shard_prefix + str(index_p)                  
                   #get db_path                   
                   db_path = params.db_path + '/' + shard_name
                   
                   if os.path.exists(db_path):
                       print "File exists"
                   else:
                       Execute(format('mkdir -p {db_path}'),logoutput=True)
                   log_file = params.log_path + '/' + shard_name + '.log'
                   pid_file = params.pid_db_path + '/' + pid_file_name + '.pid'
                   Execute(format('mongod -f /etc/mongod.conf --shardsvr  -replSet {shard_name} -port {p} -dbpath {db_path} -oplogSize 100 -logpath {log_file} -pidfilepath {pid_file}')
                           ,logoutput=True)
        
        sleep(5)
        print 'sleep waiting for all mongod started'
        #node_group  del
        #if params.node_group =='':
        #    print 'group has no data'
        #else:
        #    groups = params.node_group.split(';')
        #    tmp_db_hosts = groups[0].split(',')      
        #    del_host_port_cmd = ''            
        #    for index_i,host in enumerate(tmp_db_hosts,start=1):
        #        if current_host_name == host:                
        #           if len(tmp_db_hosts) - index_i == 0:
        #                print 'last host ' + current_host_name
        #                host_port_name0 = tmp_db_hosts[0] + ':' + params.db_ports[1]
        #                host_port_name1 = tmp_db_hosts[1] + ':' + params.db_ports[2]
        #                del_host_port_cmd = format('rs.remove("{host_port_name0}") \n')
        #                del_host_port_cmd = del_host_port_cmd + format('rs.remove("{host_port_name1}") \n')
        #            if len(tmp_db_hosts) - index_i == 1:
        #                print 'second last ' + current_host_name
        #                host_port_name = tmp_db_hosts[0] + ':' + params.db_ports[2]
        #                del_host_port_cmd = format('rs.remove("{host_port_name}") \n')
        #    if del_host_port_cmd!='':            
        #        del_cmd = format('mongo --host {current_host_name} --port 27017 <<EOF \n{del_host_port_cmd} \nEOF\n') 
        #        File('/var/run/mongo_del_config.sh',content=del_cmd,mode=0755)
        #        Execute('/var/run/mongo_del_config.sh',logoutput=True)
        
        sleep(5)
        db_hosts = config['clusterHostInfo']['mongodb_hosts']           
        # stop all services and start new all services
        #deperated not execute
        if params.node_group =='&':
           self.stop(env)
           len_host=len(db_hosts)
           len_port=len(params.db_ports)
           print "add new host now show db nodes list"
           print db_hosts
           #get shard_name
           for index,item in enumerate(db_hosts,start=0):
              if item ==current_host_name:
                #foreach db_ports
                for index_p,p in enumerate(params.db_ports,start=0):
                   #rm mongo_*.sock
                   Execute(format('rm -rf /tmp/mongodb-{p}.sock'),logoutput=True)
                   #get shard_name
                   shard_name = shard_prefix + str((index-index_p)%len_host)
                   pid_file_name = params.shard_prefix + str(index_p)                  
                   #get db_path                   
                   db_path = params.db_path + '/' + shard_name
                   
                   if os.path.exists(db_path):
                       print "File exists"
                   else:
                       Execute(format('mkdir -p {db_path}'),logoutput=True)
                   log_file = params.log_path + '/' + shard_name + '.log'
                   pid_file = params.pid_db_path + '/' + pid_file_name + '.pid'
                   Execute(format('mongod -f /etc/mongod.conf --shardsvr  -replSet {shard_name} -port {p} -dbpath {db_path} -oplogSize 100 -logpath {log_file} -pidfilepath {pid_file}')
                           ,logoutput=True)
                           
        if params.node_group =='':                
            #
            for index,item in enumerate(db_hosts,start=0):         
                shard_name= shard_prefix + str(index)
            
                members =''
                current_index=0
                current_shard=index
                while(current_index<len_port):
                    current_host = db_hosts[current_shard]
                    current_port = params.db_ports[current_index]
                    members = members+ '{_id:'+format('{current_index},host:"{current_host}:{current_port}"') 
                    if current_index == 0:
                        members = members +',priority:2'
                    members = members + '},'
                    current_index = current_index + 1
                    current_shard = (current_shard + 1)%len(db_hosts)
                members=members[:-1]
                if item == current_host_name:            
                    replica_param ='rs.initiate( {_id:'+format('"{shard_name}",version: 1,members:') + '[' + members + ']})'
        
            cmd = format('mongo --host {current_host_name} --port 27017 <<EOF \n{replica_param} \nEOF\n')
            File('/var/run/mongo_config.sh',
                 content=cmd,
                 mode=0755
            )
            Execute('/var/run/mongo_config.sh',logoutput=True)
        else:
            # add shard 
            groups = params.node_group.split(';')
            tmp_db_hosts = groups[0].split(',') 
            
            del_host_port_param = ''
                   
            for index_i,host in enumerate(tmp_db_hosts,start=1):
                if current_host_name == host:                
                    if len(tmp_db_hosts) - index_i == 0:
                        print 'last host ' + current_host_name
                        host_port_name0 = tmp_db_hosts[0] + ':' + params.db_ports[1]
                        host_port_name1 = tmp_db_hosts[1] + ':' + params.db_ports[2]
                        del_host_port_param = format('rs.remove("{host_port_name0}") \n')
                        del_host_port_param = del_host_port_param + format('rs.remove("{host_port_name1}") \n')
                    if len(tmp_db_hosts) - index_i == 1:
                        print 'second last ' + current_host_name
                        host_port_name = tmp_db_hosts[0] + ':' + params.db_ports[2]
                        del_host_port_param = format('rs.remove("{host_port_name}") \n')
                        
            for index,item in enumerate(db_hosts,start=0):         
                shard_name= shard_prefix + str(index)
                        
                members =''
                add_shard_param = ''
                current_index=0
                current_shard=index
                while(current_index<len_port):
                    current_host = db_hosts[current_shard]
                    current_port = params.db_ports[current_index]
                    members = members+ '{_id:'+format('{current_index},host:"{current_host}:{current_port}"') 
                    add_shard_param = add_shard_param + format('rs.add("{current_host}:{current_port}") \n') 
                    if current_index == 0:
                        members = members +',priority:2'
                    members = members + '},'
                    current_index = current_index + 1
                    current_shard = (current_shard + 1)%len(db_hosts)
                members=members[:-1]
                if item == current_host_name and item in groups[1]:            
                    replica_param ='rs.initiate( {_id:'+format('"{shard_name}",version: 1,members:') + '[' + members + ']})'
                if item == current_host_name and item in groups[0]:            
                    replica_param = add_shard_param
                    if del_host_port_param != '':
                        replica_param =  del_host_port_param + replica_param
        
            cmd = format('mongo --host {current_host_name} --port 27017 <<EOF \n{replica_param} \nEOF\n')
            File('/var/run/mongo_config.sh',
                 content=cmd,
                 mode=0755
            )
            Execute('/var/run/mongo_config.sh',logoutput=True)

    def stop(self, env):
        print "stop services.."
        import params                
                
        for index_p,p in enumerate(params.db_ports,start=0):                   
            #get shard_name
            shard_name = params.shard_prefix + str(index_p)                         
            pid_file = params.pid_db_path + '/' + shard_name + '.pid'                  
            cmd =format('cat {pid_file} | xargs kill -9 ')
            try:
               Execute(cmd,logoutput=True)
            except:
               print 'can not find pid process,skip this'
                           

    def restart(self, env):
        self.configure(env)
        print "restart mongodb"
        #Execute('service mongod restart')
        #self.status(env)
        self.stop(env)
        self.start(env)

    def status(self, env):
        print "checking status..."
        
        import params        
            
        for index_p,p in enumerate(params.db_ports,start=0):                   
            shard_name = params.shard_prefix + str(index_p)                         
            pid_file = params.pid_db_path + '/' + shard_name + '.pid'
            check_process_status(pid_file)            

if __name__ == "__main__":
    MongoMaster().execute()
