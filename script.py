import os
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown as md
from datetime import datetime

# dictionary to collect parsed .md files
CONTENT = {}

# iterates through posts (contents)
for md_post in os.listdir('contents'):
    file_path = os.path.join('contents', md_post)

    # .md files are opened with read mode
    with open(file_path, 'r') as file:
        CONTENT[md_post] = md(file.read(), extras=['metadata'])

# posts in content dir are sorted with lambda by created_at --> datetime
POSTS = {
    post: CONTENT[post] for post in
    sorted(CONTENT, key=lambda post: datetime.strptime(CONTENT[post].metadata['date'], '%Y-%m-%d  %H:%M'), reverse=True)
}

# path searcher. In this case, searches through templates dirs
file_loader_env = Environment(loader=FileSystemLoader(searchpath='templates'))
# index.html file is accessed via "file_loader_env"
index_template = file_loader_env.get_template('index.html')
# post_detail.html file is accessed via "file_loader_env"
post_detail_template = file_loader_env.get_template('post_detail.html')

# metadata is accessed
index_posts_metadata = [CONTENT[post].metadata for post in POSTS]
# metadata is taken to index.html with render
index_html_content = index_template.render(posts=index_posts_metadata)

# new index.html is created with static info in it
with open('index.html', 'w') as file:
    file.write(index_html_content)

# to get an access to metadata  through .html file, metadata is collected through iteration
for post in POSTS:
    post_metadata = POSTS[post].metadata

    # variable are passed via post_context
    post_context = {
        'content': POSTS[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
    }

    # access to post_context is granted via rendering
    post_html_content = post_detail_template.render(post=post_context)

    # a path to create a uniques static html in a dir based on slug

    post_file_path = './output/posts/{slug}/index.html'.format(slug=post_metadata['slug'])

    # dirs are created based on path
    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)

    # post_detail.html is opened written with content in it
    with open(post_file_path, 'w') as file:
        file.write(post_html_content)
