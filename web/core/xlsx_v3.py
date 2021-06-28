import os
import django
import xlsxwriter
import datetime
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carbure.settings")
django.setup()

from core.models import MatierePremiere, Biocarburant, Pays, Depot, Entity, ProductionSite, LotTransaction
from certificates.models import EntityISCCTradingCertificate, EntityDBSTradingCertificate, EntityREDCertTradingCertificate, EntitySNTradingCertificate


UNKNOWN_PRODUCERS = [{'name': 'ITANOL', 'country': 'IT', 'production_site': 'BERGAMO', 'ref': 'ISCC-IT-100001010', 'date':'2017-12-01', 'dc':'IT_001_2020'},
                    {'name': 'ITANOL', 'country': 'IT', 'production_site': 'FIRENZE', 'ref': '', 'date':'2014-03-01', 'dc':''},
                    {'name': 'PORTUGASOIL', 'country': 'PT', 'production_site': 'LISBOA', 'ref': 'ISCC-PT-100001110', 'date':'2011-10-01', 'dc':''},
                    {'name': 'PORTUGASOIL', 'country': 'PT', 'production_site': 'PORTO', 'ref': '', 'date':'2013-07-01', 'dc':''},
                    {'name': 'BIOCATALAN', 'country': 'ES', 'production_site': 'EL MASNOU', 'ref': '', 'date':'2016-02-01', 'dc':'ES_012_2016'},
                    {'name': 'BIOCATALAN', 'country': 'ES', 'production_site': 'TARRAGONA', 'ref': 'ISCC-ES-100005010', 'date':'2019-12-01', 'dc':''},
                    {'name': 'BIOBAO', 'country': 'ES', 'production_site': 'HONDARRIBIA', 'ref': 'ISCC-ES-100004010', 'date':'2007-11-01', 'dc':'ES_011_2018'},
                    {'name': 'BONDUELLE', 'country': 'FR', 'production_site': 'TOURS', 'ref': 'ISCC-FR-100001011', 'date':'2001-01-01', 'dc':''},
                    {'name': 'BONDUELLE', 'country': 'FR', 'production_site': 'NUEIL LES AUBIERS', 'ref': '', 'date':'2004-06-01', 'dc':'FR_042_2016'},
                    {'name': 'GEANTVERT', 'country': 'FR', 'production_site': 'BRUZAC', 'ref': 'ISCC-FR-100001013', 'date':'2005-04-01', 'dc':''},
                    {'name': 'GEANTVERT', 'country': 'FR', 'production_site': 'NIMES', 'ref': '', 'date':'1997-07-01', 'dc':'FR_002_2017'},
                    {'name': '', 'country': '', 'production_site': '', 'ref': '', 'date':'2016-02-01', 'dc':'ES_012_2016'},
                    {'name': '', 'country': '', 'production_site': '', 'ref': '', 'date':'2019-12-01', 'dc':''},
                    {'name': '', 'country': '', 'production_site': '', 'ref': '', 'date':'2007-11-01', 'dc':'ES_011_2018'},
                    {'name': '', 'country': '', 'production_site': '', 'ref': 'ISCC-FR-100001011', 'date':'2001-01-01', 'dc':''},
                    {'name': '', 'country': '', 'production_site': '', 'ref': '', 'date':'2004-06-01', 'dc':'FR_042_2016'},
                    {'name': '', 'country': '', 'production_site': '', 'ref': '', 'date':'2005-04-01', 'dc':''},
                    {'name': '', 'country': '', 'production_site': '', 'ref': 'ISCC-FR-100001014', 'date':'1997-07-01', 'dc':'FR_002_2017'},
                    ]

FOREIGN_CLIENTS = [{'name': 'BP', 'country': 'GB', 'delivery_site': 'DOVER'},
                    {'name': 'BP', 'country': 'GB', 'delivery_site': 'LIVERPOOL'},
                    {'name': 'BP', 'country': 'GB', 'delivery_site': 'MANCHESTER'},
                    {'name': 'EXXON', 'country': 'US', 'delivery_site': 'BOSTON'},
                    {'name': 'EXXON', 'country': 'US', 'delivery_site': 'HOBOKEN'},
                    {'name': 'IBERDROLA', 'country': 'ES', 'delivery_site': 'BCN'},
                    {'name': 'IBERDROLA', 'country': 'ES', 'delivery_site': 'BILBAO'},
                    ]


SUPPLIERS = [{'name': 'LUR BERRI', 'sref': 'ISCC-FR-200000042'}, 
    {'name': 'ITANOL', 'sref': 'ISCC-IT-200000014'},
    {'name': 'FINNHUB', 'sref': 'ISCC-FI-200000078'},
    {'name': 'DEUTSCHE BIOFUELS GMBH', 'sref': 'ISCC-DE-200000001'},
    {'name': 'NL OIL ', 'sref': 'ISCC-NL-200000001'},
    {'name':'', 'sref': 'ISCC-DE-200000002'},
    {'name':'', 'sref': 'ISCC-BE-200000001'},
    {'name':'', 'sref': 'ISCC-ES-200000001'},
    {'name':'', 'sref': 'ISCC-NL-200000002'},
]

def get_random_dae():
    today = datetime.date.today()
    return 'TEST%dFR0000%d' % (today.year, random.randint(100000, 900000))

def get_my_certificates(entity=None):
    # certificates
    iscc_certificates = EntityISCCTradingCertificate.objects.all()
    dbs_certificates = EntityDBSTradingCertificate.objects.all()
    redcert_certificates = EntityREDCertTradingCertificate.objects.all()
    sn_certificates = EntitySNTradingCertificate.objects.all()

    if entity is not None:
        iscc_certificates = iscc_certificates.filter(entity=entity)[10:]
        dbs_certificates = dbs_certificates.filter(entity=entity)[10:]
        redcert_certificates = redcert_certificates.filter(entity=entity)[10:]
        sn_certificates = sn_certificates.filter(entity=entity)[10:]

    certs = [c.certificate.certificate_id for c in iscc_certificates]
    certs += [c.certificate.certificate_id for c in dbs_certificates]
    certs += [c.certificate.certificate_id for c in redcert_certificates]
    certs += [c.certificate.certificate_id for c in sn_certificates]

    if len(certs) == 0:
        certs.append('No certificates found')
    return certs

def make_producers_or_traders_lots_sheet_advanced(workbook, entity, nb_lots, is_producer=True):
    worksheet_lots = workbook.add_worksheet("lots")
    psites = ProductionSite.objects.filter(producer=entity)
    clients = Entity.objects.filter(entity_type__in=['Opérateur', 'Trader']).exclude(id=entity.id)
    mps = MatierePremiere.objects.all()
    bcs = Biocarburant.objects.all()
    delivery_sites = Depot.objects.all()
    countries = Pays.objects.all()

    my_vendor_certificates = get_my_certificates(entity=entity)

    # header
    bold = workbook.add_format({'bold': True})
    columns = ['producer', 'production_site', 'production_site_country', 'production_site_reference',
               'production_site_commissioning_date', 'double_counting_registration',
               'supplier', 'supplier_certificate', 'vendor_certificate',
               'volume', 'biocarburant_code', 'matiere_premiere_code', 'pays_origine_code',
               'eec', 'el', 'ep', 'etd', 'eu', 'esca', 'eccs', 'eccr', 'eee',
               'dae', 'champ_libre', 'client', 'delivery_date', 'delivery_site', 'delivery_site_country']
    if entity.has_mac:
        columns.append('mac')
    for i, c in enumerate(columns):
        worksheet_lots.write(0, i, c, bold)

    # rows
    clientid = 'import_batch_%s' % (datetime.date.today().strftime('%Y%m%d'))
    today = datetime.date.today().strftime('%d/%m/%Y')
    for i in range(nb_lots):
        client = random.choice(clients)
        bc = random.choice(bcs)
        my_vendor_certificate = random.choice(my_vendor_certificates)
        if bc.is_alcool:
            mp = random.choice([mp for mp in mps if mp.compatible_alcool])
        elif bc.is_graisse:
            mp = random.choice([mp for mp in mps if mp.compatible_graisse])
        else:
            mp = random.choice(mps)

        country = random.choice(countries)
        site = random.choice(delivery_sites)
        volume = random.randint(34000, 36000)

        is_imported = random.random() < 0.3
        if not is_producer:
            is_imported = True
        supplier_is_not_the_producer = random.random() < 0.5
        destination = random.choice([1, 0, -1])

        row = []
        # production site
        if is_imported:
            p = random.choice(UNKNOWN_PRODUCERS)
            row += [p['name'], p['production_site'], p['country'], p['ref'], p['date'], p['dc'] if mp.is_double_compte else '']
            if supplier_is_not_the_producer:
                supplier = random.choice(SUPPLIERS)
                row += [supplier['name'], supplier['sref']]
            else:
                row += [p['name'], p['ref']]
        else:
            if not len(psites):
                continue
            p = random.choice(psites)
            production_certifs = p.productionsitecertificate_set.all()
            if production_certifs.count() > 0:
                production_certif = production_certifs[0].natural_key()['certificate_id']
            else:
                production_certif = ''
            row += [p.producer.name, p.name, p.country.code_pays, production_certif, '', '', '', '']

        # vendor (me)
        row += [my_vendor_certificate]
        # lot details
        row += [volume, bc.code, mp.code, country.code_pays, random.randint(8, 13), random.randint(2, 5), random.randint(1, 3), random.randint(1, 2), float(random.randint(5, 30)) / 10.0, 0, 0, 0, 0, get_random_dae(), clientid]
        if destination == 1:
            # client is not in carbure
            c = random.choice(FOREIGN_CLIENTS)
            row += [c['name'], today, c['delivery_site'], c['country']]
        elif destination == -1:
            # into mass balance (i am the client)
            row += ['', today, site.depot_id, 'FR']
        else:
            # regular transaction. sell to someone else
            row += [client.name, today, site.depot_id, 'FR']

        if entity.has_mac:
            row += [0]

        colid = 0
        for elem in row:
            worksheet_lots.write(i+1, colid, elem)
            colid += 1


def make_mb_extract_sheet(workbook, entity):
    worksheet_lots = workbook.add_worksheet("lots")
    clients = Entity.objects.filter(entity_type__in=['Opérateur', 'Producteur', 'Trader']).exclude(id=entity.id)
    delivery_sites = Depot.objects.all()
    mb_lots = LotTransaction.objects.filter(carbure_client=entity, delivery_status='A', lot__status="Validated", lot__fused_with=None)

    # 4/10 chances of having an exported lot
    exported_lots = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    # header
    bold = workbook.add_format({'bold': True})
    columns = ['carbure_id', 'volume', 'dae', 'champ_libre', 'client', 'delivery_date', 'delivery_site', 'delivery_site_country']
    for i, c in enumerate(columns):
        worksheet_lots.write(0, i, c, bold)

    clientid = 'import_batch_%s' % (datetime.date.today().strftime('%Y%m%d'))
    today = datetime.date.today().strftime('%Y-%m-%d')
    if not len(mb_lots):
        return
    for i in range(10):
        client = random.choice(clients)
        site = random.choice(delivery_sites)
        exported = random.choice(exported_lots)
        lot_source = random.choice(mb_lots)

        row = [lot_source.lot.carbure_id, int(lot_source.lot.volume / 2), get_random_dae(), clientid]
        if exported == 1:
            # client is not in carbure
            c = random.choice(FOREIGN_CLIENTS)
            row += [c['name'], today, c['delivery_site'], c['country']]
        else:
            # regular transaction. sell to someone else
            row += [client.name, today, site.depot_id, '']

        colid = 0
        for elem in row:
            worksheet_lots.write(i+1, colid, elem)
            colid += 1


def make_mb_extract_sheet_bcghg(workbook, entity):
    worksheet_lots = workbook.add_worksheet("lots")
    clients = Entity.objects.filter(entity_type__in=['Opérateur', 'Producteur', 'Trader']).exclude(id=entity.id)
    delivery_sites = Depot.objects.all()
    mb_lots = LotTransaction.objects.filter(carbure_client=entity, delivery_status='A', lot__status="Validated", lot__fused_with=None)

    # 4/10 chances of having an exported lot
    exported_lots = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    # header
    bold = workbook.add_format({'bold': True})
    columns = ['biocarburant_code', 'matiere_premiere_code', 'ghg_total', 'depot', 'volume', 'dae', 'champ_libre', 'client', 'delivery_date', 'delivery_site', 'delivery_site_country']
    for i, c in enumerate(columns):
        worksheet_lots.write(0, i, c, bold)

    clientid = 'import_batch_%s' % (datetime.date.today().strftime('%Y%m%d'))
    today = datetime.date.today().strftime('%d/%m/%Y')
    if not len(mb_lots):
        return
    for i in range(10):
        client = random.choice(clients)
        site = random.choice(delivery_sites)
        exported = random.choice(exported_lots)
        lot_source = random.choice(mb_lots)

        row = [lot_source.lot.biocarburant.code, lot_source.lot.matiere_premiere.code, lot_source.lot.ghg_total, 
               lot_source.carbure_delivery_site.depot_id if lot_source.delivery_site_is_in_carbure else lot_source.unknown_delivery_site, 
               int(lot_source.lot.volume / 2), get_random_dae(), clientid]
        if exported == 1:
            # client is not in carbure
            c = random.choice(FOREIGN_CLIENTS)
            row += [c['name'], today, c['delivery_site'], c['country']]
        else:
            # regular transaction. sell to someone else
            row += [client.name, today, site.depot_id, '']

        colid = 0
        for elem in row:
            worksheet_lots.write(i+1, colid, elem)
            colid += 1



def make_producers_lots_sheet_simple(workbook, entity):
    worksheet_lots = workbook.add_worksheet("lots")
    psites = ProductionSite.objects.filter(producer=entity)
    clients = Entity.objects.filter(entity_type__in=['Opérateur', 'Trader'])
    mps = MatierePremiere.objects.all()
    bcs = Biocarburant.objects.all()
    delivery_sites = Depot.objects.all()
    countries = Pays.objects.all()

    my_vendor_certificates = get_my_certificates(entity=entity)

    # header
    bold = workbook.add_format({'bold': True})
    columns = ['production_site', 'volume', 'biocarburant_code', 'matiere_premiere_code', 'pays_origine_code',
               'production_site_reference', 'vendor_certificate',
               'eec', 'el', 'ep', 'etd', 'eu', 'esca', 'eccs', 'eccr', 'eee',
               'dae', 'champ_libre', 'client', 'delivery_date', 'delivery_site']
    if entity.has_mac:
        columns.append('mac')               
    for i, c in enumerate(columns):
        worksheet_lots.write(0, i, c, bold)

    clientid = 'import_batch_%s' % (datetime.date.today().strftime('%Y%m%d'))
    today = datetime.date.today().strftime('%d/%m/%Y')

    if not len(psites):
        return

    for i in range(10):
        client = random.choice(clients)
        bc = random.choice(bcs)
        my_vendor_certificate = random.choice(my_vendor_certificates)

        if bc.is_alcool:
            mp = random.choice([mp for mp in mps if mp.compatible_alcool])
        elif bc.is_graisse:
            mp = random.choice([mp for mp in mps if mp.compatible_graisse])
        else:
            mp = random.choice(mps)

        country = random.choice(countries)
        site = random.choice(delivery_sites)
        volume = random.randint(34000, 36000)

        p = random.choice(psites)

        production_certifs = p.productionsitecertificate_set.all()
        if production_certifs.count() > 0:
            production_certif = production_certifs[0].natural_key()['certificate_id']
        else:
            production_certif = ''

        row = [p.name, volume, bc.code, mp.code, country.code_pays, production_certif, my_vendor_certificate, random.randint(8, 13), random.randint(2, 5), random.randint(1, 3), random.randint(1, 2), float(random.randint(5, 30)) / 10.0, 0, 0, 0, 0, get_random_dae(), clientid]
        row += [client.name, today, site.depot_id]

        if entity.has_mac:
            row += [0]

        colid = 0
        for elem in row:
            worksheet_lots.write(i+1, colid, elem)
            colid += 1


def make_operators_lots_sheet(workbook, entity):
    worksheet_lots = workbook.add_worksheet("lots")
    mps = MatierePremiere.objects.all()
    bcs = Biocarburant.objects.all()
    delivery_sites = Depot.objects.all()
    countries = Pays.objects.all()

    # header
    bold = workbook.add_format({'bold': True})
    # difference with producer/trader: no 'client' column and no 'vendor_certificate' column
    columns = ['producer', 'production_site', 'production_site_country', 'production_site_reference',
               'production_site_commissioning_date', 'double_counting_registration',
               'supplier', 'supplier_certificate',
               'volume', 'biocarburant_code', 'matiere_premiere_code', 'pays_origine_code',
               'eec', 'el', 'ep', 'etd', 'eu', 'esca', 'eccs', 'eccr', 'eee',
               'dae', 'champ_libre', 'delivery_date', 'delivery_site', 'delivery_site_country']

    for i, c in enumerate(columns):
        worksheet_lots.write(0, i, c, bold)

    # rows
    clientid = 'import_batch_%s' % (datetime.date.today().strftime('%Y%m%d'))
    today = datetime.date.today().strftime('%Y-%m-%d')
    for i in range(10):
        bc = random.choice(bcs)
        if bc.is_alcool:
            mp = random.choice([mp for mp in mps if mp.compatible_alcool])
        elif bc.is_graisse:
            mp = random.choice([mp for mp in mps if mp.compatible_graisse])
        else:
            mp = random.choice(mps)
        country = random.choice(countries)
        site = random.choice(delivery_sites)
        volume = random.randint(34000, 36000)
        row = []
        # producer
        p = random.choice(UNKNOWN_PRODUCERS)
        row += [p['name'], p['production_site'], p['country'], p['ref'], p['date'], p['dc'] if mp.is_double_compte else '']
        # supplier
        supplier_is_not_the_producer = random.random() < 0.5
        if supplier_is_not_the_producer:
            supplier = random.choice(SUPPLIERS)
            row += [supplier['name'], supplier['sref']]
        else:
            row += [p['name'], p['ref']]
        # lot
        row += [volume, bc.code, mp.code, country.code_pays, random.randint(8, 13), random.randint(2, 5), random.randint(1, 3), random.randint(1, 2), float(random.randint(5, 30)) / 10.0, 0, 0, 0, 0, get_random_dae(), clientid]
        row += [today, site.depot_id, site.country.code_pays]
        colid = 0
        for elem in row:
            worksheet_lots.write(i+1, colid, elem)
            colid += 1


def make_mps_sheet(workbook):
    worksheet_mps = workbook.add_worksheet("MatieresPremieres")
    mps = MatierePremiere.objects.all()
    # header
    bold = workbook.add_format({'bold': True})
    worksheet_mps.write('A1', 'code', bold)
    worksheet_mps.write('B1', 'name', bold)
    worksheet_mps.write('C1', 'category', bold)
    # content
    row = 1
    for m in mps:
        worksheet_mps.write(row, 0, m.code)
        worksheet_mps.write(row, 1, m.name)
        worksheet_mps.write(row, 2, m.category)
        row += 1


def make_biofuels_sheet(workbook):
    worksheet_biocarburants = workbook.add_worksheet("Biocarburants")
    biocarburants = Biocarburant.objects.all()
    # header
    bold = workbook.add_format({'bold': True})
    worksheet_biocarburants.write('A1', 'code', bold)
    worksheet_biocarburants.write('B1', 'name', bold)
    # content
    row = 1
    for b in biocarburants:
        worksheet_biocarburants.write(row, 0, b.code)
        worksheet_biocarburants.write(row, 1, b.name)
        row += 1


def make_countries_sheet(workbook):
    worksheet_pays = workbook.add_worksheet("Pays")
    pays = Pays.objects.all()
    # header
    bold = workbook.add_format({'bold': True})
    worksheet_pays.write('A1', 'code', bold)
    worksheet_pays.write('B1', 'name', bold)
    # content
    row = 1
    for p in pays:
        worksheet_pays.write(row, 0, p.code_pays)
        worksheet_pays.write(row, 1, p.name)
        row += 1


def make_clients_sheet(workbook):
    worksheet_operateurs = workbook.add_worksheet("Societes")
    operators = Entity.objects.filter(entity_type__in=['Opérateur', 'Producteur', 'Trader']).order_by('name')
    # header
    bold = workbook.add_format({'bold': True})
    worksheet_operateurs.write('A1', 'name', bold)
    # content
    row = 1
    for o in operators:
        worksheet_operateurs.write(row, 0, o.name)
        row += 1


def make_deliverysites_sheet(workbook):
    worksheet_sites = workbook.add_worksheet("SitesDeLivraison")
    depots = Depot.objects.all().order_by('country', 'id')
    # header
    bold = workbook.add_format({'bold': True})
    worksheet_sites.write('A1', 'code', bold)
    worksheet_sites.write('B1', 'name', bold)
    worksheet_sites.write('C1', 'city', bold)
    # content
    row = 1
    for d in depots:
        worksheet_sites.write(row, 0, d.depot_id)
        worksheet_sites.write(row, 1, d.name)
        worksheet_sites.write(row, 2, d.city)
        row += 1


def template_producers_simple(entity):
    # Create an new Excel file and add a worksheet.
    location = '/tmp/carbure_template_simple.xlsx'
    workbook = xlsxwriter.Workbook(location)
    make_producers_lots_sheet_simple(workbook, entity)
    make_mps_sheet(workbook)
    make_biofuels_sheet(workbook)
    make_countries_sheet(workbook)
    make_clients_sheet(workbook)
    make_deliverysites_sheet(workbook)
    workbook.close()
    return location


def template_producers_advanced(entity, nb_lots=10):
    # Create an new Excel file and add a worksheet.
    location = '/tmp/carbure_template_advanced.xlsx'
    workbook = xlsxwriter.Workbook(location)
    make_producers_or_traders_lots_sheet_advanced(workbook, entity, nb_lots, is_producer=True)
    make_mps_sheet(workbook)
    make_biofuels_sheet(workbook)
    make_countries_sheet(workbook)
    make_clients_sheet(workbook)
    make_deliverysites_sheet(workbook)
    workbook.close()
    return location


def template_operators(entity):
    # Create an new Excel file and add a worksheet.
    location = '/tmp/carbure_template_operators.xlsx'
    workbook = xlsxwriter.Workbook(location)
    make_operators_lots_sheet(workbook, entity)
    make_mps_sheet(workbook)
    make_biofuels_sheet(workbook)
    make_countries_sheet(workbook)
    make_deliverysites_sheet(workbook)
    workbook.close()
    return location


def template_traders(entity):
    # Create an new Excel file and add a worksheet.
    location = '/tmp/carbure_template_traders.xlsx'
    workbook = xlsxwriter.Workbook(location)
    make_producers_or_traders_lots_sheet_advanced(workbook, entity, nb_lots=10, is_producer=False)
    make_mps_sheet(workbook)
    make_biofuels_sheet(workbook)
    make_countries_sheet(workbook)
    make_clients_sheet(workbook)
    make_deliverysites_sheet(workbook)
    workbook.close()
    return location


def template_stock(entity):
    # Create an new Excel file and add a worksheet.
    location = '/tmp/carbure_template_mb.xlsx'
    workbook = xlsxwriter.Workbook(location)
    make_mb_extract_sheet(workbook, entity)
    make_countries_sheet(workbook)
    make_clients_sheet(workbook)
    make_deliverysites_sheet(workbook)
    workbook.close()
    return location


def template_stock_bcghg(entity):
    # create a list of lots to send from stock
    # but instead of using carbure_id as a key, we'll use the biofuel and its sustainability characteristics (ghg)
    # why ?
    # because users are more likely to know the details of what they're sending than the carbure id
    # Knowing CarbureID forces them to download their stock from carbure  
    location = '/tmp/carbure_template_mb.xlsx'
    workbook = xlsxwriter.Workbook(location)
    make_mb_extract_sheet_bcghg(workbook, entity)
    make_countries_sheet(workbook)
    make_clients_sheet(workbook)
    make_deliverysites_sheet(workbook)
    workbook.close()
    return location


# API V3
def make_dump_lots_sheet(workbook, entity, transactions):
    worksheet_lots = workbook.add_worksheet("lots")
    # header
    bold = workbook.add_format({'bold': True})
    columns = ['carbure_id', 'producer', 'production_site', 'production_site_country', 'production_site_reference',
               'production_site_commissioning_date', 'double_counting_registration', 'supplier', 'supplier_certificate',
               'volume', 'biocarburant_code', 'matiere_premiere_code', 'categorie_matiere_premiere', 'pays_origine_code',
               'eec', 'el', 'ep', 'etd', 'eu', 'esca', 'eccs', 'eccr', 'eee', 'ghg_total',
               'dae', 'champ_libre', 'client', 'delivery_date', 'delivery_site', 'delivery_site_country', 'delivery_site_name']
    if entity is not None and entity.has_mac:
        columns.append('mac')
    for i, c in enumerate(columns):
        worksheet_lots.write(0, i, c, bold)

    for i, tx in enumerate(transactions):
        lot = tx.lot
        com_date = ''
        if lot.carbure_production_site:
            com_date = lot.carbure_production_site.date_mise_en_service.strftime('%d/%m/%Y') 
        elif lot.unknown_production_site_com_date:
            com_date = lot.unknown_production_site_com_date.strftime('%d/%m/%Y')
        else:
            com_date = ''
        row = [lot.carbure_id,
               lot.carbure_producer.name if lot.carbure_producer else lot.unknown_producer,
               lot.carbure_production_site.name if lot.carbure_production_site else lot.unknown_production_site,
               lot.carbure_production_site.country.code_pays if lot.carbure_production_site and lot.carbure_production_site.country else lot.unknown_production_country.code_pays if lot.unknown_production_country else '',
               lot.carbure_production_site_reference if lot.carbure_production_site else lot.unknown_production_site_reference, 
               com_date,
               lot.carbure_production_site.dc_reference if lot.carbure_production_site and lot.matiere_premiere.is_double_compte else lot.unknown_production_site_dbl_counting,
               tx.carbure_vendor.name if tx.carbure_vendor else tx.lot.unknown_supplier,
               tx.carbure_vendor_certificate if tx.carbure_vendor else tx.lot.unknown_supplier_certificate,
               lot.volume, lot.biocarburant.code if lot.biocarburant else '',
               lot.matiere_premiere.code if lot.matiere_premiere else '',
               lot.matiere_premiere.category if lot.matiere_premiere else '',
               lot.pays_origine.code_pays if lot.pays_origine else '',
               lot.eec, lot.el, lot.ep, lot.etd, lot.eu, lot.esca, lot.eccs, lot.eccr, lot.eee, lot.ghg_total,
               tx.dae, tx.champ_libre, tx.carbure_client.name if tx.client_is_in_carbure and tx.carbure_client else tx.unknown_client, 
               tx.delivery_date.strftime('%d/%m/%Y') if tx.delivery_date else '',
               tx.carbure_delivery_site.depot_id if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site,
               tx.carbure_delivery_site.country.code_pays if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site_country.code_pays if tx.unknown_delivery_site_country else '',
               tx.carbure_delivery_site.name if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site,
               ]
        if entity is not None and entity.has_mac:
            row += [tx.is_mac]

        colid = 0
        for elem in row:
            worksheet_lots.write(i+1, colid, elem)
            colid += 1


def make_dump_stocks_sheet(workbook, entity, transactions):
    worksheet_lots = workbook.add_worksheet("lots")
    # header
    bold = workbook.add_format({'bold': True})
    columns = ['carbure_id', 'producer', 'production_site', 'production_site_country', 'production_site_reference',
               'production_site_commissioning_date', 'double_counting_registration',
               'volume', 'biocarburant_code', 'matiere_premiere_code', 'pays_origine_code',
               'eec', 'el', 'ep', 'etd', 'eu', 'esca', 'eccs', 'eccr', 'eee', 'ghg_total',
               'dae', 'champ_libre', 'delivery_date', 'delivery_site', 'delivery_site_country']
    for i, c in enumerate(columns):
        worksheet_lots.write(0, i, c, bold)

    for i, tx in enumerate(transactions):
        lot = tx.lot
        row = [lot.carbure_id,
               lot.carbure_producer.name if lot.carbure_producer else lot.unknown_producer,
               lot.carbure_production_site.name if lot.carbure_production_site else lot.unknown_production_site,
               lot.carbure_production_site.country.code_pays if lot.carbure_production_site and lot.carbure_production_site.country else lot.unknown_production_country.code_pays if lot.unknown_production_country else '',
               lot.unknown_production_site_reference, 
               lot.unknown_production_site_com_date.strftime('%d/%m/%Y') if lot.unknown_production_site_com_date else '',
               lot.unknown_production_site_dbl_counting,
               lot.volume, lot.biocarburant.code if lot.biocarburant else '',
               lot.matiere_premiere.code if lot.matiere_premiere else '',
               lot.pays_origine.code_pays if lot.pays_origine else '',
               lot.eec, lot.el, lot.ep, lot.etd, lot.eu, lot.esca, lot.eccs, lot.eccr, lot.eee, lot.ghg_total,
               tx.dae, tx.champ_libre, 
               tx.delivery_date.strftime('%d/%m/%Y') if tx.delivery_date else '',
               tx.carbure_delivery_site.depot_id if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site,
               tx.carbure_delivery_site.country.code_pays if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site_country.code_pays if tx.unknown_delivery_site_country else ''
               ]

        colid = 0
        for elem in row:
            worksheet_lots.write(i+1, colid, elem)
            colid += 1


def export_transactions(entity, transactions):
    today = datetime.date.today()
    location = '/tmp/carbure_export_%s.xlsx' % (today.strftime('%Y%m%d_%H%M'))
    workbook = xlsxwriter.Workbook(location)
    make_dump_lots_sheet(workbook, entity, transactions)
    make_countries_sheet(workbook)
    make_mps_sheet(workbook)
    make_biofuels_sheet(workbook)
    make_clients_sheet(workbook)
    make_deliverysites_sheet(workbook)
    workbook.close()
    return location


def export_stocks(entity, transactions):
    today = datetime.date.today()
    location = '/tmp/carbure_stock_export_%s.xlsx' % (today.strftime('%Y%m%d_%H%M'))
    workbook = xlsxwriter.Workbook(location)
    make_dump_stocks_sheet(workbook, entity, transactions)
    make_countries_sheet(workbook)
    make_mps_sheet(workbook)
    make_biofuels_sheet(workbook)
    make_clients_sheet(workbook)
    make_deliverysites_sheet(workbook)
    workbook.close()
    return location
