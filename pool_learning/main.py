import pygame
import numpy as np

import collisions
import event
import gamestate
import graphics
import config
import ball
import rl 




MAX_EPISODES = 500
MAX_EP_STEPS = 200
ON_TRAIN = True


state_dim = 9
action_dim = 2
action_bound = [-254,254]

s_dim = state_dim
a_dim = action_dim
a_bound = action_bound

rl = rl.DDPG(a_dim, s_dim, a_bound)
def call_input():
    x=int(input("x : "))
    y=int(input("y : "))
    return x,y

def train():
    for i in range(MAX_EPISODES):
        ep_r = 0.
        for j in range(MAX_EP_STEPS):
            was_closed = False
            
            while not was_closed:
                game = gamestate.GameState()
                button_pressed = config.play_game_button
                print("-----------------time reset-----------------------")
                times=0
                store_ball_list_first=dict()
                if button_pressed == config.play_game_button:
                    game.start_pool()
                    events = event.events()
                    reward=0.
                    temp_reward=0.
                    for ball in game.balls:
                        store_ball_list_first[ball.number]=ball.ball.pos
                    print("store_ball_list_first :{}".format(store_ball_list_first))

                    first_ball=game.first_ball
                    second_ball=game.second_ball
                    
                    s=np.concatenate((store_ball_list_first[0],store_ball_list_first[9],store_ball_list_first[first_ball],store_ball_list_first[second_ball],[0.]))
                    while not (events["closed"] or game.is_game_over or events["quit_to_main_menu"]) and times<40:
                        events = event.events()
                        reward=collisions.resolve_all_collisions(game.balls, game.holes, game.table_sides,reward)
                        temp_reward=reward

                        

                        
                        
                        game.redraw_all()
                        store_ball_list=dict()
                        
                        if game.all_not_moving():

                            if reward==temp_reward and times:
                                reward=reward-1

                            print("\n*****************************")
                            
                            for ball in game.balls:
                                store_ball_list[ball.number]=ball.ball.pos
                                #print("ball {} not moving : {}".format(ball.number,ball.ball.pos))
                            
                            game.check_pool_rules()
                            

                            game.cue.make_visible(game.current_player)

                            if 0 not in store_ball_list:
                                store_ball_list[0]=game.give_value()
                            #print("如果陣列中沒有白球位置請看這裡 ： {}".format(game.give_value()))

                            print("all balls : ",store_ball_list)
                            print()
                            test=[]
                            for i in store_ball_list:
                                test.append(i)
                            
                            if 9 not in store_ball_list:
                                print("Reward_end : ",reward)
                                rl.store_transition(s, a, reward, s_)
                                continue

                            if first_ball not in store_ball_list:
                                store_ball_list[first_ball]=[0,0]

                            if second_ball not in store_ball_list:
                                store_ball_list[second_ball]=[0,0]   
                            
                            print("s",s)

                            s_=np.concatenate((store_ball_list[0],store_ball_list[9],store_ball_list[first_ball],store_ball_list[second_ball],[0.]))
                            
                            print()


                            

                            
                            
                            print("reward : {}\n".format(reward))
                            while not (
                                (events["closed"] or events["quit_to_main_menu"]) or game.is_game_over) and game.all_not_moving():
                                game.redraw_all()
                                events = event.events()
                                print("Times : ",times)
                                print()
                                if times>=40:
                                    was_closed=True
                                    break
                                times = times+1
                                if 1:
                                    #x,y=call_input()
                                    a = rl.choose_action(s)
                                    
                                    #s_, r, done = env.step(a)

                                    if first_ball not in store_ball_list:
                                        store_ball_list[first_ball]=[0,0]

                                    if second_ball not in store_ball_list:
                                        store_ball_list[second_ball]=[0,0]   

                                    a=np.clip(a, *action_bound)
                                    

                                    game.cue.cue_is_active(game, events,a)
                                    
                                    
                                    r=reward
                                    print("s_ : ",s_)
                                    print()

                                    rl.store_transition(s, a, r, s_)

                                    ep_r += r
                                    if rl.memory_full:
                                        # start to learn once has fulfilled the memory
                                        rl.learn()

                                    s = s_
                                    
                                elif game.can_move_white_ball and game.white_ball.is_clicked(events):
                                    game.white_ball.is_active(game, game.is_behind_line_break())
                    was_closed = True

                # if button_pressed == config.exit_button:
                #     was_closed = True

            
            if was_closed or j == MAX_EP_STEPS-1:
                print('Ep: %i | %s | ep_r: %.1f | step: %i' % (i, '---' if not was_closed else 'done', ep_r, j))
                break
        rl.save()
pygame.quit()

if 1:
    train()
