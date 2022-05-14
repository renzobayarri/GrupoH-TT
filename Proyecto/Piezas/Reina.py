import Pieza


class Reina(Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self._image = Pieza.Pieza.images['reina_blanca'] if is_white else Pieza.Pieza.images['reina_negra']

    def get_image(self):
        return self._image
