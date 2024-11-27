from flask import Flask, request
from atproto import Client
from dotenv import load_dotenv
import os
from BskyPost import BskyPost, PostEncoder
from BskyImage import BskyImage
from BskyVideo import BskyVideo
from ExternalLink import ExternalLink
from BskyAuthor import BskyAuthor
import json

app = Flask(__name__)

load_dotenv()
client = Client()
my_handle = os.getenv("MY_HANDLE")
client.login(my_handle, os.getenv("APP_PASSWORD"))

@app.route("/")
def hello():
    return "Root"

@app.route("/get-posts", methods=["GET"])
def get_posts():
    data = request.json
    user_handle = data["userHandle"]
    user_display_name = ""

    user_feed_response = client.get_author_feed(user_handle)

    user_posts = []

    for f in user_feed_response.feed:
        post = None
        post_videos = None
        post_images = None
        post_external_link = None

        quoted_post = None
        quoted_post_videos = None
        quoted_post_images = None
        quoted_post_external_link = None

        repost_author = None
        reply_parent_author = None
        quoted_post_reply_parent_author = None

        if f.post.author.handle == user_handle:
            user_display_name = f.post.author.display_name

        if f.post.record.reply is None or f.reason is not None:
            if f.reason is not None:
                repost_author = BskyAuthor(f.post.author.handle, f.post.author.display_name, f.post.author.avatar)
            if f.post.record.reply is not None:
                repost_author = BskyAuthor(f.post.author.handle, f.post.author.display_name, f.post.author.avatar)
                reply_parent_author = BskyAuthor(f.reply.parent.author.handle, f.reply.parent.author.display_name,
                                                 f.reply.parent.author.avatar)

            if f.post.embed is None:
                post = BskyPost(f.post.uri, f.post.record.text, user_handle, user_display_name, f.post.author.avatar,
                            f.post.author.handle, f.post.author.display_name,
                            f.post.like_count, f.post.reply_count, f.post.quote_count,
                            f.post.repost_count, f.post.record.created_at, repost_author=repost_author,
                            reply_parent_author=reply_parent_author)
            else:
                if f.post.embed.py_type == "app.bsky.embed.external#view":
                    post_external_link = ExternalLink(f.post.embed.external.description,
                                                  f.post.embed.external.title,
                                                  f.post.embed.external.uri,
                                                  f.post.embed.external.thumb)

                if f.post.embed.py_type == "app.bsky.embed.video#view":
                    if f.post.embed.aspect_ratio is not None:
                        post_videos = [BskyVideo(f.post.embed.alt, f.post.embed.playlist,
                                         f.post.embed.aspect_ratio.width,
                                         f.post.embed.aspect_ratio.height)]

                if f.post.embed.py_type == "app.bsky.embed.images#view":
                    post_images = []
                    for image in f.post.embed.images:
                        if image.aspect_ratio is not None:
                            post_images.append(BskyImage(image.alt, image.fullsize,
                                             image.aspect_ratio.width,
                                             image.aspect_ratio.height))

                # post is a quote with just text #
                if f.post.embed.py_type == "app.bsky.embed.record#view":
                    # check the quoted post for media/links #
                    for embed in f.post.embed.record.embeds:
                        if embed.py_type == "app.bsky.embed.external#view":
                            quoted_post_external_link = ExternalLink(embed.external.description,
                                                                 embed.external.title,
                                                                 embed.external.uri,
                                                                 embed.external.thumb)

                        if embed.py_type == "app.bsky.embed.images#view":
                            quoted_post_images = []
                            for image in embed.images:
                                if image.aspect_ratio is not None:
                                    quoted_post_images.append(BskyImage(image.alt, image.fullsize,
                                                     image.aspect_ratio.width,
                                                     image.aspect_ratio.height))

                        if embed.py_type == "app.bsky.embed.video#view":
                            if embed.aspect_ratio is not None:
                                quoted_post_videos = [BskyVideo(embed.alt, embed.playlist,
                                                 embed.aspect_ratio.width,
                                                 embed.aspect_ratio.height)]

                    quoted_post = BskyPost(f.post.embed.record.uri, f.post.embed.record.value.text,
                                       user_handle, user_display_name, f.post.embed.record.author.avatar,
                                       f.post.embed.record.author.handle, f.post.embed.record.author.display_name,
                                       f.post.embed.record.like_count, f.post.embed.record.reply_count,
                                       f.post.embed.record.quote_count, f.post.embed.record.repost_count,
                                       f.post.embed.record.value.created_at, quoted_post_images, quoted_post_videos,
                                       None, quoted_post_external_link)

                # post is a quote with some kind of media #
                if f.post.embed.py_type == "app.bsky.embed.recordWithMedia#view":
                    if f.post.embed.media.py_type == "app.bsky.embed.external#view":
                        post_external_link = ExternalLink(f.post.embed.media.external.description,
                                                      f.post.embed.media.external.title,
                                                      f.post.embed.media.external.uri,
                                                      f.post.embed.media.external.thumb)

                    if f.post.embed.media.py_type == "app.bsky.embed.images#view":
                        post_images = []
                        for image in f.post.embed.media.images:
                            if image.aspect_ratio is not None:
                                post_images.append(BskyImage(image.alt, image.fullsize,
                                                         image.aspect_ratio.width,
                                                         image.aspect_ratio.height))

                    if f.post.embed.media.py_type == "app.bsky.embed.video#view":
                        if f.post.embed.media.aspect_ratio is not None:
                            post_videos = [BskyVideo(f.post.embed.media.alt, f.post.embed.media.playlist,
                                             f.post.embed.media.aspect_ratio.width,
                                             f.post.embed.media.aspect_ratio.height)]

                    # check the media/link in quoted post #
                    if f.post.embed.record.record.embeds is not None:
                        for quoted_post_embed in f.post.embed.record.record.embeds:
                            if quoted_post_embed.py_type == "app.bsky.embed.external#view":
                                quoted_post_external_link = ExternalLink(quoted_post_embed.external.description,
                                                                 quoted_post_embed.external.title,
                                                                 quoted_post_embed.external.uri,
                                                                 quoted_post_embed.external.thumb)

                            if quoted_post_embed.py_type == "app.bsky.embed.images#view":
                                quoted_post_images = []
                                for image in quoted_post_embed.images:
                                    if image.aspect_ratio is not None:
                                        quoted_post_images.append(BskyImage(image.alt, image.fullsize,
                                                     image.aspect_ratio.width,
                                                     image.aspect_ratio.height))

                            if quoted_post_embed.py_type == "app.bsky.embed.video#view":
                                if quoted_post_embed.aspect_ratio is not None:
                                    quoted_post_videos = [BskyVideo(quoted_post_embed.alt, quoted_post_embed.playlist,
                                                 quoted_post_embed.aspect_ratio.width,
                                                 quoted_post_embed.aspect_ratio.height)]

                        quoted_post = BskyPost(f.post.embed.record.record.uri, f.post.embed.record.record.value.text,
                                       user_handle, user_display_name, f.post.embed.record.record.author.avatar,
                                       f.post.embed.record.record.author.handle,
                                       f.post.embed.record.record.author.display_name,
                                       f.post.embed.record.record.like_count, f.post.embed.record.record.reply_count,
                                       f.post.embed.record.record.quote_count, f.post.embed.record.record.repost_count,
                                       f.post.embed.record.record.value.created_at, quoted_post_images,
                                       quoted_post_videos, None, quoted_post_external_link)

                post = BskyPost(f.post.uri, f.post.record.text, user_handle, user_display_name, f.post.author.avatar,
                            f.post.author.handle, f.post.author.display_name,
                            f.post.like_count, f.post.reply_count, f.post.quote_count,
                            f.post.repost_count, f.post.record.created_at, post_images, post_videos, quoted_post,
                            post_external_link, repost_author, reply_parent_author)
            user_posts.append(post)

    return json.dumps(user_posts, cls=PostEncoder)

if __name__ == '__main__':
   app.run()