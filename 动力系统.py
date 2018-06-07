import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 一元动力系统可手解 略

# 二元 如 a b两地汽车租赁  a地60%还回a地 b地70%还回b地

arr1 = np.zeros([100, 2])
arr1[0] = [7000, 0]
for i in range(1, len(arr1)):
    arr1[i, 0] = arr1[i - 1, 0] * 0.6 + arr1[i - 1, 1] * 0.3
    arr1[i, 1] = arr1[i - 1, 0] * 0.4 + arr1[i - 1, 1] * 0.7

df = pd.DataFrame(arr1)
df[0].plot()
df[1].plot()
plt.show()

# 三元 民主共和独立党转移矩阵

arr3 = np.zeros([100,3])
arr3[0] = [1/3,1/3,1/3]  # 共和、民主、独立
for i in range(1,len(arr3)):
    arr3[i,0] = 0.75 * arr3[i-1,0] + 0.2 * arr3[i-1,1] + 0.4 * arr3[i-1,2]
    arr3[i, 1] = 0.05 * arr3[i - 1, 0] + 0.6 * arr3[i - 1, 1] + 0.2 * arr3[i - 1, 2]
    arr3[i, 2] = 0.2 * arr3[i - 1, 0] + 0.2 * arr3[i - 1, 1] + 0.4 * arr3[i - 1, 2]
df = pd.DataFrame(arr3)
df[0].plot()
df[1].plot()
df[2].plot()
plt.show()

# 流行病模型 s为易感染者，i为以感染者，r为移出者
# 模型假设为  s(n) = s(n-1) - a * s(n-1) * i(n-1)   i(n) = i(n-1) - 0.6 * i(n-1) + a * i(n-1) * s(n-1)
# r(n) = r(n-1) + 0.6 * i(n-1)
a = 0.001407
arr2 = np.zeros([100, 3])  # 为sir
arr2[0] = [995, 5, 0]
for i in range(1, len(arr2 + 1)):
    arr2[i, 0] = arr2[i - 1, 0] - a * arr2[i - 1, 0] * arr2[i - 1, 1]
    arr2[i, 1] = arr2[i - 1, 1] - 0.6 * arr2[i - 1, 1] + \
        a * arr2[i - 1, 1] * arr2[i - 1, 0]
    arr2[i, 2] = arr2[i - 1, 2] + 0.6 * arr2[i - 1, 1]

df2 = pd.DataFrame(arr2)
plt.plot(df2[0], label='易感染者')
plt.plot(df2[1], label='以感染者')
plt.plot(df2[2], label='无感染风险者')

plt.legend()
plt.show()
