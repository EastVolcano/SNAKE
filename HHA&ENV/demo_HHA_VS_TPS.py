from multifighters.simulation_env import CombatEnv
from multifighters.SimInput import FighterDataIn, action_range
from multifighters.SimArg import num_fighter, InitialData
from policy.warcraft import Warcraft
from policy.warcraft_1015_pro import Warcraft1015


if __name__ == '__main__':
    # ##################### initialize ########################
    env = CombatEnv()
    data_initial = InitialData()
    datain = [FighterDataIn() for m in range(num_fighter)]

    datain[0].control_mode = 3
    datain[1].control_mode = 3

    blue_policy = Warcraft1015()
    red_policy = Warcraft()

    env.initial(datain, data_initial)
    print('Sim: S T A R T ')
    # #############################################
    for i_episode in range(100):
        data_initial.random_initial()
        # data_initial.random_initial_low()
        state = env.reset(data_initial)
        blue_policy.policy_reset()
        red_policy.policy_reset()
        # ############################################
        for t in range(data_initial.len_max):
            # ————————————————————————————————— control input ——————————————————————————————————————
            for i in range(num_fighter):
                if i == 0:
                    fighter = env.world.fighters[0]
                    target = env.world.fighters[1]
                    action = blue_policy.aircraft_pro(fighter, target, control_mode=0, control_p_n=3, world=env.world)
                else:
                    fighter = env.world.fighters[1]
                    target = env.world.fighters[0]
                    action = red_policy.aircraft(fighter, target, control_mode=0, control_p_n=3)
                # normalization
                action = action_range(action)
                datain[i].control_input = [action[2], action[0], action[1], 0]
                datain[i].fire = 1
            # ———————————————————————————————————————————————————————————————————————————————————————
            terminal, next_state = env.update(datain)
            state = next_state
            # Sim End
            if terminal >= 0:
                print("Episode: \t{} ,episode len is: \t{}".format(i_episode, t), 'Blue bloods：', env.world.fighters[0].combat_data.bloods, 'Red bloods：', env.world.fighters[1].combat_data.bloods )
                print(terminal)
                break



