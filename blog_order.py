import glob
import os
import pathlib
import markdown
import frontmatter
pre_path='/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes'
files=glob.glob(pre_path+'/**/*.md')

data = pathlib.Path(files[10]).read_text(encoding='utf-8')
# md = markdown.Markdown(extensions=["markdown_meta_extension"])
# md.convert(data)
# print(md.Meta)

f=frontmatter.loads(data)
print(f['date'])