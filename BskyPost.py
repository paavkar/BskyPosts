import json

class BskyPost:
    def __init__(self, uri, text, user_handle, user_display_name, author_avatar, author_handle, author_display_name, like_count, reply_count,
                 quote_count, repost_count, created_at, images = None, videos = None, quoted_post = None, external_link = None):
        self.uri = uri
        self.text = text
        self.user_handle = user_handle
        self.user_display_name = user_display_name
        self.author_avatar = author_avatar
        self.author_handle = author_handle
        self.author_display_name = author_display_name
        self.like_count = like_count
        self.reply_count = reply_count
        self.quote_count = quote_count
        self.repost_count = repost_count
        self.created_at = created_at
        self.images = images
        self.videos = videos
        self.quoted_post = quoted_post
        self.external_link = external_link

    def to_dict(self):
        return {
            'uri': self.uri,
            'text': self.text,
            'userHandle': self.user_handle,
            'userDisplayName': self.user_display_name,
            'authorAvatar': self.author_avatar,
            'authorHandle': self.author_handle,
            'authorDisplayName': self.author_display_name,
            'likeCount': self.like_count,
            'replyCount': self.reply_count,
            'quoteCount': self.quote_count,
            'repostCount': self.repost_count,
            'createdAt': self.created_at,
            'images': [image.to_dict() for image in self.images] if self.images is not None else None,
            'videos': [video.to_dict() for video in self.videos] if self.videos is not None else None,
            'quotedPost': self.quoted_post.to_dict() if self.quoted_post is not None else None,
            'externalLink': self.external_link.to_dict() if self.external_link is not None else None
        }
class PostEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BskyPost):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)