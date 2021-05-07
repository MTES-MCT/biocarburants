import { Trans, useTranslation } from "react-i18next"

import { AppHook, useApp } from "./hooks/use-app"
import { EntityType, LotStatus } from "common/types"
import useEntity from "./hooks/use-entity"
import { UserRightProvider } from "./hooks/use-rights"

import { Alert } from "common/components/alert"
import { AlertTriangle } from "common/components/icons"
import { Redirect, Route, Switch } from "common/components/relative-route"

import Topbar from "./components/top-bar"
import Footer from "./components/footer"
import Pending from "./components/pending"
import Exit from "./components/exit"
import Registry from "./components/registry"

import Transactions from "transactions"
import Stocks from "stocks"
import Settings from "settings"
import Account from "account"
import Entities from "../entities" // not using relative path prevents import
import EntityDetails from "../entities/routes/entity-details"
import Dashboard from "dashboard"

const DevBanner = () => (
  <div
    style={{
      backgroundColor: "var(--orange-medium)",
      padding: "8px 120px",
    }}
  >
    <Trans>
      <b>Version de développement de CarbuRe :</b> les manipulations effectuées
      ici n'ont pas de répercussion et les déclarations ne sont pas prises en
      compte.
    </Trans>
  </div>
)

// has to be nested in a route so we can get data from useParams()
const Org = ({ app }: { app: AppHook }) => {
  const { entity, pending } = useEntity(app)

  // a user with entities tries to access the pending or another entity's page
  if (app.hasEntities() && !entity) {
    return <Redirect to="/" />
  }

  // a user with no entities tries to access an entity page
  if (!app.hasEntities() && !pending) {
    return <Redirect to="/" />
  }

  const isAdmin = entity?.entity_type === EntityType.Administration
  const isProd = window.location.hostname === "carbure.beta.gouv.fr"

  return (
    <UserRightProvider app={app}>
      {!isProd && <DevBanner />}

      <Topbar entity={entity} settings={app.settings} />

      <Switch>
        <Route relative exact path="account">
          <Account settings={app.settings} />
        </Route>

        <Route relative exact path="../pending">
          <Pending />
        </Route>

        <Route relative exact path="stocks">
          <Redirect relative to="in" />
        </Route>

        <Route relative path="stocks/:status">
          <Stocks entity={entity} />
        </Route>

        <Route relative exact path="transactions">
          <Redirect relative to={isAdmin ? LotStatus.Alert : LotStatus.Draft} />
        </Route>

        <Route relative path="transactions/:status">
          <Transactions entity={entity} />
        </Route>

        <Route relative path="settings">
          <Settings entity={entity} settings={app.settings} />
        </Route>

        <Route relative path="registry">
          <Registry />
        </Route>

        {isAdmin && (
          <Route relative exact path="administration">
            <Exit to="/administrators/" />
          </Route>
        )}

        {isAdmin && (
          <Route relative path="dashboard">
            <Dashboard />
          </Route>
        )}

        {isAdmin && (
          <Route relative path="entities/:id">
            <EntityDetails />
          </Route>
        )}

        {isAdmin && (
          <Route relative path="entities">
            <Entities />
          </Route>
        )}

        <Redirect relative to={isAdmin ? "dashboard" : "transactions"} />
      </Switch>

      <Footer />
    </UserRightProvider>
  )
}

const Carbure = () => {
  const app = useApp()
  const { settings, getDefaultEntity } = app

  useTranslation() // simple call so we rerender the whole app when the selected language changes

  if (settings.error === "User not verified") {
    return <Exit to="/accounts/login" />
  }

  return (
    <div id="app">
      {settings.error && (
        <Alert level="error" icon={AlertTriangle}>
          {settings.error}
        </Alert>
      )}

      {!settings.error && settings.data && (
        <Switch>
          <Route path="/org/:entity">
            <Org app={app} />
          </Route>

          <Route path="/logout">
            <Exit to="/accounts/logout" />
          </Route>

          <Redirect to={`/org/${getDefaultEntity()}`} />
        </Switch>
      )}
    </div>
  )
}

export default Carbure
