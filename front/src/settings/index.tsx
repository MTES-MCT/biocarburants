import { Trans } from "react-i18next"
import { EntitySelection } from "carbure/hooks/use-entity"
import { SettingsGetter } from "./hooks/use-get-settings"

import use2BSCertificates from "./hooks/use-2bs-certificates"
import useCompany from "./hooks/use-company"
import useDeliverySites from "./hooks/use-delivery-sites"
import useISCCCertificates from "./hooks/use-iscc-certificates"
import useNationalSystemCertificates from "./hooks/use-national-system-certificates"
import useProductionSites from "./hooks/use-production-sites"

import { Main, Title } from "common/components"
import { SettingsHeader, SettingsBody } from "./components/common"
import DeliverySitesSettings from "./components/delivery-site"
import ProductionSitesSettings from "./components/production-site"
import {
  DBSCertificateSettings,
  ISCCCertificateSettings,
  REDCertCertificateSettings,
  SNCertificateSettings,
} from "./components/certificates"
import CompanySettings from "./components/company"
import Sticky from "common/components/sticky"
import useREDCertCertificates from "./hooks/use-redcert-certificates"
import UserRights from "./components/user-rights"
import { useRights } from "carbure/hooks/use-rights"
import { EntityType, UserRole } from "common/types"

function useSettings(entity: EntitySelection, settings: SettingsGetter) {
  const company = useCompany(entity, settings)
  const productionSites = useProductionSites(entity)
  const deliverySites = useDeliverySites(entity)
  const dbsCertificates = use2BSCertificates(entity, productionSites, company)
  const isccCertificates = useISCCCertificates(entity, productionSites, company)
  const redcertCertificates = useREDCertCertificates(entity, productionSites, company) // prettier-ignore
  const nationalSystemCertificates = useNationalSystemCertificates(entity, productionSites, company) // prettier-ignore

  return {
    productionSites,
    deliverySites,
    dbsCertificates,
    isccCertificates,
    redcertCertificates,
    nationalSystemCertificates,
    company,
  }
}

type SettingsProps = {
  entity: EntitySelection
  settings: SettingsGetter
}

const Settings = ({ entity, settings }: SettingsProps) => {
  const {
    company,
    productionSites,
    deliverySites,
    dbsCertificates,
    isccCertificates,
    redcertCertificates,
    nationalSystemCertificates,
  } = useSettings(entity, settings)

  const rights = useRights()

  const isProducer = entity?.entity_type === EntityType.Producer
  const isTrader = entity?.entity_type === EntityType.Trader
  const isOperator = entity?.entity_type === EntityType.Operator
  const isAuditor = entity?.entity_type === EntityType.Auditor

  const hasCertificates = isProducer || isTrader
  const hasCSN = isProducer || isOperator

  return (
    <Main>
      <SettingsHeader>
        <Title>{entity?.name}</Title>
      </SettingsHeader>

      <Sticky>
        {!isAuditor && (
          <a href="#options">
            <Trans>Options</Trans>
          </a>
        )}
        {!isAuditor && (
          <a href="#depot">
            <Trans>Dépôts</Trans>
          </a>
        )}
        {isProducer && (
          <a href="#production">
            <Trans>Sites de production</Trans>
          </a>
        )}
        {hasCertificates && (
          <a href="#iscc">
            <Trans>Certificats ISCC</Trans>
          </a>
        )}
        {hasCertificates && (
          <a href="#2bs">
            <Trans>Certificats 2BS</Trans>
          </a>
        )}
        {hasCertificates && (
          <a href="#red">
            <Trans>Certificats REDcert</Trans>
          </a>
        )}
        {hasCertificates && (
          <a href="#sn">
            <Trans>Certificats Système National</Trans>
          </a>
        )}
        {!hasCertificates && hasCSN && (
          <a href="#sn">
            <Trans>Certificats Système National</Trans>
          </a>
        )}
        {rights.is(UserRole.Admin) && (
          <a href="#users">
            <Trans>Utilisateurs</Trans>
          </a>
        )}
      </Sticky>

      <SettingsBody>
        {!isAuditor && <CompanySettings entity={entity} settings={company} />}
        {!isAuditor && <DeliverySitesSettings settings={deliverySites} />}

        {isProducer && <ProductionSitesSettings settings={productionSites} />}

        {hasCertificates && (
          <ISCCCertificateSettings settings={isccCertificates} />
        )}

        {hasCertificates && (
          <DBSCertificateSettings settings={dbsCertificates} />
        )}

        {hasCertificates && (
          <REDCertCertificateSettings settings={redcertCertificates} />
        )}

        {(hasCertificates || hasCSN) && (
          <SNCertificateSettings settings={nationalSystemCertificates} />
        )}

        {rights.is(UserRole.Admin) && (
          <UserRights entity={entity} settings={settings} />
        )}
      </SettingsBody>
    </Main>
  )
}
export default Settings
