# This is the image manager. To access images, you import image_manager
# and use 'Image("<image name>")' to get your image. If you want to add
# images, put in 'self.image_dict' with this format: ' "name":"image path" '.

import pygame

class ImageManager:
    def __init__(self) -> None:
        

        # Put image references here.
        self.image_dict = {
            "chalkboard":"chalkboard_background.png",
            "play_button":"play_button.png",
            "play_button_hover":"play_button_hover.png",
            "settings_button":"settings_button.png",
            "settings_button_hover":"settings_button_hover.png",
            "title":"title.png",
            "quit":"quit_button.png",
            "quit_hover":"quit_button_hover.png",
            "arrow_left":"grey_arrow_left.png",
            "arrow_right":"grey_arrow_right.png",
            "arrow_left_hover":"grey_arrow_left_hover.png",
            "arrow_right_hover":"grey_arrow_right_hover.png",
            "start_button":"start_button.png",
            "start_button_hover":"start_button_hover.png",
            "back_button":"grey_back_button.png",
            "back_button_hover":"grey_back_button_hover.png",
            "numpad":"numpad_blank.png",
            "numpad_hover":"numpad_blank_hover.png",
            "backspace":"backspace.png",
            "backspace_hover":"backspace_hover.png",
            "submit":"blank.png",
            "submit_hover":"blank_hover.png",
            "red_x":"red_x.png",
            "greyed_x":"greyed_x.png",
            "clock_outline":"clock_outline.png",
            "play again":"playagain_button.png",
            "play again hover":"playagain_button_hover.png",
            "gameover screen":"gameover_title.png",
            "victory":"victory_screen.png",
            "stick man happy":"stick man happy.png",
            "stick man":"stick man normal.png",
            "stick man sad":"stick man sad.png",
            "stick man worried":"stick man worried.png",

        }


        # Do not change!
        self.image_path = "images/"


        # Prep images
        for image in self.image_dict:
            self.image_dict[image] = pygame.image.load(self.image_path+self.image_dict[image])
        


        self.custom_generated_rects = {
            0:pygame.Rect(0,0, 2000, 1200),
        }


    def get_image(self, image_name: str):
        """Returns Surface Pygame object."""
        return self.image_dict[image_name]
    
    def get_image_dict(self):
        """Get the image dictionary."""
        return self.image_dict
    
class Image(ImageManager):
    def __init__(self, image_name: str):
        super().__init__()

    
        self.image = self.get_image(image_name)

    def return_image(self):
        """Return image."""
        return self.image
    