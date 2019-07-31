import itertools
import random
import zope.event

import config
import event
import physics



def resolve_all_collisions(balls, holes, table_sides,reward):
    # destroys any circles that are in a hole
    for ball_hole_combination in itertools.product(balls, holes):
        if physics.distance_less_equal(ball_hole_combination[0].ball.pos, ball_hole_combination[1].pos, config.hole_radius):
            
            print("***************************ball_hole_combination[0]",ball_hole_combination[0].number)

            if ball_hole_combination[0].number==9:
                reward=reward+10.
            elif ball_hole_combination[0].number>=2 and ball_hole_combination[0].number<=8:
                reward =reward+0.1
            elif ball_hole_combination[0].number==0:
                reward = reward - 10.
            
            
            zope.event.notify(event.GameEvent("POTTED", ball_hole_combination[0]))

    # collides balls with the table where it is needed
    for line_ball_combination in itertools.product(table_sides, balls):
        if physics.line_ball_collision_check(line_ball_combination[0], line_ball_combination[1].ball):
            physics.collide_line_ball(line_ball_combination[0], line_ball_combination[1].ball)
    
    
    ball_list = balls.sprites()
    # ball list is shuffled to randomize ball collisions on the 1st break
    random.shuffle(ball_list)
    
    
    for ball_combination in itertools.combinations(ball_list, 2):
        if physics.ball_collision_check(ball_combination[0].ball, ball_combination[1].ball):
            physics.collide_balls(ball_combination[0].ball, ball_combination[1].ball)
            #print("ball_combination[0].ball.pos : {}".format(ball_combination[0].ball.pos))
            # print("ball_combination[0].number : {}".format(ball_combination[0].number))
            # print("ball_combination[1].number : {}".format(ball_combination[1].number))

            if ball_combination[0].number==0:
                if ball_combination[1].number==9:
                    reward = reward+1.
                elif ball_combination[1].number>=2 and ball_combination[0].number<=9:
                    reward=reward+0.01

            elif ball_combination[1].number==0:
                if ball_combination[0].number==9:
                    reward = reward+1
                elif ball_combination[0].number>=2 and ball_combination[0].number<=9:
                    reward=reward+0.01





            zope.event.notify(event.GameEvent("COLLISION", ball_combination))
    
    return reward


def check_if_ball_touches_balls(target_ball_pos, target_ball_number, balls):
    
    touches_other_balls = False
    for ball in balls:
        if target_ball_number != ball.number and \
                physics.distance_less_equal(ball.ball.pos, target_ball_pos, config.ball_radius * 2):
            touches_other_balls = True
            break
    return touches_other_balls
