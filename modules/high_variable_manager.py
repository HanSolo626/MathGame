# THE HIGH VARIABLE MANAGER #

# Pages are defined here.








#from gamedata.modules.save_manager import SaveManager
import pygame, importlib, random
from modules.button import *
from modules.page import *
from FacillimumLibraryMATH import Facillimum_Library
from modules.sound_manager import SoundManager


import sys



#############################
### HIGH VARIABLE MANAGER ###
#############################

class VariableManager:
    """The class that manages the modification of important variables such as health of actors and points."""

    def __init__(self, ai_game) -> None:
        
        # Load an instance of SaveManager
        #self.save_manager = SaveManager()


        self.current_page = None

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.FL = Facillimum_Library(self.screen)
        self.sm = SoundManager()
        
        #self.class_list = {
        #    0:HomeMenu(ai_game),
        #    1:SetupMenu(ai_game),
        #    2:SettingsMenu(ai_game),
        #    3:MainGame(ai_game),
        #    4:GameOverScreen(ai_game),
        #}
        self.class_list = {
            0:HomeMenu,
            1:SetupMenu,
            2:SettingsMenu,
            3:MainGame,
            4:GameOverScreen,
            5:VictoryScreen,
        }


        h = {}
        a = 0
        for v in self.class_list:
            h[a] = self.update_loading_screen(self.class_list[v], ai_game, a+1)
            a += 1
        self.class_list = h

        self.current_class_num = 0

        self.operation_list = {
            0:["Addition +", " + "],
            1:["Subtraction -", " - "],
            2:["Multiplication x", " x "],
            #3:["Division /", "/"],
        }
        self.current_operation = 0
        self.text_operation = self.operation_list[self.current_operation][0]

        self.difficulty_levels = {
            # name, [limit, time]
            0:["Easy", [(0, 10), 20],[(0, 5), 20]],
            1:["Medium", [(6,20), 15],[(0, 12), 15]],
            2:["Advanced", [(15,50), 15],[(6,15), 15]],
        }

        self.current_difficulty = 1
        self.text_difficulty = self.difficulty_levels[self.current_difficulty][0]

        self.current_level = []
        self.current_level_num = 0

        self.current_answer = ""

        self.tries = 5
        self.fails = 0
        self.counter = 0
        self.counter_num_to_add = 3
        self.solved_equations = []
        self.solved_num = 0



        #self.opls = OperationList()

        if ai_game != None:
            self.current_page = self.class_list[self.current_class_num]

        
    def update_loading_screen(self, object, thing, phase: int):
        self.FL.paint_screen((100,100,100))
        self.FL.draw_rect((900, 150), (1000, 600), "black", True)
        self.FL.draw_rect((((900 / self.class_list.__len__()) * phase), 150), (450, 525), "white", False)
        self.FL.draw_words("loading...", 100, (1000, 350), False, "white", True)
        self.FL.update()
        return object(thing)

    
    
    def generate_level(self):
        def func(z):
            a = []
            c = []
            while a.__len__() < 15:
                t = self.hvm.difficulty_levels[self.hvm.current_difficulty]
                if self.hvm.current_operation == 2:
                    t = t[2][0]
                else:
                    t = t[1][0]
                n1 = random.randint(t[0], t[1])
                n2 = random.randint(t[0], t[1])
                if self.hvm.current_operation == 1 and n1 < n2:
                    c = [n2, n1]
                else:
                    c = [n1, n2]
                
                if self.hvm.current_operation == 0:
                    n3 = c[0] + c[1]
                elif self.hvm.current_operation == 1:
                    n3 = c[0] - c[1]
                elif self.hvm.current_operation == 2:
                    n3  = c[0] * c[1]
                c.append(n3)
                a.append(c.copy())
                c.clear()
            self.hvm.current_level = a
            print(a)
            return a
        return func
    
    def second_generate_level(self):
        
        def func(z):
            level = []
            equations = []
            nums = []
            if self.hvm.current_operation == 0:
                g = self.hvm.current_operation + 1
            else:
                g = self.hvm.current_operation

            b = self.hvm.difficulty_levels[self.hvm.current_difficulty][g][0][1] + 1
            #for a in range(0, (b * b) + b):
            #    level.append([])
            for a in range(0, ((b-1) * (b-1)) + b):
                nums.append(a)

            for first in range(0, b):
                for second in range(0, b):
                    n1 = first
                    n2 = second

                    if self.hvm.current_operation == 1 and first < second:
                        
                        c = [n2, n1]
                    else:
                        c = [n1, n2]
                    
                    
                    if self.hvm.current_operation == 0:
                        n3 = c[0] + c[1]
                    elif self.hvm.current_operation == 1:
                        n3 = c[0] - c[1]
                    elif self.hvm.current_operation == 2:
                        n3  = c[0] * c[1]
                    c.append(n3)
                    equations.append(c.copy())
                    c.clear()

            
            while equations != []:
                selection = random.randint(0, nums.__len__())
                #print(level.__len__())
                level.append(equations.pop(selection))
                
                if nums != []:
                    nums.remove(nums.__len__()-1)
                
            for problem in level:
                y = [problem[1], problem[0], problem[2]]
                #if y in level:
                #    level.remove(y)
                for thing in level:
                    if y == thing:
                        level.remove(y)
            
                    
            self.hvm.current_level = level
            self.hvm.reset_game()
            return level
        return func
    


    def second_generate_level_hvm(self):
        level = []
        equations = []
        nums = []
        if self.current_operation == 0:
            g = self.current_operation + 1
        else:
            g = self.current_operation

        b = self.difficulty_levels[self.current_difficulty][g][0][1] + 1
        #for a in range(0, (b * b) + b):
        #    level.append([])
        for a in range(0, ((b-1) * (b-1)) + b):
            nums.append(a)

        for first in range(0, b):
            for second in range(0, b):
                n1 = first
                n2 = second

                if self.current_operation == 1 and first < second:
                    
                    c = [n2, n1]
                else:
                    c = [n1, n2]
                
                
                if self.current_operation == 0:
                    n3 = c[0] + c[1]
                elif self.current_operation == 1:
                    n3 = c[0] - c[1]
                elif self.current_operation == 2:
                    n3  = c[0] * c[1]
                c.append(n3)
                equations.append(c.copy())
                c.clear()

        
        while equations != []:
            selection = random.randint(0, nums.__len__())
            #print(level.__len__())
            level.append(equations.pop(selection))
            
            if nums != []:
                nums.remove(nums.__len__()-1)
            
        for problem in level:
            y = [problem[1], problem[0], problem[2]]
            #if y in level:
            #    level.remove(y)
            for thing in level:
                if y == thing:
                    level.remove(y)
        
                
        self.current_level = level
        self.reset_game()
        return level


            
    def load_save_data(self):
        self.save_data = importlib.import_module("save_file.py")


    def add_num(self, num):

        def func(a):
            if self.hvm.current_answer == '' and num == "0":
                return None
            if not self.hvm.current_answer.__len__() >= 5:
                self.hvm.sm.play_effect("number_click")
                self.hvm.current_answer = self.hvm.current_answer + num
            return None
        return func
    
    def add_num(self, num):
        if self.current_answer == '0' and num == "0":
            return None
        if not self.current_answer.__len__() >= 5:
            self.sm.play_effect("number_click")
            self.current_answer = self.current_answer + num
        return None
        
    
    def lose_num(self):

        def func(a):
            if not self.hvm.current_answer.__len__() == 0:
                self.hvm.sm.play_effect("erase")
                self.hvm.current_answer = self.hvm.current_answer.removesuffix(self.hvm.current_answer[self.hvm.current_answer.__len__()-1])
            return None
        return func
    
    def lose_num(self):
        if not self.current_answer.__len__() == 0:
            self.sm.play_effect("erase")
            self.current_answer = self.current_answer.removesuffix(self.current_answer[self.current_answer.__len__()-1])
        return None
        
    
    def check_answer_button(self):

        def func(a):
            if self.hvm.current_answer == '':
                return None
            if int(self.hvm.current_answer) == self.hvm.current_level[self.hvm.current_level_num][2]:
                self.hvm.current_level_num += 1
                self.hvm.current_answer = ''
                self.hvm.counter = 0
                self.hvm.sm.play_effect("ding")
                if self.hvm.current_level_num == self.hvm.current_level.__len__():
                    #self.hvm.set_current_page(5)
                    if self.hvm.current_difficulty == 2:
                        self.hvm.set_current_page(5)
                    else:
                        self.hvm.current_difficulty += 1
                        g = self.hvm.solved_equations
                        self.hvm.second_generate_level()(self)
                        self.hvm.solved_equations = g
            else:
                #self.hvm.current_answer = ''
                #self.hvm.fails += 1
                #self.hvm.counter = 0
                self.hvm.check_gameover(False)

            return None
        return func
    
    def check_answer(self):  
        if self.current_answer == '':
            return None
        if int(self.current_answer) == self.current_level[self.current_level_num][2]:
            print(self.current_level_num)
            print(self.current_level)
            self.solved_equations.append(self.current_level[self.current_level_num])
            self.current_level_num += 1
            self.current_answer = ''
            #self.counter = 0
            self.counter -= self.counter_num_to_add
            if self.counter < 0:
                self.counter = 0
            self.sm.play_effect("ding")
            if self.current_level_num == self.current_level.__len__():
                #self.set_current_page(5)
                if self.current_difficulty == 2:
                    self.set_current_page(5)
                else:
                    self.current_difficulty += 1
                    g = self.solved_equations
                    #NOTE
                    self.second_generate_level_hvm()
                    self.solved_equations = g
        else:
            #self.current_answer = ''
            #self.fails += 1
            #self.counter = 0
            self.check_gameover(False, False)

        return None
    
    def check_gameover(self, a, total_gameover=True):
        if a:
            self.hvm.current_answer = ''
            #self.hvm.fails += 1
            if total_gameover:
                self.hvm.fails = 5
            self.hvm.counter += 1
            self.hvm.sm.play_effect("buzzer")
        else:
            self.current_answer = ''
            #self.fails += 1
            if total_gameover:
                self.fails = 5
            self.counter += 1
            self.sm.play_effect("buzzer")
        if self.fails >= 5:
            if a:
                self.hvm.set_current_page(4)
            else:
                self.set_current_page(4)
            self.solved_num = self.solved_equations.__len__()
    
    def reset_game(self):
        self.current_answer = ""
        self.tries = 5
        self.fails = 0
        self.counter = 0
        self.solved_equations = []
        self.solved_num = 0
        print("test")

    def _check_gameover(self):
        if self.fails >= 5:
            self._set_current_page(4)
            #self.reset_game() NOTE
            return False
        else:
            return True


    def raise_difficulty(self):

        def func(a):
            if self.hvm.current_difficulty == 2:
                self.hvm.current_difficulty = 0
            else:
                self.hvm.current_difficulty += 1
            self.hvm.text_difficulty = self.hvm.difficulty_levels[self.hvm.current_difficulty][0]
            return None
        return func
    
    def lower_difficulty(self):

        def func(a):
            if self.hvm.current_difficulty == 0:
                self.hvm.current_difficulty = 2
            else:
                self.hvm.current_difficulty -= 1
            self.hvm.text_difficulty = self.hvm.difficulty_levels[self.hvm.current_difficulty][0]
            return None
        return func

    def raise_operation(self):
        
        def func(a):
            if self.hvm.current_operation == 2:
                self.hvm.current_operation = 0
            else:
                self.hvm.current_operation += 1
            self.hvm.text_operation = self.hvm.operation_list[self.hvm.current_operation][0]
            
            return None
        return func

    def lower_operation(self):
        
        def func(a):
            if self.hvm.current_operation == 0:
                self.hvm.current_operation = 2
            else:
                self.hvm.current_operation -= 1
            self.hvm.text_operation = self.hvm.operation_list[self.hvm.current_operation][0]

            #self.opls.text_operation = self.text_operation
            #self.opls.current_operation = self.current_operation
            return None
        return func


    def get_current_page(self):
        """Returns the current page object"""
        return self.current_page

    def get_current_save_data(self):
        """Returns current save object."""
        return self.save_data_object
    
    def load_save_data(self, save_number: int):
        """Loads the save as current_save_data, and returns it."""
        self.save_data_object = self.save_manager.load_save(save_number)
        return self.save_data_object
    

    def set_current_page(a, page_num):
        """Set the current page and init it."""

        def func(self):
            
            a.hvm.current_page = a.hvm.class_list[page_num]
            a.hvm.current_class_num = page_num
            
            #a.hvm.current_page.set_button_list(a.hvm.current_page.button_list)
            return None
        
        return func
    
    def _set_current_page(self, page_num):
        self.current_page = self.class_list[page_num]
        self.current_class_num = page_num
    

    def exit_game(self):
        """Exit the game."""
        sys.exit()


    def _print(self):
        print("print this 123")

    def none(self):
        return None







##################
##### PAGES ######
##################



class HomeMenu(Page):
    def __init__(self, ai_game) -> None:
        super().__init__(ai_game)

        self.set_background(Image("chalkboard").return_image())


        self.set_button_list([
            MainPlayButton(VariableManager.set_current_page(ai_game, 1), 700, 500),
            #SettingsButton(VariableManager.set_current_page(ai_game, 2), 50, 950),
            MainTitle(VariableManager.none, 0, 0),
            QuitButton(VariableManager.exit_game, 1800, 1000)
        ])

class SetupMenu(Page):
    def __init__(self, ai_game) -> None:
        super().__init__(ai_game)

        self.set_background(Image("chalkboard").return_image())

        self.set_button_list([
            BackButton(VariableManager.set_current_page(ai_game, 0), 50, 950),
            ArrowLeft(VariableManager.lower_operation(ai_game), 650, 200),
            ArrowRight(VariableManager.raise_operation(ai_game), 1200, 200),
            
            ArrowRight(VariableManager.raise_difficulty(ai_game), 1200, 400),
            ArrowLeft(VariableManager.lower_difficulty(ai_game), 650, 400),

            StartButton(VariableManager.set_current_page(ai_game, 3), 875, 600),
            StartButton(VariableManager.second_generate_level(ai_game), 875, 600)

        ])


class MainGame(Page):
    def __init__(self, ai_game) -> None:
        super().__init__(ai_game)

        self.set_background(Image("chalkboard").return_image())

        self.set_button_list([
            #QuitButton(VariableManager.exit_game, 50, 1000),
            BackButton(VariableManager.set_current_page(ai_game, 1), 50, 1000),

            #NumpadOne(VariableManager.add_num(ai_game, "1"), 1300, 100),
            #NumpadTwo(VariableManager.add_num(ai_game, "2"), 1500, 100),
            #NumpadThree(VariableManager.add_num(ai_game, "3"), 1700, 100),
            #NumpadFour(VariableManager.add_num(ai_game, "4"), 1300, 300),
            #NumpadFive(VariableManager.add_num(ai_game, "5"), 1500, 300),
            #NumpadSix(VariableManager.add_num(ai_game, "6"), 1700, 300),
            #NumpadSeven(VariableManager.add_num(ai_game, "7"), 1300, 500),
            #NumpadEight(VariableManager.add_num(ai_game, "8"), 1500, 500),
            #NumpadNine(VariableManager.add_num(ai_game, "9"), 1700, 500),
            #NumpadZero(VariableManager.add_num(ai_game, "0"), 1700, 700),
            #NumpadBackspace(VariableManager.lose_num(ai_game), 1300, 700),

            SubmitAnswer(VariableManager.check_answer_button(ai_game), 850, 950),
        ])

class GameOverScreen(Page):
    def __init__(self, ai_game) -> None:
        super().__init__(ai_game)

        self.set_background(Image("chalkboard").return_image())

        self.set_button_list([
            GameOverTitle(VariableManager.none, 0,0),
            PlayAgain(VariableManager.set_current_page(ai_game, 1), 850, 700),
            QuitButton(VariableManager.exit_game, 50, 1000)
        ])


class VictoryScreen(Page):
    def __init__(self, ai_game) -> None:
        super().__init__(ai_game)

        self.set_background(Image("chalkboard").return_image())

        self.set_button_list([
            VictoryTitle(VariableManager.none, 0,0),
            PlayAgain(VariableManager.set_current_page(ai_game, 1), 850, 700),
            QuitButton(VariableManager.exit_game, 50, 1000),
        ])



class SettingsMenu(Page):
    def __init__(self, ai_game) -> None:
        super().__init__(ai_game)

        self.set_background(Image("chalkboard").return_image())

        self.set_button_list([
            BackButton(VariableManager.set_current_page(ai_game, 0), 1775, 975)
        ])