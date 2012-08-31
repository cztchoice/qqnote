import HTMLParser
import codecs


class LinksParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.recording = 0
        self.istitle = 0
        self.istime = 0
        self.iscontent = 0
        self.data = []
        self.title = []
        self.time = []
        self.content = []

    def handle_starttag(self, tag, attributes):
        if tag != 'div':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attributes:
            if name == 'class' and value == 'qqshowbd':
                pass
                #break
            elif name == 'class' and value == 'notetitle bigfont':
                self.istitle = 1
                print 'match it'
                break
            elif name == 'class' and value == 'graytext timesep':
                self.istime = 1
                print 'match it'
                break
            elif name == 'id' and value == 'content':
                self.iscontent = 1
                print 'match it'
                break

        else:
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.recording:
            self.recording -= 1
            self.istitle = 0
            self.istime = 0
            self.iscontent = 0

    def handle_data(self, data):
        if data.strip() == '':
            return
        if self.recording:
            self.data.append(data)
        if self.istitle:
            self.title.append(data)
        if self.istime:
            self.time.append(data)
        if self.iscontent:
            self.content.append(data)

parser = LinksParser()
f = codecs.open('example.html', 'r', 'utf-8')
html = f.read()
parser.feed(html)
print ''.join(parser.title)
print ''.join(parser.time)
print ''.join(parser.content)

parser.close()
