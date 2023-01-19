from datetime import datetime

AUTHOR = 'Ashley Kleynhans'
SITEURL = ''
SITENAME = "Ashley's Blog"
SITETITLE = 'Ashley Kleynhans'
SITESUBTITLE = 'DevOps Engineer'
BROWSER_COLOR = '#333333'
SITELOGO = SITEURL + '/images/profile.jpeg'
FAVICON = SITEURL + '/favicon.ico'
PORT = 8000

PATH = 'content'
ROBOTS = 'index, follow'
OUTPUT_PATH = 'output/'
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
    ('stack-overflow', 'https://stackoverflow.com/users/817324/ashley-kleynhans'),
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
    'static/custom.css',
    'static/CNAME'
]

EXTRA_PATH_METADATA = {
    'static/CNAME': {'path': 'CNAME'},
    'static/robots.txt': {'path': 'robots.txt'},
    'images/favicon.ico': {'path': 'favicon.ico'}
}

THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

USE_LESS = True

PLUGIN_PATHS = [
    './pelican-plugins'
]

PLUGINS = [
    'sitemap',
    'post_stats',
    'neighbors'
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

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'pygments_style': 'solarized-dark',
            'noclasses': True,
            'guess_lang': True,
        },
        'markdown.extensions.extra': {
            'markdown.extensions.footnotes': {},
            'markdown.extensions.fenced_code': {},
        },
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {
            'title': 'Table of Contents',
            # 'anchorlink': True,
            #'permalink': True,
            'toc_depth': 3,
        },
        'pymdownx.emoji': {
            'options': {
                'attributes': {
                    'align': 'absmiddle',
                    'height': '20px',
                    'width': '20px'
                },
            },
        },
    },
    'output_format': 'html5',
}

DISQUS_SITENAME = 'trapdoor-cloud'
DISQUS_COMMENT_COUNT = True

# Google Analytics 4
GOOGLE_GLOBAL_SITE_TAG = 'G-DDEVPJLBFC'
