import {
  DepotType,
  Entity,
  EntityType,
  GESOption,
  ProductionSiteDetails,
  Transaction,
  DeliveryStatus,
  UserRole,
} from "common/types"

// ENTITIES

export const producer: Entity = {
  id: 0,
  name: "Producteur Test",
  entity_type: EntityType.Producer,
  has_mac: true,
  has_trading: true,
  default_certificate: "",
}

export const trader: Entity = {
  id: 1,
  name: "Trader Test",
  entity_type: EntityType.Trader,
  has_mac: true,
  has_trading: true,
  default_certificate: "",
}

export const operator: Entity = {
  id: 2,
  name: "Opérateur Test",
  entity_type: EntityType.Operator,
  has_mac: true,
  has_trading: false,
  default_certificate: "",
}

export const admin: Entity = {
  id: 3,
  name: "Admin Test",
  entity_type: EntityType.Administration,
  has_mac: false,
  has_trading: false,
  default_certificate: "",
}

// COUNTRIES

export const country = {
  code_pays: "FR",
  name: "France",
  name_en: "France",
  is_in_europe: true,
}

// DELIVERY SITES

export const deliverySite = {
  depot_id: "10",
  name: "Test Delivery Site",
  city: "Test City",
  country: country,
  depot_type: DepotType.Other,
  address: "Test Address",
  postal_code: "64430",
}

// PRODUCTION SITES

export const productionSite: ProductionSiteDetails = {
  name: "Test Production Site",
  country: country,
  id: 2,
  date_mise_en_service: "2000-01-31",
  site_id: "123456",
  postal_code: "64430",
  manager_name: "Bob",
  manager_phone: "012345678",
  manager_email: "bob@bobby.bob",
  ges_option: GESOption.Actual,
  eligible_dc: true,
  dc_reference: "bobobobobob",
  city: "Baigorri",
  inputs: [],
  outputs: [],
  certificates: [],
}

// ISCC CERTIFICATES

export const isccCertificate = {
  certificate_id: "ISCC Test",
  certificate_holder: "Holder Test",
  valid_from: "2020-04-25",
  valid_until: "2121-04-24",
  issuing_cb: "Authority Test",
  location: "",
  scope: ["Scope Test"],
}

export const expiredISCCCertificate = {
  certificate_id: "Expired ISCC Test",
  certificate_holder: "Expired Holder Test",
  valid_from: "1990-01-01",
  valid_until: "2000-01-01",
  issuing_cb: "Expired Authority Test",
  location: "",
  scope: ["Expired Scope Test"],
}

export const dbsCertificate = {
  certificate_id: "2BS Test",
  certificate_holder: "Holder Test",
  holder_address: "Address Test",
  valid_from: "2020-04-25",
  valid_until: "2121-04-24",
  certification_type: "",
  download_link: "",
  scope: ["Scope Test"],
  has_been_updated: false,
}

export const expired2BSCertificate = {
  certificate_id: "Expired 2BS Test",
  certificate_holder: "Expired Holder Test",
  holder_address: "Expired Address Test",
  valid_from: "1990-01-01",
  valid_until: "2000-01-01",
  certification_type: "",
  download_link: "",
  scope: ["Expired Scope Test"],
  has_been_updated: false,
}

export const redcertCertificate = {
  certificate_id: "REDCERT Test",
  certificate_holder: "Holder Test",
  holder_address: "Address Test",
  valid_from: "2020-04-25",
  valid_until: "2021-04-24",
  certification_type: "",
  download_link: "",
  scope: ["Scope Test"],
  has_been_updated: false,
}

export const expiredRedcertCertificate = {
  certificate_id: "Expired REDCERT Test",
  certificate_holder: "Expired Holder Test",
  holder_address: "Expired Address Test",
  valid_from: "1990-01-01",
  valid_until: "2000-01-01",
  certification_type: "",
  download_link: "",
  scope: ["Expired Scope Test"],
  has_been_updated: false,
}

export const snCertificate = {
  certificate_id: "SN_UN_2020_0108",
  certificate_holder: "PMSE",
  valid_from: null,
  valid_until: "2025-09-30",
  download_link: "",
  scope: ["6b"],
  type: "SN",
  has_been_updated: false,
}

export const expiredSNCertificate = {
  certificate_id: "Expired SN_UN_2020_0108",
  certificate_holder: "PMSE",
  valid_from: null,
  valid_until: "2020-09-30",
  download_link: "",
  scope: ["6b"],
  type: "SN",
  has_been_updated: false,
}

// MATIERE PREMIERE

export const matierePremiere = {
  code: "COLZA",
  name: "Colza",
  category: "CONV",
}

// BIOCARBURANT

export const biocarburant = {
  code: "EMHV",
  name: "EMHV",
}

// LOT

export const lot: Transaction = {
  lot: {
    id: 0,
    period: "2020-01",
    carbure_id: "",
    producer_is_in_carbure: true,
    carbure_producer: producer,
    unknown_producer: "",
    production_site_is_in_carbure: true,
    carbure_production_site: productionSite,
    carbure_production_site_reference: "2BS - KNOWN PSITE",
    unknown_production_site: "",
    unknown_production_country: null,
    unknown_production_site_com_date: null,
    unknown_production_site_reference: "",
    unknown_production_site_dbl_counting: "",
    volume: 12345,
    remaining_volume: 12345,
    matiere_premiere: matierePremiere,
    biocarburant: biocarburant,
    pays_origine: country,
    eec: 12,
    el: 0,
    ep: 0,
    etd: 0,
    eu: 0,
    esca: 1,
    eccs: 0,
    eccr: 0,
    eee: 0,
    ghg_total: 11,
    ghg_reference: 83.8,
    ghg_reduction: 86.87,
    status: "Draft",
    source: "MANUAL",
    parent_lot: null,
    is_split: false,
    is_fused: false,
    fused_with: null,
    data_origin_entity: producer,
    unknown_supplier: "Unknown Supplier",
    unknown_supplier_certificate: "ISCC2000 - Supplier",
    added_by: producer,
  },
  carbure_vendor: producer,
  carbure_vendor_certificate: "ISCC1000 - Vendor",
  dae: "DAETEST",
  client_is_in_carbure: true,
  carbure_client: operator,
  unknown_client: "",
  delivery_date: "2020-01-31",
  delivery_site_is_in_carbure: true,
  carbure_delivery_site: deliverySite,
  unknown_delivery_site: "",
  unknown_delivery_site_country: null,
  delivery_status: DeliveryStatus.Pending,
  champ_libre: "",
  is_forwarded: false,
  is_mac: false,
  id: 0,
  hidden_by_admin: false,
  hidden_by_auditor: false,
  highlighted_by_admin: false,
  highlighted_by_auditor: false,
}

export const entityRight = {
  name: "User",
  email: "user@company.com",
  entity: producer,
  role: UserRole.Admin,
  expiration_date: null,
}

export const entityRequest = {
  id: 1,
  user: ["user@company.com"],
  entity: producer,
  date_requested: "2020-12-22T16:18:27.233Z",
  status: "ACCEPTED",
  comment: "",
  role: UserRole.Admin,
  expiration_date: null,
}

export const entityRights = {
  status: "success",
  data: {
    rights: [entityRight],
    requests: [entityRequest],
  },
}
