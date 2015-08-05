# Map Options Will Be Alterable in the Template


class Options:
    MAP_WIDGET_HEIGHT = 480
    MAP_OPTIONS = {}
    MARKER_OPTIONS = {}

    def height(self, size):
        self.MAP_WIDGET_HEIGHT = size
        return self.MAP_WIDGET_HEIGHT

    def map_options(self, key, value):
        self.MAP_OPTIONS[key] = value
        return self.MAP_OPTIONS

    def marker_options(self, key, value):
        self.MARKER_OPTIONS[key] = value
        return self.MARKER_OPTIONS
