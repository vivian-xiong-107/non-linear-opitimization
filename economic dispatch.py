import csv
import pandas
import numpy as np
import asm
import simplex_api

#gen_bus

gen_count = 0
position = []
max_gen = []
min_gen = []

with open('/Users/xiongcaiwei/Downloads/code/economic-dispatch-csv/economic_dispatch.csv','r') as generator_bus:
    reader = csv.reader(generator_bus)
    i = 0
    for row in reader:
        if i == 0:
            i = i + 1
            continue
        if i == 1:
            power_demand = float(row[3])
        gen_count = gen_count + 1
        position.append(float(row[0]))
        max_gen.append(float(row[1]))
        min_gen.append(float(row[2]))
        i = i + 1

position = np.array(position)
max_gen = np.array(max_gen)
min_gen = np.array(min_gen)

#gen_cost

second_degree = []
first_degree = []
const = []

with open('/Users/xiongcaiwei/Downloads/code/economic-dispatch-csv/gen_cost.csv','r') as gen_cost:
    reader = csv.reader(gen_cost)
    i = 0
    for row in reader:
        if i == 0:
            i = i + 1
            continue 
        second_degree.append(float(row[0]))
        first_degree.append(float(row[1]))
        const.append(float(row[2]))

Q = np.zeros((gen_count,gen_count))
B = np.zeros((gen_count,1))
A = np.zeros((2*gen_count+1,gen_count))
C = np.zeros((2*gen_count+1,1))

for i in range(0,gen_count):
    Q[i][i] = 2*second_degree[i]
    B[i][0] = first_degree[i]

#equality_constrafloats

for i in range(0,gen_count):
    A[0][i] = 1

C[0][0] = power_demand

#generator constraints
for i in range(0,gen_count):
    A[1+i][i] = 1
for i in range(0,gen_count):
    C[1+i][0] = min_gen[i]

for i in range(0,gen_count):
    A[1+gen_count+i][i] = -1
for i in range(0,gen_count):
    C[1+gen_count+i][0] = -max_gen[i]



A1 = np.insert(A, 0, values=-A[0], axis=0)
C1 = np.insert(C,0,values=-C[0],axis=0)


asm_test = asm.ASM(Q,B,A1,C1,0)
asm_test.solve()
#print("ans",asm_test.x)
#print("The solution is:")
num = 1
for i in range(0,gen_count):
    print('Generation of Bus '+str(i+1)+':',asm_test.x[i])
#print("working_set",asm_test.working_set)
