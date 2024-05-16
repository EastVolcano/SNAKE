import numpy as np

fighter_str = '.\\MultiFighter.dll'
# missile_str = '.\\CBB_py.dll'
missile_str = '.\\for_cc_py.dll'
# missile_str = '.\\close_middle_py.dll'

log_tacview = True
log_csv = True
tcp_use = False             # 是否使用tcp进行可视化

epoch_max = 1               # 设定仿真轮次
datafreq_min = 0.01         # 最小数据更新率（底层步长为0.01s）
len_max = 60000             # 单轮仿真的步长上限

fighters_max_num = 10        # 设定仿真环境内的飞机的数量
num_blue = 2                 # 设定蓝色机数量
num_red = 2                  # 设定红色机数量
missiles_max = 4            # 设定每架飞机搭载的近距导弹的数量
missiles_max_mid = 2        # 设定每架飞机搭载的中距导弹的数量
num_fighter = num_red + num_blue

missile_without_radar = True       # 当该变量为True，表示 导弹发射和制导 不受 雷达探测范围 影响。


class InitialData(object):
    def __init__(self):
        self.train_flag = True  # 是否是RL训练模式
        self.log_tacview = True          # 是否开启内置的仿真文件记录功能
        self.log_csv = False  # 是否输出记录文件
        self.dll_str = '.\\MultiFighter.dll'         # 调用的模型路径，若加载失败，可改为绝对路径

        # 仿真设定
        self.epoch_max = epoch_max              # 仿真轮次
        self.dt = datafreq_min         # 最小数据更新率（底层步长为0.01s）
        self.len_max = len_max         # 单轮仿真长度

        # 红蓝双方战机数量
        self.num_blue = num_blue            # 蓝机数量
        self.num_red = num_red             # 红机数量
        self.originLongitude = 160.123456   # 仿真的经纬度原点位置
        self.originLatitude = 24.8976763

        # 初始载弹量
        self.missiles_max = missiles_max

        # 对抗双方的初始状态
        # 初始位置（北东地）
        # self.NED = [
        #     [50000, -2500, -10000],
        #     [50000, 2500, -10000],
        #     [-50000, -2500, -10000],
        #     [-50000, 2500, -10000],
        #     ]
        self.NED = [
            [0, 2500, -6000],
            [3510, 4000, -5500],
            [2500, 6000, -5000],
            [7000, 2000, -5000]
        ]

        # for i in range(self.num_red):
        #     self.NED.append([300, -2500 + 50 * i, -5000])
        # for i in range(self.num_blue):
        #     self.NED.append([0, -2500 + 150 * i, -5000])

        # 初始速度（马赫数）
        self.ma = [0.9, 0.9, 0.9, 0.9]
        # self.ma = [0.6, 0.6, 0.6, 0.6, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
        # self.ma = []
        # for i in range(self.num_blue + self.num_red):
        #     self.ma.append(0.8)

        # 初始航向（0度为北向）
        # self.orientation = [
        #                     180-2.862405226111748,
        #                     180+2.862405226111748,
        #                     2.862405226111748,
        #                     -2.862405226111748,
        #                     ]
        self.orientation = []

        for i in range(self.num_red):
            self.orientation.append(-90)
        for i in range(self.num_blue):
            self.orientation.append(-90)

        # 设定油量
        self.FuelKg = []
        for i in range(self.num_red + self.num_blue):
            self.FuelKg.append(0.8 * 2800)

        # 设定通信延迟
        self.comm_delay = 10

        # 记录功能
        self.log_match = log_tacview
        self.log_csv = log_csv
        self.tcp_use = tcp_use

        # 机载雷达范围设定
        self.radar_range = 40000
        self.radar_vertical_scan = 30            # 雷达垂直扫描范围
        self.radar_horizontal_scan = 30           # 雷达水平扫描范围
        self.eodas_range = 5000                    # 光电分布式探测孔径系统（EODAS）探测范围
        self.alert_missile_range = 5000                 # 来袭导弹告警范围

        self.missile_without_radar = missile_without_radar      # 导弹发射是否依赖雷达锁定的开关


