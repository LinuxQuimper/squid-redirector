#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
#    Author : Fanch317 (fanch@linuxquimper.org)
#
#    Date : 2009-09-27
#    Version 0.6
#
#    Description : Ce script est un redirecteur pour squid.
#                  Il est destinne a faire passer toute requete de depots de
#                  distributions vers des depots locaux plus rapides lors
#                  d'install-party. (Proxy transparent)

import sys,re,os.path,urllib2,logging,random

levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
LOGLEVEL = logging.INFO

# Definition des deots locaux
redirectors = {}
redirectors[0] = ["(.*\.)?archive.ubuntu.com/ubuntu", "http://127.0.0.1/ubuntu/"]
redirectors[1] = ["(.*\.)?archive.ubuntu.com/ubuntus", "http://127.0.0.1/ubuntus/"]

# Definition du chemin du fichier log et de sa verbosite
LOG_FILENAME = 'squid-redirector.log'




logging.basicConfig(filename=LOG_FILENAME,level=LOGLEVEL,format='%(asctime)s %(levelname)s %(message)s',datefmt='%d/%m/%Y %H:%M:%S')


logging.info('---------------------------------------')
logging.info('Lancement d\'thread squid-redirector.py')
logging.info('---------------------------------------')



while True:
  # URL ip-address/fqdn ident method
  line_squid = sys.stdin.readline().strip()
  
  logging.debug('Reception d\'une requete : '+line_squid)
  
  # Recuperation de l'URL
  try:
    list = line_squid.split(' ')
    url_input = list[0]
    
    # Recuperation de l'origine du client
    try:
      client_input = list[1] + rnd
    except:
      logging.warning('Impossible de recuperer l\'origine du client depuis la chaine '+line_squid)
      client_input = "NC"
    logging.info(client_input + ' Reception d\'une URL par : ' + url_input)

    i = 0
    while i < len(redirectors):
      logging.debug(client_input + ' Test sur le depot %d' %(i))

      try:
        # On test sur le depot correpond a ce genre d'URL
        if re.search('http://' + redirectors[i][0],url_input):
          logging.debug(client_input + ' L\'url correspond au depot')
          try:
            url_locale = re.sub(r'http://' + redirectors[i][0],redirectors[i][1],url_input)
            logging.debug(client_input + ' Verification de la presence du fichier local : ' + url_locale)
            urllib2.urlopen(url_locale)
            url_output = url_locale + '\n'
            logging.info(client_input + ' Ce fichier est en cache : ' + url_output)
            print url_output
            break
          except:
            # Le fichier est introuvable sur le depot
            logging.debug(client_input + ' Cette URL n\'est telechargeable dans ce depot')
      except:
        # L'URL ne correspond pas au depot
        logging.debug(client_input + ' Ce depot ne correspond pas a l\'URL')
      i = i + 1
    
    # Tout les depots ont ete testes, aucun ne correspond
    logging.info(client_input + ' Aucun depot ne contient cette URL')
    print url_input #+ '\n'
      
  except:
    logging.error(client_input + ' Impossible de recuperer l\'URL depuis la chaine '+line_squid)
    
  sys.stdout.flush()
  