from decorators import login_required
from handlers.base import Handler
from models import BlogPost
import markdown2


class NewPostHandler(Handler):
    @login_required
    def get(self):
        return self.render_template("newpost.html")

    @login_required
    def post(self):
        title = self.request.get("title")
        slug = self.request.get("slug")
        text = self.request.get("text")
        if title and slug and text:
            BlogPost.create(title, slug, text)
        return self.redirect_to("main")


class BlogPostHandler(Handler):
    def get(self, slug):
        blog_post = BlogPost.query(BlogPost.slug == slug).get()

        # markdown
        markdowner = markdown2.Markdown()
        blog_post.text = markdowner.convert(blog_post.text)

        params = {"blog": blog_post}
        self.render_template("blogpost.html", params)


class EditBlogPost(Handler):
    @login_required
    def get(self, blog_id):
        blog = BlogPost.get_by_id(int(blog_id))
        return self.render_template("blog_post_edit.html", params={"blog": blog})

    @login_required
    def post(self, blog_id):
        blog = BlogPost.get_by_id(int(blog_id))
        title = self.request.get("title")
        slug = self.request.get("slug")
        text = self.request.get("text")
        if title and slug and text:
            blog = BlogPost.update(blog_post=blog, title=title, slug=slug, text=text)
        return self.redirect_to("blog-details", slug=blog.slug)
