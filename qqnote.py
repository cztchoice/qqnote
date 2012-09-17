#!/usr/bin/python
# -*- coding: utf-8 -*-
import HTMLParser
import codecs
import sys
import os


def output(title, time, content):
    str_title = ''.join(title)
    str_time = ''.join(time)
    str_content = '\r\n'.join(content)
    #print str_title
    #print str_time
    #print str_content
    #print '-----------------------------'
    #str_title = str_title.replace('/', '')
    #str_title = str_title.replace('?', '')
    #str_title = str_title.replace(':', '')
    #file_name = r'temp/' + str_title + '.txt'
    file_name = 'temp/%d.txt' % output.val
    output.val += 1
    f = codecs.open(file_name, 'w', 'cp936')
    f.write(str_title)
    f.write(os.linesep)
    f.write(str_time)
    f.write(os.linesep)
    f.write(str_content)
    f.close()
output.val = 0


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
    #the fileencoding QQmail export is cp936
    #f = codecs.open(file_name, 'r', 'utf-8')
    f = codecs.open(file_name, 'r', 'cp936')
    html = f.read()
    parser.feed(html)
    #The last paragraph can't be handle inside the HTMLParser class
    #So I handle it here
    output(parser.title, parser.time, parser.content)
    parser.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Usage: %s file_names_to_translate" % sys.argv[0]
    for i in sys.argv[1:]:
        parse(i)
