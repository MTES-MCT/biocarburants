import React from "react"

import { Country, DepotType, OwnershipType } from "common/types"
import {
  DeliverySiteSettingsHook,
  EntityDeliverySite,
} from "../hooks/use-delivery-sites"

import styles from "./settings.module.css"

import * as common from "common/api"

import {
  Title,
  Button,
  LabelInput,
  Box,
  LoaderOverlay,
  Label,
} from "common/system"
import { AlertCircle, Cross, Plus, Return } from "common/system/icons"
import { Alert } from "common/system/alert"
import Table, { Actions, Column, Line, Row } from "common/system/table"
import { SectionHeader, SectionBody, Section } from "common/system/section"
import { DialogButtons, PromptFormProps } from "common/system/dialog"
import { LabelAutoComplete } from "common/system/autocomplete"
import RadioGroup from "common/system/radio-group"
import { EMPTY_COLUMN, SettingsForm } from "./common"
import useForm from "common/hooks/helpers/use-form"

const DEPOT_TYPE_LABELS = {
  [DepotType.EFS]: "EFS",
  [DepotType.EFPE]: "EFPE",
  [DepotType.Other]: "Autre",
}

const OWNERSHIP_LABELS = {
  [OwnershipType.Own]: "Propre",
  [OwnershipType.ThirdParty]: "Tiers",
}

// prettier-ignore
const DEPOT_TYPES = Object.entries(DEPOT_TYPE_LABELS)
  .map(([value, label]) => ({ value, label }))

// prettier-ignore
const OWNERSHIP_TYPES = Object.entries(OWNERSHIP_LABELS)
  .map(([value, label]) => ({ value, label }))

export const DeliverySiteFinderPromptFactory = (entityID?: number) =>
  function DeliverySiteFinderPrompt({
    onConfirm,
    onCancel,
  }: PromptFormProps<EntityDeliverySite>) {
    const [form, hasChange, onChange] = useForm<EntityDeliverySite>({
      depot: null,
      ownership_type: OwnershipType.ThirdParty,
    })

    return (
      <SettingsForm>
        <LabelAutoComplete
          label="Dépôt"
          placeholder="Rechercher un dépôt..."
          name="depot"
          value={form.depot}
          getQuery={common.findDeliverySites}
          onChange={onChange}
          getValue={(d) => d.depot_id}
          getLabel={(d) => d.name}
          queryArgs={[entityID]}
        />

        <Label label="Propriété">
          <RadioGroup
            row
            value={form.ownership_type}
            name="ownership_type"
            options={OWNERSHIP_TYPES}
            onChange={onChange}
          />
        </Label>

        <a
          href="mailto:carbure@beta.gouv.fr"
          target="_blank"
          rel="noreferrer"
          className={styles.settingsLink}
        >
          Le dépôt que je recherche n'est pas enregistré sur CarbuRe.
        </a>

        <DialogButtons>
          <Button
            level="primary"
            icon={Plus}
            disabled={!hasChange}
            onClick={() => onConfirm(form)}
          >
            Ajouter
          </Button>
          <Button onClick={onCancel}>Annuler</Button>
        </DialogButtons>
      </SettingsForm>
    )
  }

type DeliverySiteState = {
  name: string
  city: string
  country: Country | null
  depot_id: string
  depot_type: DepotType
  address: string
  postal_code: string
  ownership_type: OwnershipType
}

export const DeliverySitePromptFactory = (deliverySite?: EntityDeliverySite) =>
  function DeliverySitePrompt({
    onCancel,
  }: PromptFormProps<DeliverySiteState>) {
    const form: DeliverySiteState = {
      name: deliverySite?.depot?.name ?? "",
      city: deliverySite?.depot?.city ?? "",
      country: deliverySite?.depot?.country ?? null,
      depot_id: deliverySite?.depot?.depot_id ?? "",
      depot_type: deliverySite?.depot?.depot_type ?? DepotType.Other,
      address: deliverySite?.depot?.address ?? "",
      postal_code: deliverySite?.depot?.postal_code ?? "",
      ownership_type: deliverySite?.ownership_type ?? OwnershipType.Own,
    }

    return (
      <SettingsForm>
        <hr />

        <Label label="Propriété">
          <RadioGroup
            row
            readOnly
            value={form.ownership_type}
            name="ownership_type"
            options={OWNERSHIP_TYPES}
          />
        </Label>

        <hr />

        <LabelInput
          readOnly
          label="Nom du site"
          name="name"
          defaultValue={form.name}
        />
        <LabelInput
          readOnly
          label="ID de douane"
          name="depot_id"
          defaultValue={form.depot_id}
        />

        <hr />

        <Label label="Type de dépôt">
          <RadioGroup
            row
            readOnly
            value={form.depot_type}
            name="depot_type"
            options={DEPOT_TYPES}
          />
        </Label>

        <hr />

        <LabelInput
          readOnly
          label="Adresse"
          name="address"
          defaultValue={form.address}
        />

        <Box row>
          <LabelInput
            readOnly
            label="Ville"
            name="city"
            defaultValue={form.city}
          />
          <LabelInput
            readOnly
            label="Code postal"
            name="postal_code"
            defaultValue={form.postal_code}
          />
        </Box>

        <LabelInput
          readOnly
          label="Pays"
          placeholder="Rechercher un pays..."
          name="country"
          defaultValue={form.country?.name}
        />

        <hr />

        <DialogButtons>
          <Button icon={Return} onClick={onCancel}>
            Retour
          </Button>
        </DialogButtons>
      </SettingsForm>
    )
  }

const DELIVERY_SITE_COLUMNS: Column<EntityDeliverySite>[] = [
  EMPTY_COLUMN,
  {
    header: "ID",
    render: (ds) => <Line text={ds.depot!.depot_id} />,
  },
  {
    header: "Nom",
    className: styles.settingsTableColumn,
    render: (ds) => <Line text={ds.depot!.name} />,
  },
  {
    header: "Type",
    render: (ds) => <Line text={DEPOT_TYPE_LABELS[ds.depot!.depot_type]} />,
  },
  {
    header: "Ville",
    className: styles.settingsTableColumn,
    render: (ds) => (
      <Line text={`${ds.depot!.city}, ${ds.depot!.country.name}`} />
    ),
  },
]

type DeliverySitesSettingsProps = {
  settings: DeliverySiteSettingsHook
}

const DeliverySitesSettings = ({ settings }: DeliverySitesSettingsProps) => {
  const columns: Column<EntityDeliverySite>[] = [
    ...DELIVERY_SITE_COLUMNS,
    Actions([
      {
        icon: Cross,
        title: "Supprimer le dépôt",
        action: (ds) => settings.deleteDeliverySite(ds),
      },
    ]),
  ]

  const rows: Row<EntityDeliverySite>[] = settings.deliverySites.map((ds) => ({
    value: ds,
    onClick: () => settings.showDeliverySite(ds),
  }))

  return (
    <Section>
      <SectionHeader>
        <Title>Dépôts</Title>
        <Button level="primary" icon={Plus} onClick={settings.addDeliverySite}>
          Ajouter un dépôt
        </Button>
      </SectionHeader>

      {settings.isEmpty && (
        <SectionBody>
          <Alert icon={AlertCircle} level="warning">
            Aucun dépôt trouvé
          </Alert>
        </SectionBody>
      )}

      {!settings.isEmpty && (
        <Table columns={columns} rows={rows} className={styles.settingsTable} />
      )}

      {settings.isLoading && <LoaderOverlay />}
    </Section>
  )
}

export default DeliverySitesSettings