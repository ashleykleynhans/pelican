from datetime import datetime

AUTHOR = 'Ashley Kleynhans'
SITEURL = ''
SITENAME = "Ashley's Blog"
SITETITLE = 'Ashley Kleynhans'
SITESUBTITLE = 'DevOps Engineer'
BROWSER_COLOR = '#333333'
SITELOGO = SITEURL + '/images/profile.jpeg'
FAVICON = SITEURL + '/images/favicon.ico'
PORT = 8000

# Code highlighting the theme
PYGMENTS_STYLE = 'solarized-dark'

# Code blocks with line numbers
PYGMENTS_RST_OPTIONS = {
    'linenos': 'table'
}

ROBOTS = 'index, follow'

PATH = 'content'
OUTPUT_PATH = 'blog/'
TIMEZONE = 'Africa/Johannesburg'

DISABLE_URL_HASH = True

DEFAULT_LANG = 'en'
THEME = 'themes/flex'
CUSTOM_CSS = 'static/custom.css'

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDER_AS_CATEGORY = False
MAIN_MENU = True
HOME_HIDE_TAGS = True

GITHUB_CORNER_URL = 'https://github.com/ashleykleynhans/pelican'

SOCIAL = (
    ('github', 'https://github.com/ashleykleynhans'),
    ('linkedin', 'https://www.linkedin.com/in/ashleykleynhans')
)

MENUITEMS = (
    ('Archives', '/archives'),
    ('Categories', '/categories'),
    ('Tags', '/tags')
)

LINKS = (
    ('Home', '/'),
)

CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike 4.0 International License',
    'version': '4.0',
    'slug': 'by-sa',
    'icon': True,
    'language': 'en_US',
}

COPYRIGHT_YEAR = datetime.now().year
DEFAULT_PAGINATION = 10
STATIC_CHECK_IF_MODIFIED = True

STATIC_PATHS = [
    'images',
    'static',
    'images/favicon.ico',
    'static/robots.txt',
    'static/custom.css'
]

THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

USE_LESS = True

PLUGIN_PATHS = [
    './pelican-plugins'
]

PLUGINS = [
    'sitemap',
    'post_stats'
]

# Sitemap Settings
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.6,
        'pages': 0.5,
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly',
    }
}

ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = PAGE_URL + 'index.html'

# There is no other HTML content
READERS = {
    'html': None
}