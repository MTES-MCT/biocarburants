import random
import openpyxl
import datetime
import io

from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min
from django.core import serializers

from core.decorators import enrich_with_user_details, restrict_to_traders
from core.xlsx_template import create_template_xlsx_v2_traders

from core.models import Entity, Pays, Biocarburant, MatierePremiere, Depot
from core.models import LotV2, LotTransaction, TransactionError, LotV2Error, TransactionComment


def get_random(model):
    max_id = model.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        element = model.objects.filter(pk=pk).first()
        if element:
            return element


# not an API call. helper function
def load_excel_lot(context, lot_row):
    entity = context['user_entity']
    lot = LotV2()
    lot.added_by = entity
    if 'producer' in lot_row and lot_row['producer'] is not None:
        # this should be a bought or imported lot
        # check if we know the producer
        # producer_is_in_carbure = models.BooleanField(default=True)
        # carbure_producer = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.SET_NULL, related_name='producer_lotv2')
        # unknown_producer = models.CharField(max_length=64, blank=True, default='')
        match = Entity.objects.filter(name=lot_row['producer']).count()
        if match > 0:
            raise Exception("Vous ne pouvez pas déclarer des lots d'un producteur déjà inscrit sur Carbure")
        else:
            # ok, unknown producer. allow importation
            lot.producer_is_in_carbure = False
            lot.carbure_producer = None
            lot.unknown_producer = lot_row['producer']
    else:
        # default, current entity is the producer
        lot.producer_is_in_carbure = False
        lot.carbure_producer = None
        lot.unknown_producer = ''
    lot.save()

    if 'production_site' in lot_row:
        production_site = lot_row['production_site']
        lot.production_site_is_in_carbure = False
        lot.carbure_production_site = None
        if production_site is not None:
            lot.unknown_production_site = production_site
        else:
            lot.unknown_production_site = ''
    else:
        lot.production_site_is_in_carbure = False
        lot.carbure_production_site = None
        lot.unknown_production_site = ''

    if 'production_site_country' in lot_row:
        production_site_country = lot_row['production_site_country']
        lot.production_site_country = production_site_country
    else:
        lot.production_site_country = None

    if 'biocarburant_code' in lot_row:
        biocarburant = lot_row['biocarburant_code']
        try:
            lot.biocarburant = Biocarburant.objects.get(code=biocarburant)
            LotV2Error.objects.filter(lot=lot, field='biocarburant_code').delete()
        except Exception as e:
            print('Exception fetching biocarburant named %s: %s' % (biocarburant, e))
            lot.biocarburant = None
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='biocarburant_code',
                                                           error='Biocarburant inconnu',
                                                           defaults={'value': biocarburant})
    else:
        biocarburant = None
        lot.biocarburant = None
        error, c = LotV2Error.objects.update_or_create(lot=lot, field='biocarburant_code',
                                                       error='Merci de préciser le Biocarburant',
                                                       defaults={'value': biocarburant})
    if 'matiere_premiere_code' in lot_row:
        matiere_premiere = lot_row['matiere_premiere_code']
        try:
            lot.matiere_premiere = MatierePremiere.objects.get(code=matiere_premiere)
            LotV2Error.objects.filter(lot=lot, field='matiere_premiere_code').delete()
        except Exception:
            lot.matiere_premiere = None
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='matiere_premiere_code',
                                                           error='Matière Première inconnue',
                                                           defaults={'value': matiere_premiere})
    else:
        matiere_premiere = None
        lot.matiere_premiere = None
        error, c = LotV2Error.objects.update_or_create(lot=lot, field='matiere_premiere_code',
                                                       error='Merci de préciser la matière première',
                                                       defaults={'value': matiere_premiere})

    if 'volume' in lot_row:
        volume = lot_row['volume']
        try:
            lot.volume = float(volume)
            LotV2Error.objects.filter(lot=lot, field='volume').delete()
        except Exception:
            lot.volume = 0
            e, c = LotV2Error.objects.update_or_create(lot=lot, field='volume',
                                                       error='Format du volume incorrect', defaults={'value': volume})
    else:
        e, c = LotV2Error.objects.update_or_create(lot=lot, field='volume',
                                                   error='Merci de préciser un volume', defaults={'value': volume})

    if 'pays_origine_code' in lot_row:
        pays_origine = lot_row['pays_origine_code']
        try:
            lot.pays_origine = Pays.objects.get(code_pays=pays_origine)
            LotV2Error.objects.filter(lot=lot, field='pays_origine_code').delete()
        except Exception:
            lot.pays_origine = None
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='pays_origine_code',
                                                           error='Pays inconnu',
                                                           defaults={'value': pays_origine})
    else:
        pays_origine = None
        lot.pays_origine = None
        error, c = LotV2Error.objects.update_or_create(lot=lot, field='pays_origine_code',
                                                       error='Merci de préciser le pays',
                                                       defaults={'value': pays_origine})
    lot.eec = 0
    if 'eec' in lot_row:
        eec = lot_row['eec']
        try:
            lot.eec = float(eec)
        except:
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='eec',
                                                           error='Format non reconnu',
                                                           defaults={'value': eec})
    lot.el = 0
    if 'el' in lot_row:
        el = lot_row['el']
        try:
            lot.el = float(el)
        except:
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='el',
                                                           error='Format non reconnu',
                                                           defaults={'value': el})
    lot.ep = 0
    if 'ep' in lot_row:
        ep = lot_row['ep']
        try:
            lot.ep = float(ep)
        except:
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='ep',
                                                           error='Format non reconnu',
                                                           defaults={'value': ep})
    lot.etd = 0
    if 'etd' in lot_row:
        etd = lot_row['etd']
        try:
            lot.etd = float(etd)
        except:
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='etd',
                                                           error='Format non reconnu',
                                                           defaults={'value': etd})
    lot.eu = 0
    if 'eu' in lot_row:
        eu = lot_row['eu']
        try:
            lot.eu = float(eu)
        except:
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='eu',
                                                           error='Format non reconnu',
                                                           defaults={'value': eu})
    lot.esca = 0
    if 'esca' in lot_row:
        esca = lot_row['esca']
        try:
            lot.esca = float(esca)
        except:
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='esca',
                                                           error='Format non reconnu',
                                                           defaults={'value': esca})
    lot.eccs = 0
    if 'eccs' in lot_row:
        eccs = lot_row['eccs']
        try:
            lot.eccs = float(eccs)
        except:
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='eccs',
                                                           error='Format non reconnu',
                                                           defaults={'value': eccs})
    lot.eccr = 0
    if 'eccr' in lot_row:
        eccr = lot_row['eccr']
        try:
            lot.eccr = float(eccr)
        except:
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='eccr',
                                                           error='Format non reconnu',
                                                           defaults={'value': eccr})
    lot.eee = 0
    if 'eee' in lot_row:
        eee = lot_row['eee']
        try:
            lot.eee = float(eee)
        except:
            error, c = LotV2Error.objects.update_or_create(lot=lot, field='eee',
                                                           error='Format non reconnu',
                                                           defaults={'value': eee})
    # calculs ghg
    lot.ghg_total = round(lot.eec + lot.el + lot.ep + lot.etd + lot.eu - lot.esca - lot.eccs - lot.eccr - lot.eee, 2)
    lot.ghg_reference = 83.8
    lot.ghg_reduction = round((1.0 - (lot.ghg_total / lot.ghg_reference)) * 100.0, 2)
    lot.source = 'EXCEL'
    lot.save()

    transaction = LotTransaction()
    transaction.lot = lot
    transaction.save()
    transaction.vendor_is_in_carbure = False
    transaction.carbure_vendor = None
    if 'vendor' in lot_row:
        vendor = lot_row['vendor']
        transaction.unknown_vendor = vendor
    else:
        transaction.unknown_vendor = None
    transaction.client_is_in_carbure = True
    transaction.carbure_client = entity
    transaction.unknown_client = ''

    if 'dae' in lot_row:
        dae = lot_row['dae']
        if dae is not None:
            transaction.dae = dae
            TransactionError.objects.filter(tx=transaction, field='dae').delete()
        else:
            e, c = TransactionError.objects.update_or_create(tx=transaction, field='dae', error="Merci de préciser le numéro de DAE/DAU",
                                                             defaults={'value': dae})
    else:
        e, c = TransactionError.objects.update_or_create(tx=transaction, field='dae', error="Merci de préciser le numéro de DAE/DAU",
                                                         defaults={'value': None})

    if 'delivery_date' not in lot_row or lot_row['delivery_date'] == '':
        transaction.delivery_date = None
        lot.period = ''
        e, c = TransactionError.objects.update_or_create(tx=transaction, field='delivery_date',
                                                         error="Merci de préciser la date de livraison",
                                                         defaults={'value': None})
    else:
        try:
            delivery_date = lot_row['delivery_date']
            year = int(delivery_date[0:4])
            month = int(delivery_date[5:7])
            day = int(delivery_date[8:10])
            dd = datetime.date(year=year, month=month, day=day)
            transaction.delivery_date = dd
            lot.period = dd.strftime('%Y-%m')
            TransactionError.objects.filter(tx=transaction, field='delivery_date').delete()
        except Exception:
            msg = "Format de date incorrect: veuillez entrer une date au format AAAA-MM-JJ"
            e, c = TransactionError.objects.update_or_create(tx=transaction, field='delivery_date',
                                                             error=msg,
                                                             defaults={'value': delivery_date})

    if 'delivery_site' in lot_row and lot_row['delivery_site'] is not None:
        delivery_site = lot_row['delivery_site']
        matches = Depot.objects.filter(depot_id=delivery_site).count()
        if matches:
            transaction.delivery_site_is_in_carbure = True
            transaction.carbure_delivery_site = Depot.objects.get(depot_id=delivery_site)
            transaction.unknown_client = ''
        else:
            transaction.delivery_site_is_in_carbure = False
            transaction.carbure_delivery_site = None
            transaction.unknown_delivery_site = delivery_site
        TransactionError.objects.filter(tx=transaction, field='delivery_site').delete()
    else:
        transaction.delivery_site_is_in_carbure = False
        transaction.carbure_delivery_site = None
        transaction.unknown_delivery_site = ''
        e, c = TransactionError.objects.update_or_create(tx=transaction, field='delivery_site',
                                                         defaults={'value': None, 'error': "Merci de préciser un site de livraison"})

    if transaction.delivery_site_is_in_carbure is False:
        if 'delivery_site_country' in lot_row:
            try:
                country = Pays.objects.get(code_pays=lot_row['delivery_site_country'])
                transaction.unknown_delivery_site_country = country
            except Exception:
                error, c = TransactionError.objects.update_or_create(tx=transaction, field='delivery_site_country',
                                                                     error='Champ production_site_country incorrect',
                                                                     defaults={'value': lot_row['delivery_site_country']})
        else:
            error, c = TransactionError.objects.update_or_create(tx=transaction, field='delivery_site_country',
                                                                 error='Merci de préciser une valeur dans le champ production_site_country',
                                                                 defaults={'value': None})

    transaction.ghg_total = lot.ghg_total
    transaction.ghg_reduction = lot.ghg_reduction

    if 'champ_libre' in lot_row:
        transaction.champ_libre = lot_row['champ_libre']
    transaction.save()
    lot.save()


@login_required
@enrich_with_user_details
@restrict_to_traders
def excel_template_download(request, *args, **kwargs):
    context = kwargs['context']
    file_location = create_template_xlsx_v2_traders(context['user_entity'])
    try:
        with open(file_location, 'rb') as f:
            file_data = f.read()
            # sending response
            response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="carbure_template_traders.xlsx"'
            return response
    except Exception as e:
        return JsonResponse({'status': "error", 'message': "Error creating template file", 'error': str(e)}, status=500)


@login_required
@enrich_with_user_details
@restrict_to_traders
def excel_template_upload(request, *args, **kwargs):
    context = kwargs['context']
    file = request.FILES.get('file')
    if file is None:
        return JsonResponse({'status': "error", 'message': "Merci d'ajouter un fichier"}, status=400)
    # we can load the file
    wb = openpyxl.load_workbook(file)
    lots_sheet = wb['lots']
    colid2field = {}
    lots = []
    # create a dictionary from the line
    for i, row in enumerate(lots_sheet):
        if i == 0:
            # header
            for i, col in enumerate(row):
                colid2field[i] = col.value
        else:
            lot = {}
            for i, col in enumerate(row):
                field = colid2field[i]
                lot[field] = col.value
            lots.append(lot)
    total_lots = len(lots)
    lots_loaded = 0
    for lot in lots:
        try:
            load_excel_lot(context, lot)
            lots_loaded += 1
        except Exception as e:
            print(e)
    return JsonResponse({'status': "success", 'message': "%d/%d lots chargés correctement" % (lots_loaded, total_lots)})


@login_required
@enrich_with_user_details
@restrict_to_traders
def get_in(request, *args, **kwargs):
    context = kwargs['context']
    # lots assigned by others + lots imported
    transactions = LotTransaction.objects.filter(carbure_client=context['user_entity'], delivery_status__in=['N', 'AC', 'AA'], lot__status="Validated")
    lot_ids = [t.lot.id for t in transactions]
    lots = LotV2.objects.filter(id__in=lot_ids)
    errors = LotV2Error.objects.filter(lot__in=lots)
    sez = serializers.serialize('json', lots, use_natural_foreign_keys=True)
    txsez = serializers.serialize('json', transactions, use_natural_foreign_keys=True)
    errsez = serializers.serialize('json', errors, use_natural_foreign_keys=True)
    return JsonResponse({'lots': sez, 'errors': errsez, 'transactions': txsez})


@login_required
@enrich_with_user_details
@restrict_to_traders
def get_drafts(request, *args, **kwargs):
    context = kwargs['context']
    lots = LotV2.objects.filter(added_by=context['user_entity'], status='Draft')
    transactions_ids = set([tx['id__min'] for tx in LotTransaction.objects.filter(lot__in=lots).values('lot_id', 'id').annotate(Min('id'))])
    errors = LotV2Error.objects.filter(lot__in=lots)
    first_transactions = LotTransaction.objects.filter(id__in=transactions_ids)
    sez = serializers.serialize('json', lots, use_natural_foreign_keys=True)
    txsez = serializers.serialize('json', first_transactions, use_natural_foreign_keys=True)
    errsez = serializers.serialize('json', errors, use_natural_foreign_keys=True)
    return JsonResponse({'lots': sez, 'errors': errsez, 'transactions': txsez})


@login_required
@enrich_with_user_details
@restrict_to_traders
def get_out(request, *args, **kwargs):
    context = kwargs['context']
    transactions = LotTransaction.objects.filter(carbure_client=context['user_entity'], delivery_status='A', lot__status="Validated", lot__fused_with=None)
    lot_ids = [t.lot.id for t in transactions]
    lots = LotV2.objects.filter(id__in=lot_ids)
    sez = serializers.serialize('json', lots, use_natural_foreign_keys=True)
    txsez = serializers.serialize('json', transactions, use_natural_foreign_keys=True)
    return JsonResponse({'lots': sez, 'transactions': txsez})


@login_required
@enrich_with_user_details
@restrict_to_traders
def delete_lots(request, *args, **kwargs):
    context = kwargs['context']
    lot_ids = request.POST.get('lots', None)
    errors = []
    if not lot_ids:
        return JsonResponse({'status': 'error', 'message': 'Missing lot ids'}, status=400)
    ids = lot_ids.split(',')
    for lotid in ids:
        lot = LotV2.objects.get(id=lotid, added_by=context['user_entity'], status='Draft')
        try:
            lot.delete()
        except Exception as e:
            errors.append({'message': 'Impossible de supprimer le lot %s: introuvable ou déjà validé' % (), 'extra': str(e)})
    return JsonResponse({'status': 'success', 'message': '%d lots supprimés' % (len(ids) - len(errors)), 'errors': errors})


# not an api call
def validate_lot(lot, tx):
    if not tx.dae:
        return False, 'Validation impossible. DAE manquant'
    if not tx.delivery_site_is_in_carbure and not tx.unknown_delivery_site:
        return False, 'Validation impossible. Site de livraison manquant'
    if tx.delivery_site_is_in_carbure and not tx.carbure_delivery_site:
        return False, 'Validation impossible. Site de livraison manquant'
    if not tx.delivery_date:
        return False, 'Validation impossible. Date de livraison manquante'
    if tx.client_is_in_carbure and not tx.carbure_client:
        return False, 'Validation impossible. Veuillez renseigner un client'
    if not tx.client_is_in_carbure and not tx.unknown_client:
        return False, 'Validation impossible. Veuillez renseigner un client'
    if not lot.volume:
        return False, 'Validation impossible. Veuillez renseigner le volume'
    if not lot.pays_origine:
        return False, 'Validation impossible. Veuillez renseigner le pays d\'origine de la matière première'
    try:
        today = datetime.date.today()
        # [PAYS][YYMM]P[IDProd]-[1....]-([S123])
        # FR2002P001-1
        if lot.producer_is_in_carbure:
            lot.carbure_id = "%s%sP%d-%d" % ('FR', today.strftime('%y%m'), lot.carbure_producer.id, lot.id)
        else:
            lot.carbure_id = "%s%sP%s-%d" % ('FR', today.strftime('%y%m'), 'XXX', lot.id)
        lot.status = "Validated"
        lot.save()
    except Exception:
        return False, 'Erreur lors de la validation du lot'
    return True, 'success'


@login_required
@enrich_with_user_details
@restrict_to_traders
def accept_lots(request, *args, **kwargs):
    context = kwargs['context']
    tx_ids = request.POST.get('tx_ids', None)
    errors = []
    if not tx_ids:
        return JsonResponse({'status': 'error', 'message': 'Missing tx ids'}, status=400)
    ids = tx_ids.split(',')
    for txid in ids:
        try:
            tx = LotTransaction.objects.get(id=txid, carbure_client=context['user_entity'], delivery_status__in=['N', 'AC', 'AA'])
            if tx.lot.status == 'Draft':
                success, msg = validate_lot(tx.lot, tx)
                if success is False:
                    errors.append(msg)
                    continue
            tx.delivery_status = 'A'
            tx.save()
        except Exception as e:
            errors.append({'message': 'Impossible d\'accepter la transaction: introuvable ou déjà validée', 'extra': str(e)})
    return JsonResponse({'status': 'success', 'message': '%d lots acceptés' % (len(ids) - len(errors)), 'errors': errors})


@login_required
@enrich_with_user_details
@restrict_to_traders
def declare_lots(request, *args, **kwargs):
    context = kwargs['context']
    lot_ids = request.POST.get('lots', None)
    results = []
    if not lot_ids:
        return JsonResponse({'status': 'error', 'message': 'Aucun lot sélectionné'}, status=400)

    ids = lot_ids.split(',')
    for lotid in ids:
        try:
            lot = LotV2.objects.get(id=lotid, added_by=context['user_entity'], status='Draft')
            # we use .get() below because we should have a single transaction for this lot
            tx = LotTransaction.objects.get(lot=lot)
        except Exception as e:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Impossible de valider le lot %s: introuvable ou déjà validé' % (), 'extra': str(e)})
            continue
        # make sure all mandatory fields are set
        if not tx.dae:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. DAE manquant'})
            continue
        if not tx.delivery_site_is_in_carbure and not tx.unknown_delivery_site:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Site de livraison manquant'})
            continue
        if tx.delivery_site_is_in_carbure and not tx.carbure_delivery_site:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Site de livraison manquant'})
            continue
        if not tx.delivery_date:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Date de livraison manquante'})
            continue
        if tx.client_is_in_carbure and not tx.carbure_client:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Veuillez renseigner un client'})
            continue
        if not tx.client_is_in_carbure and not tx.unknown_client:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Veuillez renseigner un client'})
            continue
        if not lot.volume:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Veuillez renseigner le volume'})
            continue
        if not lot.pays_origine:
            msg = 'Validation impossible. Veuillez renseigner le pays d\'origine de la matière première'
            results.append({'lot_id': lotid, 'status': 'error', 'message': msg})
            continue
        try:
            today = datetime.date.today()
            # [PAYS][YYMM]P[IDProd]-[1....]-([S123])
            # FR2002P001-1
            if lot.producer_is_in_carbure:
                lot.carbure_id = "%s%sP%d-%d" % ('FR', today.strftime('%y%m'), lot.carbure_producer.id, lot.id)
            else:
                lot.carbure_id = "%s%sP%s-%d" % ('FR', today.strftime('%y%m'), 'XXX', lot.id)
            lot.status = "Validated"
            lot.save()
        except Exception:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Erreur lors de la validation du lot'})
            continue
        results.append({'lot_id': lotid, 'status': 'sucess'})
    return JsonResponse({'status': 'success', 'message': results})


@login_required
@enrich_with_user_details
@restrict_to_traders
def reject_lot(request, *args, **kwargs):
    context = kwargs['context']
    # new lot or edit?
    tx_id = request.POST.get('tx_id', None)
    tx_comment = request.POST.get('comment', '')
    if tx_id is None:
        return JsonResponse({'status': 'error', 'message': "Missing TX ID from POST data"}, status=400)
    if tx_comment == '':
        return JsonResponse({'status': 'error', 'message': "Un commentaire est obligatoire en cas de refus"}, status=400)
    try:
        tx = LotTransaction.objects.get(carbure_client=context['user_entity'], delivery_status__in=['N', 'AC', 'AA'], id=tx_id)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': "Transaction inconnue", 'extra': str(e)}, status=400)
    tx.delivery_status = 'R'
    tx.save()
    txerr = TransactionComment()
    txerr.entity = context['user_entity']
    txerr.tx = tx
    txerr.comment = tx_comment
    txerr.save()
    return JsonResponse({'status': 'success', 'tx_id': tx.id})


@login_required
@enrich_with_user_details
@restrict_to_traders
def accept_lot(request, *args, **kwargs):
    context = kwargs['context']
    # new lot or edit?
    tx_id = request.POST.get('tx_id', None)
    if tx_id is None:
        return JsonResponse({'status': 'error', 'message': "Missing TX ID from POST data"}, status=400)
    try:
        tx = LotTransaction.objects.get(carbure_client=context['user_entity'], delivery_status__in=['N', 'AC', 'AA'], id=tx_id)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': "Transaction inconnue", 'extra': str(e)}, status=400)
    tx.delivery_status = 'A'
    tx.save()
    return JsonResponse({'status': 'success', 'tx_id': tx.id})


@login_required
@enrich_with_user_details
@restrict_to_traders
def accept_lot_with_correction(request, *args, **kwargs):
    context = kwargs['context']
    # new lot or edit?
    tx_id = request.POST.get('tx_id', None)
    tx_comment = request.POST.get('comment', '')
    if tx_id is None:
        return JsonResponse({'status': 'error', 'message': "Missing TX ID from POST data"}, status=400)
    if tx_comment == '':
        return JsonResponse({'status': 'error', 'message': "Un commentaire est obligatoire"}, status=400)
    try:
        tx = LotTransaction.objects.get(carbure_client=context['user_entity'], delivery_status__in=['N', 'AC', 'AA'], id=tx_id)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': "Transaction inconnue", 'extra': str(e)}, status=400)
    tx.delivery_status = 'AC'
    tx.save()
    txc = TransactionComment()
    txc.entity = context['user_entity']
    txc.tx = tx
    txc.comment = tx_comment
    txc.save()
    return JsonResponse({'status': 'success', 'tx_id': tx.id})


@login_required
@enrich_with_user_details
@restrict_to_traders
def export_drafts(request, *args, **kwargs):
    context = kwargs['context']
    today = datetime.datetime.now()
    filename = 'export_%s.csv' % (today.strftime('%Y%m%d_%H%M%S'))

    transactions = LotTransaction.objects.filter(lot__added_by=context['user_entity'], lot__status="Draft")

    buffer = io.BytesIO()
    header = "producer;production_site;production_site_country;production_site_reference;production_site_commissioning_date;double_counting_registration;volume;biocarburant_code;\
              matiere_premiere_code;pays_origine_code;eec;el;ep;etd;eu;esca;eccs;eccr;eee;e;dae;champ_libre;client;delivery_date;delivery_site;delivery_site_country\n"
    buffer.write(header.encode())
    for tx in transactions:
        lot = tx.lot
        line = [lot.carbure_producer.name if lot.producer_is_in_carbure else lot.unknown_producer,
                lot.carbure_production_site.name if lot.production_site_is_in_carbure else lot.unknown_production_site,
                lot.carbure_production_site.country.code_pays if lot.production_site_is_in_carbure and lot.carbure_production_site.country else lot.unknown_production_country.code_pays if lot.unknown_production_country else '',
                lot.unknown_production_site_reference,
                lot.unknown_production_site_com_date,
                lot.unknown_production_site_dbl_counting,
                lot.volume,
                lot.biocarburant.code if lot.biocarburant else '',
                lot.matiere_premiere.code if lot.matiere_premiere else '',
                lot.pays_origine.code_pays if lot.pays_origine else '',
                lot.eec, lot.el, lot.ep, lot.etd, lot.eu, lot.esca,
                lot.eccs, lot.eccr, lot.eee, lot.ghg_total,
                # tx
                tx.dae,
                tx.champ_libre,
                tx.carbure_client.name if tx.client_is_in_carbure else tx.unknown_client,
                tx.delivery_date,
                tx.carbure_delivery_site.depot_id if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site,
                tx.carbure_delivery_site.country.code_pays if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site_country
                ]
        csvline = '%s\n' % (';'.join([str(k) for k in line]))
        buffer.write(csvline.encode('iso-8859-1'))
    csvfile = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
    response.write(csvfile)
    return response


@login_required
@enrich_with_user_details
@restrict_to_traders
def export_in(request, *args, **kwargs):
    context = kwargs['context']
    today = datetime.datetime.now()
    filename = 'export_%s.csv' % (today.strftime('%Y%m%d_%H%M%S'))

    transactions = LotTransaction.objects.filter(carbure_client=context['user_entity'], delivery_status__in=['N', 'AC', 'AA'], lot__status="Validated")

    buffer = io.BytesIO()
    header = "producer;production_site;production_site_country;production_site_reference;production_site_commissioning_date;double_counting_registration;volume;biocarburant_code;\
              matiere_premiere_code;pays_origine_code;eec;el;ep;etd;eu;esca;eccs;eccr;eee;e;dae;champ_libre;client;delivery_date;delivery_site;delivery_site_country\n"
    buffer.write(header.encode())
    for tx in transactions:
        lot = tx.lot
        line = [lot.carbure_producer.name if lot.producer_is_in_carbure else lot.unknown_producer,
                lot.carbure_production_site.name if lot.production_site_is_in_carbure else lot.unknown_production_site,
                lot.carbure_production_site.country.code_pays if lot.production_site_is_in_carbure and lot.carbure_production_site.country else lot.unknown_production_country.code_pays if lot.unknown_production_country else '',
                lot.unknown_production_site_reference,
                lot.unknown_production_site_com_date,
                lot.unknown_production_site_dbl_counting,
                lot.volume,
                lot.biocarburant.code if lot.biocarburant else '',
                lot.matiere_premiere.code if lot.matiere_premiere else '',
                lot.pays_origine.code_pays if lot.pays_origine else '',
                lot.eec, lot.el, lot.ep, lot.etd, lot.eu, lot.esca,
                lot.eccs, lot.eccr, lot.eee, lot.ghg_total,
                # tx
                tx.dae,
                tx.champ_libre,
                tx.carbure_client.name if tx.client_is_in_carbure else tx.unknown_client,
                tx.delivery_date,
                tx.carbure_delivery_site.depot_id if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site,
                tx.carbure_delivery_site.country.code_pays if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site_country
                ]
        csvline = '%s\n' % (';'.join([str(k) for k in line]))
        buffer.write(csvline.encode('iso-8859-1'))
    csvfile = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
    response.write(csvfile)
    return response


@login_required
@enrich_with_user_details
@restrict_to_traders
def export_out(request, *args, **kwargs):
    context = kwargs['context']
    today = datetime.datetime.now()
    filename = 'export_%s.csv' % (today.strftime('%Y%m%d_%H%M%S'))

    transactions = LotTransaction.objects.filter(carbure_client=context['user_entity'], delivery_status='A', lot__status="Validated", lot__fused_with=None)

    buffer = io.BytesIO()
    header = "producer;production_site;production_site_country;production_site_reference;production_site_commissioning_date;double_counting_registration;volume;biocarburant_code;\
              matiere_premiere_code;pays_origine_code;eec;el;ep;etd;eu;esca;eccs;eccr;eee;e;dae;champ_libre;client;delivery_date;delivery_site;delivery_site_country\n"
    buffer.write(header.encode())
    for tx in transactions:
        lot = tx.lot
        line = [lot.carbure_producer.name if lot.producer_is_in_carbure else lot.unknown_producer,
                lot.carbure_production_site.name if lot.production_site_is_in_carbure else lot.unknown_production_site,
                lot.carbure_production_site.country.code_pays if lot.production_site_is_in_carbure and lot.carbure_production_site.country else lot.unknown_production_country.code_pays if lot.unknown_production_country else '',
                lot.unknown_production_site_reference,
                lot.unknown_production_site_com_date,
                lot.unknown_production_site_dbl_counting,
                lot.volume,
                lot.biocarburant.code if lot.biocarburant else '',
                lot.matiere_premiere.code if lot.matiere_premiere else '',
                lot.pays_origine.code_pays if lot.pays_origine else '',
                lot.eec, lot.el, lot.ep, lot.etd, lot.eu, lot.esca,
                lot.eccs, lot.eccr, lot.eee, lot.ghg_total,
                # tx
                tx.dae,
                tx.champ_libre,
                tx.carbure_client.name if tx.client_is_in_carbure else tx.unknown_client,
                tx.delivery_date,
                tx.carbure_delivery_site.depot_id if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site,
                tx.carbure_delivery_site.country.code_pays if tx.delivery_site_is_in_carbure else tx.unknown_delivery_site_country
                ]
        csvline = '%s\n' % (';'.join([str(k) for k in line]))
        buffer.write(csvline.encode('iso-8859-1'))
    csvfile = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
    response.write(csvfile)
    return response


@login_required
@enrich_with_user_details
@restrict_to_traders
def validate_lots(request, *args, **kwargs):
    context = kwargs['context']
    lot_ids = request.POST.get('lots', None)
    results = []
    if not lot_ids:
        return JsonResponse({'status': 'error', 'message': 'Aucun lot sélectionné'}, status=400)

    ids = lot_ids.split(',')
    for lotid in ids:
        try:
            lot = LotV2.objects.get(id=lotid, added_by=context['user_entity'], status='Draft')
            # we use .get() below because we should have a single transaction for this lot
            tx = LotTransaction.objects.get(lot=lot)
        except Exception as e:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Impossible de valider le lot: introuvable ou déjà validé' % (), 'extra': str(e)})
            continue
        # make sure all mandatory fields are set
        if not tx.dae:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. DAE manquant'})
            continue
        if not tx.delivery_site_is_in_carbure and not tx.unknown_delivery_site:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Site de livraison manquant'})
            continue
        if tx.delivery_site_is_in_carbure and not tx.carbure_delivery_site:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Site de livraison manquant'})
            continue
        if not tx.delivery_date:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Date de livraison manquante'})
            continue
        tx.client_is_in_carbure = True
        tx.carbure_client = context['user_entity']
        if not lot.volume:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Veuillez renseigner le volume'})
            continue
        if not lot.pays_origine:
            msg = 'Validation impossible. Veuillez renseigner le pays d\'origine de la matière première'
            results.append({'lot_id': lotid, 'status': 'error', 'message': msg})
            continue

        if lot.producer_is_in_carbure and lot.carbure_production_site is None:
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Validation impossible. Veuillez renseigner le site de production'})
            continue
        try:
            today = datetime.date.today()
            lot.carbure_id = "%s%sP%s-%d" % ('FR', today.strftime('%y%m'), 'XXX', lot.id)
            lot.status = "Validated"
            if tx.carbure_client == context['user_entity']:
                tx.delivery_status = 'A'
                tx.save()
            lot.save()
        except Exception as e:
            print('exception during validation: %s' % (e))
            results.append({'lot_id': lotid, 'status': 'error', 'message': 'Erreur lors de la validation du lot'})
            continue
        results.append({'lot_id': lotid, 'status': 'sucess'})
    print({'status': 'success', 'message': results})
    return JsonResponse({'status': 'success', 'message': results})