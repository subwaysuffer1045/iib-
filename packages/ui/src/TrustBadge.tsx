import React from 'react'

type VerificationStatus = 'verified' | 'needs_review' | 'draft' | 'pending' | 'rejected'

interface TrustBadgeProps {
  trust_score: number
  verification_status: VerificationStatus
  show_score?: boolean
  size?: 'sm' | 'md'
  onClick?: () => void
}

const statusConfig: Record<VerificationStatus, {
  label: string
  icon: string
  containerClass: string
  textClass: string
  borderClass: string
}> = {
  verified: {
    label: 'Verified',
    icon: '✦',
    containerClass: 'bg-emerald-500/8',
    textClass: 'text-emerald-400',
    borderClass: 'border-emerald-500/20',
  },
  needs_review: {
    label: 'Under Review',
    icon: '◎',
    containerClass: 'bg-amber-400/8',
    textClass: 'text-amber-400',
    borderClass: 'border-amber-400/20',
  },
  pending: {
    label: 'Verifying',
    icon: '○',
    containerClass: 'bg-blue-500/8',
    textClass: 'text-blue-400',
    borderClass: 'border-blue-500/20',
  },
  draft: {
    label: 'Unverified',
    icon: '◌',
    containerClass: 'bg-white/5',
    textClass: 'text-slate-500',
    borderClass: 'border-white/8',
  },
  rejected: {
    label: 'Rejected',
    icon: '✕',
    containerClass: 'bg-red-500/8',
    textClass: 'text-red-400',
    borderClass: 'border-red-500/20',
  },
}

export const TrustBadge: React.FC<TrustBadgeProps> = ({
  trust_score,
  verification_status,
  show_score = true,
  size = 'sm',
  onClick,
}) => {
  const config = statusConfig[verification_status]
  const isInteractive = !!onClick

  return (
    <span
      onClick={onClick}
      className={`
        inline-flex items-center gap-1.5 rounded-full border font-sans font-medium
        ${config.containerClass} ${config.textClass} ${config.borderClass}
        ${size === 'sm' ? 'px-2 py-0.5 text-[11px]' : 'px-2.5 py-1 text-xs'}
        ${isInteractive ? 'cursor-pointer hover:opacity-80 transition-opacity' : ''}
      `}
    >
      <span className="font-mono text-[10px]">{config.icon}</span>
      <span>{config.label}</span>
      {show_score && verification_status === 'verified' && (
        <span className="font-mono opacity-70">{trust_score}</span>
      )}
    </span>
  )
}
