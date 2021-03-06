import React, { useEffect, useRef, useState } from "react"
import cl from "clsx"

import styles from "./select.module.css"

import { SystemProps } from "."
import { Checkbox, Input } from "./input"
import { Cross } from "./icons"
import { LoaderOverlay } from "common/components"
import {
  DropdownItem,
  DropdownLabel,
  DropdownOptions,
  useDropdown,
} from "./dropdown"
import { useTranslation } from "react-i18next"
import useAPI from "common/hooks/use-api"

type Value = string | number | boolean | null
export type Option = { value: Value; label: string }
export type SelectValue = Value | Value[] | null

// check if the value is empty
function isEmpty(value: SelectValue) {
  if (Array.isArray(value)) {
    return value.length === 0
  } else {
    return value ?? true
  }
}

// check if the given opton is selected
function isSelected(value: SelectValue, option: Option) {
  if (Array.isArray(value)) {
    return value.includes(option.value)
  } else {
    return value === option.value
  }
}

// combine selected values in one element with their label
function renderSelected(
  value: SelectValue,
  options: Option[],
  placeholder: string
) {
  let selected

  if (Array.isArray(value)) {
    selected = options
      .filter((o) => value.includes(o.value))
      .map((v) => v.label)
      .join(", ")
  } else {
    selected = options.find((o) => o.value === value)?.label
  }

  return selected || placeholder
}

// get only options containing the given query
function filterOptions(options: Option[], query: string) {
  return query.length > 0
    ? options.filter((option) => option.label.toLowerCase().includes(query))
    : options
}

// custom hook  for managing select
function useSelect(
  value: SelectValue,
  placeholder: string | undefined,
  options: Option[],
  onChange: SelectProps["onChange"],
  multiple: boolean
) {
  const { t } = useTranslation()

  const dd = useDropdown()
  const [query, setQuery] = useState("")

  // reset the value, reset the query, close the menu
  function reset(e: React.MouseEvent) {
    e.stopPropagation()
    onChange(null)
    setQuery("")
    dd.toggle(false)
  }

  // select an option
  function select(option: Option, e?: React.MouseEvent) {
    if (!multiple) {
      // single value selection
      return onChange(option.value)
    }

    // prevent closing of option list
    e && e.stopPropagation()

    if (!Array.isArray(value)) {
      onChange([option.value])
    } else if (value.includes(option.value)) {
      onChange(value.filter((key) => key !== option.value))
    } else {
      onChange([...value, option.value])
    }
  }

  function onQueryChange(e: React.ChangeEvent<HTMLInputElement>) {
    setQuery(e.target.value.toLowerCase())
  }

  // what to display in the dropdown label
  const selected = renderSelected(
    value,
    options,
    placeholder ?? t("Choisir une valeur")
  )

  // filter options according to search query
  const queryOptions = filterOptions(options, query)

  return {
    dd,
    selected,
    queryOptions,
    query,
    select,
    reset,
    onQueryChange,
    setQuery,
  }
}

const asycNoop = () => Promise.resolve([])

type SelectProps = SystemProps & {
  above?: boolean
  placeholder?: string
  level?: "primary" | "inline"
  search?: boolean
  multiple?: boolean
  clear?: boolean
  value: SelectValue
  options?: Option[]
  getOptions?: (...a: any[]) => Promise<Option[]>
  getArgs?: any[]
  onChange: (value: SelectValue) => void
}

export const Select = ({
  above,
  value,
  placeholder,
  options: localOptions,
  level,
  className,
  children,
  onChange,
  search = false,
  multiple = false,
  clear = false,
  getOptions = asycNoop,
  getArgs = [],
  ...props
}: SelectProps) => {
  const { t } = useTranslation()

  const [remoteOptions, getRemoteOptions] = useAPI(getOptions)
  const options = localOptions ?? remoteOptions.data ?? []

  const { dd, query, selected, queryOptions, reset, select, onQueryChange } =
    useSelect(value, placeholder, options, onChange, multiple)

  const container = useRef<HTMLDivElement>(null)

  // refresh select option when opened
  useEffect(() => {
    if (dd.isOpen) {
      getRemoteOptions(...getArgs)
    }
  }, [dd.isOpen, getRemoteOptions, ...getArgs]) // eslint-disable-line react-hooks/exhaustive-deps

  // load select options if value is defined but options are not loaded yet
  useEffect(() => {
    if (Array.isArray(value) && value.length > 0 && options.length === 0) {
      getRemoteOptions(...getArgs)
    }
  }, [value, getRemoteOptions, options.length, ...getArgs]) // eslint-disable-line react-hooks/exhaustive-deps

  const isLoading = !Boolean(localOptions) && remoteOptions.loading

  const labelClassName = cl(styles.selectLabel, className, {
    [styles.selectPrimary]: level === "primary",
    [styles.selectInline]: level === "inline",
  })

  return (
    <div {...props} ref={container} onClick={dd.toggle}>
      <DropdownLabel className={labelClassName} onEnter={() => dd.toggle(true)}>
        <span title={selected} className={styles.selectValue}>
          {selected}
        </span>

        {clear && !isEmpty(value) && (
          <Cross className={styles.selectCross} onClick={reset} />
        )}
      </DropdownLabel>

      {dd.isOpen && container.current && (
        <DropdownOptions
          above={above}
          parent={container.current}
          options={queryOptions}
          onChange={select}
        >
          {(options, focused) => (
            <React.Fragment>
              {search && (
                <DropdownItem allowFocus>
                  <Input
                    type="text"
                    placeholder={t("Rechercher...")}
                    className={styles.selectSearch}
                    value={query}
                    onChange={onQueryChange}
                    onClick={(e) => e.stopPropagation()}
                  />
                </DropdownItem>
              )}

              {options.map((option, i) => (
                <DropdownItem
                  key={option.value?.toString() ?? i}
                  title={option.label}
                  focused={focused === i}
                  selected={isSelected(value, option)}
                  onClick={(e) => select(option, e)}
                >
                  {multiple && (
                    <Checkbox
                      readOnly
                      checked={isSelected(value, option)}
                      className={styles.selectMultiple}
                    />
                  )}

                  <span>{option.label}</span>
                </DropdownItem>
              ))}

              {isLoading && <LoaderOverlay />}
            </React.Fragment>
          )}
        </DropdownOptions>
      )}
    </div>
  )
}

export default Select
