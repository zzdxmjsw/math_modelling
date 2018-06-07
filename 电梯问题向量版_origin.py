import numpy as np
import pandas as pd


class elevator_system():
    """
    :param between(i)     乘客到达间隔时间 [1,30]
    :param arrive(i)      乘客到达时间 [0,4800]
    :param floor(i)       乘客选择的楼层 [1,12]
    :param cus_el_time(i) 乘客在电梯中的时间
    :param cus_wait_time(i)乘客的等待时间，包括在电梯中
    :param cus_del_time(i)乘客在所花的总时间，上两项之和
    :param sel_vec(j)     一辆电梯0到12层的选择，0和1
    :param flr_vec(j)     一辆电梯0到12层每层的选择数
    :param occupant(j)    一辆电梯内的人数 [1,12]
    :param return_time(j) 一辆电梯回到一楼的时间点 [0,4800]
    :param first(j)       一辆电梯每批次搭乘的第一个乘客编号
    :param que_custom     等电梯的第一个乘客序号
    :param queue_len      当前排队总长度（动态变化）
    :param start_que      当前队伍开始排起来的时间点 [0,4800]
    :param stops(j)       一辆电梯整个过程中的停止数？
    :param el_del(j)      一辆电梯用于运输花的总时间
    :param el_operate(j)  一辆电梯的运营总时间 （由于等待和空置比上一参数长）
    :param limit          电梯出发前最后一个上电梯的乘客的编号
    :param highest_floor  最高层
    :param remain         装完一批乘客后剩余的排队乘客
    :param que_total      所有等待了电梯的乘客数
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

    def __init__(self):
        self.between = np.random.choice(range(0, 31), [400, ])
        self.arrive = self.between.cumsum()
        self.floor = np.random.choice(range(1, 13), [400, ])
        self.cus_el_time = np.zeros([400, ])  # 对乘客
        self.cus_wait_time = np.zeros([400, ])
        self.cus_del_time = np.zeros([400, ])
        self.sel_vec = np.array([[0] * 12] * 4)
        self.flr_vec = np.array([[0] * 12] * 4)
        self.occupant = np.zeros([4, ])
        self.return_time = np.zeros([4, ])
        self.first = np.zeros([4, ])
        self.que_custom = 0
        self.queue_len = 0
        self.start_que = 0
        self.stops = np.zeros([4, ])
        self.el_del = np.zeros([4, ])  # 对电梯
        self.el_operate = np.zeros([4, ])
        self.limit = 0  # 最后上电梯乘客的编号
        self.highest_floor = 0
        self.remain = 0
        self.que_total = 0
        self.TIME = 0
        self.AVG_DEL_TIME = 0
        self.AVG_EL_TIME = 0
        self.MAX_DEL_TIME = 0
        self.MAX_EL_TIME = 0
        self.MAX_QUE_LEN = 0
        self.AVG_QUE_TIME = 0
        self.MAX_QUE_TIME = 0
        self.current_cus = 0
        self.current_el = 0

    def get_highest_floor(self, vector):
        highest = 0
        for count in range(len(vector)):
            if vector[count] != 0:
                highest = count + 1
        return highest  # 如6层返回6

    def queue(self):  # step 19~32
    # step 19
        self.que_custom = self.current_cus
        self.start_que = self.TIME
        self.queue_len = 1
        # self.arrive 不需做了

    # step 20
        self.current_cus += 1
        self.TIME += self.between[self.current_cus]
        self.queue_len += 1
    # step 21



    def core(self):  # step 5~32
        # step 5
        while self.TIME >= max(self.return_time):  # 有可用的电梯
            if self.TIME >= self.return_time[0]:
                self.current_el = 0
            elif self.TIME >= self.return_time[1]:
                self.current_el = 1
            elif self.TIME >= self.return_time[1]:
                self.current_el = 2
            elif self.TIME >= self.return_time[1]:
                self.current_el = 3
            # step 6
            self.first[self.current_el] = self.current_cus
            self.occupant[self.current_el] = 0
            # 两个楼层向量必须要重新初始化过（第二次经过时不为0）
            self.sel_vec[self.current_el] = np.array([[0] * 12] * 4)
            self.flr_vec[self.current_el] = np.array([[0] * 12] * 4)

            # step 7~10 装填电梯
            # step 7
            while self.between[self.current_cus] <= 15 and self.occupant[self.current_el] < 12:  # 未装满
                # 当前用户若选12楼，则在sel_vec 11 加
                self.sel_vec[self.current_el][self.floor[self.current_cus] - 1] = 1
                # 添加楼层信息
                self.flr_vec[self.current_el][self.floor[self.current_cus] - 1] += 1
                self.occupant[self.current_el] += 1  # 电梯内人数+1

                # step 8
                self.current_cus += 1
                self.TIME += self.between[self.current_cus]
                self.cus_del_time[self.current_cus] = 15

                # step 9
                self.return_time[self.return_time <= self.TIME] = self.TIME

                # step 10
                for k in range(self.first[self.current_el], self.current_cus):
                    self.cus_del_time[self.current_cus] += self.between[k]

            # step 11~17 开车！
            # step 12
            self.limit = self.current_cus - 1
            for k in range(self.first[self.current_el], self.limit):  # 修改电梯中每个的耗时
                up = self.floor[k] - 1  # 当前乘客需要上升的楼层（扣除1层）
                self.cus_el_time[k] = 10 * up + 3 * self.flr_vec[self.current_el][:up].sum() + 3 \
                                      + 10 * self.sel_vec[self.current_el][:up].sum() + 5
                # 上升时间（一层10s）+ 之前楼层下电梯乘客时间（每人3s）+ 自己下电梯 + 之前楼层关开门（5s*2）+ 当前楼层开门

                # step 13
                self.cus_del_time[k] += self.cus_el_time[k]

                # step 14
                self.AVG_DEL_TIME += self.cus_del_time[k]

                # step 15
                self.MAX_DEL_TIME = max(self.MAX_DEL_TIME, self.cus_del_time[k])

                # step 16
                self.MAX_EL_TIME = max(self.MAX_EL_TIME, self.cus_el_time[k])

            # step 17
            self.stops[self.current_el] += self.sel_vec[self.current_el].sum()
            self.highest_floor = self.get_highest_floor(self.sel_vec[self.current_el])
            self.el_del[self.current_el] = 20 * (self.highest_floor - 1) + 3 * self.flr_vec[self.current_el].sum() \
                                           + 10 * self.sel_vec[self.current_el].sum()
            self.return_time[self.current_el] = self.TIME + self.el_del[self.current_el]
            self.el_operate[self.current_el] += self.el_del[self.current_el]  # 不需排队，从0开始加

        self.queue()



    def run(self):
        # 单独处理第一个人
        self.cus_del_time[self.current_cus] = 15
        self.TIME = self.between[self.current_cus]
        self.return_time = np.repeat(self.TIME, 4)
        self.core()


sys1 = elevator_system()
