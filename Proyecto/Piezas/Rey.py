import Pieza


class Rey(Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self._image = Pieza.Pieza.images['rey_blanco'] if is_white else Pieza.Pieza.images['rey_negro']

    def get_image(self):
        return self._image
