import React from "react"

import { Lots, LotStatus, Transaction } from "common/types"
import { SortingSelection } from "transactions/hooks/query/use-sort-by" // prettier-ignore
import { TransactionSelection } from "transactions/hooks/query/use-selection"
import { StatusSelection } from "transactions/hooks/query/use-status"

import { useRelativePush } from "common/components/relative-route"

import Table, { Actions, arrow, Column, Row } from "common/components/table"
import * as C from "transactions/components/list-columns"
import { Edit } from "common/components/icons"
import { LotSender } from "stocks/hooks/use-send-lots"

type A = Record<string, (id: number) => void>
type CT = Column<Transaction>

const getStockActions = ({ createDrafts, convertETBE }: A): CT =>
  Actions((tx: Transaction) => {
    const actions = [
      {
        icon: Edit,
        title: "Préparer l'envoi",
        action: (tx: Transaction) => createDrafts(tx.id),
      },
    ]

    return actions
  })

type StockTableProps = {
  stock: Lots | null
  status: StatusSelection
  sorting: SortingSelection
  selection: TransactionSelection
  sender: LotSender
}

export const StockTable = ({
  stock,
  status,
  sorting,
  selection,
  sender,
}: StockTableProps) => {
  const relativePush = useRelativePush()
  const createDrafts = sender.createDrafts

  const columns = []

  if (status.is(LotStatus.Inbox)) {
    columns.push(
      C.selector(selection),
      C.periodSimple,
      C.dae,
      C.biocarburant,
      C.matierePremiere,
      C.vendor,
      C.origine,
      C.depot,
      C.ghgReduction,
      arrow
    )
  }

  if (status.is(LotStatus.Stock)) {
    columns.push(
      C.selector(selection),
      C.periodSimple,
      C.carbureID,
      C.biocarburantInStock,
      C.matierePremiere,
      C.vendor,
      C.origine,
      C.depot,
      C.ghgReduction,
      getStockActions({ createDrafts })
    )
  }

  if (status.is(LotStatus.ToSend)) {
    columns.push(
      C.selector(selection),
      C.periodSimple,
      C.dae,
      C.biocarburant,
      C.matierePremiere,
      C.client,
      C.origine,
      C.destination,
      C.ghgReduction,
      arrow
    )
  }

  if (stock === null) {
    return null
  }

  const rows: Row<Transaction>[] = stock.lots.map((tx) => ({
    value: tx,
    onClick: () => relativePush(`${tx.id}`),
  }))

  return (
    <Table
      columns={columns}
      rows={rows}
      sortBy={sorting.column}
      order={sorting.order}
      onSort={sorting.sortBy}
    />
  )
}
