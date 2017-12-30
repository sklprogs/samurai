#!/usr/bin/python3

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','./locale')

import sys
import urllib.request
import bs4 as bs
import shutil as sl
import shared as sh


class Parse:
    
    def __init__(self,text):
        self._breaks = []
        self._tab    = ' ' * 4
        self._text   = text
        self._width, self._height = sl.get_terminal_size()
        sh.log.append ('Parse.__init__'
                      ,_('INFO')
                      ,_('Terminal size: %d columns, %d lines') \
                      % (self._width,self._height)
                      )
        self._width -= 2 + len(self._tab)
        if self._width <= 0:
            print(self._width) # todo: del
            sh.log.append ('Parse.__init__'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )
            self._width = 80
        
    def pretty(self):
        if self._text:
            text = sh.Text(text=self._text,Silent=False)
            text.convert_line_breaks()
            text.strip_lines()
            text.tabs2spaces()
            text.replace_x()
            text.delete_duplicate_spaces()
            self._text = text.text
            # Allow only 2 consequent line breaks
            while '\n\n\n' in self._text:
                self._text = self._text.replace('\n\n\n','\n\n')
            # cur # todo: del
            #self._text = self._text.splitlines()
            #self._text = '\n'.join([self._tab + line for line in self._text])
        else:
            sh.log.append ('Parse.pretty'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def wrap(self):
        if self._width:
            lst = list(self._text)
            count   = 0
            i       = 0
            space_i = 0
            while i < len(lst):
                if lst[i].isspace():
                    space_i = i
                if lst[i] == '\n':
                    count = -1
                if count == self._width:
                    lst[space_i] = '\n'
                    self._breaks.append(space_i)
                    count = i - space_i
                i += 1
                count += 1
            self._text = ''.join(lst)
        else:
            sh.log.append ('Parse.wrap'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def delete_tags(self):
        if self._text:
            try:
                self.soup = bs.BeautifulSoup(self._text,'html.parser')
                for script in self.soup.find_all('script'): #,src=False
                    script.decompose()
                self._text = self.soup.get_text()
            except:
                sh.log.append ('Parse.delete_tags'
                              ,_('WARNING')
                              ,_('Failed to parse the page!')
                              )
        else:
            sh.log.append ('Parse.delete_tags'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def add_tabs(self):
        lst = list(self._text)
        i = len(lst) - 1
        while i >= 0:
            if lst[i] == '\n' and not i in self._breaks:
                if i + 1 < len(lst):
                    if lst[i+1] != '\n' and not lst[i+1].isspace():
                        lst.insert(i+1,self._tab)
            i -= 1
        self._text = ''.join(lst)



class Browse:
    
    def __init__(self,text):
        self._text = text
        
    def run(self):
        if self._text:
            print(self._text)
        else:
            sh.log.append ('Browse.run'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )


if __name__ == '__main__':
    if sys.argv and len(sys.argv) > 1:
        timer = sh.Timer()
        timer.start()
        if sys.argv[1].startswith('http'):
            #url = 'https://youtube.com'
            #url = 'https://en.wikipedia.org/wiki/Bushido'
            get = sh.Get(url=sys.argv[1])
            get.run()
            parse = Parse(text=get._html)
            parse.delete_tags()
        else:
            text = sh.ReadTextFile(file=sys.argv[1]).get()
            parse = Parse(text=text)
        parse.pretty()
        parse.wrap()
        parse.add_tabs()
        timer.end()
        browse = Browse(text=parse._text)
        browse.run()
    # todo: do not warn when console UI is ready
    else:
        sh.log.append ('samurai'
                      ,_('INFO')
                      ,_('Please provide a URL as a command-line argument!')
                      )
