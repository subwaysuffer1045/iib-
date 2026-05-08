import React from 'react'

interface DeadlineChipProps {
  apply_by?: string | null  // ISO date string
  is_expiring_soon?: boolean
}

function getDaysLeft(dateStr: string): number {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const deadline = new Date(dateStr)
  deadline.setHours(0, 0, 0, 0)
  return Math.ceil((deadline.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: '2-digit'
  })
}

export const DeadlineChip: React.FC<DeadlineChipProps> = ({
  apply_by,
  is_expiring_soon,
}) => {
  if (!apply_by) {
    return (
      <span className="text-[11px] text-slate-600 font-mono">No deadline</span>
    )
  }

  const days = getDaysLeft(apply_by)

  if (days < 0) {
    return (
      <span className="inline-flex items-center gap-1 text-[11px] font-mono text-red-500/70">
        <span>Expired</span>
      </span>
    )
  }

  if (days === 0) {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-red-500/12 border border-red-500/25 text-[11px] font-mono text-red-400 animate-pulse">
        ⚡ Today
      </span>
    )
  }

  if (days <= 3 || is_expiring_soon) {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-red-500/8 border border-red-500/20 text-[11px] font-mono text-red-400">
        ⚡ {days}d left
      </span>
    )
  }

  if (days <= 7) {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-400/8 border border-amber-400/20 text-[11px] font-mono text-amber-400">
        {days}d left
      </span>
    )
  }

  return (
    <span className="inline-flex items-center gap-1 text-[11px] font-mono text-slate-500">
      {formatDate(apply_by)}
    </span>
  )
}
