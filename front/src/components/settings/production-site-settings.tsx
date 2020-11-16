import React, { useEffect } from "react"

import { EntitySelection } from "../../hooks/helpers/use-entity"
import {
  Biocarburant,
  Country,
  MatierePremiere,
  ProductionSite,
} from "../../services/types"

import styles from "./settings.module.css"

import * as api from "../../services/settings"
import * as common from "../../services/common"
import useAPI from "../../hooks/helpers/use-api"
import useForm from "../../hooks/helpers/use-form"

import { Title, Box, Button, LabelInput, LoaderOverlay, Label } from "../system"
import { AlertCircle, Cross, Plus } from "../system/icons"
import { Alert } from "../system/alert"
import Table, { Actions, Column, Line, Row } from "../system/table"

import { SectionHeader, SectionBody, Section } from "../system/section"
import { confirm, prompt, PromptFormProps } from "../system/dialog"
import { LabelAutoComplete, MultiAutocomplete } from "../system/autocomplete"
import { EMPTY_COLUMN } from "."

type ProductionSiteState = {
  name: string
  country: Country | null
  date_mise_en_service: string
  matieres_premieres: MatierePremiere[]
  biocarburants: Biocarburant[]
}

const ProductionSitePrompt = ({
  onConfirm,
  onCancel,
}: PromptFormProps<ProductionSiteState>) => {
  const [productionSite, hasChanged, onChange] = useForm<ProductionSiteState>({
    name: "",
    country: null,
    date_mise_en_service: "",
    matieres_premieres: [],
    biocarburants: [],
  })

  const canSave = Boolean(
    hasChanged &&
      productionSite.country &&
      productionSite.date_mise_en_service &&
      productionSite.name
  )

  return (
    <Box as="form">
      <LabelInput label="Nom du site" name="name" onChange={onChange} />

      <LabelAutoComplete
        label="Pays"
        placeholder="Rechercher un pays..."
        name="country"
        value={productionSite.country}
        getValue={(c) => c?.code_pays ?? ""}
        getLabel={(c) => c?.name ?? ""}
        getQuery={common.findCountries}
        onChange={onChange}
      />

      <LabelInput
        type="date"
        label="Date de mise en service"
        name="date_mise_en_service"
        onChange={onChange}
      />

      <Label label="Matieres premieres">
        <MultiAutocomplete
          value={productionSite.matieres_premieres}
          name="matieres_premieres"
          placeholder="Ajouter matières premières..."
          getValue={(o) => o.code}
          getLabel={(o) => o.name}
          getQuery={common.findMatieresPremieres}
          onChange={onChange}
        />
      </Label>

      <Label label="Biocarburants">
        <MultiAutocomplete
          value={productionSite.biocarburants}
          name="biocarburants"
          placeholder="Ajouter biocarburants..."
          getValue={(o) => o.code}
          getLabel={(o) => o.name}
          getQuery={common.findBiocarburants}
          onChange={onChange}
        />
      </Label>

      <Box row className={styles.dialogButtons}>
        <Button
          level="primary"
          icon={Plus}
          disabled={!canSave}
          onClick={() => productionSite && onConfirm(productionSite)}
        >
          Ajouter
        </Button>
        <Button onClick={onCancel}>Annuler</Button>
      </Box>
    </Box>
  )
}

const PRODUCTION_SITE_COLUMNS: Column<ProductionSite>[] = [
  EMPTY_COLUMN,
  {
    header: "Nom",
    className: styles.settingsTableColumn,
    render: (ps) => <Line text={ps.name} />,
  },
  {
    header: "Pays",
    className: styles.settingsTableColumn,
    render: (ps) => <Line text={ps.country?.name} />,
  },
  {
    header: "Date de mise en service",
    className: styles.settingsTableColumn,
    render: (ps) => <Line text={ps.date_mise_en_service} />,
  },
]
type ProductionSitesSettingsProps = {
  entity: EntitySelection
}

const ProductionSitesSettings = ({ entity }: ProductionSitesSettingsProps) => {
  const [requestGetProductionSites, resolveGetProductionSites] = useAPI(common.findProductionSites) // prettier-ignore
  const [requestAddProductionSite, resolveAddProductionSite] = useAPI(api.addProductionSite) // prettier-ignore
  const [requestDelProductionSite, resolveDelProductionSite] = useAPI(api.deleteProductionSite) // prettier-ignore

  const [requestSetProductionSiteMP, resolveSetProductionSiteMP] = useAPI(api.setProductionSiteMP) // prettier-ignore
  const [requestSetProductionSiteBC, resolveSetProductionSiteBC] = useAPI(api.setProductionSiteBC) // prettier-ignore

  const entityID = entity?.id
  const productionSites = requestGetProductionSites.data ?? []

  const isLoading =
    requestAddProductionSite.loading ||
    requestGetProductionSites.loading ||
    requestDelProductionSite.loading ||
    requestSetProductionSiteBC.loading ||
    requestSetProductionSiteMP.loading

  const isEmpty = productionSites.length === 0

  function refresh() {
    if (entityID) {
      resolveGetProductionSites("", entityID)
    }
  }

  async function createProductionSite() {
    const data = await prompt(
      "Ajout site de production",
      "Veuillez entrer les informations de votre nouveau site de production.",
      ProductionSitePrompt
    )

    if (entityID && data && data.country) {
      const ps = await resolveAddProductionSite(
        entityID,
        data.name,
        data.date_mise_en_service,
        true,
        data.country.code_pays
      )

      if (ps) {
        const mps = data.matieres_premieres.map((mp) => mp.code)
        await resolveSetProductionSiteMP(ps.id, mps)

        const bcs = data.biocarburants.map((bc) => bc.code)
        await resolveSetProductionSiteBC(ps.id, bcs)
      }

      refresh()
    }
  }

  async function removeProductionSite(ps: ProductionSite) {
    if (
      await confirm(
        "Suppression site",
        `Voulez-vous vraiment supprimer le site de production "${ps.name}" ?`
      )
    ) {
      resolveDelProductionSite(ps.id).then(refresh)
    }
  }

  useEffect(() => {
    if (entityID) {
      resolveGetProductionSites("", entityID)
    }
  }, [entityID, resolveGetProductionSites])

  const columns = [
    ...PRODUCTION_SITE_COLUMNS,
    Actions([
      {
        icon: Cross,
        title: "Supprimer le site de production",
        action: removeProductionSite,
      },
    ]),
  ]

  const rows: Row<ProductionSite>[] = productionSites.map((ps) => ({ value: ps })); // prettier-ignore

  return (
    <Section>
      <SectionHeader>
        <Title>Sites de production</Title>
        <Button level="primary" icon={Plus} onClick={createProductionSite}>
          Ajouter un site de production
        </Button>
      </SectionHeader>

      {isEmpty && (
        <SectionBody>
          <Alert icon={AlertCircle} level="warning">
            Aucun site de production trouvé
          </Alert>
        </SectionBody>
      )}

      {!isEmpty && (
        <Table columns={columns} rows={rows} className={styles.settingsTable} />
      )}

      {isLoading && <LoaderOverlay />}
    </Section>
  )
}

export default ProductionSitesSettings