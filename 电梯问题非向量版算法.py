import random
# np.random.chisquare() 员工到达时间可以用卡方分布来模拟。但要注意：
# 1、要用相减来使分布向右贴近八点 2、多数人集中于7:50左右到，不可过于超过八点 3、卡方一定大于0，所以要控制使得适当的有迟到
# 但题目只要求7:50 ~ 9:10
# 设有最多不超过400名员工

"""
    :param between(i)     乘客到达间隔时间 [1,30]
    :param arrive(i)      乘客到达时间 [0,4800]
    :param floor(i)       乘客选择的楼层 [1,12]
    :param el_time(i)     乘客在电梯中的时间
    :param wait_time(i)   乘客的等待时间，包括在电梯中
    :param del_time(i)    乘客在所花的总时间，上两项之和
    :param sel_vec(j)     一辆电梯0到12层的选择，0和1
    :param flr_vec(j)     一辆电梯0到12层每层的选择数
    :param occupant(j)    一辆电梯内的人数 [1,12]
    :param return(j)      一辆电梯回到一楼的时间点 [0,4800]
    :param first(j)       一辆电梯每批次搭乘的第一个乘客编号
    :param que_custom     等电梯的第一个乘客序号
    :param queue          排队总长度
    :param start_que      当前队伍开始排起来的时间点 [0,4800]
    :param stop(j)        一辆电梯整个过程中的停止数？
    :param el_del(j)      一辆电梯用于运输花的总时间
    :param el_operate(j)  一辆电梯的运营总时间 （由于等待和空置比上一参数长）
    :param limit          电梯出发前最后一个上电梯的乘客的编号
    :param max_floor      最高层
    :param remain         装完一批乘客后剩余的排队乘客
    :param que_total      所有在需等待电梯的乘客数
    :param TIME           计时器
    :param AVG_DEL_TIME   乘客从到达大厅至到达目的地所花的平均时间
    :param AVG_EL_TIME    乘客在电梯中的平均时间
    :param MAX_DEL_TIME   乘客从到达大厅至到达目的地所花的最大时间
    :param MAX_EL_TIME    乘客在电梯中的最大时间
    :param MAX_QUE_LEN    所形成的最大队列长度
    :param AVG_QUE_TIME   乘客排队所花的平均时间
    :param MAX_QUE_TIME   乘客排队所花的最大时间

    :returns AVG_DEL_TIME,AVG_EL_TIME,MAX_DEL_TIME,MAX_ELTIME,QUE_LEN,AVG_QUE_TIME,MAX_QUE_TIME,stop
"""


def vec_sum(start, end, vector):
    sum_num = 0
    for count in range(start, end + 1):
        sum_num += vector[count]
    return sum_num


def get_highest_floor(vector):
    highest = 0
    for count in range(len(vector)):
        if vector[count] != 0:
            highest = count + 1
    return highest


# step 1 initialize parameters
AVG_DEL_TIME, AVG_EL_TIME, MAX_DEL_TIME, MAX_EL_TIME, MAX_QUE_LEN, AVG_QUE_TIME, MAX_QUE_TIME = [
    0] * 7

# STEP 2

i = 1  # 第一个顾客
between_1 = random.choice(range(0, 31))
floor_1 = random.choice(range(1, 13))
variables = locals()
del_time_1 = 15
for cus in range(2, 401):
    variables['del_time_%s' % cus] = 0
    variables['between_%s' % cus] = random.choice(range(0, 31))
    variables['floor_%s' % cus] = random.choice(range(1, 13))
# step 3
TIME = variables['between_%s' % i]

for el in range(1, 5):
    variables['return_%s' % el] = variables['between_%s' % i]
    variables['stop_%s' % el] = 0
    variables['operate_%s' % el] = 0
    variables['first_%s' % el] = 0
    variables['occupant_%s' % el] = 0
    variables['sel_vec_%s' % el] = [0] * 12
    variables['flr_vec_%s' % el] = [0] * 12


for cus in range(1, 401):
    variables['wait_%s' % cus] = 0
    variables['el_time_%s' % cus] = 0

# step 4&5
while TIME < 4800:
    # 确定当前电梯 el
    if TIME >= variables['return_%s' % 1]:
        el = 1
    elif TIME >= variables['return_%s' % 2]:
        el = 2
    elif TIME >= variables['return_%s' % 3]:
        el = 3
    elif TIME >= variables['return_%s' % 4]:
        el = 4
    else:
        pass  # step 19

# step 6  # 给乘客编号并初始化两个向量
    variables['first_%s' % el] = i
    variables['occupant_%s' % el] = 0
    sel_vec = [0] * 12
    flr_vec = [0] * 12
# step 7

    variables['sel_vec_%s' % el][variables['floor_%s' % i] - 1] = 1
    variables['flr_vec_%s' % el][variables['floor_%s' % i] - 1] = 1
    variables['occupant_%s' % el] += 1
# step 8
    i += 1
    between = random.choice(range(0, 31))
    floor = random.choice(range(0, 13))
    TIME += between
    variables['del_time_%s' % i] = 15
# step 9
    for k in range(1, 5):  # 同步所有电梯的时间
        if TIME >= variables['return_%s' % k]:
            variables['return_%s' % el] = TIME
# step 10
    if between < 15 and variables['occupant_%s' %
                                  el] < 12:  # 若未满载且下一乘客到达时间小于15秒，继续等待
        for k in range(
                variables['first_%s' % el], i):  # 从该电梯第一个乘客到前一个乘客(当前乘客以加上了15秒
            variables['del_time_%s' % i] += between  # 给deliver 计时器加上这个间隔
        # TODO: goto step 7

    else:  # 不等你了！开车！
        limit = i - 1  # 也就是截止到上一个人

# step 11 开车过程 12~16
        for cus in range(variables['first_%s' % el], limit + 1):  # 送每一个乘客下车
            # step 12
            N = variables['floor_%s' % cus] - 1
            variables['el_time_%s' %
                      cus] = 10 * N + 3 * vec_sum(1, N, variables['flr_vec_%s' % el]) + 3 \
                             + 10 * vec_sum(1, N, variables['sel_vec_%s' % el]) + 5
# step 13
            variables['del_time_%s' %
                      cus] += variables['el_time_%s' %
                                        cus]  # 该乘客的运输时间
# step 14
            AVG_DEL_TIME += variables['del_time_%s' % cus]  # 总的运输时间（未平均
# step 15
            if variables['del_time_%s' % cus] > MAX_DEL_TIME:  # 若超过最大运输时间
                MAX_DEL_TIME = variables['del_time_%s' % cus]
# step 16
            if variables['el_time_%s' % cus] > MAX_EL_TIME:  # 若超过最大电梯中时间
                MAX_EL_TIME = variables['el_time_%s' % cus]
# step 17
        variables['stop_%s' %
                  el] += vec_sum(1, 12, variables['sel_vec_%s' % el])

        max_floor = get_highest_floor(variables['sel_vec_%s' % el])
        variables['el_del_%s' % el] = 20 * (max_floor - 1) + 3 * vec_sum(1, 12, variables['flr_vec_%s' % el]) \
                                      + 10 * vec_sum(1, 12, variables['sel_vec_%s' % el])
        variables['return_%s' % el] = TIME + variables['el_del_%s' % el]
        variables['operate_%s' % el] += variables['el_del_%s' % el]
# step 18