import { useEffect } from "react"
import { useTranslation } from "react-i18next"
import { Lots, TransactionQuery } from "common/types"
import * as api from "../api"
import useAPI from "common/hooks/use-api"
import { getStocks, getStockSnapshot } from "../api"
import { EntitySelection } from "carbure/hooks/use-entity"

export interface StockHook {
  loading: boolean
  error: string | null
  data: Lots | null
  getStock: () => void
  exportAllTransactions: () => void
}

export function useGetStockSnapshot(entity: EntitySelection) {
  const { t } = useTranslation()
  const [snapshot, resolveStockSnapshot] = useAPI(getStockSnapshot)

  function getSnapshot() {
    if (entity !== null) {
      resolveStockSnapshot(entity.id, t)
    }
  }

  useEffect(getSnapshot, [resolveStockSnapshot, entity, t])

  return { ...snapshot, getSnapshot }
}

// fetches current transaction list when parameters change
export function useGetStocks(query: TransactionQuery): StockHook {
  const [stock, resolveStocks] = useAPI(getStocks)

  function exportAllTransactions() {
    if (query.entity_id >= 0) {
      api.downloadStocks(query)
    }
  }

  function getStock() {
    if (query.entity_id >= 0) {
      delete query.year
      resolveStocks(query)
    }
  }

  useEffect(getStock, [resolveStocks, query])

  return { ...stock, getStock, exportAllTransactions }
}
