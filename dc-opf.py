import csv
import pandas
import numpy as np
import asm
import simplex_api
import math

#bus_data

bus_count = 0
power_demand = []

with open('dcopf-csv/bus_data.csv','r') as bus_i:
    reader = csv.reader(bus_i)
    i = 0
    for row in reader:
        if i == 0:
            i = i + 1
            continue
        bus_count = bus_count + 1
        power_demand.append(float(row[1]))

power_demand = np.array(power_demand)

#gen_bus

gen_count = 0
position = []
max_gen = []
min_gen = []

with open('dcopf-csv/generator_data.csv','r') as generator_bus:
    reader = csv.reader(generator_bus)
    i = 0
    for row in reader:
        if i == 0:
            i = i + 1
            continue
        gen_count = gen_count + 1
        position.append(float(row[0]))
        max_gen.append(float(row[1]))
        min_gen.append(float(row[2]))

position = np.array(position)
max_gen = np.array(max_gen)
min_gen = np.array(min_gen)

#branch_data

from_bus = []
to_bus = []
x = np.zeros((bus_count,bus_count))
angmin = []
angmax = []
branch_count = 0


with open('dcopf-csv/branch_data.csv','r') as generator_bus:
    reader = csv.reader(generator_bus)
    i = 0
    for row in reader:
        if i == 0:
            i = i + 1
            continue
        from_bus.append(int(row[0]))
        to_bus.append(int(row[1]))
        x[int(row[0])-1][int(row[1])-1] = float(row[2])
        x[int(row[1])-1][int(row[0])-1] = float(row[2])
        angmin.append(float(row[3]))
        angmax.append(float(row[4]))
        branch_count = branch_count + 1

#gen_cost

second_degree = []
first_degree = []
const = []

with open('dcopf-csv/gen_cost.csv','r') as gen_cost:
    reader = csv.reader(gen_cost)
    i = 0
    for row in reader:
        if i == 0:
            i = i + 1
            continue 
        second_degree.append(float(row[0]))
        first_degree.append(float(row[1]))
        const.append(float(row[2]))

Q = np.zeros((gen_count+bus_count-1,gen_count+bus_count-1))
B = np.zeros((gen_count+bus_count-1,1))
imaginary_part = np.zeros((bus_count,bus_count))
A = np.zeros((bus_count+2*gen_count+2*branch_count,gen_count+bus_count-1))
C = np.zeros((bus_count+2*gen_count+2*branch_count,1))

for i in range(0,gen_count):
    Q[i][i] = 2*second_degree[i]
    B[i][0] = first_degree[i]
for i in range(0,bus_count-1):
    Q[gen_count+i][gen_count+i] = 0

#equality_constrafloats

for i in range(0,bus_count):
    for j in range(0,bus_count):
        if i == j:
            temp = 0
            for k in range(0,bus_count):
                if x[i][k] != 0:
                    temp = temp + 1/x[i][k]
            imaginary_part[i][j] = temp
        else:
            if x[i][j] != 0:
                imaginary_part[i][j] = -1/x[i][j]

for i in range(0,gen_count):
    A[i][i] = -1
for i in range(0,bus_count):
    for j in range(1,bus_count):
        A[i][gen_count+j-1] = imaginary_part[i][j]
for i in range(0,bus_count):
    C[i][0] = -power_demand[i] -imaginary_part[i][0] * 360

#generator constraints
for i in range(0,gen_count):
    A[bus_count+i][i] = 1
for i in range(0,gen_count):
    C[bus_count+i][0] = min_gen[i]

for i in range(0,gen_count):
    A[bus_count+gen_count+i][i] = -1
for i in range(0,gen_count):
    C[bus_count+gen_count+i][0] = -max_gen[i]

#power flow constraints
for i in range(0,branch_count):
    if from_bus[i] == 1:
        A[bus_count+2*gen_count+i][gen_count+to_bus[i]-2] = -1
        C[bus_count+2*gen_count+i][0] = angmin[i] - 360
    else:
        A[bus_count+2*gen_count+i][gen_count+from_bus[i]-2] = 1
        A[bus_count+2*gen_count+i][gen_count+to_bus[i]-2] = -1
        C[bus_count+2*gen_count+i][0] = angmin[i]


for i in range(0,branch_count):
    if from_bus[i] == 1:
        A[bus_count+2*gen_count+branch_count+i][gen_count+to_bus[i]-2] = 1
        C[bus_count+2*gen_count+branch_count+i][0] = -angmax[i] + 360
    else:
        A[bus_count+2*gen_count+branch_count+i][gen_count+from_bus[i]-2] = -1
        A[bus_count+2*gen_count+branch_count+i][gen_count+to_bus[i]-2] = 1
        C[bus_count+2*gen_count+branch_count+i][0] = -angmax[i]

A1 = np.insert(A,0, values=-A[0], axis=0)
C1 = np.insert(C,0,values=-C[0],axis=0)

for i in range(1,bus_count):
    A1 = np.insert(A1, 0, values=-A[i], axis=0)
    C1 = np.insert(C1,0,values=-C[i],axis=0)

asm_test = asm.ASM(Q,B,A1,C1,0)
asm_test.solve()
for i in range(0,bus_count):
    print('Generation of Bus '+str(i+1)+':',asm_test.x[i])

