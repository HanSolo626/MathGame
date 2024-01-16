import pygame

from modules.image_manager import *

from modules.sound_manager import *

class Button:
    """The parent class for all buttons."""
    
    def __init__(self, function, x: int, y: int) -> None:
        
        self.action = None
        self.hover_image = None
        self.normal_image = None
        self.sound = None
        self.words = str
        self.letter_size = 0
        self.letter_color = (0, 0 ,0)
        self.current_image = None
        self.funtion = function

        self.x = x
        self.y = y

        self.sm = SoundManager()



        
    def set_stats(self, action, words: str, normal_image: pygame.Surface, hover_image: pygame.Surface, letter_size: int, letter_color, sound_effect: str):
        """
        Set the image, letter size, letter color, and sound of the button. letter_color must be (R,G,B) format. example for red: (255, 0, 0). \n
        NOTE: When setting hover_image, put in None if no hover current_image is desired.
        """

        self.action = action
        self.words = words
        self.hover_image = hover_image
        self.normal_image = normal_image
        self.letter_size = letter_size
        self.letter_color = letter_color
        self.sound = sound_effect

        self.image_rect = self.normal_image.get_rect()
        self.image_rect.x = self.x
        self.image_rect.y = self.y

        # Create a font object to make words.
        self.font =  pygame.font.SysFont("", self.letter_size)

        # Render a Surface from the font object.
        self.word_image = self.font.render(self.words, True, self.letter_color)
        self.word_image_rect = self.word_image.get_rect()
        self.word_image_rect.center = self.image_rect.center

        if hover_image == None:
            self.hover_image = self.normal_image

        self.current_image = self.hover_image


    def check_button(self, mouse_button_status):
        """Check if the button is being clicked and do whatever asignment it was given."""

        # Little peice of logic that ensures that button is only clicked once.
        if not mouse_button_status:
            self.click = True


        # If the mouse is hovering over the current_image rect...
        if self.image_rect.collidepoint(pygame.mouse.get_pos()):
            self.perform_hover_function()

            # Set current image to hover image
            self.current_image = self.hover_image
            self.image_rect = self.hover_image.get_rect()
            self.image_rect.x = self.x
            self.image_rect.y = self.y

            # If the mouse is clicked too...
            if mouse_button_status and self.click:
                self.perform_click_function()
                if self.sound != None:
                    self.sm.play_effect(self.sound)
                self.click = False

        else:
            self.current_image = self.normal_image
            self.image_rect = self.normal_image.get_rect()
            self.image_rect.x = self.x
            self.image_rect.y = self.y


    def perform_click_function(self):
        """Do the function when the button is being clicked on."""
        self.action(self)
        


    def perform_hover_function(self):
        """Do the function when the button is being hovered over. (AKA, DO NOTHING)"""
        return None


    def draw_button(self, screen):
        """Draw the button on the passed in screen."""
        screen.blit(self.current_image, self.image_rect)
        screen.blit(self.word_image, self.word_image_rect)




class TextField:
    """The parent class for text fields, used to display just text."""
    def __init__(self, text, x: int, y: int) -> None:
        
        self.text = text
        self.x = x
        self.y = y
        self.moving_text = None

        self.text_number = 0
        if type(self.text) == type(str):
            self.text_length = self.text.__len__()
        else:
            self.text_length = 0
        self.currently_displayed_text = ""
        self.sound_played = False

        self.sm = SoundManager()


    def set_stats(self, letter_size: int, letter_color, sound_effect: str, moving_text: bool):
        """Set the the font size, the letter color, and the sound effect name, to be played when the text is displayed."""

        self.letter_size = letter_size
        self.letter_color = letter_color
        self.sound_effect = sound_effect
        self.moving_text = moving_text

        self.font =  pygame.font.SysFont("", self.letter_size)

        if not self.moving_text:
            self.sound_played = True
            self.text_number = self.text_length
            self.currently_displayed_text = self.text


    def draw_button(self, screen):
        """Draw the text field while updating the text span."""

        if type(self.text) != type(str):
            self.currently_displayed_text = self.text(self)
            #print(self.currently_displayed_text)
        
        word_image = self.font.render(self.currently_displayed_text, True, self.letter_color)
        word_image_rect = word_image.get_rect()
        word_image_rect.x = self.x
        word_image_rect.y = self.y
        screen.blit(word_image, word_image_rect)

        
        if not self.text_number == self.text_length:
            self.currently_displayed_text += self.text[self.text_number]
            self.text_number += 1

        if self.sound_played == False:
            self.sm.play_effect(self.sound_effect)
            self.sound_played = True

    def check_button(self, mouse_pos):
        return None












class MainPlayButton(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("play_button").return_image(), Image("play_button_hover").return_image(), 0, "black", "click")

class SettingsButton(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("settings_button").return_image(), Image("settings_button_hover").return_image(), 0, "black", "click")

class MainTitle(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("title").return_image(), None, 0, "black", None)

class QuitButton(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("quit").return_image(), Image("quit_hover").return_image(), 0, "black", "click")

class ArrowRight(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("arrow_right").return_image(), Image("arrow_right_hover").return_image(), 0, "black", "click")

class ArrowLeft(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("arrow_left").return_image(), Image("arrow_left_hover").return_image(), 0, "black", "click")

class BackButton(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("back_button").return_image(), Image("back_button_hover").return_image(), 0, "black", "click")

class StartButton(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("start_button").return_image(), Image("start_button_hover").return_image(), 0, "black", "click")



class NumpadOne(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "1", Image("numpad").return_image(), Image("numpad_hover").return_image(), 90, "black", None)

class NumpadTwo(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "2", Image("numpad").return_image(), Image("numpad_hover").return_image(), 90, "black", None)

class NumpadThree(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "3", Image("numpad").return_image(), Image("numpad_hover").return_image(), 90, "black", None)

class NumpadFour(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "4", Image("numpad").return_image(), Image("numpad_hover").return_image(), 90, "black", None)

class NumpadFive(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "5", Image("numpad").return_image(), Image("numpad_hover").return_image(), 90, "black", None)

class NumpadSix(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "6", Image("numpad").return_image(), Image("numpad_hover").return_image(), 90, "black", None)

class NumpadSeven(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "7", Image("numpad").return_image(), Image("numpad_hover").return_image(), 90, "black", None)

class NumpadEight(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "8", Image("numpad").return_image(), Image("numpad_hover").return_image(), 90, "black", None)

class NumpadNine(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "9", Image("numpad").return_image(), Image("numpad_hover").return_image(), 90, "black", None)

class NumpadZero(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "0", Image("numpad").return_image(), Image("numpad_hover").return_image(), 90, "black", None)

class NumpadBackspace(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("backspace").return_image(), Image("backspace_hover").return_image(), 0, "black", None)


class SubmitAnswer(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "Submit", Image("submit").return_image(), Image("submit_hover").return_image(), 60, "black", None)

class GameOverTitle(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("gameover screen").return_image(), None, 0, "black", None)

class PlayAgain(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("play again").return_image(), Image("play again hover").return_image(), 0, "black", "click")

class VictoryTitle(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "", Image("victory").return_image(), None, 0, "black", None)


class SimpleField(TextField):
    """just text"""
    def __init__(self, text: str, x: int, y: int) -> None:
        super().__init__(text, x, y)

        self.set_stats(50, (255, 255, 255), None, False)


class BasicText(TextField):
    """Has moving text"""
    def __init__(self, text: str, x: int, y: int) -> None:
        super().__init__(text, x, y)

        self.set_stats(40, (255,255,255), None, True)



class TestButton(Button):
    def __init__(self, function, x: int, y: int) -> None:
        super().__init__(function, x, y)

        self.set_stats(function, "yay", Image("ArrowRight").return_image(), None, 50, (255,0,0), None)
