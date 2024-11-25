from flask import Flask, request
from atproto import Client
from dotenv import load_dotenv
import os
from BskyPost import BskyPost, PostEncoder
from BskyImage import BskyImage
from BskyVideo import BskyVideo
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
        if f.post.author.handle == user_handle:
            user_display_name = f.post.author.display_name
        if f.post.embed is None:
            post = BskyPost(f.post.uri, f.post.record.text, user_handle, user_display_name, f.post.author.avatar, f.post.author.handle, f.post.author.display_name,
                        f.post.like_count, f.post.reply_count, f.post.quote_count,
                        f.post.repost_count, f.post.record.created_at)
            user_posts.append(post)
        else:
            if f.post.embed.py_type == "app.bsky.embed.video#view":
                post_videos = [BskyVideo(f.post.embed.alt, f.post.embed.playlist,
                                         f.post.embed.aspect_ratio.width,
                                         f.post.embed.aspect_ratio.height)]
                post = BskyPost(f.post.uri, f.post.record.text, user_handle, user_display_name, f.post.author.avatar,
                                f.post.author.handle, f.post.author.display_name,
                                f.post.like_count, f.post.reply_count, f.post.quote_count,
                                f.post.repost_count, f.post.record.created_at, None, post_videos)
            if f.post.embed.py_type == "app.bsky.embed.images#view":
                post_images = []
                for image in f.post.embed.images:
                    post_images.append(BskyImage(image.alt, image.fullsize,
                                             image.aspect_ratio.width,
                                             image.aspect_ratio.height))
                post = BskyPost(f.post.uri, f.post.record.text, user_handle, user_display_name, f.post.author.avatar, f.post.author.handle, f.post.author.display_name,
                            f.post.like_count, f.post.reply_count, f.post.quote_count,
                            f.post.repost_count, f.post.record.created_at, post_images)
            user_posts.append(post)

    return json.dumps(user_posts, cls=PostEncoder)

if __name__ == '__main__':
   app.run()