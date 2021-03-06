import React, { Fragment, useEffect, useState } from "react"
import { Trans, useTranslation } from "react-i18next"

import { LotStatus, Transaction, ConvertETBE } from "common/types"
import useForm from "common/hooks/use-form"
import { Box, LoaderOverlay } from "common/components"
import { Input, LabelInput } from "common/components/input"
import { Button } from "common/components/button"
import { Alert } from "common/components/alert"
import { Check, AlertCircle } from "common/components/icons"
import {
  Dialog,
  DialogButtons,
  DialogTitle,
  PromptProps,
} from "common/components/dialog"
import Select from "common/components/select"
import useAPI from "common/hooks/use-api"
import Table, { Column } from "common/components/table"
import * as C from "transactions/components/list-columns"
import * as api from "../api"
import { prettyVolume } from "transactions/helpers"

const PART_ETH_IN_ETBE = 0.47
const CONVERT_20_TO_15 = 0.995

function compareVolumes(volume: number, attributions: VolumeAttributions) {
  let total_attributions = Object.values(attributions).reduce(
    (total, vol) => total + vol,
    0
  )

  return volume - total_attributions
}

const initialState: ConvertETBE = {
  volume_etbe: 0,
  volume_etbe_eligible: 0,
  volume_ethanol: 0,
  volume_denaturant: 0,
}

type ConvertETBEPromptProps = PromptProps<ConvertETBE[]> & {
  entityID: number
}

type VolumeAttributions = {
  [key: number]: number
}

export const ConvertETBEComplexPrompt = ({
  entityID,
  onResolve,
}: ConvertETBEPromptProps) => {
  const { t } = useTranslation()
  const [depot, setDepot] = useState<string | null>(null)

  const [attributions, setAttributions] = useState<VolumeAttributions>({})

  const [depots, getDepots] = useAPI(api.getDepots)
  const [stocks, getStocks] = useAPI(api.getStocks)

  const lots = stocks.data?.lots ?? []
  const vEthanolInStock = lots.reduce((t, tx) => t + tx.lot.remaining_volume, 0)

  const { data, hasChange, onChange } = useForm<ConvertETBE>(initialState)

  useEffect(() => {
    getDepots(entityID, "ETH")
  }, [getDepots, entityID])

  useEffect(() => {
    if (depot) {
      getStocks({
        status: LotStatus.Stock,
        entity_id: entityID,
        delivery_sites: [depot],
        biocarburants: ["ETH"],
      })
    }
  }, [getStocks, entityID, depot])

  const volumeDiff = compareVolumes(data.volume_ethanol, attributions)
  const canSave = hasChange && volumeDiff === 0

  function handleAttribution(tx: Transaction) {
    return (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value
      let nextAttributions: VolumeAttributions

      if (value === "") {
        nextAttributions = { ...attributions }
        delete nextAttributions[tx.id]
      } else {
        const volume = Math.min(parseFloat(value), tx.lot.remaining_volume)
        nextAttributions = {
          ...attributions,
          [tx.id]: volume,
        }
      }

      setAttributions(nextAttributions)
    }
  }

  const convertedVolume: Column<Transaction> = {
    header: t("Volume à convertir"),
    render: (tx) => (
      <Input
        type="number"
        min={0}
        max={tx.lot.remaining_volume}
        value={attributions[tx.id]}
        onChange={handleAttribution(tx)}
      />
    ),
  }

  const columns = [
    C.padding,
    C.carbureID(t),
    C.biocarburantInStock(t),
    C.matierePremiere(t),
    convertedVolume,
    C.ghgReduction(t),
    C.padding,
  ]

  const rows = lots.map((stock) => ({ value: stock }))

  const usedVolume =
    data.volume_ethanol * CONVERT_20_TO_15 + data.volume_denaturant
  const ratio = usedVolume / data.volume_etbe

  const volEligibleETBE = data.volume_etbe * (ratio / PART_ETH_IN_ETBE)

  const ratioEthToETBE = (data.volume_ethanol / data.volume_etbe) * 100.0
  const ratioEthToETBEWithDenaturant =
    ((data.volume_ethanol + data.volume_denaturant) / data.volume_etbe) * 100.0

  const conversionDetails = Object.entries(attributions)
    .map<ConvertETBE>(([txID, volume]) => {
      const ratio = volume / data.volume_ethanol
      return {
        volume_ethanol: volume,
        volume_etbe: ratio * data.volume_etbe,
        volume_etbe_eligible: ratio * volEligibleETBE,
        volume_denaturant: ratio * data.volume_denaturant,
        previous_stock_tx_id: parseInt(txID, 10),
      }
    })
    .filter((d) => d.volume_ethanol > 0)

  return (
    <Dialog wide onResolve={onResolve}>
      <DialogTitle text={t("Conversion ETBE")} />

      <Box>
        <Select
          value={depot as any}
          options={(depots.data as any) ?? []}
          placeholder={t("Choisir un dépôt")}
          onChange={setDepot as any}
          style={{ marginTop: 24, marginBottom: 16 }}
        />

        {depot && (
          <Fragment>
            <Box row>
              <LabelInput
                type="number"
                label={t("Volume d'ETBE produit")}
                name="volume_etbe"
                value={data.volume_etbe}
                onChange={onChange}
                style={{ flex: 1, marginRight: 16 }}
              />

              <LabelInput
                readOnly
                disabled
                type="number"
                label={t("Volume d'ETBE éligible (à titre informatif)")}
                name="volume_etbe"
                value={isNaN(volEligibleETBE) ? 0 : volEligibleETBE.toFixed(2)}
                style={{ flex: 1 }}
              />
            </Box>

            <Box row>
              <LabelInput
                type="number"
                label={t(`Volume d'Éthanol utilisé ({{remaining}} litres disponibles)`, { remaining: prettyVolume(vEthanolInStock) })} // prettier-ignore
                name="volume_ethanol"
                value={data.volume_ethanol}
                onChange={onChange}
                style={{ flex: 1, marginRight: 16 }}
              />

              <LabelInput
                type="number"
                label={t("Volume total de dénaturant")}
                name="volume_denaturant"
                value={data.volume_denaturant}
                onChange={onChange}
                style={{ flex: 1 }}
              />
            </Box>

            {!isNaN(ratioEthToETBE) && (
              <Alert
                level="info"
                icon={AlertCircle}
                style={{ marginTop: 8, marginBottom: 16 }}
              >
                <Trans>
                  Ratio d'Éthanol:
                  <b style={{ margin: "0 4px" }}>
                    {{ ratio: ratioEthToETBE.toFixed(2) }}%
                  </b>
                  ({{ fullRatio: ratioEthToETBEWithDenaturant.toFixed(2) }}%
                  dénaturant inclus)
                </Trans>
              </Alert>
            )}
          </Fragment>
        )}

        {!isNaN(volumeDiff) && volumeDiff !== 0 && (
          <Alert level="error" icon={AlertCircle} style={{ marginBottom: 16 }}>
            <Trans>
              Les volumes ne correspondent pas (
              {{ volume: prettyVolume(volumeDiff) }} litres)
            </Trans>
          </Alert>
        )}

        {data.volume_ethanol > data.volume_etbe && (
          <Alert level="error" icon={AlertCircle} style={{ marginBottom: 16 }}>
            <Trans>
              Le volume d'ETBE produit est inférieur au volume d'Éthanol
            </Trans>
          </Alert>
        )}

        {rows.length > 0 && (
          <div style={{ marginLeft: -24, marginRight: -24 }}>
            <Table columns={columns} rows={rows} />
          </div>
        )}

        <DialogButtons>
          <Button
            level="primary"
            icon={Check}
            disabled={!canSave}
            onClick={() => onResolve(conversionDetails)}
          >
            <Trans>Valider</Trans>
          </Button>
          <Button onClick={() => onResolve()}>
            <Trans>Annuler</Trans>
          </Button>
        </DialogButtons>
      </Box>

      {stocks.loading && <LoaderOverlay />}
    </Dialog>
  )
}
