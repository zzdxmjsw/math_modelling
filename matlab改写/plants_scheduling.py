import pandas as pd
import pulp

# 数据导入
factories = pd.read_excel('plants.xlsx')
factories.index = pd.MultiIndex.from_product([[1,2,3,4,5,6,7,8,9,10,11,12],['A','B']])
factories.index.names = ['month','factory']

demand = pd.read_excel('demand.xlsx')
demand.index.name='month'

# 模型设定
model = pulp.LpProblem("Cost minimising scheduling problem", pulp.LpMinimize)

# 规划变量值产量
production = pulp.LpVariable.dicts("production",
                                     ((month, factory) for month, factory in factories.index),
                                     lowBound=0,
                                     cat='Integer')  # month and factory
# 规划变量值生产状态
factory_status = pulp.LpVariable.dicts("factory_status",
                                     ((month, factory) for month, factory in factories.index),
                                     cat='Binary')  # open or off


model += pulp.lpSum(
    [production[month, factory] * factories.loc[(month, factory), 'Variable_Costs'] for month, factory in factories.index]
    + [factory_status[month, factory] * factories.loc[(month, factory), 'Fixed_Costs'] for month, factory in factories.index]
)  # 目标函数--各月成本之和最小


months = demand.index
for month in months:  # 每月产量必须等于需求量
    model += production[(month, 'A')] + production[(month, 'B')] == demand.loc[month, 'Demand']


for month, factory in factories.index:  # 用以确认on or off
    min_production = factories.loc[(month, factory), 'Min_Capacity']
    max_production = factories.loc[(month, factory), 'Max_Capacity']  # 由最大最小确定on off，若off，0<=产量<=0
    model += production[(month, factory)] >= min_production * factory_status[month, factory]  # 产量大于等于最小产量
    model += production[(month, factory)] <= max_production * factory_status[month, factory]  # 产量小于等于最大产量

model += factory_status[5, 'B'] == 0  # 第5月B一定关闭（题目给定
model += production[5, 'B'] == 0  # 因此第5月B产量一定为0

model.solve()


output = []
for month, factory in production:
    var_output = {
        'Month': month,
        'Factory': factory,
        'Production': production[(month, factory)].varValue,
        'Factory Status': factory_status[(month, factory)].varValue
    }
    output.append(var_output)
output_df = pd.DataFrame.from_records(output).sort_values(['Month', 'Factory'])
output_df.set_index(['Month', 'Factory'], inplace=True)

print(pulp.value(model.objective))
