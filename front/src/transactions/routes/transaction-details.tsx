import React from "react"

import { LotStatus, EntityType, UserRole } from "common/types"
import { EntitySelection } from "carbure/hooks/use-entity"
import { LotDeleter } from "transactions/hooks/actions/use-delete-lots"
import { LotAcceptor } from "transactions/hooks/actions/use-accept-lots"
import { LotRejector } from "transactions/hooks/actions/use-reject-lots"
import { LotValidator } from "transactions/hooks/actions/use-validate-lots"
import { LotAdministrator } from "transactions/hooks/actions/use-admin-lots"

import styles from "../components/form.module.css"

import useTransactionDetails from "../hooks/use-transaction-details"
import useNavigate from "../hooks/query/use-navigate"

import {
  AlertTriangle,
  Check,
  Cross,
  Return,
  Save,
  ChevronLeft,
  ChevronRight,
  Edit,
} from "common/components/icons"
import { Box, LoaderOverlay } from "common/components"
import { AsyncButton, Button } from "common/components/button"
import Modal from "common/components/modal"
import TransactionForm from "../components/form"
import { StatusTitle } from "../components/status"
import Comments from "../components/form-comments"
import ValidationErrors from "../components/form-errors"
import TransactionHistory from "../components/history"
import { useRights } from "carbure/hooks/use-rights"

const EDITABLE = [LotStatus.Draft, LotStatus.ToFix]
const COMMENTABLE = [LotStatus.ToFix, LotStatus.Inbox]

type TransactionDetailsProps = {
  entity: EntitySelection
  deleter: LotDeleter
  validator: LotValidator
  acceptor: LotAcceptor
  rejector: LotRejector
  administrator: LotAdministrator
  transactions: number[]
  refresh: () => void
}

const TransactionDetails = ({
  entity,
  deleter,
  validator,
  acceptor,
  rejector,
  administrator,
  transactions,
  refresh,
}: TransactionDetailsProps) => {
  const {
    form,
    hasChange,
    details,
    request,
    comment,
    status,
    fieldErrors,
    validationErrors,
    transaction,
    change,
    submit,
    close,
    addComment,
    refreshDetails,
  } = useTransactionDetails(entity, refresh)

  const rights = useRights()
  const navigator = useNavigate(transactions)

  const isEditable = EDITABLE.includes(status)
  const isCommentable = COMMENTABLE.includes(status)

  const isAdmin = entity?.entity_type === EntityType.Administration
  const isAuditor = entity?.entity_type === EntityType.Auditor

  const isVendor =
    Boolean(entity) && transaction?.carbure_vendor?.id === entity!.id
  const isVendorOperator =
    transaction?.carbure_vendor?.entity_type === EntityType.Operator

  const hasErrors =
    validationErrors.length > 0 || Object.keys(fieldErrors).length > 0

  const canModify = rights.is(UserRole.Admin, UserRole.ReadWrite)

  async function run(
    action: (i: number) => Promise<boolean>,
    nextOnDone: boolean = false
  ) {
    if (await action(form.id)) {
      refreshDetails()

      if (nextOnDone) {
        navigator.next()
      }
    }
  }

  return (
    <Modal onClose={close}>
      <StatusTitle editable={isEditable} details={details.data} entity={entity}>
        Détails de la transaction {form.carbure_id}
      </StatusTitle>

      <TransactionForm
        id="transaction-details"
        entity={entity}
        readOnly={!isEditable || !canModify}
        transaction={form}
        error={details.error ?? request.error}
        errors={fieldErrors}
        onChange={change}
      />

      {hasErrors && <ValidationErrors errors={validationErrors} />}

      {details.data && details.data.comments.length > 0 && (
        <Comments
          readOnly={!isCommentable}
          loading={comment.loading}
          comments={details.data.comments}
          onComment={addComment}
        />
      )}

      {Boolean(details.data?.updates?.length) && (
        <TransactionHistory history={details.data?.updates} />
      )}

      <div className={styles.transactionFormButtons}>
        {canModify && isEditable && (
          <AsyncButton
            disabled={!hasChange}
            submit="transaction-details"
            icon={Save}
            level="primary"
            loading={request.loading}
            onClick={submit}
          >
            Sauvegarder
          </AsyncButton>
        )}

        {canModify && status === LotStatus.Draft && (
          <AsyncButton
            disabled={hasChange}
            icon={Check}
            level="success"
            loading={validator.loading}
            onClick={() => run(validator.validateLot)}
          >
            Envoyer
          </AsyncButton>
        )}

        {canModify && status === LotStatus.ToFix && (
          <AsyncButton
            disabled={hasChange}
            icon={Check}
            level="success"
            loading={validator.loading}
            onClick={() => run(validator.validateAndCommentLot)}
          >
            Renvoyer
          </AsyncButton>
        )}

        {canModify && isEditable && (
          <AsyncButton
            icon={Cross}
            level="danger"
            loading={deleter.loading}
            onClick={() => run(deleter.deleteLot, true)}
          >
            Supprimer
          </AsyncButton>
        )}

        {canModify &&
          status === LotStatus.Inbox &&
          transaction?.delivery_status !== "AC" && (
            <React.Fragment>
              <AsyncButton
                icon={Check}
                level="success"
                loading={acceptor.loading}
                onClick={() => run(acceptor.acceptLot)}
              >
                Accepter
              </AsyncButton>

              {!transaction?.lot.parent_lot && !isVendorOperator && (
                <AsyncButton
                  icon={AlertTriangle}
                  level="warning"
                  loading={acceptor.loading}
                  onClick={() => run(acceptor.acceptAndCommentLot)}
                >
                  Accepter sous réserve
                </AsyncButton>
              )}

              <AsyncButton
                icon={Cross}
                level="danger"
                loading={rejector.loading}
                onClick={() => run(rejector.rejectLot, true)}
              >
                Refuser
              </AsyncButton>
            </React.Fragment>
          )}

        {canModify &&
          isVendor &&
          !isAdmin &&
          !isAuditor &&
          [LotStatus.Accepted, LotStatus.Declaration].includes(status) && (
            <AsyncButton
              icon={Edit}
              level="warning"
              loading={acceptor.loading}
              onClick={() => run(acceptor.amendLot)}
            >
              Corriger
            </AsyncButton>
          )}

        {canModify &&
          !isVendor &&
          !isAdmin &&
          !isAuditor &&
          !isVendorOperator &&
          [LotStatus.Accepted, LotStatus.Declaration].includes(status) && (
            <AsyncButton
              icon={Edit}
              level="warning"
              loading={acceptor.loading}
              onClick={() => run(acceptor.askForCorrection)}
            >
              Demander une correction
            </AsyncButton>
          )}

        {isAdmin && (
            <React.Fragment>
              <AsyncButton
                disabled={transaction?.hidden_by_admin}
                icon={Check}
                level="success"
                loading={administrator.loading}
                onClick={() => run(administrator.markAsRead, true)}
              >
                Cacher Lot
              </AsyncButton>
              <AsyncButton
                disabled={transaction?.highlighted_by_admin}
                icon={Cross}
                level="warning"
                loading={administrator.loading}
                onClick={() => run(administrator.markForReview, true)}
              >
                Mettre de côté
              </AsyncButton>
            </React.Fragment>
          )}

        <Box row className={styles.transactionNavButtons}>
          <Button
            icon={ChevronLeft}
            disabled={!navigator.hasPrev}
            onClick={navigator.prev}
          >
            Lot Précédent
          </Button>

          <Button
            icon={ChevronRight}
            disabled={!navigator.hasNext}
            onClick={navigator.next}
          >
            Lot Suivant
          </Button>

          <Button icon={Return} onClick={close}>
            Retour
          </Button>
        </Box>
      </div>

      {details.loading && <LoaderOverlay />}
    </Modal>
  )
}

export default TransactionDetails
