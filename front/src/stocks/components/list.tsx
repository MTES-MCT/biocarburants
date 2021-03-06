import React from "react"
import { Trans } from "react-i18next"

import {
  LotStatus,
  TransactionQuery,
  TransactionSummary,
  UserRole,
} from "common/types"
import { SortingSelection } from "transactions/hooks/query/use-sort-by"
import { PageSelection } from "common/components/pagination"
import { LotUploader } from "transactions/hooks/actions/use-upload-file"
import { LotDeleter } from "transactions/hooks/actions/use-delete-lots"
import { LotValidator } from "transactions/hooks/actions/use-validate-lots"
import { LotDuplicator } from "transactions/hooks/actions/use-duplicate-lots"
import { LotAcceptor } from "transactions/hooks/actions/use-accept-lots"
import { LotRejector } from "transactions/hooks/actions/use-reject-lots"
import { LotSender } from "stocks/hooks/use-send-lots"
import { StatusSelection } from "transactions/hooks/query/use-status"
import { TransactionSelection } from "transactions/hooks/query/use-selection"
import { StockHook } from "../hooks/use-stock-list"
import {
  NoResult,
  SummaryFilter,
} from "transactions/components/list-special-filters"

import { AlertCircle } from "common/components/icons"
import { Box, LoaderOverlay } from "common/components"
import { Alert } from "common/components/alert"
import Pagination from "common/components/pagination"

import {
  ActionBar,
  ExportActions,
  InboxActions,
} from "transactions/components/list-actions"

import {
  StockActions,
  StockImportActions,
  StockDraftActions,
} from "./list-actions"
import { StockTable } from "./list-table"

import styles from "./list.module.css"
import { SearchSelection } from "transactions/hooks/query/use-search"
import { useRights } from "carbure/hooks/use-rights"
import { EntitySelection } from "carbure/hooks/use-entity"
import { ApiState } from "common/hooks/use-api"
import { FilterSelection } from "transactions/hooks/query/use-filters"

type StockListProps = {
  stock: StockHook
  sorting: SortingSelection
  pagination: PageSelection
  search: SearchSelection
  filters: FilterSelection
  status: StatusSelection
  selection: TransactionSelection
  deleter: LotDeleter
  uploader: LotUploader
  validator: LotValidator
  acceptor: LotAcceptor
  rejector: LotRejector
  duplicator: LotDuplicator
  sender: LotSender
  summary: ApiState<TransactionSummary>
  entity: EntitySelection
  query: TransactionQuery
}

export const StockList = ({
  stock,
  sorting,
  pagination,
  search,
  filters,
  status,
  selection,
  deleter,
  uploader,
  acceptor,
  rejector,
  sender,
  summary,
  entity,
  query,
}: StockListProps) => {
  const rights = useRights()

  const txs = stock.data
  const isLoading = stock.loading
  const isError = typeof stock.error === "string"
  const isEmpty = txs === null || txs.lots.length === 0

  const canModify = rights.is(UserRole.Admin, UserRole.ReadWrite)
  const filterCount = Object.values(filters.selected).filter(Boolean).length

  return (
    <Box className={styles.stockList}>
      {isError && (
        <Alert level="error" icon={AlertCircle}>
          {stock.error}
        </Alert>
      )}

      {!isError && (
        <ActionBar search={search}>
          <ExportActions
            isEmpty={isEmpty}
            onExportAll={stock.exportAllTransactions}
          />

          {canModify && status.is(LotStatus.ToSend) && (
            <StockImportActions uploader={uploader} />
          )}

          {canModify && status.is(LotStatus.ToSend) && (
            <StockDraftActions
              disabled={isEmpty}
              hasSelection={selection.selected.length > 0}
              uploader={uploader}
              deleter={deleter}
              sender={sender}
            />
          )}

          {canModify && status.is(LotStatus.Inbox) && (
            <InboxActions
              disabled={isEmpty}
              hasSelection={selection.selected.length > 0}
              acceptor={acceptor}
              rejector={rejector}
            />
          )}

          {canModify && status.is(LotStatus.Stock) && (
            <StockActions
              onForward={sender.forwardLots}
              onConvertETBE={sender.convertETBEComplex}
            />
          )}
        </ActionBar>
      )}

      {!isEmpty && (
        <SummaryFilter
          stock
          filterCount={filterCount}
          loading={summary.loading}
          txCount={summary.data?.tx_ids.length ?? 0}
          totalVolume={summary.data?.total_volume ?? 0}
          query={query}
          selection={selection.selected}
          entity={entity}
          onReset={() => {
            filters.reset()
            selection.reset()
            search.setQuery("")
          }}
        />
      )}

      {!isError && isEmpty && (
        <NoResult
          loading={isLoading}
          filterCount={filterCount}
          onReset={filters.reset}
        />
      )}

      {!isError && !isEmpty && (
        <React.Fragment>
          <Box>
            <StockTable
              stock={txs!}
              sorting={sorting}
              status={status}
              selection={selection}
              sender={sender}
            />
            {isLoading && <LoaderOverlay />}
          </Box>

          <Pagination pagination={pagination} total={txs!.total} />
        </React.Fragment>
      )}
    </Box>
  )
}
