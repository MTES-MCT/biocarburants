import { useEffect } from "react"
import { useTranslation } from "react-i18next"

import { EntitySelection } from "carbure/hooks/use-entity"
import { ProductionSiteDetails, UserRole } from "common/types"

import useAPI from "common/hooks/use-api"
import * as api from "../api"
import {
  ProductionSitePrompt,
  ProductionSiteState,
} from "../components/production-site"
import { confirm, prompt } from "common/components/dialog"
import { useNotificationContext } from "common/components/notifications"
import { useRights } from "carbure/hooks/use-rights"

export interface ProductionSiteSettingsHook {
  isEmpty: boolean
  isLoading: boolean
  productionSites: ProductionSiteDetails[]
  editProductionSite: (p: ProductionSiteDetails) => void
  createProductionSite?: () => void
  removeProductionSite?: (p: ProductionSiteDetails) => void
  refresh?: () => void
}

export default function useProductionSites(
  entity: EntitySelection
): ProductionSiteSettingsHook {
  const { t } = useTranslation()
  const rights = useRights()
  const notifications = useNotificationContext()

  const canModify = rights.is(UserRole.Admin, UserRole.ReadWrite)

  const [requestGetProductionSites, resolveGetProductionSites] = useAPI(api.getProductionSites) // prettier-ignore
  const [requestAddProductionSite, resolveAddProductionSite] = useAPI(api.addProductionSite) // prettier-ignore
  const [requestDelProductionSite, resolveDelProductionSite] = useAPI(api.deleteProductionSite) // prettier-ignore
  const [requestUpdateProductionSite, resolveUpdateProductionSite] = useAPI(api.updateProductionSite) // prettier-ignore

  const [requestSetProductionSiteMP, resolveSetProductionSiteMP] = useAPI(api.setProductionSiteMP) // prettier-ignore
  const [requestSetProductionSiteBC, resolveSetProductionSiteBC] = useAPI(api.setProductionSiteBC) // prettier-ignore
  const [requestSetProductionSiteCertificates, resolveSetProductionSiteCertificates] = useAPI(api.setProductionSiteCertificates) // prettier-ignore

  const entityID = entity?.id
  const productionSites = requestGetProductionSites.data ?? []

  const isLoading =
    requestAddProductionSite.loading ||
    requestGetProductionSites.loading ||
    requestDelProductionSite.loading ||
    requestSetProductionSiteBC.loading ||
    requestSetProductionSiteMP.loading ||
    requestUpdateProductionSite.loading ||
    requestSetProductionSiteCertificates.loading

  const isEmpty = productionSites.length === 0

  function refresh() {
    if (typeof entityID !== "undefined") {
      resolveGetProductionSites(entityID)
    }
  }

  async function createProductionSite() {
    const data = await prompt<ProductionSiteState>((resolve) => (
      <ProductionSitePrompt
        entity={entity}
        title={t("Ajout site de production")}
        description={t("Veuillez entrer les informations de votre nouveau site de production.")} // prettier-ignore
        onResolve={resolve}
      />
    ))

    if (typeof entityID !== "undefined" && data && data.country) {
      const ps = await resolveAddProductionSite(
        entityID,
        data.name,
        data.date_mise_en_service,
        data.country.code_pays,
        data.ges_option,
        data.site_id,
        data.city,
        data.postal_code,
        data.eligible_dc,
        data.dc_reference,
        data.manager_name,
        data.manager_phone,
        data.manager_email
      )

      if (ps) {
        const mps = data.matieres_premieres.map((mp) => mp.code)
        await resolveSetProductionSiteMP(entityID, ps.id, mps)

        const bcs = data.biocarburants.map((bc) => bc.code)
        await resolveSetProductionSiteBC(entityID, ps.id, bcs)

        const cs = data.certificates.map((c) => c.certificate_id)
        await resolveSetProductionSiteCertificates(entityID, ps.id, cs)

        notifications.push({
          level: "success",
          text: t("Le site de production a bien été créé !"),
        })

        refresh()
      } else {
        notifications.push({
          level: "error",
          text: t("Impossible de créer le site de production."),
        })
      }
    }
  }

  async function editProductionSite(ps: ProductionSiteDetails) {
    const data = await prompt<ProductionSiteState>((resolve) => (
      <ProductionSitePrompt
        title={t("Modification site de production")}
        description={t("Veuillez entrer les nouvelles informations de votre site de production.")} // prettier-ignore
        entity={entity}
        productionSite={ps}
        onResolve={resolve}
        readOnly={!canModify}
      />
    ))

    if (typeof entityID !== "undefined" && data && data.country) {
      const res = await resolveUpdateProductionSite(
        entityID,
        ps.id,
        data.name,
        data.date_mise_en_service,
        data.country.code_pays,
        data.ges_option,
        data.site_id,
        data.city,
        data.postal_code,
        data.eligible_dc,
        data.dc_reference,
        data.manager_name,
        data.manager_phone,
        data.manager_email
      )

      const mps = data.matieres_premieres.map((mp) => mp.code)
      await resolveSetProductionSiteMP(entityID, ps.id, mps)

      const bcs = data.biocarburants.map((bc) => bc.code)
      await resolveSetProductionSiteBC(entityID, ps.id, bcs)

      const cs = data.certificates.map((c) => c.certificate_id)
      await resolveSetProductionSiteCertificates(entityID, ps.id, cs)

      if (res) {
        refresh()

        notifications.push({
          level: "success",
          text: t("Le site de production a bien été modifié !"),
        })
      } else {
        notifications.push({
          level: "error",
          text: t("Impossible de modifier le site de production."),
        })
      }
    }
  }

  async function removeProductionSite(ps: ProductionSiteDetails) {
    if (
      await confirm(
        t("Suppression site"),
        t("Voulez-vous vraiment supprimer le site de production {{site}} ?", { site: ps.name }) // prettier-ignore
      )
    ) {
      const res = await resolveDelProductionSite(entityID, ps.id)

      if (res) {
        refresh()

        notifications.push({
          level: "success",
          text: t("Le site de production a bien été supprimé !"),
        })
      } else {
        notifications.push({
          level: "error",
          text: t("Impossible de supprimer le site de production"),
        })
      }
    }
  }

  useEffect(() => {
    if (typeof entityID !== "undefined") {
      resolveGetProductionSites(entityID)
    }
  }, [entityID, resolveGetProductionSites])

  return {
    isEmpty,
    isLoading,
    productionSites,
    createProductionSite,
    editProductionSite,
    removeProductionSite,
    refresh,
  }
}
