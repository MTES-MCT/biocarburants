import React from "react"

import {
  TransactionDetailsHook,
  TransactionFormState,
} from "../hooks/use-transaction-details"

import styles from "./transaction-form.module.css"

import {
  findBiocarburants,
  findCountries,
  findEntities,
  findMatieresPremieres,
  findProducers,
  findProductionSites,
  findDeliverySites,
} from "../services/common"

import { Box, LabelCheckbox, LabelInput, LabelTextArea } from "./system"
import AutoComplete from "./system/autocomplete"

// shorthand to build autocomplete value & label getters
const get = (key: string) => (obj: { [k: string]: any } | null) =>
  obj && key in obj ? String(obj[key]) : ""

type TransactionFormProps = {
  readOnly?: boolean
  transaction: TransactionFormState
  children: React.ReactNode
  onChange: TransactionDetailsHook[1]
  onSubmit?: (e: React.FormEvent<HTMLFormElement>) => void
}

const TransactionForm = ({
  children,
  readOnly = false,
  transaction: tr,
  onChange,
  onSubmit,
}: TransactionFormProps) => {
  function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    onSubmit && onSubmit(e)
  }

  return (
    <form className={styles.transactionForm} onSubmit={submit}>
      <div className={styles.transactionFields}>
        <Box>
          <AutoComplete
            readOnly={readOnly}
            label="Producteur"
            name="carbure_producer"
            value={tr.carbure_producer}
            getValue={get("id")}
            getLabel={get("name")}
            getQuery={findProducers}
            onChange={onChange}
          />
          <AutoComplete
            readOnly={readOnly}
            label="Site de production"
            name="carbure_production_site"
            value={tr.carbure_production_site}
            getValue={get("id")}
            getLabel={get("name")}
            getQuery={findProductionSites}
            onChange={onChange}
          />
          <LabelInput
            readOnly={readOnly}
            type="number"
            label="Volume à 20°C en Litres"
            name="volume"
            value={tr.volume}
            onChange={onChange}
          />
          <AutoComplete
            readOnly={readOnly}
            label="Biocarburant"
            name="biocarburant"
            value={tr.biocarburant}
            getValue={get("code")}
            getLabel={get("name")}
            getQuery={findBiocarburants}
            onChange={onChange}
          />
          <AutoComplete
            readOnly={readOnly}
            label="Matiere Premiere"
            name="matiere_premiere"
            value={tr.matiere_premiere}
            getValue={get("code")}
            getLabel={get("name")}
            getQuery={findMatieresPremieres}
            onChange={onChange}
          />
          <AutoComplete
            readOnly={readOnly}
            label="Pays d'origine"
            name="pays_origine"
            value={tr.pays_origine}
            getValue={get("code_pays")}
            getLabel={get("name")}
            getQuery={findCountries}
            onChange={onChange}
          />
        </Box>

        <Box className={styles.middleColumn}>
          <LabelInput
            readOnly={readOnly}
            label="Numéro douanier (DAE, DAA...)"
            name="dae"
            value={tr.dae}
            onChange={onChange}
          />
          <AutoComplete
            readOnly={readOnly}
            label="Client"
            name="carbure_client"
            value={tr.client}
            getValue={get("id")}
            getLabel={get("name")}
            getQuery={findEntities}
            onChange={onChange}
          />
          <AutoComplete
            readOnly={readOnly}
            label="Site de livraison"
            name="delivery_site"
            value={tr.delivery_site}
            getValue={get("depot_id")}
            getLabel={get("name")}
            getQuery={findDeliverySites}
            onChange={onChange}
          />
          <LabelInput
            readOnly={readOnly}
            type="date"
            label="Date de livraison"
            name="delivery_date"
            value={tr.delivery_date}
            onChange={onChange}
          />
          <LabelTextArea
            label="Champ Libre"
            name="champ_libre"
            value={tr.champ_libre}
            onChange={onChange}
          />
        </Box>

        <Box>
          <div className={styles.transactionGES}>
            <Box>
              <LabelInput
                readOnly={readOnly}
                type="number"
                label="EEC"
                name="eec"
                value={tr.eec}
                step={0.1}
                onChange={onChange}
              />
              <LabelInput
                readOnly={readOnly}
                type="number"
                label="EL"
                name="el"
                value={tr.el}
                step={0.1}
                onChange={onChange}
              />
              <LabelInput
                readOnly={readOnly}
                type="number"
                label="EP"
                name="ep"
                value={tr.ep}
                step={0.1}
                onChange={onChange}
              />
              <LabelInput
                readOnly={readOnly}
                type="number"
                label="ETD"
                name="etd"
                value={tr.etd}
                step={0.1}
                onChange={onChange}
              />
            </Box>

            <Box>
              <LabelInput
                readOnly={readOnly}
                type="number"
                label="ESCA"
                name="esca"
                value={tr.esca}
                step={0.1}
                onChange={onChange}
              />
              <LabelInput
                readOnly={readOnly}
                type="number"
                label="ECCS"
                name="eccs"
                value={tr.eccs}
                step={0.1}
                onChange={onChange}
              />
              <LabelInput
                readOnly={readOnly}
                type="number"
                label="ECCR"
                name="eccr"
                value={tr.eccr}
                step={0.1}
                onChange={onChange}
              />
              <LabelInput
                readOnly={readOnly}
                type="number"
                label="EEE"
                name="eee"
                value={tr.eee}
                step={0.1}
                onChange={onChange}
              />
            </Box>
          </div>

          <LabelInput
            readOnly={readOnly}
            type="number"
            label="EU"
            name="eu"
            value={tr.eu}
            step={0.1}
            className={styles.transactionTotal}
            onChange={onChange}
          />

          <LabelCheckbox
            name="mac"
            label="Mise à consommation ?"
            checked={tr.mac}
            className={styles.transactionMAC}
            onChange={onChange}
          />
        </Box>
      </div>

      <div className={styles.transactionFormButtons}>{children}</div>
    </form>
  )
}

export default TransactionForm
