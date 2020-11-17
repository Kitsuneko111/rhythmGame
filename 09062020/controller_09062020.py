from model import *
from view import *


class Controller:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._view.register(self)

    def get_player_center(self):
        return self._model.player.pos_x, self._model.player.pos_y

    def get_player_size(self):
        return self._model.player.width, self._model.player.height

    def move_player(self, x, y):
        player = self._model.player
        x_move = player.vel*x
        y_move = player.vel*y
        ##print(x_move, y_move)
        self._model.player.move(x_move, y_move)
        ##print(player.pos_x, player.pos_y)

    def get_obstacles(self):
        self._model.trigger_obstacle_creation()
        return self._model.obstacles

    def get_lives(self):
        return self._model.player.lives

    def stop(self):
        self._model.obstacles = []
        self._model.player = Player()

    def get_points(self):
        return self._model.player.points


if __name__ == "__main__":
    m = Model()
    v = View()
    c = Controller(m, v)
    v.run_view()
