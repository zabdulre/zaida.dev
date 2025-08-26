from datetime import datetime
from pathlib import Path
import time

blogsFolder = '/root/zaida.dev/blogs'
datePrintFormat: str = "%b %m, %Y"

class Blog:
    def __init__(self, name: str, authors: str, date: str, content: str):
        self.title: str = name
        self.authors: str = authors
        self.date: str = date
        self.content: str = content
        self.url: str = name.replace(" ", "-").rstrip()
        
blogsDict: dict[str, Blog] = {}

def process_ready(blog : Path) -> (Blog|None):
    timestamp: float = time.time()
    with blog.open() as f:
        title: str = f.readline()
        authors: str = f.readline()
        content: str = f.read()
    with open(blog.with_name(blog.name[:-5]+"published"), 'w') as file:
        file.write(str(timestamp) + "\n" + title + authors + content)
        blog.unlink()
        return Blog(title, authors, datetime.fromtimestamp(timestamp).strftime(datePrintFormat), content)
    return None

def process_published(blog : Path) -> (Blog|None):
    with blog.open() as f:
        date: str = datetime.fromtimestamp(float(f.readline())).strftime(datePrintFormat)
        title: str = f.readline()
        authors: str = f.readline()
        content: str = f.read()
        return Blog(title, authors, date, content)
    return None

def refreshBlogsIfStale() -> (None):
    initialize : bool = len(blogsDict) == 0
    blogsPath : Path = Path(blogsFolder)
    blogFiles: list[Path] = [i for i in blogsPath.iterdir() if i.is_file() and i.exists()]
    processedBlogs : list[Blog] = []
    for i in blogFiles:
        j: Blog | None
        if i.name.endswith('.ready'):
            j = process_ready(i)
        elif i.name.endswith('.published') and initialize:
            j = process_published(i)
        else:
            continue
        
        if j is not None:
            processedBlogs.append(j)
    sorted(processedBlogs, key= lambda b: datetime.strptime(b.date, datePrintFormat).timestamp())
    for i in processedBlogs:
        blogsDict[i.url] = i #TODO optimize memory usage here
    return None


#TODO consider adding a file that saves this info kind of like a cache and this code only runs when the file gets out of date or some static array
#TODO check whether dates work
#TODO consider changing content to preview and only load the first few lines. Then add a function to get that specific blog when it is clicked
#TODO consider ways to bring up a blog when it is clicked (javascript vs template) and implement that
#TODO instead of using dateStringFormat, just use a timestamp
#TODO server log instead of throwing internal server error
#TODO implement links to blogs
#TODO add ordinal suffixes for dates