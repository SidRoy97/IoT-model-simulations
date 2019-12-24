import SimPy.Simulation as Sim
from random import Random,expovariate,randint,seed
import  constant
import time
import math


class G :
	master_node_attr = None
	slave_nodes_attr = [] # array of objects of class node that has the attributes

#components for master node computation
class node_master :
	master_node_id = None # contains address of slave node
	master_node_queries_queue = [] # queue that has the queries to be processed
	master_processor_id = None # contains address of the processor object
	master_processor_queue = [] # queue that has processor requests
	master_disk_id = None  #contains id for disk
	master_disk_queue = [] # queue for disk
	master_disk_curr_head = constant.DEFAULT_DISK_HEAD
	master_sensor_id = None


#components for slave node computation
class nodes:
	slave_node_id = None # contains address of slave node
	node_queries_queue = [] # queue that has the queries to be processed
	processor_id = None # contains address of the processor object
	processors_queue = [] # queue that has processor requests
	disk_id = None  #contains id for disk
	disk_queue = [] # queue for disk
	disk_curr_head = constant.DEFAULT_DISK_HEAD
	sensor_id = None


#this class sorts computation equally among master and the slave nodes
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
			no_of_slaves = constant.NO_SLAVE_NODES

			#distributing computation proportionally between master and slaves
			choice = randint(0,no_of_slaves+1)



			#master computation
			if (choice % 6) == 0 :
				print("Computing in the master node")
				G.master_node_attr.master_node_queries_queue.append((req,operation_no)) #adds the request to master queue
				print("sent request no:",req, "to master node")
				if  len(G.master_node_attr.master_node_queries_queue) == 1 : #if the node did not have any queries
					Sim.reactivate(G.master_node_attr.master_node_id) #if the node is idle, reactivate
				yield Sim.hold,self, abs(constant.RND.expovariate(constant.QUERY_RATE))


			#slave computation
			else :
				print("Computing in the slave nodes")

				node_no = curr_node_index
				curr_node_index = (curr_node_index + 1)%(constant.NO_SLAVE_NODES) #choose slave node using RR
				G.slave_nodes_attr[node_no].node_queries_queue.append((req,operation_no)) #adds the request to queue
				print("sent request no:",req, "to node", node_no)
				if  len(G.slave_nodes_attr[node_no].node_queries_queue) == 1 : #if the node did not have any queries
					Sim.reactivate(G.slave_nodes_attr[node_no].slave_node_id) #if the node is idle, reactivate
				yield Sim.hold,self,1#abs(constant.RND.expovariate(constant.QUERY_RATE))

#creating query for master node computation
class master_node_identifier(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self) :
		while(1) :
			print("hello i am master node ")
			if len(G.master_node_attr.master_node_queries_queue) == 0 : #if queue is empty, sleep
				yield Sim.passivate, self
				print("reactivated")

			yield Sim.hold,self,1#0.5*abs(constant.RND.expovariate(constant.QUERY_RATE))

			print("query_created for req no",G.master_node_attr.master_node_queries_queue[0][0])
			time_of_use = self.sim.now()
			query_obj = master_query() #create query object to process the query
			Sim.activate(query_obj,query_obj.run(G.master_node_attr.master_node_queries_queue[0]))
			if self.interrupted() :
				yield Sim.hold , self ,1#abs(self.interruptLeft - time_of_use) #check for break down
			G.master_node_attr.master_node_queries_queue.pop(0) #remove request after processed
			#print("query done master")



# first come first served
class master_processor(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self) :
		while(1) :
			print("processor")
			if len(G.master_node_attr.master_processor_queue) == 0 : #sleep if there are no requests
				yield Sim.passivate, self
				print("reactivated master processor")
			#print("processor alloted for req no",G.master_node_attr.master_processor_queue[0][0])
			yield Sim.hold,self,6+constant.CLOUD_PROC_RATE

			#yield Sim.hold,self, 4*abs(constant.RND.expovariate(constant.QUERY_RATE))
			Sim.reactivate(G.master_node_attr.master_processor_queue[0][1]) #reactivate the query object
			G.master_node_attr.master_processor_queue.pop(0) #remove request from queue

#first come first served

class master_disk(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self) :
		while(1) :
			print("disk")
			if len(G.master_node_attr.master_disk_queue) == 0 :
				yield Sim.passivate, self
				print("reactivated master disk")
			#print("disk alloted for req no",G.master_node_attr.master_disk_queue[0][0])

			#try:

				#yield Sim.hold,self,abs(constant.RND.expovariate(G.master_node_attr.master_disk_queue[0][2] - G.master_node_attr.master_disk_curr_head)) #wait for time proportional to the distance from the current head
			yield Sim.hold,self,6+constant.CLOUD_DISK_RATE

			#except:

			#	print("an exception has occured in master")


			#G.master_node_attr.master_disk_curr_head = G.master_node_attr.master_disk_queue[0][2]#reactivate query object
			Sim.reactivate(G.master_node_attr.master_disk_queue[0][1])
			G.master_node_attr.master_disk_queue.pop(0)




class master_query(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self, request_query) :
		while(1) :

			#yield Sim.hold,self,10#6000*abs(constant.RND.expovariate(constant.QUERY_RATE))
			G.master_node_attr.master_processor_queue.append((request_query,self))
			if  len(G.master_node_attr.master_processor_queue) >= 1 :
					Sim.reactivate(G.master_node_attr.master_processor_id)
			yield Sim.passivate,self

			yield Sim.hold,self, 82 + constant.RND.expovariate(constant.QUERY_RATE)

			disk_addr = randint(1,360) #generate disk address
			#yield Sim.hold,self,4000*constant.RND.expovariate(constant.QUERY_RATE)
			G.master_node_attr.master_disk_queue.append((request_query,self,disk_addr))
			if  len(G.master_node_attr.master_disk_queue) >= 1 :
					Sim.reactivate(G.master_node_attr.master_disk_id)
			yield Sim.passivate,self

			print("query done - master")







#generate interrupts randomly for master node



class master_sensor(Sim.Process):
	def __init__(self):
		Sim.Process.__init__(self)

	def run(self) :
		while(1) :
			print("Sensor master ")
			yield Sim.hold,self, abs(constant.RND.expovariate((constant.DELAY)))






class slave_node(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self, node_no) :
		while(1) :
			print("hello i am slave node ", node_no)
			if len(G.slave_nodes_attr[node_no].node_queries_queue) == 0 : #if queue is empty, sleep
				yield Sim.passivate, self
				print("reactivated", node_no)

			yield Sim.hold,self,1#0.5*abs(constant.RND.expovariate(constant.QUERY_RATE))

			print("query_created for req no",G.slave_nodes_attr[node_no].node_queries_queue[0][0])
			time_of_use = self.sim.now()



			query_obj = query() #create query object to process the query
			Sim.activate(query_obj,query_obj.run(G.slave_nodes_attr[node_no].node_queries_queue[0], node_no))

			if self.interrupted() :
				yield Sim.hold , self ,1#abs(self.interruptLeft - time_of_use) #check for break down
			G.slave_nodes_attr[node_no].node_queries_queue.pop(0) #remove request after processed
			#print("query done")

# first come first served
class processor(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self, node_no) :
		while(1) :
			print("processor", node_no)
			if len(G.slave_nodes_attr[node_no].processors_queue) == 0 : #sleep if there are no requests
				yield Sim.passivate, self
				print("reactivated", node_no)
			#print("processor alloted for req no",G.slave_nodes_attr[node_no].processors_queue[0][0])
			yield Sim.hold,self,3/constant.fact+constant.FOG_PROC_RATE
			print("proclen",len(G.slave_nodes_attr[node_no].processors_queue))
			if(len(G.slave_nodes_attr[node_no].processors_queue)!= 0):
				Sim.reactivate(G.slave_nodes_attr[node_no].processors_queue[0][2]) #reactivate the query object
				G.slave_nodes_attr[node_no].processors_queue.pop(0) #remove request from queue

#first come first served

class disk(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self, node_no) :
		while(1) :
			print("disk", node_no)
			if len(G.slave_nodes_attr[node_no].disk_queue) == 0 :
				yield Sim.passivate, self
				print("reactivated", node_no)
			#print("disk alloted for req no",G.slave_nodes_attr[node_no].disk_queue[0][0])
			#try:
				#yield Sim.hold,self,abs(constant.RND.expovariate(G.slave_nodes_attr[node_no].disk_queue[0][3] - G.slave_nodes_attr[node_no].disk_curr_head)) #wait for time proportional to the distance from the current head
			yield Sim.hold,self,3/constant.fact+constant.FOG_DISK_RATE
			#except:
			#	print("exception")
			#G.slave_nodes_attr[node_no].disk_curr_head = G.slave_nodes_attr[node_no].disk_queue[0][3] #reactivate query object
			#print("check2",len(G.slave_nodes_attr[node_no].disk_queue))
			if(len(G.slave_nodes_attr[node_no].disk_queue)!=0):
				Sim.reactivate(G.slave_nodes_attr[node_no].disk_queue[0][2])
				G.slave_nodes_attr[node_no].disk_queue.pop(0)


class query(Sim.Process) :
	def __init__(self):
		Sim.Process.__init__(self)
	def run(self, request_query,node_no) :
		while(1) :

			#print("query done")
			#yield Sim.hold,self,10#000*abs(constant.RND.expovariate(constant.QUERY_RATE))
			G.slave_nodes_attr[node_no].processors_queue.append((request_query,node_no,self))
			if  len(G.slave_nodes_attr[node_no].processors_queue) >= 1 :
				Sim.reactivate(G.slave_nodes_attr[node_no].processor_id)

			yield Sim.passivate,self
			yield Sim.hold,self, 82 +constant.RND.expovariate(constant.QUERY_RATE)
			disk_addr = randint(1,360) #generate disk address
			#yield Sim.hold,self,2000*abs(constant.RND.expovariate(constant.QUERY_RATE))
			G.slave_nodes_attr[node_no].disk_queue.append((request_query,node_no,self,disk_addr))
			if  len(G.slave_nodes_attr[node_no].disk_queue) >= 1 :
					Sim.reactivate(G.slave_nodes_attr[node_no].disk_id)
			yield Sim.passivate,self

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


			if((node_no+1) < constant.NO_SLAVE_NODES):
				yield Sim.hold,self, abs(constant.RND.expovariate((constant.Q*constant.AVG_SENSOR_RATE)))
			else:
				yield Sim.hold,self, abs(constant.RND.expovariate((constant.R*constant.AVG_SENSOR_RATE)))

			'''
			print("Sensor master ")
			yield Sim.hold,self, abs(constant.RND.expovariate(((constant.NO_SENSOR1*constant.SENSOR_RATE_1)+(constant.NO_SENSOR2*constant.SENSOR_RATE_2))))
			'''

def main() :



	start = time.time()

	Sim.initialize()
	master_node_sim = master_node()

	G.master_node_attr = node_master()
	G.master_node_attr.master_node_id = master_node_identifier()
	G.master_node_attr.master_processor_id = master_processor()
	G.master_node_attr.master_disk_id = master_disk()
	#G.master_node_attr.master_sensor_id = master_sensor()
	Sim.activate(G.master_node_attr.master_node_id,G.master_node_attr.master_node_id.run())
	Sim.activate(G.master_node_attr.master_processor_id,G.master_node_attr.master_processor_id.run())
	Sim.activate(G.master_node_attr.master_disk_id,G.master_node_attr.master_disk_id.run())
	#Sim.activate(G.master_node_attr.master_sensor_id,G.master_node_attr.master_sensor_id.run())

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
	Sim.simulate(until=1000)

	print("current time is",Sim.now())

if __name__ == '__main__': main()
