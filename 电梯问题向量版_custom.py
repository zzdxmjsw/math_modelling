import numpy as np
import pandas as pd
import os


class data_reader():
    def __init__(self, custom_num):
        self.between_path = 'between.csv'
        self.arrive_path = 'arrive.csv'
        self.floor_path = 'floor.csv'
        self.custom_num = custom_num

    def read_between(self):
        if os.path.exists(self.between_path):
            array = np.loadtxt(self.between_path)
            return array
        else:
            array = np.random.choice(range(0, 25), [self.custom_num, ])
            np.savetxt(self.between_path, array)
            return array

    def read_arrive(self):
        if os.path.exists(self.between_path):
            between = np.loadtxt(self.between_path)
            arrive = between.cumsum()
            np.savetxt(self.arrive_path, arrive)
            return arrive
        else:
            between = self.read_between()
            arrive = between.cumsum()
            np.savetxt(self.arrive_path, arrive)
            return arrive

    def read_floor(self):
        if os.path.exists(self.floor_path):
            array = np.loadtxt(self.floor_path)
            array = array.astype(np.int)
            return array
        else:
            array = np.random.choice(range(2, 13), [self.custom_num, ])
            np.savetxt(self.floor_path, array)
            return array


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
    :param el_del(j)      一辆电梯用于运输当前乘客花的时间
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

    def __init__(self, custom_num):
        # 乘客选择数据
        self.reader = data_reader(custom_num)
        self.cus_num = custom_num
        # self.between = np.random.choice(range(0, 25), [custom_num, ])
        self.between = data_reader.read_between(self.reader)
        # self.arrive = self.between.cumsum()
        self.arrive = data_reader.read_arrive(self.reader)
        # self.floor = np.random.choice(range(2, 13), [custom_num, ])
        self.floor = data_reader.read_floor(self.reader)

        df = pd.DataFrame([self.arrive,self.floor]).T
        df.to_csv('data.csv')

        # 乘客时间数据
        self.cus_el_time = np.zeros([custom_num, ])  # 对乘客
        self.cus_wait_time = np.zeros([custom_num, ])
        self.cus_del_time = np.zeros([custom_num, ])

        # 电梯运行数据
        self.sel_vec = np.array([[0] * 12] * 4)
        self.flr_vec = np.array([[0] * 12] * 4)
        self.occupant = np.array([0] * 4)
        self.return_time = np.array([0] * 4)
        self.first = np.array([0] * 4)

        # 排队数据
        self.que_custom = 0
        self.queue_len = 0
        self.start_que = 0

        # 电梯数据
        self.stops = np.zeros([4, ])
        self.el_del = np.zeros([4, ])  # 对电梯
        self.el_operate = np.zeros([4, ])
        self.limit = 0  # 最后上电梯乘客的编号

        # 统计数据
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
        self.el_available = np.ones([4, ])  # 一开始全部可乘坐

    def judge_loadable(self, time) -> int:  # 待修改：是判断return_time 还是 self.el_available
        for el in range(0, 4):
            if self.return_time[el] <= time:
                return el
        return -1

    def get_highest_floor(self, vector):
        highest = 0
        for count in range(len(vector)):
            if vector[count] != 0:
                highest = count + 1
        return highest  # 如6层返回6

    def get_loaded_full(self,start,end,el):
        for cus in range(start, end + 1):  # 电梯 共12人
            self.occupant[el] += 1
            self.sel_vec[el][self.floor[cus] - 1] = 1
            self.flr_vec[el][self.floor[cus] - 1] += 1
            # 乘客
            self.cus_del_time[cus] = self.return_time[el] - self.arrive[cus]
            self.cus_wait_time[cus] = self.return_time[el] - self.arrive[cus]

    def get_loaded_not_full(self,start,end,el):
        for cus in range(start, end + 1):
            self.occupant[el] += 1
            self.sel_vec[el][self.floor[cus] - 1] = 1
            self.flr_vec[el][self.floor[cus] - 1] += 1
            self.cus_del_time[cus] = self.arrive[self.current_cus - 1] + 15 - self.arrive[cus]
            self.cus_wait_time[cus] = self.arrive[self.current_cus - 1] + 15 - self.arrive[cus]

    def operate_none_queue(self):
        self.limit = self.current_cus
        for cus in range(
                self.first[self.current_el], self.limit + 1):  # 修改电梯中每个的耗时
            up = self.floor[cus] - 1  # 当前乘客需要上升的楼层（扣除1层）
            self.cus_el_time[cus] = 10 * up + 3 * self.flr_vec[self.current_el][:up].sum(
            ) + 3 + 10 * self.sel_vec[self.current_el][:up].sum() + 5  # 电梯时间
            self.cus_del_time[cus] = self.TIME + self.cus_el_time[cus] - self.arrive[cus]  # 没有排队
            self.AVG_DEL_TIME += self.cus_del_time[cus]
            self.MAX_DEL_TIME = max(self.MAX_DEL_TIME, self.cus_del_time[cus])
            self.MAX_EL_TIME = max(self.MAX_EL_TIME, self.cus_el_time[cus])

        self.stops[self.current_el] += self.sel_vec[self.current_el].sum()  # 不清零
        self.highest_floor = self.get_highest_floor(
            self.sel_vec[self.current_el])
        self.el_del[self.current_el] = 20 * (self.highest_floor - 1) + 3 * self.flr_vec[self.current_el].sum() \
            + 10 * self.sel_vec[self.current_el].sum()
        self.return_time[self.current_el] = self.TIME + \
            self.el_del[self.current_el]
        self.el_operate[self.current_el] += self.el_del[self.current_el]
        self.occupant[self.current_el] = 0
        self.sel_vec[self.current_el] = np.array([[0] * 12])
        self.flr_vec[self.current_el] = np.array([[0] * 12])

    def operate_queue(self):
        for cus in range(self.first[self.current_el], self.limit):
            up = self.floor[cus] - 1  # 当前乘客需要上升的楼层（扣除1层）
            self.cus_el_time[cus] = 10 * up + 3 * self.flr_vec[self.current_el][:up].sum(
            ) + 3 + 10 * self.sel_vec[self.current_el][:up].sum() + 5  # 电梯时间
            self.cus_del_time[cus] += self.cus_el_time[cus]  # 没有排队
            self.AVG_DEL_TIME += self.cus_del_time[cus]
            self.MAX_DEL_TIME = max(self.MAX_DEL_TIME, self.cus_del_time[cus])
            self.MAX_EL_TIME = max(self.MAX_EL_TIME, self.cus_el_time[cus])

        self.stops[self.current_el] += self.sel_vec[self.current_el].sum()
        self.highest_floor = self.get_highest_floor(
            self.sel_vec[self.current_el])
        self.el_del[self.current_el] = 20 * (self.highest_floor - 1) + 3 * self.flr_vec[self.current_el].sum() \
            + 10 * self.sel_vec[self.current_el].sum()
        self.return_time[self.current_el] = self.TIME + \
            self.el_del[self.current_el]
        self.el_operate[self.current_el] += self.el_del[self.current_el]
        self.occupant[self.current_el] = 0
        self.sel_vec[self.current_el] = np.array([[0] * 12])
        self.flr_vec[self.current_el] = np.array([[0] * 12])

    def init_queue(self):
        self.que_custom = self.current_cus
        self.start_que = self.TIME
        self.queue_len = 0

    def queue(self):
        if self.queue_len == 0:
            self.init_queue()
        self.queue_len += 1
        # self.current_el = self.judge_loadable(self.TIME)
        self.remain = self.queue_len

    def handle_none_queue(self):
        if self.occupant[self.current_el] == 0:  # 若电梯为空，存入第一个上的人
            self.first[self.current_el] = self.current_cus
        # step 7
        self.occupant[self.current_el] += 1
        # 当前电梯当前顾客这一层选中（sel_vec从0开始
        self.sel_vec[self.current_el][self.floor[self.current_cus] - 1] = 1
        self.flr_vec[self.current_el][self.floor[self.current_cus] - 1] += 1
        #  step 8
        self.cus_del_time[self.current_cus] += 15
        # step 9
        self.return_time[self.return_time <= self.TIME] = self.TIME

        # step 10
        if self.current_cus == self.cus_num - 1:
            if self.occupant[self.current_el] == 12:
                self.TIME += 15
                self.operate_none_queue()
        else:
            if self.occupant[self.current_el] == 12 or self.between[self.current_cus + 1] > 15:  # 发车
                self.TIME += 15
                self.operate_none_queue()


    def run(self):
        current_cus_num = 0
        while current_cus_num < self.cus_num:  # 循环判断
            print('第%s人' % str(current_cus_num+1))
            self.current_cus = current_cus_num
            self.TIME = self.arrive[self.current_cus]  # 更新当前时间
            self.current_el = self.judge_loadable(self.TIME)

            if self.current_el == -1:  # 没有电梯
                self.queue()
                self.que_total += 1
                current_cus_num += 1  # 下一循环

            else:  # 有电梯
                if self.queue_len == 0:  # 直接上电梯
                    self.handle_none_queue()
                    current_cus_num += 1

                else:  # 排队后上电梯  #!!!!注意乘客for循环和队伍前面人不要混起来了
                    # 要区分是否在当前乘客前电梯抵达----之前在排队，你到的时间可能电梯已经到了接走乘客又走了
                    # self.queue_len -= 1  严禁这样的操作！便判断边修改
                    if self.remain >= 12:  # 取等。此时直接走
                        self.first[self.current_el] = self.que_custom
                        self.limit = self.que_custom + 11  # 加11才是最后一个人编号
                        self.AVG_QUE_TIME += (self.return_time[self.current_el] -
                                              self.arrive[self.que_custom:self.limit +
                                                          1]).sum()

                        '''for cus in range(
                                self.que_custom, self.limit + 1):  # 电梯 共12人
                            self.occupant[self.current_el] += 1
                            self.sel_vec[self.current_el][self.floor[cus] - 1] = 1
                            self.flr_vec[self.current_el][self.floor[cus] - 1] += 1
                            # 乘客
                            self.cus_del_time[cus] = self.return_time[self.current_el] - self.arrive[cus]
                            self.cus_wait_time[cus] = self.return_time[self.current_el] - self.arrive[cus]'''
                        self.get_loaded_full(self.que_custom,self.limit,self.current_el)

                        # 队伍
                        self.MAX_QUE_TIME = max(
                            self.MAX_QUE_TIME, self.return_time[self.current_el] - self.start_que)
                        self.MAX_QUE_LEN = max(
                            self.MAX_QUE_LEN, self.queue_len)

                        self.operate_queue()
                        self.queue_len = self.remain - 12
                        self.remain -= 12
                        self.que_custom += 12  # 加12之后是下一批第一个
                        if not self.limit == self.cus_num - 1:  # 考虑刚好12人，最后一人之后没人情况
                            self.start_que = self.arrive[self.limit + 1]

                        # 对当前用户,原封不动重新循环 即保持current_cus_num 不变（不加1

                    else:  # 不足12人，还可以补员,假设10人
                        # 先重载数据，增加等待时间
                        self.occupant[self.current_el] = 0
                        self.sel_vec[self.current_el] = np.array([[0] * 12])
                        self.flr_vec[self.current_el] = np.array([[0] * 12])
                        self.first[self.current_el] = self.que_custom
                        # self.limit = self.que_custom + self.queue_len +
                        # self.occupant[self.current_el] - 1  # 不用-1
                        self.limit = self.current_cus - 1  # 这种else下可以确定为是前一人 然后再判断当前乘客

                        '''for cus in range(self.que_custom, self.limit + 1):
                            self.occupant[self.current_el] += 1
                            self.sel_vec[self.current_el][self.floor[cus] - 1] = 1
                            self.flr_vec[self.current_el][self.floor[cus] - 1] += 1
                            self.cus_del_time[cus] = self.arrive[self.current_cus-1]+15 - self.arrive[cus]
                            self.cus_wait_time[cus] = self.arrive[self.current_cus-1]+15 - self.arrive[cus]'''
                        self.get_loaded_not_full(self.que_custom,self.limit,self.current_el)

                        self.TIME = max(self.arrive[self.limit],self.return_time[self.current_el])
                        if self.current_cus<=128 and self.arrive[self.current_cus] <= self.TIME + 15 \
                                and self.occupant[self.current_el] < 12:  # 等待时间未到，还能载走
                            self.limit = self.current_cus
                            #self.occupant[self.current_el] += 1
                            self.sel_vec[self.current_el][self.floor[self.current_cus] - 1] = 1
                            self.flr_vec[self.current_el][self.floor[self.current_cus] - 1] += 1
                            # self.que_custom = 0
                            current_cus_num += 1  # 下一循环

                        else:  # 超过15s
                            # 发车后才确定最终排队数据
                            self.AVG_QUE_TIME += (self.return_time[self.current_el] -
                                                  self.arrive[self.que_custom:self.limit +
                                                              1]).sum()  # 排队时间以电梯回来为准


                            # 考虑是否有多辆电梯同时在等
                            self.TIME = self.arrive[self.current_cus - 1] + 15
                            self.operate_queue()  # 这一步先做，因为要把前一波送走，再判断有没有别的电梯
                            self.remain = 0

                            self.MAX_QUE_LEN = max(
                                self.MAX_QUE_LEN, self.queue_len)
                            self.MAX_QUE_TIME = max(
                                self.MAX_QUE_TIME, self.return_time[self.current_el] - self.start_que)

                            self.queue_len = 0
                            # 没有queue了

                            # 对当前用户：-----考原封不动重新开始




# todo:12人限制
# todo:在下一人来之前排队的人等到了电梯？
# todo:self.queue()的时间调整
# todo:avg_el_time
sys1 = elevator_system(320)
sys1.run()
