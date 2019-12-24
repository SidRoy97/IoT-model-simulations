from random import Random,expovariate,randint,seed
import math

NO_SLAVE_NODES = 13
MAXTIME = 100.0
RND = Random(1234)
WRITE = 0
READ = 1
DEFAULT_DISK_HEAD = 180

#fact = math.factorial(NO_SLAVE_NODES)

QUERY_RATE = 1.0

SENSOR_RATE_1 = 1.0


SENSOR_RATE_2 = 1.0


CLOUD_PROC_POWER = 0.106
FOG_PROC_POWER = 0.496
MIST_PROC_POWER = 0.61
EDGE_PROC_POWER = 0.98

CLOUD_DISK_POWER = 0.01
FOG_DISK_POWER = 0.73
EDGE_DISK_POWER = 0.99
MIST_DISK_POWER = 0.99

#ES_PROC_TIME = 1
#ES_DISK_TIME = ES_PROC_TIME * 10

#CLOUD_DISK_RATE = CLOUD_DISK_POWER
#FOG_DISK_RATE = FOG_DISK_POWER
#EDGE_DISK_RATE = EDGE_DISK_POWER
#MIST_DISK_RATE = MIST_DISK_POWER





QUERY1_RATE = 1
QUERY2_RATE = 2
QUERY3_RATE = 3
QUERY4_RATE = 4
QUERY5_RATE = 8
QUERY6_RATE = 8.5
QUERY7_RATE = 9

DISK1_RATE = 1
DISK2_RATE = 2
DISK3_RATE = 3
DISK4_RATE = 4
DISK5_RATE = 8
DISK6_RATE = 8.5
DISK7_RATE = 9


QUERY1_TIME = 0.0208
QUERY2_TIME = 0.0139
QUERY3_TIME = 0.0264
QUERY4_TIME = 0.7909
QUERY5_TIME = 0.6628
QUERY6_TIME = 0.6335
QUERY7_TIME = 0.8494

DISK1_TIME = 0.0000032
DISK2_TIME = 0.00000312
DISK3_TIME = 0.00069
DISK4_TIME = 0.0000565
DISK5_TIME = 0.00000312
DISK6_TIME = 0.00000312
DISK7_TIME = 0.0000565


master_cloud_proc_time_1 = QUERY1_TIME * CLOUD_PROC_POWER
master_cloud_proc_time_2 = QUERY2_TIME * CLOUD_PROC_POWER
master_cloud_proc_time_3 = QUERY3_TIME * CLOUD_PROC_POWER
master_cloud_proc_time_4 = QUERY4_TIME * CLOUD_PROC_POWER
master_cloud_proc_time_5 = QUERY5_TIME * CLOUD_PROC_POWER
master_cloud_proc_time_6 = QUERY6_TIME * CLOUD_PROC_POWER
master_cloud_proc_time_7 = QUERY7_TIME * CLOUD_PROC_POWER


master_cloud_disk_time_1 = DISK1_TIME * CLOUD_DISK_POWER
master_cloud_disk_time_2 = DISK2_TIME * CLOUD_DISK_POWER
master_cloud_disk_time_3 = DISK3_TIME * CLOUD_DISK_POWER
master_cloud_disk_time_4 = DISK4_TIME * CLOUD_DISK_POWER
master_cloud_disk_time_5 = DISK5_TIME * CLOUD_DISK_POWER
master_cloud_disk_time_6 = DISK6_TIME * CLOUD_DISK_POWER
master_cloud_disk_time_7 = DISK7_TIME * CLOUD_DISK_POWER


slave_fog_proc_time_1 = QUERY1_TIME * FOG_PROC_POWER
slave_fog_proc_time_2 = QUERY2_TIME * FOG_PROC_POWER
slave_fog_proc_time_3 = QUERY3_TIME * FOG_PROC_POWER
slave_fog_proc_time_4 = QUERY4_TIME * FOG_PROC_POWER
slave_fog_proc_time_5 = QUERY5_TIME * FOG_PROC_POWER
slave_fog_proc_time_6 = QUERY6_TIME * FOG_PROC_POWER
slave_fog_proc_time_7 = QUERY7_TIME * FOG_PROC_POWER


slave_fog_disk_time_1 = DISK1_TIME * FOG_DISK_POWER
slave_fog_disk_time_2 = DISK2_TIME * FOG_DISK_POWER
slave_fog_disk_time_3 = DISK3_TIME * FOG_DISK_POWER
slave_fog_disk_time_4 = DISK4_TIME * FOG_DISK_POWER
slave_fog_disk_time_5 = DISK5_TIME * FOG_DISK_POWER
slave_fog_disk_time_6 = DISK6_TIME * FOG_DISK_POWER
slave_fog_disk_time_7 = DISK7_TIME * FOG_DISK_POWER


slave_edge_proc_time_1 = QUERY1_TIME * EDGE_PROC_POWER
slave_edge_proc_time_2 = QUERY2_TIME * EDGE_PROC_POWER
slave_edge_proc_time_3 = QUERY3_TIME * EDGE_PROC_POWER
slave_edge_proc_time_4 = QUERY4_TIME * EDGE_PROC_POWER
slave_edge_proc_time_5 = QUERY5_TIME * EDGE_PROC_POWER
slave_edge_proc_time_6 = QUERY6_TIME * EDGE_PROC_POWER
slave_edge_proc_time_7 = QUERY7_TIME * EDGE_PROC_POWER


slave_edge_disk_time_1 = DISK1_TIME * EDGE_DISK_POWER
slave_edge_disk_time_2 = DISK2_TIME * EDGE_DISK_POWER
slave_edge_disk_time_3 = DISK3_TIME * EDGE_DISK_POWER
slave_edge_disk_time_4 = DISK4_TIME * EDGE_DISK_POWER
slave_edge_disk_time_5 = DISK5_TIME * EDGE_DISK_POWER
slave_edge_disk_time_6 = DISK6_TIME * EDGE_DISK_POWER
slave_edge_disk_time_7 = DISK7_TIME * EDGE_DISK_POWER


slave_mist_proc_time_1 = QUERY1_TIME * MIST_PROC_POWER
slave_mist_proc_time_2 = QUERY2_TIME * MIST_PROC_POWER
slave_mist_proc_time_3 = QUERY3_TIME * MIST_PROC_POWER
slave_mist_proc_time_4 = QUERY4_TIME * MIST_PROC_POWER
slave_mist_proc_time_5 = QUERY5_TIME * MIST_PROC_POWER
slave_mist_proc_time_6 = QUERY6_TIME * MIST_PROC_POWER
slave_mist_proc_time_7 = QUERY7_TIME * MIST_PROC_POWER


slave_mist_disk_time_1 = DISK1_TIME * MIST_DISK_POWER
slave_mist_disk_time_2 = DISK2_TIME * MIST_DISK_POWER
slave_mist_disk_time_3 = DISK3_TIME * MIST_DISK_POWER
slave_mist_disk_time_4 = DISK4_TIME * MIST_DISK_POWER
slave_mist_disk_time_5 = DISK5_TIME * MIST_DISK_POWER
slave_mist_disk_time_6 = DISK6_TIME * MIST_DISK_POWER
slave_mist_disk_time_7 = DISK7_TIME * MIST_DISK_POWER



SL_N_1 = 3
SL_N_2 = 2
SL_N_3 = 7
SL_N_4 = 13
SL_N_5 = 1
SL_N_6 = 3
SL_N_7 = 13


S_N_1_1 = 540
S_N_1_2 = 0
S_N_2_1 = 360
S_N_2_2 = 0
S_N_3_1 = 360
S_N_3_2 = 100
S_N_4_1 = 540
S_N_4_2 = 1000
S_N_5_1 = 1
S_N_5_2 = 0
S_N_6_1 = 540
S_N_6_2 = 0
S_N_7_1 = 540
S_N_7_2 = 1000

S_R_1_1 = 1.0
S_R_1_2 = 0.0
S_R_2_1 = 1.0
S_R_2_2 = 0.0
S_R_3_1 = 1.0
S_R_3_2 = 2.8
S_R_4_1 = 1.0
S_R_4_2 = 5.6
S_R_5_1 = 1.0
S_R_5_2 = 0.0
S_R_6_1 = 1.0
S_R_6_2 = 0.0
S_R_7_1 = 1.0
S_R_7_2 = 5.6

AVG_SENSOR_RATE_1 = (S_R_1_1+S_R_1_2)/2.0
AVG_SENSOR_RATE_2 = (S_R_2_1+S_R_2_2)/2.0
AVG_SENSOR_RATE_3 = (S_R_3_1+S_R_3_2)/2.0
AVG_SENSOR_RATE_4 = (S_R_4_1+S_R_4_2)/2.0
AVG_SENSOR_RATE_5 = (S_R_5_1+S_R_5_2)/2.0
AVG_SENSOR_RATE_6 = (S_R_6_1+S_R_6_2)/2.0
AVG_SENSOR_RATE_7 = (S_R_7_1+S_R_7_2)/2.0

Q1=(S_N_1_1+S_N_1_2)/SL_N_1
R1=(S_N_1_1+S_N_1_2)%SL_N_1
Q2=(S_N_2_1+S_N_2_2)/SL_N_2
R2=(S_N_2_1+S_N_2_2)%SL_N_2
Q3=(S_N_3_1+S_N_3_2)/SL_N_3
R3=(S_N_3_1+S_N_3_2)%SL_N_3
Q4=(S_N_4_1+S_N_4_2)/SL_N_4
R4=(S_N_4_1+S_N_4_2)%SL_N_4
Q5=(S_N_5_1+S_N_5_2)/SL_N_5
R5=(S_N_5_1+S_N_5_2)%SL_N_5
Q6=(S_N_6_1+S_N_6_2)/SL_N_6
R6=(S_N_6_1+S_N_6_2)%SL_N_6
Q7=(S_N_7_1+S_N_7_2)/SL_N_7
R7=(S_N_7_1+S_N_7_2)%SL_N_7

TL1 = (S_N_1_1+S_N_1_2)*AVG_SENSOR_RATE_1
TL2 = (S_N_2_1+S_N_2_2)*AVG_SENSOR_RATE_2
TL3 = (S_N_3_1+S_N_3_2)*AVG_SENSOR_RATE_3
TL4 = (S_N_4_1+S_N_4_2)*AVG_SENSOR_RATE_4
TL5 = (S_N_5_1+S_N_5_2)*AVG_SENSOR_RATE_5
TL6 = (S_N_6_1+S_N_6_2)*AVG_SENSOR_RATE_6
TL7 = (S_N_7_1+S_N_7_2)*AVG_SENSOR_RATE_7



INTERRUPT_RATE = 1
ELAPSED_TIME_1 = 0.027
