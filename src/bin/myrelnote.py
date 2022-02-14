import re
import sys
import optparse

from urllib import request
from bs4 import BeautifulSoup

class MyRelnote():

   def strip_tags(self, s):
       return re.sub(r'<.+?>', "", s)

   def pretty_str(self, s):
       return re.sub(r'\s+', " ", s.replace("\n", " ").replace("\r", " ")).strip()

   def main(self):
       parser = optparse.OptionParser(usage="usage: %prog [options] release-note-url")
       parser.add_option('--format', action='store', default='markdown', help='markdown or confluence')
       opts, args = parser.parse_args()

       if (len(args) < 1):
           parser.print_help()
           sys.exit(1)

       response = request.urlopen(args[0])
       soup = BeautifulSoup(response, features='html.parser')
       response.close()

       for changelog in soup.select('.simplesect > div > ul[type=disc].itemizedlist > li.listitem, h3.title'):
           output = self.pretty_str(self.strip_tags(str(changelog)))

           if str(changelog).find('<h3') != -1:
               if opts.format == 'confluence':
                   print('h1. ' + output)
                   print('||Changelog||')
               elif opts.format == 'markdown':
                   print('# ' + output)
                   print('| Changelog |')
                   print('|------- |')
                   pass
           else:
               if opts.format == 'confluence':
                   print('| ' + output + ' |')
               elif opts.format == 'markdown':
                   print('| ' + output + ' |')

relnote = MyRelnote()
relnote.main()
