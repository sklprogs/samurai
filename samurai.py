#!/usr/bin/python3

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','./locale')

import sys
import urllib.request
import bs4 as bs
import shared as sh


class Parse:
    
    def __init__(self,code):
        self._text = ''
        self._tab  = ' ' * 4
        self._code = code
        
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
            self._text = self._text.splitlines()
            self._text = '\n'.join([self._tab + line for line in self._text])
        else:
            sh.log.append ('Parse.pretty'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def run(self):
        if self._code:
            self.soup = bs.BeautifulSoup(self._code,'html.parser')
            for script in self.soup.find_all('script'): #,src=False
                script.decompose()
            self._text = self.soup.get_text()
            self.pretty()
            return self._text
        else:
            sh.log.append ('Parse.run'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )


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
        #url = 'https://youtube.com'
        #url = 'https://en.wikipedia.org/wiki/Bushido'
        get = sh.Get(url=sys.argv[1])
        get.run()
        parse = Parse(code=get._html)
        text  = parse.run()
        timer.end()
        browse = Browse(text=text)
        browse.run()
    # todo: do not warn when console UI is ready
    else:
        sh.log.append ('samurai'
                      ,_('INFO')
                      ,_('Please provide a URL as a command-line argument!')
                      )
