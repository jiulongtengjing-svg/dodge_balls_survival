import pyxel


GAME_TITLE = "Dodge Ball!!"
KURYU_Y = 96
GAME_TIMER = 2700
GAME_COMPLETE_DISPLAY_TIMER = 120
GENERATE_TIMER = 2701
        
class Ball:
    NUM_BALL = 10
    BALL_WIDTH = 8
    BALL_HEIGHT = 8
    BALL_BOUNCE_Y = 128 - BALL_HEIGHT
    def __init__(self, app):
        self.app = app
        self.balls = []
        pyxel.load("my_resource.pyxres")
            
            
        self.app.ball = self
    def check_kuryu_collison(self, x, y):
        if not self.app.game_clear:
            if not self.app.is_title:
                return self.app.kuryu_x - x <= 7 and x - self.app.kuryu_x <= 11 and abs(KURYU_Y + 8 - y) <= 10

    def handle_ball_collisions(self):
        for ball in self.balls:
            if self.check_kuryu_collison(ball[0],ball[1]):
                self.app.game_over = True
                self.app.is_effect_on = True
                pyxel.playm(1)
                
    def handle_ball_generate(self):
            x = pyxel.rndi(-Ball.BALL_WIDTH, pyxel.width)
            y = pyxel.rndi(0, 30)
            vx = pyxel.rndf(0.1, 1.0)
            vy = pyxel.rndf(0.1, 1.0)
            return self.balls.append((x,y,vx,vy))
                               
    def update(self):
        if not self.app.game_over: 
            if self.app.generate_timer % 300 == 0:
                self.handle_ball_generate()
        else:
            return
            
        for i, (x, y, vx, vy) in enumerate(self.balls):
            x += vx
            vx += 0.01
            y += vy
            vy += 0.1
            if y >= Ball.BALL_BOUNCE_Y:
                y = Ball.BALL_BOUNCE_Y
                pyxel.playm(2)
                vy *= -0.95
            if x >= pyxel.width:
                x = -8
                y = pyxel.rndi(0,50)
                vx = pyxel.rndf(0.1, 1.0)
                vy = pyxel.rndf(0.1, 1.0)    
            
            self.balls[i] = (x, y, vx, vy)
                 
        self.handle_ball_collisions()
    
    def draw_effect(self):
        effect_x = self.app.kuryu_x + pyxel.rndi(7, 11)
        effect_y = KURYU_Y + pyxel.rndi(7, 11)
        effect_radius = pyxel.rndi(4,7)
        effect_color = pyxel.rndi(7,10)
        pyxel.circ(effect_x, effect_y, effect_radius, effect_color)
    
            
    def draw(self):
        for ball in self.balls:
            pyxel.blt(
                ball[0],
                ball[1],
                0,
                8,
                0,
                8,
                8,
                1    
            )
            
        if self.app.is_effect_on:
            self.draw_effect()
            
                
class App:
    BALL_SPAWN_INTERVAL = 300
    def __init__(self):
        pyxel.init(128, 128, title = GAME_TITLE)
        pyxel.load("my_resource.pyxres")
        self.is_title = True
        self.game_over = True
        self.reset_game()
        pyxel.playm(0, loop = True)
        
        
        pyxel.run(self.update, self.draw)
        
    def reset_game(self):
        self.game_clear = False
        self.game_over = False
        self.kuryu_x = 56
        self.timer = GAME_TIMER
        self.generate_timer = GENERATE_TIMER
        self.game_over_display_timer = 60
        self.game_complete_display_timer = GAME_COMPLETE_DISPLAY_TIMER
        self.ball_spawn_interval = 0
        self.left_timer = self.timer/30
        self.ball = None
        self.is_effect_on = False
        Ball(self)
        

    def handle_kuryu(self):
        if self.kuryu_x <= 0:
            self.kuryu_x = 0
        if self.kuryu_x >= pyxel.width - 16:
            self.kuryu_x = pyxel.width - 16  
            
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                self.kuryu_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                self.kuryu_x += 2     
            
    def handle_game_clear(self):
        
        if self.timer == 0:
            self.game_clear = True
            if self.game_complete_display_timer == 0:
                self.is_title = True
                self.game_clear = False
            else:
                self.game_complete_display_timer -= 1
        else:
            if not self.game_over:
                self.timer -= 1
                self.left_timer = self.timer/30
            else:
                self.timer = self.timer
            
    def handle_ball_generate_interval(self):
        if self.generate_timer == 0:
            self.generate_timer = 0
        else:
            self.generate_timer -= 1
            
                
    def handle_game_over(self):
        if self.game_over_display_timer == 0:
                self.is_title = True
                self.game_over = False
                self.is_effect_on = False
                    
        else:
            self.game_over_display_timer -= 1
            
    def update(self):
        if self.is_title:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
                self.is_title = False
                self.reset_game()
            return
        
        else:
            self.handle_ball_generate_interval()
            self.handle_game_clear()
            self.ball.update()
            if self.game_over:
                self.handle_game_over() 
            else:
                self.handle_kuryu()         
        
    
    def draw_title(self):
        pyxel.text(pyxel.width/2-20, pyxel.height/2-5, GAME_TITLE, 9)
        pyxel.text(pyxel.width/2-62, pyxel.height/2+10, "-Press Enter Key/ Tap X Button-", 10)
        
    def draw_kuryu(self):
        pyxel.blt(
            self.kuryu_x,
            KURYU_Y,
            0,
            16,
            0,
            16,
            16,
            1
        )
        
          
    def draw_game_clear(self):
        pyxel.text(pyxel.width/2-27, pyxel.height/2- 5, "Game Complete!!", 10)
        
    def draw_game_over(self):
        pyxel.text(pyxel.width/2-20, pyxel.height/2- 5, "Game Over", 10)
        
    def draw_timer(self):
        
        time_control = "TIMER:"+ str(round(self.left_timer))
        pyxel.text(10,10, time_control, 0)
                   
    def draw(self):
        
        pyxel.blt(0,0,0,32,0,128,128)
        self.draw_kuryu()
        
        
        if self.is_title:
            self.draw_title()
        else:
            self.ball.draw()
            self.draw_timer()
            
        if self.game_clear:
            self.draw_game_clear()
            
        if self.game_over:
            self.draw_game_over()
                  
App()
        