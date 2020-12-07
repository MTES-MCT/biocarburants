import { useState } from "react"

import { PageSelection } from "../../system/pagination"
import { SelectValue } from "../../system/select"
import { Filters } from "../../types"

const defaultState = {}

export interface FilterSelection {
  selected: { [k in Filters]?: SelectValue }
  select: (type: Filters, value: SelectValue) => void
  reset: () => void
}

// manage current filter selection
export default function useFilterSelection(
  pagination: PageSelection
): FilterSelection {
  const [selected, setFilters] = useState<FilterSelection["selected"]>(
    defaultState
  )

  function select(type: Filters, value: SelectValue) {
    pagination.setPage(0)
    setFilters({ ...selected, [type]: value })
  }

  function reset() {
    setFilters(defaultState)
  }

  return { selected, select, reset }
}