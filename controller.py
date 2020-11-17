from model import *
from view import *


class Controller:
    """class for going between UI and backend"""
    def __init__(self, model, view):
        self._model = model
        self._view:View = view
        self._view.register(self)
        self._model.register_c(self)

    def start(self, song):
        self._view.run_game(song)

    def get_player_center(self):
        """for getting the player location"""
        return self._model.player.pos_x, self._model.player.pos_y

    def get_player_size(self):
        """for getting player size"""
        return self._model.player.width, self._model.player.height

    def move_player(self, x, y):
        """works out where/how the player should move"""
        player = self._model.player
        if player.jump > 0:
            # print(player.jump)
            x_move = player.vel*player.jumpvel*x
            y_move = player.vel*player.jumpvel*y
        else:
            x_move = player.vel*x
            y_move = player.vel*y
        self._model.player.move(x_move, y_move)
        if player.jump > 0:
            player.jump -= 0.1

        # if player.jump_off > 0:
            # player.jump_off -= 1

    def get_jump(self):
        """returns the state of the jump cooldown"""
        return self._model.player.jump_off, self._model.player.jump_min

    def get_obstacles(self):
        """returns the obstacle information and ticks the backend"""
        self._model.obstacle_tick()
        return self._model.obstacles

    def get_lives(self):
        """gets player lives"""
        return self._model.player.lives

    def stop(self):
        """stops the backend"""
        self._model.obstacles = []
        self._model.player = Player()

    def get_points(self):
        """gets the number of obstacles avoided"""
        return self._model.player.points

    def set_bpm(self, bpm):
        """sets the bpm for the backend"""
        self._model.set_bpm(bpm)
        # self._model.player.jump_min = self._model.player.jump_min // bpm
        # print(self._model.player.jump_min//bpm, self._model.player.jump_min, bpm)

    def jump(self):
        """makes the player jump"""
        if self._model.player.jump_off <= 0:
            self._model.player.jump = self._model.player.max_jump
            self._model.player.jump_off = self._model.player.jump_min
            # print(self._model.player.jump_min)

    def set_jump_min(self):
        """sets the jump cooldown"""
        self._model.player.jump_min = self._model.player.jump_min // self._model.bpm
        self._model.player.jump_off = 1
        self._model.player.jump = 0

    def quit(self):
        self._view.quit()

    def get_buttons(self, menu, x, y):
        return self._model.menus[menu].return_button_info(x, y)

    def get_statics(self, menu):
        return self._model.menus[menu].return_statics_info()

    def pressed(self, button, menu):
        self._model.menus[menu].buttons[button].press()

    def get_player_name(self):
        return self._view.ask_player_name()

    def end(self):
        self._model.save_score(self.get_points(),
                               self._model.difficulty,
                               self._model.songs[self._model.track_no][0],
                               self.get_player_name())


if __name__ == "__main__":
    m = Model()
    v = View()
    c = Controller(m, v)
    v.run_view()

'''
1. give input a bpm and then pregen obstacles from this - randomisation currently
2. shape rotation calculations - Done
2.5. Shape rotation hitboxes - done
3. bpm -> rotation ?
4. 'jumping' upon space or other key for a small boost - done
5. something or other, inbuilt menu? - escape plan?
'''
