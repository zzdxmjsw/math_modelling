import numpy as np
import pandas as pd


# arrive = np.random.normal(80,50,[1000])
# arrive[arrive < 0] = 0.1

def boat_queue_unique(boat_num):
    arrive = np.random.uniform(15, 154, [boat_num])
    unload = np.random.uniform(45, 90, [boat_num])

    cal_info = np.zeros([boat_num, 9])
    cal_info[:, 0] = arrive
    cal_info[:, 3] = unload

    df = pd.DataFrame(
        cal_info,
        columns=[
            '间隔',
            '到达时间',
            '开始时间',
            '卸货时间',
            '结束时间',
            '排队长度',
            '等待时间',
            '在港时间',
            '空闲时间'])

    df['到达时间'] = df['间隔'].cumsum()

    for i in range(boat_num):
        if i == 0:
            df.ix[i, 2] = df.ix[i, 1]  # 开始时间
            df.ix[i, 4] = df.ix[i, 2] + df.ix[i, 3]  # 结束时间
            df.ix[i, 5] = 0  # 排队长度
            df.ix[i, 6] = 0  # 等待时间
            df.ix[i, 7] = df.ix[i, 3]  # 在港时间
            df.ix[i, 8] = df.ix[i, 1]  # 空闲时间
        else:
            if df.ix[i, 1] < df.ix[i - 1, 4]:  # 到达时未结束
                df.ix[i, 2] = df.ix[i - 1, 4]  # 上艘结束时开始
                df.ix[i, 4] = df.ix[i, 2] + df.ix[i, 3]  # 结束时间
                count = 0
                j = i
                while j != 0 and df.ix[j - 1, 4] > df.ix[i, 1]:
                    count += 1
                    j -= 1
                df.ix[i, 5] = count  # 排队长度
                df.ix[i, 6] = df.ix[i, 2] - df.ix[i, 1]  # 等待时间
                df.ix[i, 7] = df.ix[i, 4] - df.ix[i, 1]  # 在港时间
                df.ix[i, 8] = 0  # 没有空闲时间
            else:  # 到达时没有船
                df.ix[i, 2] = df.ix[i, 1]  # 到达时开始
                df.ix[i, 4] = df.ix[i, 2] + df.ix[i, 3]  # 结束时间
                df.ix[i, 5] = 0  # 不需排队
                df.ix[i, 6] = 0  # 不需等待
                df.ix[i, 7] = df.ix[i, 3]  # 在港时间为卸货时间
                df.ix[i, 8] = df.ix[i, 2] - df.ix[i - 1, 4]  # 空闲时间

    avg_at_port = np.average(df['在港时间'])
    max_at_port = np.max(df['在港时间'])
    avg_wait = np.average(df['等待时间'])
    max_wait = np.max(df['等待时间'])
    per_free = df.ix[:, 8].sum() / np.max(df.ix[:, 4])
    max_queue = np.max(df.ix[:, 5])

    print('平均在港时间：', avg_at_port)
    print('最大在港时间：', max_at_port)
    print('平均等待时间：', avg_wait)
    print('最大等待时间：', max_wait)
    print('设备空置率：', per_free)
    print('最大排队长度', max_queue)
    return df


def boat_queue_normal(boat_num):
    arrive = np.random.normal(80, 50, [boat_num])
    arrive[arrive < 15] = 15
    arrive[arrive > 145] = 145
    unload = np.random.normal(66, 36, [boat_num])
    unload[unload < 45] = 45
    unload[unload > 90] = 90

    cal_info = np.zeros([boat_num, 9])
    cal_info[:, 0] = arrive
    cal_info[:, 3] = unload

    df = pd.DataFrame(
        cal_info,
        columns=[
            '间隔',
            '到达时间',
            '开始时间',
            '卸货时间',
            '结束时间',
            '排队长度',
            '等待时间',
            '在港时间',
            '空闲时间'])

    df['到达时间'] = df['间隔'].cumsum()

    for i in range(boat_num):
        if i == 0:
            df.ix[i, 2] = df.ix[i, 1]  # 开始时间
            df.ix[i, 4] = df.ix[i, 2] + df.ix[i, 3]  # 结束时间
            df.ix[i, 5] = 0  # 排队长度
            df.ix[i, 6] = 0  # 等待时间
            df.ix[i, 7] = df.ix[i, 3]  # 在港时间
            df.ix[i, 8] = df.ix[i, 1]  # 空闲时间
        else:
            if df.ix[i, 1] < df.ix[i - 1, 4]:  # 到达时未结束
                df.ix[i, 2] = df.ix[i - 1, 4]  # 上艘结束时开始
                df.ix[i, 4] = df.ix[i, 2] + df.ix[i, 3]  # 结束时间
                count = 0
                j = i
                while j != 0 and df.ix[j - 1, 4] > df.ix[i, 1]:
                    count += 1
                    j -= 1
                df.ix[i, 5] = count  # 排队长度
                df.ix[i, 6] = df.ix[i, 2] - df.ix[i, 1]  # 等待时间
                df.ix[i, 7] = df.ix[i, 4] - df.ix[i, 1]  # 在港时间
                df.ix[i, 8] = 0  # 没有空闲时间
            else:  # 到达时没有船
                df.ix[i, 2] = df.ix[i, 1]  # 到达时开始
                df.ix[i, 4] = df.ix[i, 2] + df.ix[i, 3]  # 结束时间
                df.ix[i, 5] = 0  # 不需排队
                df.ix[i, 6] = 0  # 不需等待
                df.ix[i, 7] = df.ix[i, 3]  # 在港时间为卸货时间
                df.ix[i, 8] = df.ix[i, 2] - df.ix[i - 1, 4]  # 空闲时间

    avg_at_port = np.average(df['在港时间'])
    max_at_port = np.max(df['在港时间'])
    avg_wait = np.average(df['等待时间'])
    max_wait = np.max(df['等待时间'])
    per_free = df.ix[:, 8].sum() / np.max(df.ix[:, 4])
    max_queue = np.max(df.ix[:, 5])

    print('平均在港时间：', avg_at_port)
    print('最大在港时间：', max_at_port)
    print('平均等待时间：', avg_wait)
    print('最大等待时间：', max_wait)
    print('设备空置率：', per_free)
    print('最大排队长度', max_queue)
    return df

result = boat_queue_normal(1000)

