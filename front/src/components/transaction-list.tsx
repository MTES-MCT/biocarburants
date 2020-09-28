import React from "react"
import cl from "clsx"
import { useHistory } from "react-router-dom"

import { Lot, Lots, LotStatus } from "../services/types"
import { PageSelection } from "../hooks/use-transactions"

import styles from "./transaction-list.module.css"

import { truncate } from "../utils/format"
import { getStatus } from "../services/lots"

import { Alert, Box, Table } from "./system"
import { AlertCircle, Check, ChevronRight, Copy, Cross } from "./system/icons"
import Pagination from "./pagination"

const COLUMNS = [
  "Statut",
  "Date d'ajout",
  "N° Douane",
  "Client",
  "Biocarburant",
  "Provenance",
  "Destination",
  "Mat. Première",
  "Économie",
]

const STATUS = {
  [LotStatus.Draft]: "Brouillon",
  [LotStatus.Validated]: "Envoyé",
  [LotStatus.ToFix]: "À corriger",
  [LotStatus.Accepted]: "Accepté",
  [LotStatus.Weird]: "Problème",
}

const Status = ({ value }: { value: LotStatus }) => (
  <span
    className={cl(styles.status, {
      [styles.statusValidated]: value === LotStatus.Validated,
      [styles.statusToFix]: value === LotStatus.ToFix,
      [styles.statusAccepted]: value === LotStatus.Accepted,
    })}
  >
    {STATUS[value]}
  </span>
)

const Line = ({ text, small = false }: { text: string; small?: boolean }) => (
  <span title={text} className={cl(small && styles.extraInfo)}>
    {truncate(text, small ? 40 : 18)}
  </span>
)

const TwoLines = ({ top, bottom }: { top: string; bottom: string }) => (
  <div className={styles.dualRow}>
    <Line text={top} />
    <Line small text={bottom} />
  </div>
)

const TransactionRow = ({ transaction }: { transaction: Lot }) => {
  const history = useHistory()

  return (
    <tr
      className={styles.transactionRow}
      onClick={() => history.push(`/transactions/${transaction.lot.id}`)}
    >
      <td>
        <input type="checkbox" name={transaction.dae} />
      </td>

      <td>
        <Status value={getStatus(transaction)} />
      </td>

      <td>
        <Line text={transaction.lot.period} />
      </td>

      <td>
        <Line text={transaction.dae} />
      </td>

      <td>
        <Line
          text={transaction.carbure_client?.name ?? transaction.unknown_client}
        />
      </td>

      <td>
        <TwoLines
          top={transaction.lot.biocarburant.name}
          bottom={`${transaction.lot.volume}L`}
        />
      </td>

      <td>
        <TwoLines
          top={
            transaction.lot.carbure_producer?.name ??
            transaction.lot.unknown_producer
          }
          bottom={
            transaction.lot.carbure_production_site?.country.name ??
            transaction.lot.unknown_production_country
          }
        />
      </td>

      <td>
        <TwoLines
          top={
            transaction.carbure_delivery_site?.city ??
            transaction.unknown_delivery_site
          }
          bottom={
            transaction.carbure_delivery_site?.country.name ??
            transaction.unknown_delivery_site_country?.name
          }
        />
      </td>

      <td>
        <TwoLines
          top={transaction.lot.matiere_premiere.name}
          bottom={transaction.lot.pays_origine.name}
        />
      </td>

      <td>
        <Line text={`${transaction.lot.ghg_reduction}%`} />
      </td>

      <td className={styles.actionColumn}>
        <ChevronRight className={styles.transactionArrow} />

        <div className={styles.transactionActions}>
          <Copy size={20} title="Dupliquer le lot" />
          <Check size={20} title="Valider le lot" />
          <Cross size={20} title="Supprimer le lot" />
        </div>
      </td>
    </tr>
  )
}

type TransactionListProps = {
  transactions: Lots | null
  pagination: PageSelection
}

const TransactionList = ({
  transactions,
  pagination,
}: TransactionListProps) => {
  if (transactions === null || transactions.lots.length === 0) {
    return (
      <Box className={styles.transactionList}>
        <Alert type="warning">
          <AlertCircle />
          Aucune transaction trouvée pour ces paramètres
        </Alert>
      </Box>
    )
  }

  return (
    <Box className={styles.transactionList}>
      <Table columns={COLUMNS} rows={transactions.lots}>
        {(transaction) => (
          <TransactionRow key={transaction.lot.id} transaction={transaction} />
        )}
      </Table>

      <Pagination
        page={pagination.selected.page}
        limit={pagination.selected.limit}
        total={transactions.total}
        onChange={pagination.setPage}
      />
    </Box>
  )
}

export default TransactionList
