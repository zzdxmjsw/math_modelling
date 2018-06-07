import numpy as np
import pandas as pd
import pulp

demand = np.array([[20],[16],[13],[16],[19],[14],[12]])
demand_df = pd.DataFrame(demand)
demand_df.columns = ['demand']
demand_df.index = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

day_num_dict = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
num_day_dict = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}

def wrap_func(day_num):
    times = day_num // 7
    remain_num = day_num % 7
    if remain_num == 0:
        day_num -= (times-1) * 7
    else:
        day_num -= times * 7
    return day_num

# 初始化函数
model = pulp.LpProblem('stuff time_series assignment',pulp.LpMinimize)

# 设置变量

worker_days = pulp.LpVariable.dicts('worker day',
                                  (weekday for weekday in  demand_df.index) ,
                                  cat='Integer')

# 设置最优化函数
model += pulp.lpSum(worker_days[weekday] for weekday in demand_df.index)

# 约束
for day in demand_df.index:  # 对周一到周日按需求加约束
    start_day = day_num_dict[day] + 3
    end_day = day_num_dict[day] + 7
    model += pulp.lpSum(
        [worker_days[num_day_dict[wrap_func(continuous_day)]] for continuous_day in range(start_day,end_day+1)])\
             >= demand_df.loc[day,'demand']  # 具体约束条件

model.solve()

for day in demand_df.index:
    print('{0} 需要{1}个职员'.format(day,worker_days[day].varValue))