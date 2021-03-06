#!/usr/bin/env python
# coding: utf-8

# Extraction des certificats ISCC https://www.iscc-system.org/certificates/all-certificates/
import argparse
import requests
import urllib.request
from bs4 import BeautifulSoup

import json
import pandas as pd
from datetime import date # Pour le nom du fichier sauvegardé

from os import listdir
from os.path import isfile
import shutil
import re

rootUrl = 'https://www.iscc-system.org/wp-admin/admin-ajax.php?action=get_wdtable&table_id=9'
DESTINATION_FOLDER = '/tmp/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
PAGELENGTH = 3000

def get_wdtNonce():
    html_content = requests.get('https://www.iscc-system.org/certificates/all-certificates/', headers=HEADERS).text
    soup = BeautifulSoup(html_content, "lxml")
    wdtNonceTag = soup.find("input", attrs={"name": "wdtNonceFrontendEdit_9"}).attrs
    wdtNonce = wdtNonceTag['value']
    print('wdtNonce:', wdtNonce)
    return wdtNonce

def get_certificateData(nonce, recordsTotal, test, latest):
    # On parcourt le tableau de résultats, en incrémentant de 1000 à chaque fois.
    # On stocke le tableau dans une liste de tableau
    allData = []
    start = 0
    if latest:
        start = recordsTotal - PAGELENGTH
    if test:
        recordsTotal = PAGELENGTH
    while start < recordsTotal:
        print(start)
        r = requests.post(rootUrl, data ={'length': PAGELENGTH, 'start': start, 'draw': 1, 'wdtNonce': nonce}, headers=HEADERS)
        certificates = json.loads(r.content.decode('utf-8'))
        data = pd.DataFrame.from_dict(certificates['data'])
        allData.append(data)
        start = start + PAGELENGTH
    return allData

def cleanCertificateData(data):
    allData = pd.concat(data)
    allData.columns = ['cert_status', 'certificate', 'certificate_holder', 'scope',
                       'raw_material', 'addons', 'valid_from', 'valid_until', 'issuing_cb',
                       'map', 'certificate_report', 'audit_report', "unknown_column"]

    # extraction de la balise HTML
    allData['certificate_holder'] = allData['certificate_holder'].str.replace('.*title="(.*)">.*', '\\1')
    allData['raw_material'] = allData['raw_material'].str.replace('.*title="(.*)">.*', '\\1')
    allData['issuing_cb'] = allData['issuing_cb'].str.replace('.*title="(.*)">.*', '\\1')
    allData['map'] = allData['map'].str.replace('.*href="(.*)">.*', '\\1')
    allData['certificate_report'] = allData['certificate_report'].str.replace('.*href="(.*)">.*', '\\1')
    allData['audit_report'] = allData['audit_report'].str.replace('.*href="(.*)">.*', '\\1')
    return allData

def download_certificates(args):
    # On récupère le wdtNonce du jour
    nonce = get_wdtNonce()
    
    # Nombre de requêtes
    r = requests.post(rootUrl, data ={'length': 1, 'start': 0, 'draw': 1, 'wdtNonce': nonce}, headers=HEADERS)
    recordsTotal = int(json.loads(r.content.decode('utf-8'))['recordsTotal'])
    print('# of certificates: ' + str(recordsTotal))

    # Récupération du contenu
    data = get_certificateData(nonce, recordsTotal, args.test, args.latest)
    # On retire les balises html pour ne garder que le contenu
    cleaned_data = cleanCertificateData(data)
    # Sauvegarde
    filename = "%s/Certificates_%s.csv" % (DESTINATION_FOLDER, str(date.today()))
    pd.DataFrame.to_csv(cleaned_data, filename, index=False)
    
    ## Comparaison pour extraire les doublons
    # 1) Création d'un historique
    files = [f for f in listdir(DESTINATION_FOLDER) if isfile('%s/%s' % (DESTINATION_FOLDER, f))]
    files.sort()
    certificatesFiles = [f for f in files if re.match('Certificates_[0-9]{4}-[0-9]{2}-[0-9]{2}.csv', f)]
    histoFiles = [f for f in files if re.match('History_[0-9]{4}-[0-9]{2}-[0-9]{2}.csv', f)]

    # Il n'y a pas d'historique --> le fichier crée est celui du jour. Il y a maintenant un historique
    if len(histoFiles) == 0 :
        histoFile = re.sub('Certificates', 'History', certificatesFiles[-1])
        shutil.copy('%s/%s' % (DESTINATION_FOLDER, certificatesFiles[-1]), '%s/%s' % (DESTINATION_FOLDER, histoFile))

    # 2) Ouverture et concaténation    
    files = [f for f in listdir(DESTINATION_FOLDER) if isfile('%s/%s' % (DESTINATION_FOLDER, f))]
    files.sort()
    histoFiles = [f for f in files if re.match('History_[0-9]{4}-[0-9]{2}-[0-9]{2}.csv', f)]
    histo = pd.read_csv('%s/%s' % (DESTINATION_FOLDER, histoFiles[-1]))
    histo['date']  = str(re.sub('History_([0-9]{4}-[0-9]{2}-[0-9]{2}).csv', '\\1', histoFiles[-1]))

    certificates = pd.read_csv('%s/%s' % (DESTINATION_FOLDER, certificatesFiles[-1]))
    certificates['date'] = str(re.sub('Certificates_([0-9]{4}-[0-9]{2}-[0-9]{2}).csv', '\\1', certificatesFiles[-1]))


    # On concatène l'historique et les certificats du jour
    # On regarde les certificats qui ont plusieurs dates de fin. 
    histo_and_new = pd.concat([certificates, histo])
    histo_and_new = histo_and_new.drop_duplicates(subset=histo_and_new.columns.difference(['date', 'index']))
    pd.DataFrame.to_csv(histo_and_new, '%s/History_%s.csv' % (DESTINATION_FOLDER, str(date.today())), index=False)

    # On sauve dans un fichier les potentiels doublons.
    dup = histo_and_new.drop_duplicates(['certificate','valid_until'])
    boolean = dup.duplicated(['certificate'])
    dup = dup[boolean]
    pd.DataFrame.to_csv(dup, '%s/Duplicates_%s.csv' % (DESTINATION_FOLDER, str(date.today())), index = False)

def main():
    parser = argparse.ArgumentParser(description='Delete old database backups')
    parser.add_argument('--test', dest='test', action='store_true', default=False, help='test mode')
    parser.add_argument('--latest', dest='latest', action='store_true', default=False, help='only fetch latest certificates')        
    args = parser.parse_args()
    download_certificates(args)
    


if __name__ == '__main__':
    main()
