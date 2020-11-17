import { useEffect } from "react"

import { EntitySelection } from "../helpers/use-entity"
import { ISCCCertificate } from "../../services/types"

import { confirm, prompt } from "../../components/system/dialog"
import * as api from "../../services/settings"
import useAPI from "../helpers/use-api"
import { ISCCPrompt } from "../../components/settings/iscc-certificates-settings"

export interface ISCCCertificateSettingsHook {
  isEmpty: boolean
  isLoading: boolean
  certificates: ISCCCertificate[]
  addISCCCertificate: () => void
  deleteISCCCertificate: (d: ISCCCertificate) => void
}

export default function useISCCCertificates(
  entity: EntitySelection
): ISCCCertificateSettingsHook {
  const [requestGetISCC, resolveGetISCC] = useAPI(api.getISCCCertificates)
  const [requestAddISCC, resolveAddISCC] = useAPI(api.addISCCCertificate)
  const [requestDelISCC, resolveDelISCC] = useAPI(api.deleteISCCCertificate)

  const entityID = entity?.id
  const certificates = requestGetISCC.data ?? []

  const isLoading =
    requestGetISCC.loading || requestAddISCC.loading || requestDelISCC.loading

  const isEmpty = certificates.length === 0

  function refresh() {
    if (entityID) {
      resolveGetISCC(entityID)
    }
  }

  async function addISCCCertificate() {
    const data = await prompt(
      "Ajouter un certificat ISCC",
      "Vous pouvez rechercher parmi les certificats recensés sur Carbure et ajouter celui qui vous correspond.",
      ISCCPrompt
    )

    if (entityID && data) {
      resolveAddISCC(entityID, data.certificate_id).then(() =>
        resolveGetISCC(entityID)
      )
    }
  }

  async function deleteISCCCertificate(iscc: ISCCCertificate) {
    if (
      entityID &&
      (await confirm(
        "Suppresion certificat",
        `Voulez-vous vraiment supprimer le certificat ISCC "${iscc.certificate_id}" ?`
      ))
    ) {
      resolveDelISCC(entityID, iscc.certificate_id).then(refresh)
    }
  }

  useEffect(() => {
    if (entityID) {
      resolveGetISCC(entityID)
    }
  }, [entityID, resolveGetISCC])

  return {
    isLoading,
    isEmpty,
    certificates,
    addISCCCertificate,
    deleteISCCCertificate,
  }
}