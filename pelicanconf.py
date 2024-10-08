AUTHOR = 'AI'
SITENAME = 'AI-generated blog'
SITEURL = "https://blog.cfdemo.site"

PATH = "content"
STATIC_PATHS = ['images', 'static']
EXTRA_PATH_METADATA = {'static/favicon.ico': {'path': 'favicon.ico'},}

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/")
)

# Social widget
# SOCIAL = (
#     ("You can add links in your config file", "#"),
#     ("Another social link", "#"),
# )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Theme
THEME = 'themes/Peli-Kiera'

# Plugins
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['readtime', 'neighbors']