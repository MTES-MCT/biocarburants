import api from "common/services/api"
import {
  Settings,
  GESOption,
  DBSCertificate,
  ISCCCertificate,
  ProductionSite,
  ProductionSiteDetails,
  ProductionCertificate,
  OwnershipType,
  REDCertCertificate,
  SNCertificate,
  EntityRights,
} from "common/types"
import { EntitySelection } from "carbure/hooks/use-entity"

export function getSettings(): Promise<Settings> {
  return api.get("/settings/")
}

export function getProductionSites(
  entityID: number
): Promise<ProductionSiteDetails[]> {
  return api.get("/settings/get-production-sites", {
    entity_id: entityID,
  })
}

export function addProductionSite(
  producerID: number,
  name: string,
  date_mise_en_service: string,
  country_code: string,
  ges_option: GESOption,
  site_id: string,
  city: string,
  postal_code: string,
  eligible_dc: boolean,
  dc_reference: string,
  manager_name: string,
  manager_phone: string,
  manager_email: string
): Promise<ProductionSite> {
  return api.post("/settings/add-production-site", {
    entity_id: producerID,
    name: name,
    date_mise_en_service: date_mise_en_service,
    ges_option: ges_option,
    country_code: country_code,
    site_id,
    city,
    postal_code,
    eligible_dc,
    dc_reference,
    manager_name,
    manager_phone,
    manager_email,
  })
}

export function updateProductionSite(
  entity_id: number,
  production_site_id: number,
  name: string,
  date_mise_en_service: string,
  country_code: string,
  ges_option: GESOption,
  site_id: string,
  city: string,
  postal_code: string,
  eligible_dc: boolean,
  dc_reference: string,
  manager_name: string,
  manager_phone: string,
  manager_email: string
) {
  return api.post("/settings/update-production-site", {
    entity_id,
    production_site_id,
    name,
    date_mise_en_service,
    ges_option,
    country_code,
    site_id,
    city,
    postal_code,
    eligible_dc,
    dc_reference,
    manager_name,
    manager_phone,
    manager_email,
  })
}

export function deleteProductionSite(
  entity_id: number | undefined,
  productionSiteID: number
) {
  return api.post("/settings/delete-production-site", {
    entity_id: entity_id,
    production_site_id: productionSiteID,
  })
}

export function setProductionSiteMP(
  entity_id: number,
  productionSiteID: number,
  matieresPremieres: string[]
) {
  return api.post("/settings/set-production-site-matieres-premieres", {
    entity_id: entity_id,
    production_site_id: productionSiteID,
    matiere_premiere_codes: matieresPremieres,
  })
}

export function setProductionSiteBC(
  entity_id: number,
  productionSiteID: number,
  biocarburants: string[]
) {
  return api.post("/settings/set-production-site-biocarburants", {
    entity_id: entity_id,
    production_site_id: productionSiteID,
    biocarburant_codes: biocarburants,
  })
}

export function deleteProductionSiteMP(
  entity_id: number,
  productionSiteID: number,
  matiere_premiere_code: string
) {
  return api.post("/settings/delete-production-site-matiere-premiere", {
    entity_id: entity_id,
    production_site_id: productionSiteID,
    matiere_premiere_code: matiere_premiere_code,
  })
}

export function deleteProductionSiteBC(
  entity_id: number,
  productionSiteID: number,
  biocarburant_code: string
) {
  return api.post("/settings/delete-production-site-biocarburant", {
    entity_id: entity_id,
    production_site_id: productionSiteID,
    biocarburant_code: biocarburant_code,
  })
}

export function findCertificates(
  query: string,
  entity_id: number
): Promise<ProductionCertificate[]> {
  return api.get("/settings/get-my-certificates", {
    entity_id,
    query,
  })
}

export function setProductionSiteCertificates(
  entity_id: number,
  production_site_id: number,
  certificate_ids: string[]
) {
  return api.post("/settings/set-production-site-certificates", {
    entity_id,
    production_site_id,
    certificate_ids,
  })
}

export function getDeliverySites(entity_id: number) {
  return api.get("/settings/get-delivery-sites", {
    entity_id,
  })
}

export function addDeliverySite(
  entity_id: number,
  delivery_site_id: string,
  ownership_type: OwnershipType,
  blending_outsourced: boolean,
  blending_entity_id: EntitySelection
) {
  return api.post("/settings/add-delivery-site", {
    entity_id,
    delivery_site_id,
    ownership_type,
    blending_outsourced,
    blending_entity_id: blending_entity_id?.id ?? null,
  })
}

export function deleteDeliverySite(
  entity_id: number,
  delivery_site_id: string
) {
  return api.post("/settings/delete-delivery-site", {
    entity_id,
    delivery_site_id,
  })
}

export function enablePublicDirectory(entityID: number) {
  return api.post("/settings/enable-public-directory", {
    entity_id: entityID,
  })
}

export function disablePublicDirectory(entityID: number) {
  return api.post("/settings/disable-public-directory", {
    entity_id: entityID,
  })
}

export function enableMAC(entityID: number) {
  return api.post("/settings/enable-mac", {
    entity_id: entityID,
  })
}

export function disableMAC(entityID: number) {
  return api.post("/settings/disable-mac", {
    entity_id: entityID,
  })
}

export function enableTrading(entityID: number) {
  return api.post("/settings/enable-trading", {
    entity_id: entityID,
  })
}

export function disableTrading(entityID: number) {
  return api.post("/settings/disable-trading", {
    entity_id: entityID,
  })
}

export function getISCCCertificates(
  entityID: number
): Promise<ISCCCertificate[]> {
  return api.get("/settings/get-iscc-certificates", {
    entity_id: entityID,
  })
}

export function addISCCCertificate(entityID: number, certificate_id: string) {
  return api.post("/settings/add-iscc-certificate", {
    entity_id: entityID,
    certificate_id: certificate_id,
  })
}

export function deleteISCCCertificate(
  entityID: number,
  certificate_id: string
) {
  return api.post("/settings/delete-iscc-certificate", {
    entity_id: entityID,
    certificate_id: certificate_id,
  })
}

export function updateISCCCertificate(
  entity_id: number,
  old_certificate_id: string,
  new_certificate_id: string
) {
  return api.post("/settings/update-iscc-certificate", {
    entity_id,
    old_certificate_id,
    new_certificate_id,
  })
}

export function get2BSCertificates(
  entityID: number
): Promise<DBSCertificate[]> {
  return api.get("/settings/get-2bs-certificates", {
    entity_id: entityID,
  })
}

export function add2BSCertificate(entityID: number, certificate_id: string) {
  return api.post("/settings/add-2bs-certificate", {
    entity_id: entityID,
    certificate_id: certificate_id,
  })
}

export function delete2BSCertificate(entityID: number, certificate_id: string) {
  return api.post("/settings/delete-2bs-certificate", {
    entity_id: entityID,
    certificate_id: certificate_id,
  })
}

export function update2BSCertificate(
  entity_id: number,
  old_certificate_id: string,
  new_certificate_id: string
) {
  return api.post("/settings/update-2bs-certificate", {
    entity_id,
    old_certificate_id,
    new_certificate_id,
  })
}

export function getREDCertCertificates(
  entityID: number
): Promise<REDCertCertificate[]> {
  return api.get("/settings/get-redcert-certificates", {
    entity_id: entityID,
  })
}

export function addREDCertCertificate(
  entityID: number,
  certificate_id: string
) {
  return api.post("/settings/add-redcert-certificate", {
    entity_id: entityID,
    certificate_id: certificate_id,
  })
}

export function deleteREDCertCertificate(
  entityID: number,
  certificate_id: string
) {
  return api.post("/settings/delete-redcert-certificate", {
    entity_id: entityID,
    certificate_id: certificate_id,
  })
}

export function updateREDCertCertificate(
  entity_id: number,
  old_certificate_id: string,
  new_certificate_id: string
) {
  return api.post("/settings/update-redcert-certificate", {
    entity_id,
    old_certificate_id,
    new_certificate_id,
  })
}

export function getSNCertificates(entityID: number): Promise<SNCertificate[]> {
  return api.get("/settings/get-sn-certificates", {
    entity_id: entityID,
  })
}

export function addSNCertificate(entityID: number, certificate_id: string) {
  return api.post("/settings/add-sn-certificate", {
    entity_id: entityID,
    certificate_id: certificate_id,
  })
}

export function deleteSNCertificate(entityID: number, certificate_id: string) {
  return api.post("/settings/delete-sn-certificate", {
    entity_id: entityID,
    certificate_id: certificate_id,
  })
}

export function updateSNCertificate(
  entity_id: number,
  old_certificate_id: string,
  new_certificate_id: string
) {
  return api.post("/settings/update-sn-certificate", {
    entity_id,
    old_certificate_id,
    new_certificate_id,
  })
}

export function getEntityRights(entity_id: number): Promise<EntityRights> {
  return api.get("/settings/get-entity-rights", { entity_id })
}

export function inviteUser(
  entity_id: number,
  role: string,
  expiration_date: string,
  email: string
) {
  return api.post("/settings/invite-user", {
    entity_id,
    role,
    expiration_date,
    email,
  })
}

export function revokeUserRights(entity_id: number, email: string) {
  return api.post("/settings/revoke-user", { entity_id, email })
}

export function acceptUserRightsRequest(entity_id: number, request_id: number) {
  return api.post("/settings/accept-user", { entity_id, request_id })
}

export function setDefaultCertificate(
  entity_id: number,
  certificate_id: string,
  certificate_type: string
) {
  return api.post("/settings/set-default-certificate", {
    entity_id,
    certificate_id,
    certificate_type,
  })
}
