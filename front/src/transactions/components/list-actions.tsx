import React from "react"
import cl from "clsx"
import { Trans, useTranslation } from "react-i18next"

import { LotDeleter } from "transactions/hooks/actions/use-delete-lots"
import { LotUploader } from "transactions/hooks/actions/use-upload-file"
import { LotValidator } from "transactions/hooks/actions/use-validate-lots"
import { LotAcceptor } from "transactions/hooks/actions/use-accept-lots"
import { LotRejector } from "transactions/hooks/actions/use-reject-lots"

import { Link } from "common/components/relative-route"
import { Box } from "common/components"
import { AsyncButton, Button } from "common/components/button"
import {
  Check,
  Cross,
  Download,
  Plus,
  Upload,
  Forward,
  Search,
  Pin,
  EyeOff,
} from "common/components/icons"
import { prompt } from "common/components/dialog"

import {
  TraderImportPrompt,
  OperatorImportPrompt,
  ProducerImportPrompt,
} from "./import"
import { OperatorForwardPrompt } from "./forward"

import styles from "./list-actions.module.css"
import { LotForwarder } from "transactions/hooks/actions/use-forward-lots"
import { EntityDeliverySite } from "settings/hooks/use-delivery-sites"
import { TransactionSelection } from "transactions/hooks/query/use-selection"
import { SearchSelection } from "transactions/hooks/query/use-search"
import { Input, InputProps } from "common/components/input"
import { LotAuditor } from "transactions/hooks/actions/use-audits"
import { LotAdministrator } from "transactions/hooks/actions/use-admin-lots"

type ExportActionsProps = {
  isEmpty: boolean
  onExportAll: () => void
}

export const ExportActions = ({ isEmpty, onExportAll }: ExportActionsProps) => (
  <Button icon={Download} disabled={isEmpty} onClick={onExportAll}>
    <Trans>Exporter</Trans>
  </Button>
)

type ImportActionsProps = {
  uploader: LotUploader
}

export const ProducerImportActions = ({ uploader }: ImportActionsProps) => {
  async function onUpload() {
    const file = await prompt<File>((resolve) => (
      <ProducerImportPrompt uploader={uploader} onResolve={resolve} />
    ))

    if (file) {
      uploader.uploadFile(file)
    }
  }

  return (
    <AsyncButton icon={Upload} loading={uploader.loading} onClick={onUpload}>
      <Trans>Importer lots</Trans>
    </AsyncButton>
  )
}
export const TraderImportActions = ({ uploader }: ImportActionsProps) => {
  async function onUpload() {
    const file = await prompt<File>((resolve) => (
      <TraderImportPrompt uploader={uploader} onResolve={resolve} />
    ))

    if (file) {
      uploader.uploadFile(file)
    }
  }

  return (
    <AsyncButton icon={Upload} loading={uploader.loading} onClick={onUpload}>
      <Trans>Importer lots</Trans>
    </AsyncButton>
  )
}

export const OperatorImportActions = ({ uploader }: ImportActionsProps) => {
  async function onUpload() {
    const file = await prompt<File>((resolve) => (
      <OperatorImportPrompt uploader={uploader} onResolve={resolve} />
    ))

    if (file) {
      uploader.uploadOperatorFile(file)
    }
  }

  return (
    <AsyncButton icon={Upload} loading={uploader.loading} onClick={onUpload}>
      <Trans>Importer lots</Trans>
    </AsyncButton>
  )
}

export const CreateActions = () => (
  <Link relative to="add">
    <Button icon={Plus} level="primary">
      <Trans>Créer lot</Trans>
    </Button>
  </Link>
)

type DraftActionsProps = {
  disabled: boolean
  hasSelection: boolean
  uploader: LotUploader
  deleter: LotDeleter
  validator: LotValidator
}

export const DraftActions = ({
  disabled,
  hasSelection,
  deleter,
  validator,
}: DraftActionsProps) => {
  const { t } = useTranslation()

  function onValidate() {
    if (hasSelection) {
      validator.validateSelection()
    } else {
      validator.validateAll()
    }
  }

  function onDelete() {
    if (hasSelection) {
      deleter.deleteSelection()
    } else {
      deleter.deleteAll()
    }
  }

  return (
    <React.Fragment>
      <AsyncButton
        icon={Check}
        level="success"
        loading={validator.loading}
        disabled={disabled}
        onClick={onValidate}
      >
        <Trans>
          Envoyer {{ what: hasSelection ? t("sélection") : t("tout") }}
        </Trans>
      </AsyncButton>

      <AsyncButton
        icon={Cross}
        level="danger"
        loading={deleter.loading}
        disabled={disabled}
        onClick={onDelete}
      >
        <Trans>
          Supprimer {{ what: hasSelection ? t("sélection") : t("tout") }}
        </Trans>
      </AsyncButton>
    </React.Fragment>
  )
}

type ToFixActionsProps = {
  disabled: boolean
  deleter: LotDeleter
}

export const ToFixActions = ({ disabled, deleter }: ToFixActionsProps) => {
  return (
    <AsyncButton
      icon={Cross}
      level="danger"
      loading={deleter.loading}
      disabled={disabled}
      onClick={deleter.deleteSelection}
    >
      <Trans>Supprimer sélection</Trans>
    </AsyncButton>
  )
}

type InboxActionsProps = {
  disabled: boolean
  hasSelection: boolean
  acceptor: LotAcceptor
  rejector: LotRejector
}

export const InboxActions = ({
  disabled,
  hasSelection,
  acceptor,
  rejector,
}: InboxActionsProps) => {
  const { t } = useTranslation()

  function onAccept() {
    if (hasSelection) {
      acceptor.acceptSelection()
    } else {
      acceptor.acceptAllInbox()
    }
  }

  function onReject() {
    if (hasSelection) {
      rejector.rejectSelection()
    } else {
      rejector.rejectAllInbox()
    }
  }

  return (
    <React.Fragment>
      <AsyncButton
        icon={Check}
        level="success"
        loading={acceptor.loading}
        disabled={disabled}
        onClick={onAccept}
      >
        <Trans>
          Accepter {{ what: hasSelection ? t("sélection") : t("tout") }}
        </Trans>
      </AsyncButton>

      <AsyncButton
        icon={Cross}
        level="danger"
        loading={rejector.loading}
        disabled={disabled}
        onClick={onReject}
      >
        <Trans>
          Refuser {{ what: hasSelection ? t("sélection") : t("tout") }}
        </Trans>
      </AsyncButton>
    </React.Fragment>
  )
}

type AdminActionsProps = {
  disabled: boolean
  administrator: LotAdministrator
}

export const AdminActions = ({
  disabled,
  administrator,
}: AdminActionsProps) => {
  return (
    <React.Fragment>
      <AsyncButton
        icon={Pin}
        level="success"
        loading={administrator.loading}
        disabled={disabled}
        onClick={administrator.markSelectionForReview}
      >
        <Trans>Épingler sélection</Trans>
      </AsyncButton>

      <AsyncButton
        icon={EyeOff}
        level="warning"
        loading={administrator.loading}
        disabled={disabled}
        onClick={administrator.markSelectionAsRead}
      >
        <Trans>Ignorer sélection</Trans>
      </AsyncButton>
    </React.Fragment>
  )
}

type AuditorActionsProps = {
  disabled: boolean
  auditor: LotAuditor
}

export const AuditorActions = ({ disabled, auditor }: AuditorActionsProps) => {
  return (
    <React.Fragment>
      <AsyncButton
        icon={Pin}
        level="success"
        loading={auditor.loading}
        disabled={disabled}
        onClick={auditor.highlightLotSelection}
      >
        <Trans>Épingler sélection</Trans>
      </AsyncButton>

      <AsyncButton
        icon={EyeOff}
        level="warning"
        loading={auditor.loading}
        disabled={disabled}
        onClick={auditor.hideLotSelection}
      >
        <Trans>Ignorer sélection</Trans>
      </AsyncButton>
    </React.Fragment>
  )
}

type OperatorOutsourcedBlendingProps = {
  disabled: boolean
  forwarder: LotForwarder
  outsourceddepots: EntityDeliverySite[] | undefined
  selection: TransactionSelection
}

export const OperatorOutsourcedBlendingActions = ({
  disabled,
  forwarder,
  outsourceddepots,
  selection,
}: OperatorOutsourcedBlendingProps) => {
  async function onForward() {
    const validated = await prompt<boolean>((resolve) => (
      <OperatorForwardPrompt
        outsourceddepots={outsourceddepots}
        onResolve={resolve}
      />
    ))

    if (validated) {
      forwarder.forwardSelection(selection, outsourceddepots)
    }
  }
  return (
    <Button
      disabled={disabled}
      level="primary"
      icon={Forward}
      onClick={onForward}
    >
      <Trans>Transférer</Trans>
    </Button>
  )
}

// SEARCH INPUT COMPONENT

export const SearchInput = ({ className, ...props }: InputProps) => (
  <div className={cl(styles.searchInput, className)}>
    <Input {...props} className={styles.searchInput} />
    <Search size={24} />
  </div>
)

export const ActionBar = ({
  search,
  children,
}: {
  search: SearchSelection
  children: React.ReactNode
}) => {
  const { t } = useTranslation()

  return (
    <Box row className={cl(styles.actionBar)}>
      {children}
      <SearchInput
        placeholder={t("Rechercher des lots...")}
        value={search.query}
        onChange={(e) => search.setQuery(e.target.value)}
        style={{ marginLeft: "auto" }}
      />
    </Box>
  )
}
