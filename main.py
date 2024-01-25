import pygame, sys, os

from PIL import Image as pilImage
from PIL import ImageDraw as pilImageDraw
from FacillimumLibraryMATH import Facillimum_Library
from modules.high_variable_manager import VariableManager
from modules.page import *
from modules.high_variable_manager import *
from modules.sound_manager import *



class Main:
    def __init__(self) -> None:
        
        pygame.init()

        self.screen = pygame.display.set_mode((2000, 1200), pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption("MATH Time Attack")
        pygame.display.set_icon(pygame.image.load("math game logo time.png"))

        self.FL = Facillimum_Library(self.screen)
        
        self.hvm = VariableManager(self)
        self.iml = ImageManager()
        self.sm = SoundManager()

        self.fpsClock = pygame.time.Clock()
        
        self.time = 0

        # Page numbers:
        # 0: Main menu
        # 1: Settings
        # 2: Game
        self.current_page = 0
        self.left_click = False
        self.right_click = False
        self.left_down = False
        self.right_down = False

        self.pie_amount = 0
        self.pie_clocks = []
        self.pies_made = False

        self.clock_outline_img = pygame.transform.scale(self.iml.get_image("clock_outline"), (150, 150))


    def check_events(self):

        self.check_mouse()
        
        for event in pygame.event.get():

            # Check for quit
            if event.type == pygame.QUIT:
                sys.exit()

            # Check numpad numbers
            elif event.type == pygame.KEYDOWN and self.hvm.current_class_num == 3:
                if event.key == pygame.K_1:
                    self.hvm.add_num("1")
                elif event.key == pygame.K_2:
                    self.hvm.add_num("2")
                elif event.key == pygame.K_3:
                    self.hvm.add_num("3")
                elif event.key == pygame.K_4:
                    self.hvm.add_num("4")
                elif event.key == pygame.K_5:
                    self.hvm.add_num("5")
                elif event.key == pygame.K_6:
                    self.hvm.add_num("6")
                elif event.key == pygame.K_7:
                    self.hvm.add_num("7")
                elif event.key == pygame.K_8:
                    self.hvm.add_num("8")
                elif event.key == pygame.K_9:
                    self.hvm.add_num("9")
                elif event.key == pygame.K_0:
                    self.hvm.add_num("0")
                elif event.key == pygame.K_BACKSPACE:
                    self.hvm.lose_num()
                elif event.key == pygame.K_RETURN:
                    self.hvm.check_answer()

            # Check for mouse clicks
            elif event.type == pygame.MOUSEBUTTONUP:
                if not pygame.mouse.get_pressed()[0]:
                    self.left_down = False
                    self.left_click = False
                if not pygame.mouse.get_pressed()[2]:
                    self.right_click = False
                    self.right_down = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                        self.left_click = True
                        self.left_down = True
                    
                    
                if pygame.mouse.get_pressed()[2]:
                        self.right_click = True
                        self.right_down = True

        
    def check_mouse(self):
        if self.left_down:
            self.left_click = False
        if self.right_down:
            self.right_click = False

        
    def generate_pie_clocks(self, amount):
        if type(amount[self.hvm.current_operation][1]) == type(""):
            amount = amount[1][1]
        else:
            amount = amount[self.hvm.current_operation][1]
        
        margin = 360 / amount + 1
        self.pie_amount = 0
        self.pie_clocks = []
        j = []

        image = pilImage.new("RGB", (220, 220), (75,75,75))
        draw = pilImageDraw.Draw(image)
        string = "pie"+str(amount)+".png"
        self.pie_clocks.append(string)
        image.save(string)

        for a in range(0, amount):
            b = (a+1) * margin
            #b = a * margin
            image = pilImage.new("RGB", (220, 220), (75,75,75))
            draw = pilImageDraw.Draw(image)
            draw.pieslice((0, 0, 220, 220), start=0, end=b, fill="white")
            string = "pie"+str(a)+".png"
            #string = "pie"+str(a)+".png"
            self.pie_clocks.append(string)
            image.save(string)


        for filename in self.pie_clocks:
            f = pygame.transform.flip(pygame.transform.rotate(pygame.image.load(filename), 90), True, False)
            f = pygame.transform.scale(f, (120, 120))
            j.append(f)

        for file in self.pie_clocks:
            os.remove(file)
        self.pie_clocks = j
        self.pie_clocks.reverse()
        self.pie_amount = amount

        return self.pie_clocks
    
    def negate_number(self, number):
        return number - (number * 2)
    
    def get_clock_display(self):

        if self.hvm.current_operation == 0:
            a = self.hvm.difficulty_levels[self.hvm.current_difficulty][1][1]
        else:
            a = self.hvm.difficulty_levels[self.hvm.current_difficulty][self.hvm.current_operation][1]

        return a - self.hvm.counter + 1
    

    def check_current_page(self):
        """Check the current page."""
        self.hvm.current_page.check_buttons(self.left_click)






    def run_program(self):
        
        while True:
            self.check_events()
            self.check_current_page()


            # Update and draw everything
            
            self.hvm.current_page.draw_self()

            if self.hvm.current_class_num == 0:
                self.FL.draw_image(self.iml.get_image("stick man"), (300, 900), True)

            if self.hvm.current_class_num == 1:
                self.FL.draw_words(self.hvm.text_operation, 60, (1000,250), False, "white", True)
                self.FL.draw_words(self.hvm.text_difficulty, 60, (1000, 450), False, "white", True)
                self.hvm.reset_game()
                self.pies_made = False

            if self.hvm.current_class_num == 4:
                if self.hvm.solved_num > 5:
                    self.FL.draw_words("Equations solved: "+str(self.hvm.solved_num), 100, (1000, 550), False, "green", True)
                    self.FL.draw_image(self.iml.get_image("stick man happy"), (1600, 800), True)
                else:
                    self.FL.draw_words("Equations solved: "+str(self.hvm.solved_num), 100, (1000, 550), False, "red", True)
                    self.FL.draw_image(self.iml.get_image("stick man sad"), (1600, 800), True)

            
            if self.hvm.current_class_num == 3:

                if self.get_clock_display() == 0:
                    self.hvm.check_gameover(False)


                if not self.pies_made:
                    self.generate_pie_clocks(self.hvm.difficulty_levels[self.hvm.current_difficulty])
                    self.pies_made = True
                
                self.pies_made = self.hvm._check_gameover()

                try:
                    xyz = self.hvm.current_level[self.hvm.current_level_num]
                except:
                    self.hvm._set_current_page(5)

                self.FL.draw_words(str(xyz[0])+self.hvm.operation_list[self.hvm.current_operation][1]+str(xyz[1])+" = "+self.hvm.current_answer,
                                   150, (1000, 600), False, "white", True)
                
                

                #self.FL.draw_words()
                
                #for x in range(0, self.hvm.tries):
                #    self.FL.draw_image(self.iml.get_image("greyed_x"), ((200*(x+1)+100, 100)), False)
                #for x in range(0, self.hvm.fails):
                #    self.FL.draw_image(self.iml.get_image("red_x"), ((200*(x+1)+100, 100)), False)

                try:
                    self.FL.draw_image(self.pie_clocks[self.hvm.counter], (1750, 200), True)
                except:
                    self.pies_made = self.hvm._check_gameover()

                if self.get_clock_display() < 5:
                    self.FL.draw_words(str(self.get_clock_display()-1), 75, (1750, 200), False, "red", True)
                    self.FL.draw_image(self.iml.get_image("stick man worried"), (1600, 800), True)
                else:
                    self.FL.draw_words(str(self.get_clock_display()-1), 75, (1750, 200), False, "black", True)

                    if self.get_clock_display() < 9:
                        self.FL.draw_image(self.iml.get_image("stick man sad"), (1600, 800), True)
                    elif self.get_clock_display() < 12:
                        self.FL.draw_image(self.iml.get_image("stick man"), (1600, 800), True)
                    else:
                        self.FL.draw_image(self.iml.get_image("stick man happy"), (1600, 800), True)


                self.FL.draw_image(self.clock_outline_img, (1750, 200), True)

                #self.FL.draw_words(str(self.hvm.current_level_num)+" "+str(self.hvm.current_level.__len__()), 40, (0,0), False, "black", False)
                #self.FL.draw_words(str(self.hvm.current_level.__len__()), 40, (0,0), False, "black", False)
                
        
                if self.time >= 60:
                    self.hvm.counter += 1
                    self.time = 0

                    if self.get_clock_display() < 5 and self.get_clock_display() != 0:
                        self.sm.play_effect("beep")
                else:
                    self.time += 1

            

            self.FL.update()
            # Ensures that game runs at even framerate (60 frames per second).
            self.fpsClock.tick(60)

if __name__ == "__main__":
    ai = Main()
    ai.run_program()