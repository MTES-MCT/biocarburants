import { TransactionSelection } from "../query/use-selection"

import * as api from "transactions/api"
import useAPI from "../../../common/hooks/use-api"

import { useNotificationContext } from "../../../common/components/notifications"
import { TransactionQuery } from "common/types"

export interface LotAdministrator {
  loading: boolean
  markAsRead: (txID: number) => Promise<boolean>
  markForReview: (txID: number) => Promise<boolean>
  hideAlerts: (txIDs: number[]) => Promise<boolean>
  highlightAlerts: (txIDs: number[]) => Promise<boolean>
}

export default function useAdministrateLots(
  selection: TransactionSelection,
  query: TransactionQuery,
  refresh: () => void,
): LotAdministrator {
  const notifications = useNotificationContext()

  const [requestHide, resolveHideLots] = useAPI(api.postHideLots)
  const [requestHighlight, resolveHighlightLots] = useAPI(api.postHighlightLots)
  const [requestHideAlert, resolveHideAlerts] = useAPI(api.postHideAlerts)
  const [requestHighlightAlert, resolveHighlightAlerts] = useAPI(api.postHighlightAlerts)

  async function notify(promise: Promise<any>) {
    const res = await promise

    if (res) {
      refresh()

      notifications.push({
        level: "success",
        text: "Succès"         
      })
    } else {
      notifications.push({
        level: "error",
        text: "Erreur"
      })
    }
  }

  async function markAsRead(txID: number) {
    await notify(resolveHideLots([txID]))
    return true
  }

  async function markForReview(txID: number) {
    await notify(resolveHighlightLots([txID]))
    return true
  }

  async function hideAlerts(alertIDs: number[]) {
    await notify(resolveHideAlerts(alertIDs))
    return true
  }

  async function highlightAlerts(alertIDs: number[]) {
    await notify(resolveHighlightAlerts(alertIDs))
    return true
  }

  return {
    loading: requestHide.loading || requestHideAlert.loading || requestHighlightAlert.loading || requestHighlight.loading,
    markAsRead,
    markForReview,
    hideAlerts,
    highlightAlerts,
  }
}
