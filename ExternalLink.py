class ExternalLink:
    def __init__(self, description, title, uri, thumbnail):
        self.description = description
        self.title = title
        self.uri = uri
        self.thumbnail = thumbnail

    def to_dict(self):
        return {
            'description': self.description,
            'title': self.title,
            'uri': self.uri,
            'thumbnail': self.thumbnail
        }