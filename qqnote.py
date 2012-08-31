import HTMLParser
import codecs
import sys


def myjoin(list):
    temp = ''.join(list)
    return temp


def output(title, time, content):
    str_title = myjoin(title)
    str_time = myjoin(time)
    str_content = myjoin(content)
    #print str_title
    #print str_time
    #print str_content
    #print '-----------------------------'
    str_title = str_title.replace('/', '')
    file_name = r'temp/' + str_title
    f = codecs.open(file_name, 'w', 'utf-8')
    f.write(str_time)
    f.write('\n')
    f.write(str_content)
    f.close()


class LinksParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.recording = 0
        self.istitle = 0
        self.istime = 0
        self.iscontent = 0
        self.newpara = 0
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
                if self.newpara:
                    output(self.title, self.time, self.content)
                    self.title = []
                    self.time = []
                    self.content = []
                self.newpara = 1
                #break
            elif name == 'class' and value == 'notetitle bigfont':
                self.istitle = 1
                break
            elif name == 'class' and value == 'graytext timesep':
                self.istime = 1
                break
            elif name == 'id' and value == 'content':
                self.iscontent = 1
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
        #test whether data is an empty string
        if data.strip() == '':
            return
        #Keep the \r\n in the string
        temp = data.strip(' ')
        if self.recording:
            if self.istitle:
                self.title.append(temp)
            elif self.istime:
                self.time.append(temp)
            elif self.iscontent:
                self.content.append(temp)


def parse(file_name):
    parser = LinksParser()
    f = codecs.open(file_name, 'r', 'utf-8')
    html = f.read()
    parser.feed(html)
    #The last paragraph can't be handle inside the HTMLParser class
    #So I handle it here
    output(parser.title, parser.time, parser.content)
    parser.close()


if __name__ == '__main__':
    for i in sys.argv[1:]:
        parse(i)
