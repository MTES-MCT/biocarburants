import React from "react"

import { LotStatus } from "common/types"
import { SortingSelection } from "common/hooks/query/use-sort-by"
import { PageSelection } from "common/system/pagination"
import { LotUploader } from "common/hooks/actions/use-upload-file"
import { LotDeleter } from "common/hooks/actions/use-delete-lots"
import { LotValidator } from "common/hooks/actions/use-validate-lots"
import { LotDuplicator } from "common/hooks/actions/use-duplicate-lots"
import { LotAcceptor } from "common/hooks/actions/use-accept-lots"
import { LotRejector } from "common/hooks/actions/use-reject-lots"
import { LotSender } from "common/hooks/actions/use-send-lots"
import { StatusSelection } from "common/hooks/query/use-status"
import { TransactionSelection } from "common/hooks/query/use-selection"
import { StockHook } from "../hooks/use-stock"

import styles from "./stock-list.module.css"

import { AlertCircle } from "common/system/icons"
import { Box, LoaderOverlay } from "common/system"
import { Alert } from "common/system/alert"
import Pagination from "common/system/pagination"

import {
  ActionBar,
  ExportActions,
  InboxActions,
  InboxSummaryActions,
} from "transactions/components/transaction-actions"

import {
  StockActions,
  StockImportActions,
  StockDraftActions,
} from "./stock-actions"
import { StockTable } from "./stock-table"

type StockListProps = {
  stock: StockHook
  sorting: SortingSelection
  pagination: PageSelection
  status: StatusSelection
  selection: TransactionSelection
  deleter: LotDeleter
  uploader: LotUploader
  validator: LotValidator
  acceptor: LotAcceptor
  rejector: LotRejector
  duplicator: LotDuplicator
  sender: LotSender
}

export const StockList = ({
  stock,
  sorting,
  pagination,
  status,
  selection,
  deleter,
  uploader,
  acceptor,
  rejector,
  sender,
}: StockListProps) => {
  const txs = stock.data

  const isLoading = stock.loading
  const isError = typeof stock.error === "string"
  const isEmpty = txs === null || txs.lots.length === 0

  return (
    <Box className={styles.stockList}>
      {isError && (
        <Alert level="error" icon={AlertCircle}>
          {stock.error}
        </Alert>
      )}

      {!isError && (
        <ActionBar>
          <ExportActions
            isEmpty={isEmpty}
            onExportAll={stock.exportAllTransactions}
          />

          {status.is(LotStatus.Inbox) && <InboxSummaryActions />}

          {status.is(LotStatus.ToSend) && (
            <StockImportActions uploader={uploader} />
          )}

          {status.is(LotStatus.ToSend) && (
            <StockDraftActions
              disabled={isEmpty}
              hasSelection={selection.selected.length > 0}
              uploader={uploader}
              deleter={deleter}
              sender={sender}
            />
          )}

          {status.is(LotStatus.Inbox) && (
            <InboxActions
              disabled={isEmpty}
              hasSelection={selection.selected.length > 0}
              acceptor={acceptor}
              rejector={rejector}
            />
          )}

          {status.is(LotStatus.Stock) && <StockActions />}
        </ActionBar>
      )}

      {!isError && isEmpty && (
        <Alert level="warning" icon={AlertCircle}>
          Aucune transaction trouvée pour ces paramètres
        </Alert>
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