from handlers.base import Handler
from models import BlogPost
import markdown2


class MainHandler(Handler):
    def get(self):
        posts = BlogPost.query().order(-BlogPost.datetime).fetch()

        # convert markdown to html
        posts2 = []
        markdowner = markdown2.Markdown()

        for post in posts:
            post.text = post.text[:500] + "..."
            post.text = markdowner.convert(post.text)
            posts2.append(post)

        params = {"posts": posts2}
        self.render_template('index.html', params)


class AboutHandler(Handler):
    def get(self):
        self.render_template('about.html')


class ForbiddenHandler(Handler):
    def get(self):
        self.render_template('403.html')
