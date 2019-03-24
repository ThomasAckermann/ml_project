import numpy as np
from time import sleep
# from tempfile import * 
from scipy.optimize import curve_fit
# import random
import scipy as sp
import scipy.optimize as opt
import sys 
import traceback
import random
import copy

moves = np.array([[]])
path = './agent_code/qn_agent/'
timer_ = 0
crate_counter = 0


def func_curve(X, a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8, a_9, a_10, a_11, a_12, a_13, a_14, a_15, a_16, a_17, a_18, a_19, a_20, a_21, a_22, a_23, a_24, a_25, a_26, a_27):
    (x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8, x_9, x_10, x_11, x_12, x_13, x_14, x_15, x_16, x_17, x_18, x_19, x_20, x_21, x_22, x_23, x_24, x_25, x_26) = X
    return a_1*x_1 + a_2*x_2 + a_3*x_3 + a_4*x_4 + a_5*x_5 + a_6*x_6 + a_7*x_7 + a_8*x_8 + a_9*x_9 + a_10*x_10 + a_11*x_11 + a_12*x_12 + a_13*x_13 + a_14*x_14 + a_15*x_15 + a_16*x_16 + a_17*x_17 + a_18*x_18 + a_19*x_19 + a_20*x_20 + a_21*x_21 + a_22*x_22 + a_23*x_23 + a_24*x_24 + a_25*x_25 + a_26*x_26 + a_27 

def func_curve_backup(X, a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8, a_9, a_10, a_11, a_12, a_13, a_14, a_15, a_16, a_17, a_18, a_19):
    (x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8, x_9, x_10, x_11, x_12, x_13, x_14, x_15, x_16, x_17, x_18) = X
    return a_1*x_1 + a_2*x_2 + a_3*x_3 + a_4*x_4 + a_5*x_5 + a_6*x_6 + a_7*x_7 + a_8*x_8 + a_9*x_9 + a_10*x_10 + a_11*x_11 + a_12*x_12 + a_13*x_13 + a_14*x_14 + a_15*x_15 + a_16*x_16 + a_17*x_17 + a_18*x_18 + a_19


def func_curve_2(X, a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8):
    (x_1, x_2, x_3, x_4, x_5, x_6, x_7) = X
    return a_1*x_1 + a_2*x_2 + a_3*x_3 + a_4*x_4 + a_5*x_5 + a_6*x_6 + a_7*x_7 + a_8


def positions(self):
    agent = self.game_state['self']
    agent_pos = np.array([agent[0], agent[1]])
    coins = np.array(self.game_state['coins'])
    if len(coins) == 0:
        # return agent_pos three times, otherwise the agent would try to go to the top left corner, this way he "tries to stay where he is"
        return agent_pos, agent_pos, np.zeros(2)
    else:
        dist = np.array([])   
        for i in range(len(coins)):
            dist = np.append(dist, np.linalg.norm(agent_pos - coins[i]))
        coin = coins[np.argmin(dist)]
        mean_coin = []
        
        for i in range(len(coins)):
            if dist[i] != 0:
                mean_coin.append((agent_pos - coins[i])/dist[i]**(3/2))
        if (len(np.shape(mean_coin)) > 1):
            mean_coin = np.sum(mean_coin, axis=0)
        if np.linalg.norm(mean_coin) != 0: 
            mean_coin = (mean_coin)/ np.linalg.norm(mean_coin) 
        # mean_coin[1] = -1 * mean_coin[1]
        # print(mean_coin)
        if (mean_coin == []):
            mean_coin = np.zeros(2)
        return agent_pos, np.array(coin), mean_coin # agent_pos, absolute pos naechster coin, richtung mean coin

def difference(self):
    agent_pos, coin, mean_coin = positions(self) 
    arena = self.game_state['arena']
    diff = np.linalg.norm(agent_pos - coin)
    if diff != 0 :
        direction = (agent_pos - coin) / diff
    else:
        direction = np.zeros(2)

    #with open('{}error.txt'.format(path), 'a') as f:
    #    f.write(str(direction) + ' ' + str(mean_coin) + '\n')
    #print(mean_coin)
    #print(*mean_coin)
    return np.array([diff, *direction, *mean_coin])



def crate_positions(self):
    agent = self.game_state['self']
    agent_pos = np.array([agent[0], agent[1]])
    arena = self.game_state['arena']
    crates = []
    for i in range(np.shape(arena)[0]):
        for j in range(np.shape(arena)[1]):
            if arena[i][j] == 1:
                crates.append([i,j])#, axis=0)
    crates = np.array(crates) 
    if len(crates) == 0:
        # return agent_pos three times, otherwise the agent would try to go to the top left corner, this way he "tries to stay where he is"
        return agent_pos, agent_pos, np.zeros(2)
    else:
        dist = np.array([])   
        for i in range(len(crates)):
            dist = np.append(dist, np.linalg.norm(agent_pos - crates[i]))
        crate = crates[np.argmin(dist)]
        mean_crate = []
        
        for i in range(len(crates)):
            if dist[i] != 0:
                mean_crate.append((agent_pos - crates[i])/dist[i]**(3/2))
        if (len(np.shape(mean_crate)) > 1):
            mean_crate = np.sum(mean_crate, axis=0)
        if np.linalg.norm(mean_crate) != 0: 
            mean_crate = (mean_crate)/ np.linalg.norm(mean_crate) 
        # mean_coin[1] = -1 * mean_coin[1]
        # print(mean_coin)
        if (mean_crate == []):
            mean_crate = np.zeros(2)
        return agent_pos, np.array(crate), mean_crate # agent_pos, absolute pos naechster coin, richtung mean coin

def crate_diff(self):
    agent_pos, crate, mean_crate = crate_positions(self)     
    diff = np.linalg.norm(agent_pos - crate)
    if diff != 0 :
        direction = (agent_pos - crate) / diff
    else:
        direction = np.zeros(2)

    #with open('{}error.txt'.format(path), 'a') as f:
    #    f.write(str(direction) + ' ' + str(mean_coin) + '\n')
    #print(mean_coin)
    #print(*mean_coin)
    return np.array([*direction, *mean_crate])

def check_even_odd(position):
    # 1 means, that the row/column is free
    # x and y are swapped, because the y direction is free if the x value is odd
    position = np.array(position)[np.r_[1, 0]] #np.r_ does the swap of x and y
    return position % 2
   
def last_move(self):
    forbidden = np.zeros(4)
    try:
        last_move_ = self.events[0]
    except:
        last_move_ = -1
    if (last_move_ in [0, 1, 2, 3]):
        forbidden[int(last_move_ + 1 - 2 * (last_move_ % 2))] = 1
    return forbidden


def own_bomb_ticking(self):
    #returns 1 if own bomb is ticking, else 0
    bomb_possible = self.game_state['self'][3]
    return (bomb_possible + 1) % 2

def bomb_difference(self):
    agent = self.game_state['self']
    agent_pos = np.array([agent[0], agent[1]])
    arena = np.array(self.game_state['arena'])
    bombs = np.array(self.game_state['bombs']) 
    if len(bombs)==0: 
        bomb = agent_pos
    else:
        bombs = bombs[:,:2]
        dist = np.array([])   
        for i in range(len(bombs)):
            dist = np.append(dist, np.linalg.norm(agent_pos - bombs[i])) 
        bomb = bombs[np.argmin(dist)]  
    diff = np.linalg.norm(agent_pos - bomb)
    if diff != 0 :
        direction = (agent_pos - bomb) / diff
    else:
        direction = agent_pos # sinnvoll? aber zumindest mal sinnvoller als 0 oder? 
    return np.array([diff, *direction])

def explosion_radius_single_bomb(coordinates):
    check_free = check_even_odd(coordinates)
    x, y, x_, y_ = *coordinates, *check_free
    row = [[item, y] for item in np.unique(np.clip(np.r_[x-3:x+4], 0, 16))] if x_ else [[x, y]]
    column = [[x, item] for item in np.unique(np.clip(np.r_[y-3:y+4], 0, 16))] if y_ else [[x, y]] 
    return row + column

def position_in_danger(position, self):
    danger = 0
    for bomb in self.game_state['bombs']:
        if (list(position) in explosion_radius_single_bomb(bomb[:2])):
            danger = 1 if bomb[2] > 1 else 10 # 10 if the position will be deadly in the next step
    return danger

def number_of_crates_in_explosion_radius(self):
    own_pos = np.array(self.game_state['self'][:2])
    explosion_radius = explosion_radius_single_bomb(own_pos)
    tiles = np.array([self.game_state['arena'][tuple(item)] for item in explosion_radius])
    return len(np.arange(len(tiles))[tiles == 1])

def next_move_danger(self):
    # returns 0 if no danger is in the corresponding direction or a wall 
    danger = np.zeros(4)
    own_pos = np.array(self.game_state['self'][:2])
    pos_diffs = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]]) #np.concatenate((np.eye(2), -np.eye(2)), axis = 0) müsste noch umsortiert werden
    for i in range(4):
        danger[i] = position_in_danger(own_pos + pos_diffs[i], self)
        if (np.abs(self.game_state['arena'][tuple(own_pos + pos_diffs[i])]) == 1):
            danger[i] = 0.8
    return danger

def directions_blocked(self):
    # returns 0 if direction is free, 1 if it is blocked 
    blocked = np.zeros(4)
    own_pos = np.array(self.game_state['self'][:2])
    pos_diffs = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]]) #np.concatenate((np.eye(2), -np.eye(2)), axis = 0) müsste noch umsortiert werden
    for i in range(4):
        blocked[i] = np.abs(self.game_state['arena'][tuple(own_pos + pos_diffs[i])])
    return blocked
    


def q_function(theta_q, features):
    f = theta_q[:,-1]
    for i in range(len(features)):
        f = f + theta_q[:, i] * features[i] 
    return f

def build_features (self):
    features = difference(self) # [diff, *direction, *mean_coin] also 5 Werte, Indizes 0, 1, 2, 3, 4
    features = np.append(features, check_even_odd(self.game_state['self'][:2])) # 2 Werte, Indizes 5, 6
    features = np.append(features, last_move(self)) # 4 Werte, Indizes 7, 8, 9, 10
    features = np.append(features, position_in_danger(self.game_state['self'][:2], self)) # 1 Wert, Index 11
    features = np.append(features, own_bomb_ticking(self)) # 1 Wert, Index 12
    features = np.append(features, number_of_crates_in_explosion_radius(self)) # 1 Wert, Index 13
    features = np.append(features, directions_blocked(self)) # 4 Werte, Indizes 14, 15, 16, 17
    features = np.append(features, next_move_danger(self)) # 4 Werte 18 19 20 21
    features = np.append(features, crate_diff(self)) # 4 werte 22 23 24 25 
    return features

def setup(self):
    np.random.seed(1)
    q_data = np.load('agent_code/qn_agent/q_data.npy')
    # print(len(q_data))
    if len(q_data) > 6000:
        q_data = q_data[-6000:]
        np.save('agent_code/qn_agent/q_data.npy', q_data)
    pass

def sigmoid(x):
    return 1/(1+ np.exp(-1 * x))

def act(self):  
    try:
        with open('{}round_number.txt'.format(path), 'r') as f:
            round_number = int(f.read())
        q_data = np.load('agent_code/qn_agent/q_data.npy')
        all_data = np.load('agent_code/qn_agent/all_data.npy')


        features = build_features(self)

        theta_q = np.load('agent_code/qn_agent/theta_q.npy')

        action = {0:'LEFT', 1:'RIGHT', 2:'UP', 3:'DOWN', 4:'WAIT', 5:'BOMB'}

        q_value = q_function(theta_q, features)

        #eps = 0.8 - np.min((round_number, 500))/500 * 0.6
        eps = 0.25 - np.min((round_number, 500))/500 * 0.2
        e = np.random.uniform(0,1)
        if e < eps:
            chosen_action = int(np.random.choice([0,1,2,3,4,5], p = [0.2, 0.2, 0.2, 0.2, 0.1, 0.1]))
        else:
            chosen_action = int(np.argmax(q_value))
        
        q_data = np.append(q_data, [np.array([chosen_action, q_value[chosen_action], *features])], axis=0)
        all_data = np.append(all_data, [np.array([chosen_action, q_value[chosen_action], *features])], axis=0)

        np.save('agent_code/qn_agent/q_data.npy', q_data)
        np.save('agent_code/qn_agent/all_data.npy', all_data)
        
        self.next_action = action[chosen_action]
        

        #print(action[chosen_action])
        #print('theta')
        #print(theta_q)
        #print('features')
        #print('q_values')
        #print(q_value)
        
    except Exception as e:
        print('Exception as e:')
        print('line: ', sys.exc_info()[2].tb_lineno)
        print(type(e), e) 
        print('Traceback:')
        traceback.print_tb(sys.exc_info()[2], file = sys.stdout)
        print('end of traceback.')
    return None

def reward_update(self):
    try:
        reward_update_(self)
    except Exception as e:
        print('Exception as e:')
        print('line: ', sys.exc_info()[2].tb_lineno)
        print(type(e), e) 
        print('Traceback:')
        traceback.print_tb(sys.exc_info()[2], file = sys.stdout)
        print('end of traceback.')
        

def reward_update_(self):
    global moves
    #sleep(10)
    
    history = np.load('agent_code/qn_agent/q_data.npy')
    last_event = history[-1]
    features = last_event[2:]

    event_dict = {0 : "MOVED_LEFT",
            1 : "MOVED_RIGHT",
            2 : "MOVED_UP",
            3 : "MOVED_DOWN",
            4 : "WAITED",
            5 : "INTERRUPTED",
            6 : "INVALID_ACTION",
            7 : "BOMB_DROPPED",
            8 : "BOMB_EXPLODED",
            9 : "CRATE_DESTROYED",
            10 : "COIN_FOUND",
            11 : "COIN_COLLECTED",
            12 : "KILLED_OPPONENT",
            13 : "KILLED_SELF",
            14 : "GOT_KILLED",
            15 : "OPPONENT_ELIMINATED",
            16 : "SURVIVED_ROUND"}

    rewards = {"MOVED_LEFT" : -2+features[1]+0.2*features[3]+0.2*features[5]-3*features[7]-2*features[18]+0.3*features[22]+0.1*features[24], 
                    "MOVED_RIGHT" : -2-features[1]-0.2*features[3]+0.2*features[5]-3*features[8]-2*features[19]-0.3*features[22]-0.1*features[24],
                    "MOVED_UP" : -2+features[2]+0.2*features[4]+0.2*features[6]-3*features[9]-2*features[20]+0.3*features[23]+0.1*features[25],
                    "MOVED_DOWN" : -2-features[2]-0.2*features[4]+0.2*features[6]-3*features[10]-2*features[21]-0.3*features[23]-0.1*features[25],
                    "WAITED" : -6 - 40 * features[11], 
                    "INTERRUPTED" : -1,
                    "INVALID_ACTION" : -5 - 5*features[5] - 5*features[6] - 20*features[12] - 10*np.clip(np.sum(features[14:18]), 0, 1),
                    
                    "BOMB_DROPPED" :  -4 + 5*features[13],
                    "BOMB_EXPLODED" : 0, 
                    
                    "CRATE_DESTROYED" : 2,
                    "COIN_FOUND" : 0,
                    "COIN_COLLECTED" : 20,

                    "KILLED_OPPONENT" : 0,
                    "KILLED_SELF" : -200,

                    "GOT_KILLED" : 0,
                    "OPPONENT_ELIMINATED" : 0,
                    "SURVIVED_ROUND" : 200}


    reward = np.sum([rewards[event_dict[item]] for item in self.events])

    global crate_counter
    for event in self.events:
        if event == 9:
            crate_counter += 1

    #print('last_event', last_event)

    # print('test 1')
    # print(moves)
    moves = np.append(moves, [last_event[0], reward, *features])
    # print('test 2')
    # try:
    #     with open('test_reward_q.txt', 'a') as f:
    #         #print(q_value)
    #         f.write(str(reward)[:] + '\n')
    #         #f.write(str(p_value)[1:-1] + '\n')
    #         pass
    # except:
    #     pass
    moves = np.reshape(moves, (int(len(moves.flat)/(2+len(features))), 2+len(features)))


    #features = build_features(self)
    #theta_q = np.load('agent_code/qn_agent/theta_q.npy')     
    #print('theta', theta_q[:, -4:])
    #print('reward', reward, '; features[7:]', features[7:])
    #if (self.game_state['step'] % 10 == 0):
    #    print('|abstand|nearest|nearest|mean   |mean   |evenodd|evenodd|lastmov|lastmov|lastmov|lastmov|pos in |ownbomb|number |')
    #    print('|coin   |coin x |coin y |coin x |coin y |   x   |   y   |right  |left   |down   |up     |danger |ticking|crates |')
    #print(30*'-')
    #print(features) #14 Werte
    #fea_pri = ''
    #for feature in features: fea_pri += '| {}       '.format(feature)[:7] + ' '
    #print(fea_pri)
    #sleep(2)

    return None


def end_of_episode(self):

    try:
        global moves
        theta_q = np.load('agent_code/qn_agent/theta_q.npy')     
        history = np.load('agent_code/qn_agent/q_data.npy')
        all_data = np.load('agent_code/qn_agent/all_data.npy')
        #history = history[:-1]
        y_array = np.load('agent_code/qn_agent/y_data.npy')
        alpha = 0.04 
        gamma = 0.1
        n = 5    
        for t in range(len(moves)):
            if (t >= len(moves) - n):
                n = len(moves) - t - 1
            q_next = np.max(q_function(theta_q, moves[t + n, 2:])) 
            y_t = np.sum([gamma**(t_ - t - 1) * moves[t_, 1] for t_ in range(t + 1, t + n + 1)]) + gamma**n * q_next
            y_array = np.append(y_array, y_t)
            # print(moves[t_, 1] for t_ in range(t+1, t+n+1)) 
            # print(moves[:,1])
            # try:
            #     with open('test_reward_qnn.txt', 'a') as f:
            #         #print(q_value)
            #         f.write(str(np.sum([gamma**(t_ - t - 1) * moves[t_, 1] for t_ in range(t + 1, t + n + 1)]))[:] + '\n')
            #         #f.write(str(p_value)[1:-1] + '\n')
            #         pass
            # except:
            #     pass

            q_update = history[-len(moves) + t, 1] + alpha * (y_t - history[-len(moves) + t, 1])   
            # print('Q_n: ', y_t)
            history[-len(moves) + t, 1] = q_update
            #chosen_action = int(history[t, 0])
            #regression_data = history[history[:,0]==chosen_action][:,1:]   
            # theta = opt.least_squares(func, x0=start, method='lm', args=[regression_data, y_array])['x']
            # popt,cov = curve_fit(func, (regression_data[:, 1:].T), regression_data[:, 0])#, p0=theta_q[chosen_action])
        

            # if len(history) <= 800:
                # pass
            # else: 
                # theta_q[chosen_action] = np.array([*popt])
        

        global path
        global crate_counter
        with open('{}round_number.txt'.format(path), 'r') as f:
            round_number = int(f.read())
            # print(round_number)
        with open('{}round_number.txt'.format(path), 'w') as f:
            f.write(str(round_number + 1))
        with open('{}moves.txt'.format(path), 'a') as f:
            new_coins = self.game_state['self'][4]
            last_score = self.game_state['self'][4]
            f.write(str(round_number) + ' ' + str(len(moves)) + ' ' + str(new_coins) + ' ' + str(crate_counter) + '\n')
            crate_counter = 0

        if (round_number % 100 == 0):
            # print(theta_q)
            try: 
                # print('hallo')
                theta = []
                for i in range(6):
                    if len(history) != len(y_array):
                        #print('h:', len(history), '; y:', len(y_array), '; moves:', len(moves))
                        mi = min(len(history), len(y_array))
                        history = history[:mi]
                        y_array = y_array[:mi]

                    regression_data = copy.deepcopy(history)

                    if len(all_data) > 6000:
                        tmp = all_data[:-6000]
                        if len(tmp) > 6000:
                            tmp = tmp[np.array(random.sample(list(np.arange(len(tmp))), 6000))]
                        regression_data = np.append(tmp, regression_data, axis = 0)
                    
                    mask = regression_data[:,0]==i
                    regression_data = regression_data[mask][:, 1:]
                    
                    #print(np.shape(regression_data[:, 1:].T), 'und', np.shape(regression_data[:, 0]))
                    popt, pcov = curve_fit(func_curve, (regression_data[:, 1:].T), regression_data[:, 0], p0=theta_q[i])
                    theta.append(popt)



                np.save('agent_code/qn_agent/theta_q.npy', theta)
            except Exception as e:
                print(e)
                print('theta unverändert')
                print('Exception as e:')
                print('line: ', sys.exc_info()[2].tb_lineno)
                print(type(e), e) 
                print('Traceback:')
                traceback.print_tb(sys.exc_info()[2], file = sys.stdout)
                print('end of traceback.')
                pass
            
        # for i in range(4):
        #     regression_data = history[history[:,0]==int(i)][:,1:]
        #     popt,cov = curve_fit(func, (regression_data[:, 1:].T), regression_data[:, 0])
        #     theta_q[chosen_action] = np.array([*popt])
        
        np.save('agent_code/qn_agent/q_data.npy', history)
        np.save('agent_code/qn_agent/all_data.npy', all_data)
        np.save('agent_code/qn_agent/y_data.npy', y_array)
        q_data = np.load('agent_code/qn_agent/q_data.npy')

        
        if len(q_data) > 6000:
            q_data = q_data[-6000:]
            y_array = y_array[-6000:]
            
            np.save('agent_code/qn_agent/y_data.npy', y_array)
            np.save('agent_code/qn_agent/q_data.npy', q_data)
        last_len_q_data = len(q_data)

        # print(self.events)    
        #print('END')
        moves = np.array([[]])    
    except Exception as e:
        print('Exception as e:')
        print('line: ', sys.exc_info()[2].tb_lineno)
        print(type(e), e) 
        print('Traceback:')
        traceback.print_tb(sys.exc_info()[2], file = sys.stdout)
        print('end of traceback.')
        

    return None


