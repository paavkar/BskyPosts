class BskyVideo:
    def __init__(self, alt_text, playlist,
                 aspect_ratio_width, aspect_ratio_height):
        self.alt_text = alt_text
        self.playlist = playlist
        self.aspect_ratio_width = aspect_ratio_width
        self.aspect_ratio_height = aspect_ratio_height

    def to_dict(self):
        return {
            'altText': self.alt_text,
            'playlist': self.playlist,
            'aspectRatioWidth': self.aspect_ratio_width,
            'aspectRatioHeight': self.aspect_ratio_height
        }