# Ashley's Blog (https://trapdoor.cloud)

This is the source code for my personal blog, which can be
found at [trapdoor.cloud][https://trapdoor.cloud].

The blog is powered by [Pelican](http://getpelican.com/),
which generates static HTML from Markdown files, and
uses the [Flex](https://github.com/alexandrevicenzi/Flex)
theme.

## Build and run locally

```bash
git clone https://github.com/ashleykleynhans/pelican
cd pelican
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
pelican -r -l
```

You can now access the blog in your browser at:
[http://127.0.0.1:8000](http://127.0.0.1:8000).


