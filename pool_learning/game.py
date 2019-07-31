import pygame

import collisions
import event
import gamestate
import graphics
import config
import ball
class Game():
    def __init__(self,x,y):
        self.was_closed = False
        
        self.play(x,y)
    def play(self,x,y):
        self.was_closed = False
        while not self.was_closed:
            game = gamestate.GameState()
            button_pressed = config.play_game_button
            if button_pressed == config.play_game_button:
                game.start_pool()
                events = event.events()
                self.reward=0
                while not (events["closed"] or game.is_game_over or events["quit_to_main_menu"]):
                    events = event.events()
                    self.reward=collisions.resolve_all_collisions(game.balls, game.holes, game.table_sides,self.reward)
                    
                    game.redraw_all()
                    store_ball_list=dict()
                    if game.all_not_moving():
                        
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
                        print("reward : {}".format(self.reward))

                        
                        while not (
                            (events["closed"] or events["quit_to_main_menu"]) or game.is_game_over) and game.all_not_moving():
                            game.redraw_all()
                            events = event.events()
                            if 1:
                                # x=int(input("x : "))
                                # y=int(input("y : "))
                                game.cue.cue_is_active(game, events,(x,y))
                            elif game.can_move_white_ball and game.white_ball.is_clicked(events):
                                game.white_ball.is_active(game, game.is_behind_line_break())
                        self.return_command=str(self.reward)+"*"+str(self.was_closed)
                self.was_closed = True

        # if button_pressed == config.exit_button:
        #     was_closed = True
    
    pygame.quit()
