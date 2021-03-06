import React from "react"
import cl from "clsx"

import styles from "./icons.module.css"
import { SystemProps } from "."

// icons were adapted from https://github.com/tabler/tabler-icons

export type IconProps = SystemProps & {
  size?: number
  color?: string
  stroke?: number
  className?: string
  title?: string
  onClick?: (e: React.MouseEvent) => void
}

const Icon = ({
  size = 24,
  color = "currentColor",
  stroke = 2,
  className,
  title,
  children,
  ...props
}: IconProps) => (
  <svg
    className={cl("icon", className)}
    width={size}
    height={size}
    viewBox="0 0 24 24"
    strokeWidth={stroke}
    stroke={color}
    fill="none"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <title>{title}</title>
    {children}
  </svg>
)

export const ChevronDown = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-chevron-down", className)}>
    <polyline points="6 9 12 15 18 9" />
  </Icon>
)

export const ChevronLeft = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-chevron-down", className)}>
    <polyline points="15 6 9 12 15 18" />
  </Icon>
)

export const ChevronRight = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-chevron-right", className)}>
    <polyline points="9 6 15 12 9 18" />
  </Icon>
)

export const Plus = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-plus", className)}>
    <line x1={12} y1={5} x2={12} y2={19} />
    <line x1={5} y1={12} x2={19} y2={12} />
  </Icon>
)

export const Search = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-search", className)}>
    <circle cx="10" cy="10" r="7" />
    <line x1="21" y1="21" x2="15" y2="15" />
  </Icon>
)

export const Cross = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-cross", className)}>
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </Icon>
)

export const AlertCircle = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-cross", className)}>
    <circle cx="12" cy="12" r="9" />
    <line x1="12" y1="8" x2="12" y2="12" />
    <line x1="12" y1="16" x2="12.01" y2="16" />
  </Icon>
)

export const Copy = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-cross", className)}>
    <rect x="8" y="8" width="12" height="12" rx="2" />
    <path d="M16 8v-2a2 2 0 0 0 -2 -2h-8a2 2 0 0 0 -2 2v8a2 2 0 0 0 2 2h2" />
  </Icon>
)

export const Check = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-cross", className)}>
    <path d="M5 12l5 5l10 -10" />
  </Icon>
)

export const Save = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-save", className)}>
    <path d="M6 4h10l4 4v10a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2" />
    <circle cx="12" cy="14" r="2" />
    <polyline points="14 4 14 8 8 8 8 4" />
  </Icon>
)

export const Message = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-message", className)}>
    <path d="M4 21v-13a3 3 0 0 1 3 -3h10a3 3 0 0 1 3 3v6a3 3 0 0 1 -3 3h-9l-4 4" />
    <line x1="12" y1="8" x2="12" y2="11" />
    <line x1="12" y1="14" x2="12" y2="14.01" />
  </Icon>
)

export const Loader = ({ className, ...props }: IconProps) => (
  <Icon
    {...props}
    className={cl("icon-loader", styles.loader, className)}
    title="Chargement..."
  >
    <line x1="12" y1="6" x2="12" y2="3" />
    <line x1="16.25" y1="7.75" x2="18.4" y2="5.6" />
    <line x1="18" y1="12" x2="21" y2="12" />
    <line x1="16.25" y1="16.25" x2="18.4" y2="18.4" />
    <line x1="12" y1="18" x2="12" y2="21" />
    <line x1="7.75" y1="16.25" x2="5.6" y2="18.4" />
    <line x1="6" y1="12" x2="3" y2="12" />
    <line x1="7.75" y1="7.75" x2="5.6" y2="5.6" />
  </Icon>
)

export const Rapport = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-rapport", className)}>
    <path d="M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0 0 0 -2 -2h-2" />
    <rect x="9" y="3" width="6" height="4" rx="2" />
    <line x1="9" y1="12" x2="9.01" y2="12" />
    <line x1="13" y1="12" x2="15" y2="12" />
    <line x1="9" y1="16" x2="9.01" y2="16" />
    <line x1="13" y1="16" x2="15" y2="16" />
  </Icon>
)

export const Upload = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-upload", className)}>
    <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
    <polyline points="7 11 12 16 17 11" />
    <line x1="12" y1="4" x2="12" y2="16" />
  </Icon>
)

export const Download = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-download", className)}>
    <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
    <polyline points="7 9 12 4 17 9" />
    <line x1="12" y1="4" x2="12" y2="16" />
  </Icon>
)

export const AlertTriangle = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-alert-triangle", className)}>
    <path d="M12 9v2m0 4v.01" />
    <path d="M5 19h14a2 2 0 0 0 1.84 -2.75l-7.1 -12.25a2 2 0 0 0 -3.5 0l-7.1 12.25a2 2 0 0 0 1.75 2.75" />
  </Icon>
)

export const AlertOctagon = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-alert-triangle", className)}>
    <path d="M8.7 3h6.6c0.3 0 .5 .1 .7 .3l4.7 4.7c0.2 .2 .3 .4 .3 .7v6.6c0 .3 -.1 .5 -.3 .7l-4.7 4.7c-0.2 .2 -.4 .3 -.7 .3h-6.6c-0.3 0 -.5 -.1 -.7 -.3l-4.7 -4.7c-0.2 -.2 -.3 -.4 -.3 -.7v-6.6c0 -.3 .1 -.5 .3 -.7l4.7 -4.7c0.2 -.2 .4 -.3 .7 -.3z" />
    <line x1="12" y1="8" x2="12" y2="12" />
    <line x1="12" y1="16" x2="12.01" y2="16" />
  </Icon>
)

export const Calendar = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-calendar", className)}>
    <rect x="4" y="5" width="16" height="16" rx="2" />
    <line x1="16" y1="3" x2="16" y2="7" />
    <line x1="8" y1="3" x2="8" y2="7" />
    <line x1="4" y1="11" x2="20" y2="11" />
    <line x1="11" y1="15" x2="12" y2="15" />
    <line x1="12" y1="15" x2="12" y2="18" />
  </Icon>
)

export const Return = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-return", className)}>
    <path d="M9 11l-4 4l4 4m-4 -4h11a4 4 0 0 0 0 -8h-1" />
  </Icon>
)

export const Back = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-back", className)}>
    <line x1="5" y1="12" x2="19" y2="12" />
    <line x1="5" y1="12" x2="11" y2="18" />
    <line x1="5" y1="12" x2="11" y2="6" />
  </Icon>
)

export const Edit = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-edit", className)}>
    <path d="M4 20h4l10.5 -10.5a1.5 1.5 0 0 0 -4 -4l-10.5 10.5v4" />
    <line x1="13.5" y1="6.5" x2="17.5" y2="10.5" />
  </Icon>
)

export const Refresh = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-refresh", className)}>
    <path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4" />
    <path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4" />
  </Icon>
)

export const Question = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-question", className)}>
    <path d="M8 8a3.5 3 0 0 1 3.5 -3h1a3.5 3 0 0 1 3.5 3a3 3 0 0 1 -2 3a3 4 0 0 0 -2 4" />
    <line x1="12" y1="19" x2="12" y2="19.01" />
  </Icon>
)

export const Filter = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-filter", className)}>
    <path d="M5.5 5h13a1 1 0 0 1 .5 1.5l-5 5.5l0 7l-4 -3l0 -4l-5 -5.5a1 1 0 0 1 .5 -1.5" />
  </Icon>
)

export const Alarm = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-alarm", className)}>
    <circle cx="12" cy="13" r="7" />
    <polyline points="12 10 12 13 14 13" />
    <line x1="7" y1="4" x2="4.25" y2="6" />
    <line x1="17" y1="4" x2="19.75" y2="6" />
  </Icon>
)

export const CheckCircle = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-check-circle", className)}>
    <polyline points="9 11 12 14 20 6" />
    <path d="M20 12v6a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2h9" />
  </Icon>
)

export const Bell = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-bell", className)}>
    <path d="M10 5a2 2 0 0 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6" />
    <path d="M9 17v1a3 3 0 0 0 6 0v-1" />
    <path d="M21 6.727a11.05 11.05 0 0 0 -2.794 -3.727" />
    <path d="M3 6.727a11.05 11.05 0 0 1 2.792 -3.727" />
  </Icon>
)

export const Flask = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-flask", className)}>
    <line x1="9" y1="3" x2="15" y2="3" />
    <line x1="10" y1="9" x2="14" y2="9" />
    <path d="M10 3v6l-4 11a0.7 .7 0 0 0 .5 1h11a0.7 .7 0 0 0 .5 -1l-4 -11v-6" />
  </Icon>
)

export const Forward = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-forward", className)}>
    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
    <path d="M12 18h-7a2 2 0 0 1 -2 -2v-10a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v7.5" />
    <path d="M3 6l9 6l9 -6" />
    <path d="M15 18h6" />
    <path d="M18 15l3 3l-3 3" />
  </Icon>
)

export const Certificate = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-certificate", className)}>
    <circle cx="15" cy="15" r="3" />
    <path d="M13 17.5v4.5l2 -1.5l2 1.5v-4.5" />
    <path d="M10 19h-5a2 2 0 0 1 -2 -2v-10c0 -1.1 .9 -2 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -1 1.73" />
    <line x1="6" y1="9" x2="18" y2="9" />
    <line x1="6" y1="12" x2="9" y2="12" />
    <line x1="6" y1="15" x2="8" y2="15" />
  </Icon>
)

export const UserCheck = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-user-check", className)}>
    <circle cx="9" cy="7" r="4" />
    <path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" />
    <path d="M16 11l2 2l4 -4" />
  </Icon>
)

export const Eye = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-eye", className)}>
    <path d="M10.584 10.587a2 2 0 0 0 2.828 2.83" />
    <path d="M9.363 5.365a9.466 9.466 0 0 1 2.637 -.365c4 0 7.333 2.333 10 7c-.778 1.361 -1.612 2.524 -2.503 3.488m-2.14 1.861c-1.631 1.1 -3.415 1.651 -5.357 1.651c-4 0 -7.333 -2.333 -10 -7c1.369 -2.395 2.913 -4.175 4.632 -5.341" />
  </Icon>
)

export const EyeOff = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-eye-off", className)}>
    <line x1="3" y1="3" x2="21" y2="21" />
    <path d="M10.584 10.587a2 2 0 0 0 2.828 2.83" />
    <path d="M9.363 5.365a9.466 9.466 0 0 1 2.637 -.365c4 0 7.333 2.333 10 7c-.778 1.361 -1.612 2.524 -2.503 3.488m-2.14 1.861c-1.631 1.1 -3.415 1.651 -5.357 1.651c-4 0 -7.333 -2.333 -10 -7c1.369 -2.395 2.913 -4.175 4.632 -5.341" />
  </Icon>
)

export const Pin = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-pin", className)}>
    <path d="M15 4.5l-4 4l-4 1.5l-1.5 1.5l7 7l1.5 -1.5l1.5 -4l4 -4" />
    <line x1="9" y1="15" x2="4.5" y2="19.5" />
    <line x1="14.5" y1="4" x2="20" y2="9.5" />
  </Icon>
)

export const PinOff = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-pin-off", className)}>
    <line x1="3" y1="3" x2="21" y2="21" />
    <path d="M15 4.5l-3.249 3.249m-2.57 1.433l-2.181 .818l-1.5 1.5l7 7l1.5 -1.5l.82 -2.186m1.43 -2.563l3.25 -3.251" />
    <line x1="9" y1="15" x2="4.5" y2="19.5" />
    <line x1="14.5" y1="4" x2="20" y2="9.5" />
  </Icon>
)

export const FileCheck = ({ className, ...props }: IconProps) => (
  <Icon {...props} className={cl("icon-pin", className)}>
    <path d="M14 3v4a1 1 0 0 0 1 1h4" />
    <path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z" />
    <path d="M9 15l2 2l4 -4" />
  </Icon>
)
