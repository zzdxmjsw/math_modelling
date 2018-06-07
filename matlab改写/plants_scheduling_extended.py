import pandas as pd
import pulp

"""引入工厂新开情况，同时有新开所需资金"""


# 数据导入
factories = pd.read_excel('plants.xlsx')
factories.index = pd.MultiIndex.from_product([[1,2,3,4,5,6,7,8,9,10,11,12],['A','B']])
factories.index.names = ['month','factory']

demand = pd.read_excel('demand.xlsx')
demand.index.name='month'

# 模型设定
model = pulp.LpProblem("Cost minimising scheduling problem", pulp.LpMinimize)

# 初始化变量
production = pulp.LpVariable.dicts("production",
                                     ((month, factory) for month, factory in factories.index),
                                     lowBound=0,
                                     cat='Integer')  # month and factory
factory_status = pulp.LpVariable.dicts("factory_status",
                                     ((month, factory) for month, factory in factories.index),
                                     cat='Binary')  # open or off

switch_on = pulp.LpVariable.dicts("switch_on",
                                    ((month, factory) for month, factory in factories.index),
                                    cat='Binary')

# Select index on factory A or B
factory_A_index = [tpl for tpl in factories.index if tpl[1] == 'A']
factory_B_index = [tpl for tpl in factories.index if tpl[1] == 'B']


# 目标函数--各月成本之和最小
model += pulp.lpSum(
    [production[month, factory] * factories.loc[(month, factory), 'Variable_Costs'] for month, factory in factories.index]
    + [factory_status[month, factory] * factories.loc[(month, factory), 'Fixed_Costs'] for month, factory in factories.index]
)


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


# 还有新开工厂情况
for month, factory in factories.index:
    # In month 1, if the factory is on, we assume it turned on
    if month == 1:
        model += switch_on[month, factory] == factory_status[month, factory]

    # In other months, if the factory is on in the current month AND off in the previous month, switch on = 1
    else:  # 三条件约束实现 AND逻辑
        model += switch_on[month, factory] >= factory_status[month, factory] - factory_status[month - 1, factory]
        model += switch_on[month, factory] <= 1 - factory_status[month - 1, factory]
        model += switch_on[month, factory] <= factory_status[month, factory]



model.solve()

output = []
for month, factory in production:
    var_output = {
        'Month': month,
        'Factory': factory,
        'Production': production[(month, factory)].varValue,
        'Factory Status': factory_status[(month, factory)].varValue,
        'Switch On': switch_on[(month, factory)].varValue
    }
    output.append(var_output)
output_df = pd.DataFrame.from_records(output).sort_values(['Month', 'Factory'])
output_df.set_index(['Month', 'Factory'], inplace=True)

print(pulp.value(model.objective))
