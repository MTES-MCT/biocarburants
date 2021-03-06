import { render, TestRoot } from "setupTests"
import { screen } from "@testing-library/react"
import { Route } from "common/components/relative-route"
import { Entity, LotStatus } from "common/types"

import { admin } from "common/__test__/data"
import { waitWhileLoading } from "common/__test__/helpers"
import Transactions from "../index"

import server, { setAdminLots } from "./api"
import { emptyLots } from "./data"

const TransactionsWithRouter = ({
  entity,
  status,
}: {
  entity: Entity
  status: LotStatus
}) => (
  <TestRoot url={`/org/0/transactions/${status}`}>
    <Route path="/org/0/transactions/:status">
      <Transactions entity={entity} />
    </Route>
  </TestRoot>
)

beforeAll(() => server.listen({ onUnhandledRequest: "warn" }))

afterEach(() => {
  server.resetHandlers()
})

afterAll(() => server.close())

test("operator: display an empty list of transactions", async () => {
  setAdminLots(emptyLots)

  render(<TransactionsWithRouter status={LotStatus.Alert} entity={admin} />)

  await waitWhileLoading()

  screen.getByText("Alerte")
  screen.getByText("Correction")
  screen.getByText("Lot déclaré")

  screen.getByText("Périodes")
  screen.getByText("Biocarburants")
  screen.getByText("Matières Premières")
  screen.getByText("Fournisseurs")
  screen.getByText("Clients")
  screen.getByText("Pays d'origine")
  screen.getByText("Sites de production")
  screen.getByText("Sites de livraison")

  screen.getByPlaceholderText("Rechercher des lots...")

  screen.getByText("Aucune transaction trouvée pour cette recherche")
})
