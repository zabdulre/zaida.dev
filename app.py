from flask import Flask
from flask import render_template
from utils import Blog, refreshBlogsIfStale, blogsDict

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/blog")
def blog():
    refreshBlogsIfStale()
    return render_template("blog.html", blogs=list(blogsDict.values()))

@app.route("/blog/<blogUrl>")
def getBlog(blogUrl: str):
    refreshBlogsIfStale()
    fetchedBlog: (Blog|None)=blogsDict.get(blogUrl)
    if fetchedBlog is not None:
        return render_template("base_blog.html", blog=fetchedBlog)
    
    return "404 not found"