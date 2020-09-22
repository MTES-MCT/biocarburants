import datetime
from core.models import LotValidationError, MatierePremiere, Biocarburant, Pays

# init data cache
#MPS = {m.code: m for m in MatierePremiere.objects.all()}
#BCS = {b.code: b for b in Biocarburant.objects.all()}
#COUNTRIES = {p.code_pays: p for p in Pays.objects.all()}

# definitions

oct2015 = datetime.date(year=2015, month=10, day=5)
jan2021 = datetime.date(year=2021, month=1, day=1)

rules = {}
rules['GHG_REDUC_INF_50'] = "La réduction de gaz à effet de serre est inférieure à 50%, il n'est pas possible d'enregistrer ce lot dans CarbuRe"
rules['GHG_REDUC_SUP_100'] = "La réduction de gaz à effet de serre est supérieur à 100%, il n'est pas possible d'enregistrer ce lot dans CarbuRe"
rules['PROVENANCE_MP'] = "Êtes vous sûr de la provenance de votre matière première ?"
rules['MP_BC_INCOHERENT'] = "Matière Première incohérente avec le Biocarburant"
rules['GHG_REDUC_INF_60'] = "La réduction de gaz à effet de serre est inférieure à 60% pour une usine dont la date de mise en service est ultérieure au 5 Octobre 2015. Il n'est pas possible d'enregistrer ce lot dans CarbuRe"
rules['GHG_REDUC_INF_65'] = "La réduction de gaz à effet de serre est inférieure à 65% pour une usine dont la date de mise en service est ultérieure au 1er Janvier 2021. Il n'est pas possible d'enregistrer ce lot dans CarbuRe"
rules['MISSING_REF_DBL_COUNTING'] = "Numéro d'enregistrement Double Compte manquant"


def raise_error(lot, rule_triggered, warning_to_user=True, warning_to_admin=False, block_validation=False, details=''):
    d = {'warning_to_user': warning_to_user,
         'warning_to_admin': warning_to_admin,
         'block_validation': block_validation,
         'message': rules[rule_triggered],
         'details': details,
         }
    LotValidationError.objects.update_or_create(lot=lot, rule_triggered=rule_triggered, defaults=d)


def sanity_check(lot):
    now = datetime.datetime.now()
    # réduction de GES
    if lot.ghg_reduction > 100:
        raise_error(lot, 'GHG_REDUC_SUP_100', warning_to_user=True, block_validation=True, details="GES reduction %f%%" % (lot.ghg_reduction))
    if lot.ghg_reduction < 50:
        raise_error(lot, 'GHG_REDUC_INF_50', warning_to_user=True, block_validation=True, details="GES reduction %f%%" % (lot.ghg_reduction))
    commissioning_date = lot.carbure_production_site.date_mise_en_service if lot.carbure_production_site else lot.unknown_production_site_com_date
    if commissioning_date:
        if commissioning_date > oct2015 and lot.ghg_reduction < 60:
            raise_error(lot, 'GHG_REDUC_INF_60', warning_to_user=True, block_validation=True, details="GES reduction %f%%" % (lot.ghg_reduction))
        if commissioning_date >= jan2021 and lot.ghg_reduction < 65:
            raise_error(lot, 'GHG_REDUC_INF_65', warning_to_user=True, block_validation=True, details="GES reduction %f%%" % (lot.ghg_reduction))

    # provenance des matieres premieres
    if lot.matiere_premiere:
        if lot.matiere_premiere.code == 'SOJA':
            # TODO: remplacer par une liste de pays "douteux" ou a l'inverse utiliser une whitelist et lever une alerte si le pays n'est pas dedans
            if lot.pays_origine.code_pays == 'SE':
                raise_error(lot, 'PROVENANCE_MP', warning_to_user=True, warning_admin=True, block_validation=False, details="%s de %s" % (lot.matiere_premiere.name, lot.pays_origine.name))

    if lot.biocarburant and lot.matiere_premiere:
        # consistence des matieres premieres avec biocarburant
        if lot.biocarburant.is_alcool and lot.matiere_premiere.compatible_alcool is False:
            raise_error(lot, 'MP_BC_INCOHERENT', warning_to_user=True, warning_to_admin=True, details="%s de %s" % (lot.biocarburant.name, lot.matiere_premiere.name))

        if lot.biocarburant.is_graisse and lot.matiere_premiere.compatible_graisse is False:
            raise_error(lot, 'MP_BC_INCOHERENT', warning_to_user=True, warning_to_admin=True, details="%s de %s" % (lot.biocarburant.name, lot.matiere_premiere.name))

        # double comptage, cas specifiques (Total)
        if lot.biocarburant.code in ['EMHA', 'EMHU'] and lot.matiere_premiere.code in ['HUILES_OU_GRAISSES_ANIMALES_CAT1_CAT2', 'HUILE_ALIMENTAIRE_USAGEE']:
            if lot.unknown_production_site_dbl_counting is None or (lot.carbure_production_site and not lot.carbure_production_site.dc_reference):
                raise_error(lot, 'MISSING_REF_DBL_COUNTING', warning_to_user=True, block_validation=True, details="%s de %s" % (lot.biocarburant.name, lot.matiere_premiere.name))

        if lot.biocarburant.code in ['ET'] and lot.matiere_premiere.code in ['RESIDUS_VINIQUES']:
            if lot.unknown_production_site_dbl_counting is None or (lot.carbure_production_site and not lot.carbure_production_site.dc_reference):
                raise_error(lot, 'MISSING_REF_DBL_COUNTING', warning_to_user=True, warning_to_admin=True, details="%s de %s" % (lot.biocarburant.name, lot.matiere_premiere.name))

        if lot.biocarburant.code == 'EMHA' and lot.matiere_premiere.code not in ['HUILES_OU_GRAISSES_ANIMALES_CAT1_CAT2', 'HUILES_OU_GRAISSES_ANIMALES_CAT3']:
            raise_error(lot, 'MP_BC_INCOHERENT', warning_to_user=True, warning_to_admin=True, details="%s de %s" % (lot.biocarburant.name, lot.matiere_premiere.name))

        if lot.biocarburant.code == 'EMHU' and lot.matiere_premiere.code != 'HUILE_ALIMENTAIRE_USAGEE':
            raise_error(lot, 'MP_BC_INCOHERENT', warning_to_user=True, warning_to_admin=True, details="%s de %s" % (lot.biocarburant.name, lot.matiere_premiere.name))

        if lot.biocarburant.code == 'EMHV' and lot.matiere_premiere.code not in ['COLZA', 'TOURNESOL', 'SOJA', 'HUILE_PALME', 'EFFLUENTS_HUILERIES_PALME_RAFLE']:
            raise_error(lot, 'MP_BC_INCOHERENT', warning_to_user=True, warning_to_admin=True, details="%s de %s" % (lot.biocarburant.name, lot.matiere_premiere.name))

        if lot.biocarburant.code in ['ET', 'ETBE'] and lot.matiere_premiere.code not in ['MAIS', 'BLE', 'BETTERAVE', 'CANNE_A_SUCRE', 'RESIDUS_VINIQUES']:
            raise_error(lot, 'MP_BC_INCOHERENT', warning_to_user=True, warning_to_admin=True, details="%s de %s" % (lot.biocarburant.name, lot.matiere_premiere.name))
    after = datetime.datetime.now()
    duration = after - now
    print(duration)

def queryset_sanity_check(queryset):
    for lot in queryset:
        sanity_check(lot)