import numpy as np

#  到达时间，可正态分布
# arriving_time = np.random.uniform(0, 20, size=20)
arriving_time = sorted(np.random.normal(5, 1, size=20))

# 上厕所耗时
# working = np.random.uniform(1, 3, size=20)
working = np.random.normal(1.5, 1, size=20)
working[working < 0] = np.random.uniform(1, 3, size=len(working[working < 0]))


# 每个人的时间表，初始化为0，后赋值
starting_time = np.zeros(20)
finish_time = np.zeros(20)
waiting_time = np.zeros(20)
empty_time = np.zeros(20)

#  对于第一个人
starting_time[0] = arriving_time[0]  # 开始时间赋值为到达时间
finish_time[0] = starting_time[0] + working[0]  # 结束时间再加上每个人不同的上厕所耗时
waiting_time[0] = starting_time[0] - \
    arriving_time[0]  # 等待时间等于真正开始的时间减去到达的时间，第一个人无需等待

#  对于第二个人
starting_time[1] = arriving_time[1]
finish_time[1] = starting_time[1] + working[1]
waiting_time[1] = starting_time[1] - arriving_time[1]

for i in range(2, len(arriving_time)):  # 其他人循环
    if finish_time[i - 1] > arriving_time[i] and finish_time[i - 2] > arriving_time[i]:
        starting_time[i] = min(finish_time[i - 1], finish_time[i - 2])
    else:
        starting_time[i] = arriving_time[i]
        empty_time[i] = starting_time[i] - finish_time[i - 1]
    finish_time[i] = starting_time[i] + working[i]  # 这个人的结束时间计算
    waiting_time[i] = starting_time[i] - arriving_time[i]  # 这个人的 等待时间计算

print("average waiting time is %f" % np.mean(waiting_time))
