import SimPy.Simulation as Sim
from random import Random,expovariate,randint,seed
import constant


query_choice_master = 0

disk_choice_master = 0

class G :
	slave_nodes_attr = [] # array of objects of class node  that has the attributes
class nodes:
	slave_node_id = None # contains address of slave node
	node_queries_queue = [] # queue that has the queries to be processed
	processor_id = None # contains address of the processor object
	processors_queue = [] # queue that has processor requests
	disk_id = None  #contains id for disk
	disk_queue = [] # queue for disk
	disk_curr_head = constant.DEFAULT_DISK_HEAD
	sensor_id = None

class master_node(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self) :
		seed(seed)
		req = 0
		curr_node_index = 0
		print("hi i am the master node")
		while(self.sim.now()<constant.MAXTIME) :
				req = req + 1
				operation_no = randint(0,1)	#chooses operation

				node_no = curr_node_index
				curr_node_index = (curr_node_index + 1)%(constant.NO_SLAVE_NODES) #choose slave node using RR
				G.slave_nodes_attr[node_no].node_queries_queue.append((req,operation_no)) #adds the request to queue
				print("sent request no:",req, "to node", node_no)
				if  len(G.slave_nodes_attr[node_no].node_queries_queue) == 1 : #if the node did not have any queries
					Sim.reactivate(G.slave_nodes_attr[node_no].slave_node_id) #if the node is idle, reactivate
				yield Sim.hold,self, abs(constant.RND.expovariate(constant.QUERY_RATE))

class slave_node(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self, node_no) :
		while(1) :
			print("hello i am slave node", node_no)
			if len(G.slave_nodes_attr[node_no].node_queries_queue) == 0 : #if queue is empty, sleep
				yield Sim.passivate, self
				print("reactivated", node_no)

			yield Sim.hold,self,1#0.5*abs(constant.RND.expovariate(constant.QUERY_RATE))

			print("query_created for req no",G.slave_nodes_attr[node_no].node_queries_queue[0][0])
			#time_of_use = self.sim.now()
			query_obj = query() #create query object to process the query
			Sim.activate(query_obj,query_obj.run(G.slave_nodes_attr[node_no].node_queries_queue[0], node_no))
			#if self.interrupted() :
				#yield Sim.hold , self , abs(self.interruptLeft - time_of_use) #check for break down
			G.slave_nodes_attr[node_no].node_queries_queue.pop(0) #remove request after processed
			#print("query done")

# first come first served
class processor(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self, node_no) :
		while(1) :

			proc_time = 0

			global query_choice_master

			if query_choice_master < constant.QUERY1_RATE:
				proc_time = constant.master_cloud_proc_time_1
			elif query_choice_master < constant.QUERY2_RATE:
				proc_time = constant.master_cloud_proc_time_2
			elif query_choice_master < constant.QUERY3_RATE:
				proc_time = constant.master_cloud_proc_time_3
			elif query_choice_master < constant.QUERY4_RATE:
				proc_time = constant.master_cloud_proc_time_4
			elif query_choice_master < constant.QUERY5_RATE:
				proc_time = constant.master_cloud_proc_time_5
			elif query_choice_master < constant.QUERY6_RATE:
				proc_time = constant.master_cloud_proc_time_6
			else :
				proc_time = constant.master_cloud_proc_time_7

			if(query_choice_master < 9):
				query_choice_master = query_choice_master + 1
			else:
				query_choice_master = 0

			print("processor", node_no)
			#if len(G.slave_nodes_attr[node_no].processors_queue) == 0 : #sleep if there are no requests
				#yield Sim.passivate, self
				#print("reactivated", node_no)
			#print("processor alloted for req no",G.slave_nodes_attr[node_no].processors_queue[0][0])
			yield Sim.hold,self,6+proc_time
			if(len(G.slave_nodes_attr[node_no].processors_queue)!= 0):
				#Sim.reactivate(G.slave_nodes_attr[node_no].processors_queue[0][2]) #reactivate the query object
				G.slave_nodes_attr[node_no].processors_queue.pop(0) #remove request from queue

#first come first served

class disk(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self, node_no) :
		while(1) :


			disk_time = 0

			global disk_choice_master

			if disk_choice_master < constant.DISK1_RATE:
			    disk_time = constant.master_cloud_disk_time_1
			elif disk_choice_master < constant.DISK2_RATE:
			    disk_time = constant.master_cloud_disk_time_2
			elif disk_choice_master < constant.DISK3_RATE:
			    disk_time = constant.master_cloud_disk_time_3
			elif disk_choice_master < constant.DISK4_RATE:
			    disk_time = constant.master_cloud_disk_time_4
			elif disk_choice_master < constant.DISK5_RATE:
			    disk_time = constant.master_cloud_disk_time_5
			elif disk_choice_master < constant.DISK6_RATE:
			    disk_time = constant.master_cloud_disk_time_6
			else :
			    disk_time = constant.master_cloud_disk_time_7

			if(disk_choice_master < 9):
			    disk_choice_master = disk_choice_master + 1
			else:
			    disk_choice_master = 0


			print("disk", node_no)
			#if len(G.slave_nodes_attr[node_no].disk_queue) == 0 :
				#yield Sim.passivate, self
				#print("reactivated", node_no)
			#print("disk alloted for req no",G.slave_nodes_attr[node_no].disk_queue[0][0])
			#try:
				#yield Sim.hold,self,abs(constant.RND.expovariate(G.slave_nodes_attr[node_no].disk_queue[0][3] - G.slave_nodes_attr[node_no].disk_curr_head)) #wait for time proportional to the distance from the current head
			yield Sim.hold,self,6+disk_time
			#except:
				#print("exception")
			#G.slave_nodes_attr[node_no].disk_curr_head = G.slave_nodes_attr[node_no].disk_queue[0][3] #reactivate query object
			if(len(G.slave_nodes_attr[node_no].disk_queue)!=0):
				#Sim.reactivate(G.slave_nodes_attr[node_no].disk_queue[0][2])
				G.slave_nodes_attr[node_no].disk_queue.pop(0)


class query(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self, request_query,node_no) :
		while(1) :

			#print("query done")
			#yield Sim.hold,self,2000*abs(constant.RND.expovariate(constant.QUERY_RATE))
			G.slave_nodes_attr[node_no].processors_queue.append((request_query,node_no,self))
			#if  len(G.slave_nodes_attr[node_no].processors_queue) >= 1 :
				#Sim.reactivate(G.slave_nodes_attr[node_no].processor_id)

			#yield Sim.passivate,self
			yield Sim.hold,self,82+constant.RND.expovariate(constant.QUERY_RATE)
			disk_addr = randint(1,360) #generate disk address
			#yield Sim.hold,self,2000*abs(constant.RND.expovariate(constant.QUERY_RATE))
			G.slave_nodes_attr[node_no].disk_queue.append((request_query,node_no,self,disk_addr))
			'''
			if  len(G.slave_nodes_attr[node_no].disk_queue) >= 1 :
					Sim.reactivate(G.slave_nodes_attr[node_no].disk_id)
			yield Sim.passivate,self
			'''
			print("query done")

class TimeOut(Sim.Process):
	TOPeriod = 0.5
	def __init__(self):
		Sim.Process.__init__(self)
	def Run(self,dest):
		yield Sim.hold,self,TimeOut.TOPeriod
		self.interrupt(dest)

#generate interrupts randomly for slave nodes
class sensor(Sim.Process):
	def __init__(self):
		Sim.Process.__init__(self)

	def run(self,node_no) :
		while(1) :


			print("Sensor master ")

			delay = 0

			if query_choice_master < constant.QUERY1_RATE:
				delay = constant.TL1
			elif query_choice_master < constant.QUERY2_RATE:
				delay = constant.TL2
			elif query_choice_master < constant.QUERY3_RATE:
				delay = constant.TL3
			elif query_choice_master < constant.QUERY4_RATE:
				delay = constant.TL4
			elif query_choice_master < constant.QUERY5_RATE:
				delay = constant.TL5
			elif query_choice_master < constant.QUERY6_RATE:
				delay = constant.TL6
			else :
				delay = constant.TL7





			yield Sim.hold,self, abs(constant.RND.expovariate(delay))



def main() :
	Sim.initialize()
	master_node_sim = master_node()
	# creates 4 objects of class node (4 is the number of slave nodes)
	for slave_node_index in range(constant.NO_SLAVE_NODES):
		slave_node_attr = nodes()
		slave_node_attr.slave_node_id = slave_node()
		slave_node_attr.processor_id = processor()
		slave_node_attr.disk_id = disk()
		slave_node_attr.sensor_id = sensor()
		G.slave_nodes_attr.append(slave_node_attr)
		Sim.activate(slave_node_attr.slave_node_id,slave_node_attr.slave_node_id.run(slave_node_index))
		Sim.activate(slave_node_attr.processor_id,slave_node_attr.processor_id.run(slave_node_index))
		Sim.activate(slave_node_attr.disk_id,slave_node_attr.disk_id.run(slave_node_index))
		Sim.activate(slave_node_attr.sensor_id,slave_node_attr.sensor_id.run(slave_node_index))
		if slave_node_index == constant.NO_SLAVE_NODES - 1 :
			print("slave nodes done, activating master..")
			Sim.activate(master_node_sim,master_node_sim.run())
	Sim.simulate(until=500)

if __name__ == '__main__': main()
