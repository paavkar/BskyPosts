import json

class BskyImage:
    def __init__(self, alt_text, full_size,
                 aspect_ratio_width, aspect_ratio_height):
        self.alt_text = alt_text
        self.full_size = full_size
        self.aspect_ratio_width = aspect_ratio_width
        self.aspect_ratio_height = aspect_ratio_height

    def to_dict(self):
        return {
            'altText': self.alt_text,
            'fullSize': self.full_size,
            'aspectRatioWidth': self.aspect_ratio_width,
            'aspectRatioHeight': self.aspect_ratio_height
        }