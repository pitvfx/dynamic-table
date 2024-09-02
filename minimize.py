
import re

with open("main.py") as f, open("main_compressed.py", "w") as g:
    content = f.read()
    content = re.sub(r"#(.*)\n", "\n", content)
    content = re.sub(r"(\s+)[)]", ")", content)
    content = re.sub(r"([,(])\s+", "\\1", content)
    content = '\n'.join((l for l in content.split("\n") if l.strip()))
    g.write(content)
