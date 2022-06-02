#!/usr/bin/env python3

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#    Author : Fanch317 (fanch@linuxquimper.org)
#
#    Created at: 2009-09-27
#    Edited at: 2022-06-02
#    Version 1.0
#
#    Description : Ce script est un redirecteur pour squid.
#                  Il est destinne a faire passer toute requete de depots de
#                  distributions vers des depots locaux plus rapides lors
#                  d'install-party. (Proxy transparent)

import sys,re,os.path,urllib3,logging,random,urllib.request

levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
LOGLEVEL = logging.INFO

# Definition des deots locaux
redirectors = {}
redirectors[0] = ["(.*\.)?archive.ubuntu.com/ubuntu", "http://127.0.0.1/repositories/ubuntu/"]
redirectors[1] = ["(.*\.)?security.ubuntu.com/ubuntu", "http://127.0.0.1/repositories/ubuntu-security/"]
redirectors[2] = ["(.*\.)?archlinux.fr/extra","http://127.0.0.1/repositories/archlinux"]
redirectors[3] = ["(.*\.)?mirror.tyborek.pl/arch","http://127.0.0.1/repositories/archlinux"]
redirectors[4] = ["(.*\.)?slitaz.org/packages","http://127.0.0.1/repositories/slitaz/"]
redirectors[5] = ["(.*\.)?slitaz.org/pxe","http://127.0.0.1/repositories/slitaz/pxe"]
redirectors[6] = ["(.*\.)?slitaz.org/pxe/..","http://127.0.0.1/repositories/slitaz/boot"]
redirectors[7] = ["(.*\.)?slitaz.org/boot","http://127.0.0.1/repositories/slitaz/boot"]
redirectors[8] = ["(.*\.)?ftp.fr.debian.org/debian","http://127.0.0.1/repositories/debian"]
redirectors[9] = ["(.*\.)?packages.linuxmint.com","http://127.0.0.1/repositories/linuxmint"]
redirectors[10] = ["(.*\.)?archive.canonical.com","http://127.0.0.1/repositories/canonical"]
redirectors[11] = ["(.*\.)?download.windowsupdate.com","IGNORE_NO"]
redirectors[12] = ["(.*\.)?http.debian.net/debian","http://127.0.0.1/repositories/debian"]
redirectors[13] = ["(.*\.)?debian.mirrors.ovh.net/debian","http://127.0.0.1/repositories/debian"]
redirectors[14] = ["(.*\.)?security.debian.org","http://127.0.0.1/repositories/debian-security"]
redirectors[15] = ["(.*\.)?ftp.uni-kl.de/debian","http://127.0.0.1/repositories/debian"]
redirectors[16] = ["(.*\.)?handylinux.org/repo/debian","http://127.0.0.1/repositories/handylinux"]
redirectors[17] = ["(.*\.)?manjarolinux.polymorf.fr","http://127.0.0.1/repositories/manjaro"]
redirectors[18] = ["(.*\.)?mirror.lignux.com/manjaro","http://127.0.0.1/repositories/manjaro"]
redirectors[19] = ["(.*\.)?debian.proxad.net/debian","http://127.0.0.1/repositories/debian"]
redirectors[20] = ['ftp\.(.*\.)?debian\.org/debian',"http://127.0.0.1/repositories/debian"]


# Definition du chemin du fichier log et de sa verbosite
LOG_FILENAME = '/var/log/squid/squid-redirector.log'




logging.basicConfig(filename=LOG_FILENAME,level=LOGLEVEL,format='%(asctime)s %(levelname)s %(message)s',datefmt='%d/%m/%Y %H:%M:%S')


logging.debug('---------------------------------------')
logging.debug('Lancement d\'thread squid-redirector.py')
logging.debug('---------------------------------------')



while True:
  # URL ip-address/fqdn ident method
  line_squid = sys.stdin.readline().strip()

  logging.info('Reception d\'une requete : ' + line_squid)

  # Recuperation de l'URL
  try:
    list = line_squid.split(" ")
    url_input = list[0]

    # Recuperation de l'origine du client
    try:
      client_input = list[1]
    except:
      logging.warning('Impossible de recuperer l\'origine du client depuis la chaine '+line_squid)
      client_input = "NC"

    i = 0
    found = 0
    ignore = 0

    while i < len(redirectors):

      try:
        # On test sur le depot correpond a ce genre d'URL
        if re.search(r''+redirectors[i][0],url_input):
          logging.debug(client_input + ' L\'url correspond au depot : ' + redirectors[i][0])

          if redirectors[i][1] == "IGNORE" :
            ignore = 1
            logging.debug(client_input + ' IGNORE')
          else :
            try:
              url_locale = re.sub(r'http://' + redirectors[i][0],redirectors[i][1],url_input)
              logging.debug(client_input + ' Verification de la presence du fichier local : ' + url_locale)
              req = urllib.request.Request(url=url_locale,method='HEAD')
              r = urllib.request.urlopen(req)
              logging.debug(r.status)
              url_output = url_locale #+ '\n'
              logging.debug(client_input + ' Ce fichier est en cache : ' + url_output + ' et sera servi.')
              found = 1
              break
            except:
              # Le fichier est introuvable sur le depot
              logging.debug(client_input + ' Cette URL n\'est telechargeable dans ce depot. Le fichier distant sera servi.')

      except:
        # L'URL ne correspond pas au depot
        logging.debug(client_input + ' Ce depot ne correspond pas a l\'URL')
      i = i + 1

    if ignore == 1 :
      print("http://10.9.0.1/null\n")
    else :
      # Tout les depots ont ete testes, aucun ne correspond
      if found == 0 :
        logging.debug(client_input + ' Aucun depot ne contient cette URL, le fichier distant sera servi.')
        print(url_input)
      else :
        logging.info(client_input + ' Ce fichier est en cache : ' + url_output + '. Le fichier local sera servi.')
        print(url_output)

  except:
    logging.error(client_input + ' Impossible de recuperer l\'URL depuis la chaine '+line_squid)

  sys.stdout.flush()

