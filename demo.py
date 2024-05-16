from WVRENV_PHD.simulation_env import CombatEnv
from WVRENV_PHD.SimInput import FighterDataIn, print_outdata_new
from WVRENV_PHD.SimArg import num_fighter, InitialData
from WVRENV_PHD.utils.GNCData import wgs84ToNED, ned_to_body
import numpy as np


if __name__ == '__main__':
    # ##################### 初始化设定 ########################
    # 初始化环境与输入量
    env = CombatEnv()
    data_initial = InitialData()
    datain = [FighterDataIn() for m in range(num_fighter)]

    # 飞机设定控制模式
    for i in range(num_fighter):
        datain[i].control_mode = 3

    # 完成初始化
    env.initial(datain, data_initial)

    # ###################### 开始多轮仿真 #######################
    for i_episode in range(1):
        # 重置仿真
        env.reset()
        # ###################### 开始单轮仿真 ######################
        for t in range(60000):
            # —————————————————————————————————— 编辑输入控制数据 ——————————————————————————————————————
            for i in range(num_fighter):
                datain[i].control_input = [1, 1 / 9, 0, 0]
                datain[i].target_index = i + 4
                if (t % 1 == 0) and (1 <= i <= 2):
                    datain[i].missile_fire = 1
                # elif (t == 700) and (i == 0 or i == 3):
                #     datain[i].missile_fire = 1
                elif (t % 1 == 0) and (i == 0 or i == 3):
                    datain[i].missile_fire = 1
                else:
                    datain[i].missile_fire = 0
                datain[i].fire = 1
                if env.world.fighters[i].side == 0:
                    datain[i].comm_send[0] = 5. + t * 0.01
                    datain[i].comm_send[1] = 20 + 0.1 * env.world.fighters[i].index
                else:
                    datain[i].comm_send[0] = 11.01 + 0.1 * env.world.fighters[i].index
                    datain[i].comm_send[1] = 1.07 + t * 0.01

            # 单个回合更新
            terminal = env.update(datain)
            # print(f"debug: {env.world.fighters[0].missiles[0].state}")
            # 实时可视化更新
            env.tcp_update(t)

            l_n, l_e, l_d = wgs84ToNED(env.world.fighters[1].fc_data.fLatitude, env.world.fighters[1].fc_data.fLongitude,
                                       env.world.fighters[1].fc_data.fAltitude,
                                       env.world.fighters[2].missiles[1].dataout.m_latitude,
                                       env.world.fighters[2].missiles[1].dataout.m_longitude,
                                       env.world.fighters[2].missiles[1].dataout.m_altitude)
            dist = np.linalg.norm([l_n, l_e, l_d])
            # 打印数据
            print('\n仿真步长：', t, '仿真时间： ', t * 0.01)
            print(f" mis1 state: {env.world.fighters[2].missiles[0].dataout.m_state},"
                  f" mis2 state: {env.world.fighters[2].missiles[1].dataout.m_state},"
                  f" mis2 tgt lon real: {env.world.fighters[1].fc_data.fLongitude},"
                  f" mis2 tgt lon input: {env.world.fighters[2].missiles[1].datain.target_longtitude},"
                  f" mis2 tgt lon seeker: {env.world.fighters[2].missiles[1].target_longitude},"
                  f" mis2 dist 1: {dist},"
                  f" mis2 dist 2: {env.world.fighters[2].missiles[1].dataout.distance},"
                  # f"mis3 state: {env.world.fighters[2].missiles[2].dataout.m_state},"
                  # f"mis4 state: {env.world.fighters[2].missiles[3].dataout.m_state},"
                  # f" lon {env.world.fighters[2].fc_data.fLongitude},"
                  # f" lat{env.world.fighters[2].fc_data.fLatitude},"
                  # f" alt {env.world.fighters[2].fc_data.fAltitude},"
                  # f" ma {env.world.fighters[2].fc_data.fMachNumber},"
                  # f" pitch {env.world.fighters[2].fc_data.fPitchAngle},"
                  # f" mis lon {env.world.fighters[2].missiles[0].dataout.m_longitude},"
                  # f" mis lat{env.world.fighters[2].missiles[0].dataout.m_latitude},"
                  # f" mis alt {env.world.fighters[2].missiles[0].dataout.m_altitude},"
                  # f" mis ma {env.world.fighters[2].missiles[0].dataout.m_ma},"
                  # f" mis pitch {env.world.fighters[2].missiles[0].dataout.m_pitch},"
                  )
            # print(f"state: {env.world.fighters[0].missiles[2].dataout.m_state}, "
            #       f"ma: {env.world.fighters[0].missiles[2].dataout.m_ma}, "
            #       f"target list: {env.world.fighters[0].missiles[2].target_list}, "
            #       f"target id: {env.world.fighters[0].missiles[2].target_index}, "
            #       f"guide lon: {env.world.fighters[0].missiles[2].datain.target_longtitude},"
            #       f"guide lat: {env.world.fighters[0].missiles[2].datain.target_latitude},"
            #       f"guide alt: {env.world.fighters[0].missiles[2].datain.target_altitude},"
            #       f"tgt survive: {env.world.fighters[env.world.fighters[0].missiles[2].target_index].combat_data.survive_info},"
            #       f"tgt lon: {env.world.fighters[env.world.fighters[0].missiles[2].target_index].fc_data.fLongitude},"
            #       f"tgt lat: {env.world.fighters[env.world.fighters[0].missiles[2].target_index].fc_data.fLatitude},"
            #       f"tgt alt: {env.world.fighters[env.world.fighters[0].missiles[2].target_index].fc_data.fAltitude},"
            #       )
            # print(f"figter {env.world.fighters[1].index}, survive {env.world.fighters[1].combat_data.survive_info}")
            # for fighter in env.world.fighters[0: env.num_RedFighter]:
            #     print(f"红方 {fighter.index} 机，存活：{fighter.combat_data.survive_info}，实时发送通信：{fighter.comunication_send}, 延时发送：{fighter.comunication_delayed_send}, 实时收到：{fighter.comunication_recv}")
            # for fighter in env.world.fighters[env.num_RedFighter: ]:
            #     print(f"蓝方 {fighter.index} 机，存活：{fighter.combat_data.survive_info}，实时发送通信：{fighter.comunication_send}, 延时发送：{fighter.comunication_delayed_send}, 实时收到：{fighter.comunication_recv}")
            # print_outdata_new(env)

            # 仿真结束
            if terminal >= 0:
                print("Episode: \t{} ,episode len is: \t{}".format(i_episode, t))
                print(terminal)
                break




