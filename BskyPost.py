import json

class BskyPost:
    def __init__(self, uri, text, author_handle, author_display_name, like_count, reply_count,
                 quote_count, repost_count, created_at, images = None):
        self.uri = uri
        self.text = text
        self.author_handle = author_handle
        self.author_display_name = author_display_name
        self.like_count = like_count
        self.reply_count = reply_count
        self.quote_count = quote_count
        self.repost_count = repost_count
        self.created_at = created_at
        self.images = images

    def to_dict(self):
        return {
            'uri': self.uri,
            'text': self.text,
            'authorHandle': self.author_handle,
            'authorDisplayName': self.author_display_name,
            'likeCount': self.like_count,
            'replyCount': self.reply_count,
            'quoteCount': self.quote_count,
            'repostCount': self.repost_count,
            'createdAt': self.created_at,
            'images': [image.to_dict() for image in self.images] if self.images is not None else None
        }
class PostEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BskyPost):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)