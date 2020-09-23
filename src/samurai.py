#!/usr/bin/python3

import sys
import urllib.request
import html
#import lxml.html
import shutil
import bs4 as bs

import skl_shared.shared as sh
from skl_shared.localize import _

sh.GUI_MES = False



class Parse:
    
    def __init__(self,text):
        f = '[Samurai] samurai.Parse.__init__'
        self.breaks = []
        self.tab = ' ' * 4
        self.text = text
        self.width, self.height = shutil.get_terminal_size()
        mes = _('Terminal size: {} columns, {} lines')
        mes = mes.format(self.width,self.height)
        sh.objs.get_mes(f,mes,True).show_debug()
        self.width -= 2 + len(self.tab)
        if self.width <= 0:
            mes = _('Wrong input data: "{}"!').format(self.width)
            sh.objs.get_mes(f,mes,True).show_warning()
            self.width = 80
        
    def pretty(self):
        f = '[Samurai] samurai.Parse.pretty'
        timer = sh.Timer(f) #TODO: del
        timer.start()       #TODO: del
        if self.text:
            text = sh.Text(text=self.text)
            text.convert_line_breaks()
            text.strip_lines()
            text.tabs2spaces()
            text.replace_x()
            text.delete_duplicate_spaces()
            self.text = text.text
            # Allow only 2 consequent line breaks
            while '\n\n\n' in self.text:
                self.text = self.text.replace('\n\n\n','\n\n')
        else:
            sh.com.rep_empty(f)
        timer.end() #TODO: del
                          
    def wrap(self):
        f = '[Samurai] samurai.Parse.wrap'
        timer = sh.Timer(f) #TODO: del
        timer.start()       #TODO: del
        if self.width:
            lst = list(self.text)
            count = 0
            i = 0
            space_i = 0
            while i < len(lst):
                if lst[i] == ' ':
                    space_i = i
                if lst[i] == '\n':
                    count = -1
                if count == self.width:
                    lst[space_i] = '\n'
                    self.breaks.append(space_i)
                    count = i - space_i
                i += 1
                count += 1
            self.text = ''.join(lst)
        else:
            sh.com.rep_empty(f)
        timer.end() #TODO: del
    
    def delete_tags(self):
        f = '[Samurai] samurai.Parse.delete_tags'
        timer = sh.Timer(f) #TODO: del
        timer.start()       #TODO: del
        if self.text:
            try:
                self.soup = bs.BeautifulSoup(self.text,'html.parser')
                for script in self.soup.find_all('script'): #,src=False
                    script.decompose()
                self.text = self.soup.get_text()
                #self.text = lxml.html.fromstring(self.text).text_content()
                """
                '''
                import re
                self.text = re.sub('<.*?>','',self.text)
                #from xml.etree.ElementTree import ElementTree
                #self.text = ''.join(xml.etree.ElementTree.fromstring(self.text).itertext())
                '''
                """
                self.text = html.unescape(self.text)
            except Exception as e:
                mes = _('The operation has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.get_mes(f,mes,True).show_error()
        else:
            sh.com.rep_empty(f)
        timer.end() #TODO: del
                          
    def add_tabs(self):
        f = '[Samurai] samurai.Parse.add_tabs'
        timer = sh.Timer(f) #TODO: del
        timer.start()       #TODO: del
        lst = list(self.text)
        i = len(lst) - 1
        while i >= 0:
            if lst[i] == '\n' and not i in self.breaks:
                if i + 1 < len(lst):
                    # 'isspace' will be 0,16s slower than ' '
                    if lst[i+1] != '\n' and not lst[i+1] == ' ':
                        lst.insert(i+1,self.tab)
            i -= 1
        self.text = ''.join(lst)
        timer.end() #TODO: del



class Browse:
    
    def __init__(self,text):
        self.text = text
        
    def run(self):
        f = '[Samurai] samurai.Browse.run'
        if self.text:
            print(self.text)
        else:
            sh.com.rep_empty(f)


if __name__ == '__main__':
    f = '[Samurai] samurai.__main__'
    if sys.argv and len(sys.argv) > 1:
        timer = sh.Timer()
        timer.start()
        if sys.argv[1].startswith('http'):
            #url = 'https://youtube.com'
            #url = 'https://en.wikipedia.org/wiki/Bushido'
            if len(sys.argv) > 2:
                get = sh.Get (url      = sys.argv[1]
                             ,encoding = sys.argv[2]
                             )
            else:
                get = sh.Get(url=sys.argv[1])
            get.run()
            parse = Parse(text=get.html)
            parse.delete_tags()
        else:
            text = sh.ReadTextFile(file=sys.argv[1]).get()
            parse = Parse(text=text)
        parse.pretty()
        parse.wrap()
        parse.add_tabs()
        timer.end()
        browse = Browse(text=parse.text)
        browse.run()
    else:
        #TODO: do not warn when console UI is ready
        mes = _('Please provide a URL as a command-line argument!')
        sh.objs.get_mes(f,mes,True).show_info()
