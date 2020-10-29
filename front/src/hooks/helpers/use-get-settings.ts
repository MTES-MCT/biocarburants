import { useEffect } from "react"

import { EntitySelection } from "../helpers/use-entity"

import * as api from "../../services/settings"
import useAPI from "../helpers/use-api"
import { Settings } from "../../services/types"

export type SettingsGetter = {
  loading: boolean
  error: string | null
  data: Settings | null
  resolve: () => void
}

// fetches current snapshot when parameters change
export function useGetSettings(entity: EntitySelection): SettingsGetter {
  const [settings, resolveSettings] = useAPI(api.getSettings)

  function resolve() {
    return resolveSettings().cancel
  }

  useEffect(resolve, [resolveSettings, entity])

  return { ...settings, resolve }
}