import {usePageSelection } from "../../components/system/pagination" // prettier-ignore

import useUploadLotFile from "../actions/use-upload-file"
import useDuplicateLot from "../actions/use-duplicate-lots"
import useDeleteLots from "../actions/use-delete-lots"
import useValidateLots from "../actions/use-validate-lots"

import useFilterSelection from "../query/use-filters"
import useSearchSelection from "../query/use-search"
import useTransactionSelection from "../query/use-selection"
import useSortingSelection from "../query/use-sort-by"
import useStatusSelection from "../query/use-status"
import useYearSelection from "../query/use-year"

import useEntity from "../helpers/use-entity"
import useGetSnapshot from "./use-snapshot"
import useGetLots from "./use-get-lots"

export default function useTransactions() {
  const entity = useEntity()

  const sorting = useSortingSelection()
  const pagination = usePageSelection()

  const status = useStatusSelection(pagination)
  const search = useSearchSelection(pagination)
  const filters = useFilterSelection(pagination)
  const year = useYearSelection(pagination, filters)

  const snapshot = useGetSnapshot(entity, year)
  const transactions = useGetLots(entity, status, filters, year, pagination, search, sorting) // prettier-ignore

  function refresh() {
    snapshot.getSnapshot()
    transactions.getTransactions()
  }

  const selection = useTransactionSelection(transactions.data?.lots)

  const uploader = useUploadLotFile(entity, refresh)
  const duplicator = useDuplicateLot(entity, refresh)
  const deleter = useDeleteLots(entity, selection, year, refresh)
  const validator = useValidateLots(entity, selection, year, refresh)

  return {
    entity,
    status,
    filters,
    year,
    pagination,
    snapshot,
    transactions,
    selection,
    search,
    sorting,
    deleter,
    uploader,
    duplicator,
    validator,
    refresh,
  }
}