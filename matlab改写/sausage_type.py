import pulp

model = pulp.LpProblem("Cost minimising blending problem", pulp.LpMinimize)

# Construct our decision variable lists
sausage_types = ['economy', 'premium']
ingredients = ['pork', 'wheat', 'starch']

ing_weight = pulp.LpVariable.dicts(
    "weight kg",
    ((i,
      j) for i in sausage_types for j in ingredients),
    lowBound=0,
    cat='Continuous')

# Objective Function
model += (
    pulp.lpSum([
        4.32 * ing_weight[(i, 'pork')]
        + 2.46 * ing_weight[(i, 'wheat')]
        + 1.86 * ing_weight[(i, 'starch')]
        for i in sausage_types])
)

# Constraints
# 350 economy and 500 premium sausages at 0.05 kg
model += pulp.lpSum([ing_weight['economy', j] for j in ingredients]) == 350 * 0.05
model += pulp.lpSum([ing_weight['premium', j] for j in ingredients]) == 500 * 0.05
# Economy has >= 40% pork, premium >= 60% pork
model += ing_weight['economy', 'pork'] >= (
    0.4 * pulp.lpSum([ing_weight['economy', j] for j in ingredients]))

model += ing_weight['premium', 'pork'] >= (
    0.6 * pulp.lpSum([ing_weight['premium', j] for j in ingredients]))

# Sausages must be <= 25% starch
model += ing_weight['economy', 'starch'] <= (
    0.25 * pulp.lpSum([ing_weight['economy', j] for j in ingredients]))

model += ing_weight['premium', 'starch'] <= (
    0.25 * pulp.lpSum([ing_weight['premium', j] for j in ingredients]))

# We have at most 30 kg of pork, 20 kg of wheat and 17 kg of starch available
model += pulp.lpSum([ing_weight[i, 'pork'] for i in sausage_types]) <= 30
model += pulp.lpSum([ing_weight[i, 'wheat'] for i in sausage_types]) <= 20
model += pulp.lpSum([ing_weight[i, 'starch'] for i in sausage_types]) <= 17

# We have at least 23 kg of pork to use up
model += pulp.lpSum([ing_weight[i, 'pork'] for i in sausage_types]) >= 23

model.solve()


for sausage_type in sausage_types:
    for ingredient in ingredients:
        var_value = ing_weight[(sausage_type,ingredient)].varValue
        print("The weight of {0} in {1} sausages is {2} kg".format(ingredient, sausage_type, var_value))