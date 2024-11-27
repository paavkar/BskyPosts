class BskyAuthor:
    def __init__(self, handle, display_name, avatar):
        self.handle = handle
        self.display_name = display_name
        self.avatar = avatar

    def to_dict(self):
        return {
            'handle': self.handle,
            'displayName': self.display_name,
            'avatar': self.avatar
        }