import numpy as np
import pandas as pd
import pulp

c = np.array([[3,8,2,10,3],
              [8,7,2,9,7],
              [6,4,2,7,5],
              [8,4,2,3,5],
              [9,10,6,9,10]])
c = c.reshape(25,1)
c = pd.DataFrame(c)
workers = ['A','B','C','D','E']
jobs = ['j1','j2','j3','j4','j5']
c.index=pd.MultiIndex.from_product([['A','B','C','D','E'],['j1','j2','j3','j4','j5']])
c.columns = ['time']

# c_flat = c.flatten()

model = pulp.LpProblem('assignment problem', pulp.LpMinimize)

# 设定示性变量
job_assign = pulp.LpVariable.dicts('job assignment',
                                  ((worker,job) for worker,job in c.index),
                                  cat='Binary')

#加入优化函数
model += pulp.lpSum([job_assign[worker, job] * c.loc[(worker, job), 'time'] for worker, job in c.index])

# 约束条件是每个人有事做，每件事有人做
model += pulp.lpSum([job_assign['A', job] for job in jobs]) == 1
model += pulp.lpSum([job_assign['B', job] for job in jobs]) == 1
model += pulp.lpSum([job_assign['C', job] for job in jobs]) == 1
model += pulp.lpSum([job_assign['D', job] for job in jobs]) == 1
model += pulp.lpSum([job_assign['E', job] for job in jobs]) == 1

model += pulp.lpSum([job_assign[worker, 'j1'] for worker in workers]) == 1
model += pulp.lpSum([job_assign[worker, 'j2'] for worker in workers]) == 1
model += pulp.lpSum([job_assign[worker, 'j3'] for worker in workers]) == 1
model += pulp.lpSum([job_assign[worker, 'j4'] for worker in workers]) == 1
model += pulp.lpSum([job_assign[worker, 'j5'] for worker in workers]) == 1


model.solve()

result = []
for worker,job in c.index:
    result.append(job_assign[worker,job].varValue)

result_arr = np.array(result)
result_arr = result_arr.reshape(5,5)



for worker in workers:
    for job in jobs:
        if job_assign[worker,job].varValue == 1.0:
            print("工人{0}应该做{1}".format(worker,job))

print(pulp.value(model.objective))




