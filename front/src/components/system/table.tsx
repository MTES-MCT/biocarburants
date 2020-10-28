import React from "react"
import cl from "clsx"

import { SystemProps } from "."

import styles from "./table.module.css"

export interface Column<T> {
  /** element displayed in table header */
  header?: React.ReactNode
  /** key by which this column should sort */
  sortBy?: string
  /**  a class for the `<th>` element */
  className?: string
  /** how to render a cell based on the row data */
  render: (row: T) => React.ReactNode
}

export interface Row<T> {
  /** class of the `<tr>` element  */
  className?: string
  /** callback when user clicks on row  */
  onClick?: () => void
  /** raw data for this row  */
  value: T
}

type TableProps<T> = SystemProps & {
  rows: Row<T>[]
  columns: Column<T>[]
  sortBy: string
  order: "asc" | "desc"
  onSort: (s: string) => void
}

export default function Table<T>({
  rows,
  columns,
  sortBy,
  order,
  className,
  onSort,
  ...props
}: TableProps<T>) {
  return (
    <table {...props} className={cl(styles.table, className)}>
      <thead>
        <tr>
          {columns.map((column, c) => (
            <th
              key={c}
              className={column.className}
              onClick={() => column.sortBy && onSort(column.sortBy)}
            >
              {column.header ?? null}
              {sortBy && sortBy === column.sortBy && (
                <span>{order === "asc" ? " ▲" : " ▼"}</span>
              )}
            </th>
          ))}
        </tr>
      </thead>

      <tbody>
        {rows.map((row, r) => (
          <tr key={r} className={row.className} onClick={row.onClick}>
            {columns.map((column, c) => (
              <td key={c} className={column.className}>
                {column.render(row.value)}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}
