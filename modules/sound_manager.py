import pygame, time

class SoundManager:
    def __init__(self) -> None:

        # Prep mixer, channels, and filepath extensions.
        pygame.mixer.init(30000)
        self.track_channel0 = pygame.mixer.Channel(0)
        self.effect_channel1 = pygame.mixer.Channel(1)
        self.effect_channel2 = pygame.mixer.Channel(2)
        self.effect_channel3 = pygame.mixer.Channel(3)
        self.effect_channel4 = pygame.mixer.Channel(4)
        self.effect_channel5 = pygame.mixer.Channel(5)
        self.effect_channel6 = pygame.mixer.Channel(6)
        self.effect_channel_list = [
            self.effect_channel1,
            self.effect_channel2,
            self.effect_channel3,
            self.effect_channel4,
            self.effect_channel5,
            self.effect_channel6
        ]
        self.track_path = "sounds/tracks/"
        self.effect_path = "sounds/effects/"



        # The track dictionary.
        self.track_dict = {

            # Format: "<name>:<file name>",
            
            

        }

        # The effect dictionary.
        self.effect_dict = {

            # Format: "<name>:<file name>",
            "click":"click_sound_effect.wav",
            "beep":"clock beep_quiet.wav",
            "buzzer":"gameshow_buzzer_quiet.wav",
            "ding":"ding_short.wav",
            "number_click":"chalk_click.wav",
            "erase":"erase_back.wav",
            

        }


        # Make all the files in track and effect dictionaries Sound objects.
        for sound in self.track_dict:
            self.track_dict[sound] = pygame.mixer.Sound(self.track_path+self.track_dict[sound])
        for sound in self.effect_dict:
            self.effect_dict[sound] = pygame.mixer.Sound(self.effect_path+self.effect_dict[sound])

        # Time out to allow for mixer to fully initilize.
        #time.sleep(2)



    def get_track_list(self):
        """Get the track list if you ever need it."""
        
        return self.track_dict
    

    def get_effect_dict(self):
        """Get the effect list if you ever need it."""

        return self.effect_dict
    

    def play_track(self, track_name: str):
        """Start to play a track. Note that this will overwrite the currently playing track."""

        self.track_channel0.play(self.track_dict[track_name])


    def queue_track(self, track_name: str):
        """Que up a track in the channel."""

        self.track_channel0.queue(self.track_dict[track_name])

    def pause_track(self):
        """Pause the track channel."""

        self.track_channel0.pause()

    def resume_track(self):
        """Resume the track channel."""

        self.track_channel0.unpause()

    def stop_track(self):
        """Completely stop the playback of the track."""

        self.track_channel0.stop()


    def play_effect(self, effect_name: str):
        """
        Play an effect.
        
        The function will play the effect in an idle channel. If all 
        the channels are busy, it will que the sound in Channel 1.
        """

        a = True
        for channel in self.effect_channel_list:
            if a == True and not channel.get_busy():
                channel.play(self.effect_dict[effect_name])
                a = False
        if a:
            self.effect_channel1.queue(self.effect_dict[effect_name])

    def pause_effects(self):
        """Pause all sound effect channels."""

        for channel in self.effect_channel_list:
            channel.pause()

    def resume_effects(self):
        """Resume all sound effect channels."""

        for channel in self.effect_channel_list:
            channel.unpause()

    def stop_effects(self):
        """Completely stop all sound effects."""

        for channel in self.effect_channel_list:
            channel.stop()

    