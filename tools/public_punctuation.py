"""Keep authored display copy in the user's ASCII-hyphen style, preserving markup and quotations."""
from html.parser import HTMLParser
import re

def plain_dashes(text):
    return re.sub(r'\u2013|\u2014|&(?:ndash|mdash);|&#(?:8211|8212);|&#x(?:2013|2014);', '-', text, flags=re.I)

class DisplayCopy(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text=text; self.lines=[0]; self.spans=[]; self.protected=[]
        self.lines.extend(m.end() for m in re.finditer('\n',text))
        self.feed(text)
    def pos(self):
        line,col=self.getpos(); return self.lines[line-1]+col
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style','code','pre','blockquote','q']: self.protected.append(tag)
        if not self.protected:
            raw=self.get_starttag_text()
            for m in re.finditer(r'(?P<key>title|alt|aria-label|placeholder)=(?P<quote>[\"\'])(?P<value>.*?)(?P=quote)',raw,re.S):
                self.spans.append((self.pos()+m.start('value'),self.pos()+m.end('value')))
    def handle_endtag(self,tag):
        if self.protected and tag==self.protected[-1]: self.protected.pop()
    def handle_data(self,data):
        if not self.protected:self.spans.append((self.pos(),self.pos()+len(data)))
    def handle_entityref(self,name):
        if not self.protected:self.spans.append((self.pos(),self.pos()+len(name)+2))
    def handle_charref(self,name):
        if not self.protected:self.spans.append((self.pos(),self.pos()+len(name)+3))

def public_punctuation(text):
    chunks=[]; end=0
    for start,stop in sorted(DisplayCopy(text).spans):
        chunks.extend([text[end:start],plain_dashes(text[start:stop])]); end=stop
    chunks.append(text[end:])
    return ''.join(chunks)
