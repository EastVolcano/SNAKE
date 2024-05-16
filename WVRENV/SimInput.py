import numpy as np


class FighterDataIn(object):
    def __init__(self):
        # 飞机控制模式选择（仅可在初始化时进行一次选择）
        self.control_mode = 3

        # 直接控制输入,依据操作模式代表不同含义
        # 控制模式3：[油门， 期望机体法向过载， 期望机体滚转速率， 无意义补充位]
        # 控制模式0：[油门， 纵向杆， 横向杆， 方向舵]
        self.control_input = [1, 1/9, 0, 0]

        # 航炮开火指令，1为发射，0为不发射
        self.fire = 0

        # 机载雷达锁定目标，机载雷达中，蓝色机编号依次为0,1，红色机编号为2,3
        self.target_index = 0

        # 导弹开火指令，1为发射，0为不发射
        self.missile_fire = 0

        # 通信链路
        self.communication = [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']

        # 博士论文版通信链路
        self.comm_send = np.zeros(2, dtype=np.float32)


def print_data_fighter(fighter):
    if fighter.index == 0:
        print('__________________________________________________________________________________'
              '__________________________________________________________________________________')
    if fighter.index != 0:
        print('\n')

    print('| 编号', fighter.index,
          '| 血量', '%8.3f' % fighter.combat_data.bloods,
          '| 存活标志', fighter.combat_data.survive_info,
          '| 导弹发射开关',  '%3.0f' % fighter.action.fire_missile,
          '| 剩余导弹', '%3.0f' % fighter.missiles_left,
          '| 导弹发射计数', '%3.0f' % fighter.missiles_count,
          '| 航炮开火开关', fighter.action.fire_gun,
          '| 剩余子弹', '%10.3f' % fighter.combat_data.left_bullet,
          '| 地速', '%10.5f' % fighter.fc_data.fGroundSpeed,
          '| 马赫数', '%10.5f' % fighter.fc_data.fMachNumber,
          '| 阵营', '%5.0f' % fighter.side, '|',
          '\n| 北   ', '%10.5f' % fighter.state.ned_Pos[0],
          '| 东   ', '%10.5f' % fighter.state.ned_Pos[1],
          '| 地   ', '%10.5f' % fighter.state.ned_Pos[2],
          '| 滚转', '%10.5f' % fighter.fc_data.fRollAngle,
          '| 俯仰角', '%10.5f' % fighter.fc_data.fPitchAngle,
          '| 偏航角', '%10.5f' % fighter.fc_data.fYawAngle,
          '| 剩余油量', '%10.5f' % fighter.fc_data.fNumberofFuel,
          )


def print_data_fighter_radar(fighter):
    print('| 火控雷达锁定目标', fighter.target_index,
          '| 火控雷达扫描目标', fighter.sensors.radar_list,
          '| 5km内目标', fighter.sensors.eodas_list,

          '\n| 导弹告警数量', fighter.sensors.alert_missile,
          '| 导弹告警弹目俯仰角', fighter.sensors.alert_pitch,
          '| 导弹告警弹目方位角', fighter.sensors.alert_yaw,

          '| 飞机告警数量', fighter.sensors.alert_radar,
          '| 飞机告警弹目俯仰角', fighter.sensors.alert_radar_pitch,
          '| 飞机告警弹目方位角', fighter.sensors.alert_radar_yaw)


def print_data_fighter_missile(fighter):
    for i, missile in enumerate(fighter.missiles):
        print(
            '| 导弹编号', '%5.0f' % missile.index,
            '| 导弹状态', '%5.0f' % missile.state,
            '| 导弹当前跟踪目标', '%5.0f' % missile.target_index,

            '| 发射指令', missile.launch_num,

            '| 导弹位置北', '%10.1f' % missile.ned_Pos[0],
            '| 导弹位置东', '%10.1f' % missile.ned_Pos[1],
            '| 导弹位置地', '%10.1f' % missile.ned_Pos[2],
            '| 导弹导引头可锁定目标', missile.target_list,
            )


def print_outdata_new(env):
    for i, fighter in enumerate(env.world.fighters):
        print_data_fighter(fighter)
        print_data_fighter_radar(fighter)
        print_data_fighter_missile(fighter)



def print_outdata(outdata):
    for i in range(len(outdata)):
        if i == 0:
            print('__________________________________________________________________________________'
                  '__________________________________________________________________________________')
        if i != 0:
            print('\n')

        print_selfdata(i, outdata[i])
        print_radardata(i, outdata[i])
        print_statedata(i, outdata[i])
        print_closedata(i, outdata[i])
        print_alertdata(i, outdata[i])
        print_communication(i, outdata[i])


def print_selfdata(i, data):
        print('| 编号', i,
              '| 控制模式', data.selfdata.control_mode,
              '| 剩余血量', '%10.3f' % data.selfdata.left_bloods,
              '| 剩余导弹', data.selfdata.left_missile,
              '| 剩余子弹', '%10.3f' % data.selfdata.left_bullet, '|',

              '\n| 北速度', '%10.5f' % data.selfdata.NorthVelocity,
              '| 东速度', '%10.5f' % data.selfdata.EastVelocity,
              '| 地速度', '%10.0f' % data.selfdata.VerticalVelocity,
              '| 北加速度', '%10.5f' % data.selfdata.NorthAcceleration,
              '| 东加速度', '%10.5f' % data.selfdata.EastAcceleration,
              '| 地加速度', '%10.0f' % data.selfdata.VerticalAcceleration, '|',

              '\n| 俯仰角', '%10.5f' % data.selfdata.PitchAngle,
              '| 滚转角', '%10.5f' % data.selfdata.RollAngle,
              '| 偏航角', '%10.0f' % data.selfdata.YawAngle,
              '| 俯仰角速度', '%10.5f' % data.selfdata.PitchRate,
              '| 滚转角速度', '%10.5f' % data.selfdata.RollRate,
              '| 偏航角速度', '%10.0f' % data.selfdata.YawRate, '|',

              '\n| 攻角', '%10.5f' % data.selfdata.AttackAngle,
              '| 侧滑角', '%10.5f' % data.selfdata.SideslipAngle,
              '| 经度', '%10.5f' % data.selfdata.Longitude,
              '| 纬度', '%10.5f' % data.selfdata.Latitude,
              '| 高度', '%10.0f' % data.selfdata.Altitude, '|',

              '\n| 体轴法向过载', '%10.5f' % data.selfdata.NormalLoad,
              '| 体轴侧向过载', '%10.5f' % data.selfdata.LateralLoad,
              '| 体轴纵向过载', '%10.5f' % data.selfdata.LongitudeinalLoad,
              '| 体轴法向速度', '%10.5f' % data.selfdata.NormalVelocity,
              '| 体轴侧向速度', '%10.5f' % data.selfdata.LateralVelocity,
              '| 体轴纵向速度', '%10.0f' % data.selfdata.LongitudianlVelocity, '|',

              '\n| 真空速', '%10.5f' % data.selfdata.TrueAirSpeed,
              '| 指示空速', '%10.5f' % data.selfdata.IndicatedAirSpeed,
              '| 地速', '%10.5f' % data.selfdata.GroundSpeed,
              '| 剩余油量', '%10.5f' % data.selfdata.NumberofFuel,
              '| 推力', '%10.0f' % data.selfdata.Thrust,
              '| 导弹1状态', data.selfdata.Missile1State,
              '| 导弹2状态', data.selfdata.Missile2State,'|',
              )


def print_radardata(i, data):
    print('\n| radar_data',
          '| 友机高低角', '%10.5f' % data.radardata.friend_EleAngle,
          '| 友机方位角', '%10.5f' % data.radardata.friend_AziAngle,
          '| 友机距离', '%10.5f' % data.radardata.friend_Distance,
          '| 北东地速度', '%10.5f' % data.radardata.friend_NorthVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.friend_EastVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.friend_VerticalVelocity, '|',

          '\n| 敌机1编号',  data.radardata.target1_Index,
          '| 敌机1高低角', '%10.5f' % data.radardata.target1_EleAngle,
          '| 敌机1方位角', '%10.5f' % data.radardata.target1_AziAngle,
          '| 敌机1距离', '%10.5f' % data.radardata.target1_Distance,
          '| 北东地速度', '%10.5f' % data.radardata.target1_NorthVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.target1_EastVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.target1_VerticalVelocity, '|',

          '\n| 敌机2编号',  data.radardata.target2_Index,
          '| 敌机2高低角', '%10.5f' % data.radardata.target2_EleAngle,
          '| 敌机2方位角', '%10.5f' % data.radardata.target2_AziAngle,
          '| 敌机2距离', '%10.5f' % data.radardata.target2_Distance,
          '| 北东地速度', '%10.5f' % data.radardata.target2_NorthVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.target2_EastVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.target2_VerticalVelocity, '|',
          )


def print_statedata(i, data):
    print('\n| state_data',
          '| 友机经度', '%10.5f' % data.statedata.friend_Longitude,
          '| 友机纬度', '%10.5f' % data.statedata.friend_Latitude,
          '| 友机高度', '%10.5f' % data.statedata.friend_Altitude,
          '| 友机存活', data.statedata.friend_Survive,

          '\n| 敌机1编号',  data.statedata.target1_Index,
          '| 敌机1经纬高', '%10.5f' % data.statedata.target1_Longitude,
          '| 敌机1经纬高', '%10.5f' % data.statedata.target1_Latitude,
          '| 敌机1经纬高', '%10.5f' % data.statedata.target1_Altitude,
          '| 敌机1存活', data.statedata.target1_Survive,

          '\n| 敌机2编号',  data.statedata.target2_Index,
          '| 敌机2经纬高', '%10.5f' % data.statedata.target2_Longitude,
          '| 敌机2经纬高', '%10.5f' % data.statedata.target2_Latitude,
          '| 敌机2经纬高', '%10.5f' % data.statedata.target2_Altitude,
          '| 敌机2存活', data.statedata.target2_Survive,'|',

          )


def print_closedata(i, data):
    print('\n| close_data',
          '| 友机高低角', '%10.5f' % data.closedata.friend_EleAngle,
          '| 友机方位角', '%10.5f' % data.closedata.friend_AziAngle,
          '| 友机距离', '%10.5f' % data.closedata.friend_Distance,

          '\n| 敌机1编号', data.closedata.target1_Index,
          '| 敌机1高低角', '%10.5f' % data.closedata.target1_EleAngle,
          '| 敌机1方位角', '%10.5f' % data.closedata.target1_AziAngle,
          '| 敌机1距离', '%10.5f' % data.closedata.target1_Distance,

          '\n| 敌机2编号', data.closedata.target2_Index,
          '| 敌机2高低角', '%10.5f' % data.closedata.target2_EleAngle,
          '| 敌机2方位角', '%10.5f' % data.closedata.target2_AziAngle,
          '| 敌机2距离', '%10.5f' % data.closedata.target2_Distance, '|',
          )


def print_alertdata(i, data):
    print('\n| alert_data',
          '| 飞机告警数量',data.alertdata.emergency_num,
          '| 飞机告警方位角',  data.alertdata.emergency_EleAngle,
          '| 飞机告警方位角',data.alertdata.emergency_AziAngle,

          '\n| 导弹告警数量', data.alertdata.emergency_missile_num,
          '| 导弹告警方位角',data.alertdata.emergency_missile_EleAngle,
          '| 导弹告警方位角',data.alertdata.emergency_missile_AziAngle,
          )

def print_communication(i, data):
    print('\n| 接受的友机信息', data.communication,)
