import React from 'react'

interface StatusCardProps {
  icon: string
  title: string
  value: string | number
  delta?: string
  deltaPositive?: boolean
  subtitle?: string
}

export const StatusCard: React.FC<StatusCardProps> = ({
  icon,
  title,
  value,
  delta,
  deltaPositive,
  subtitle,
}) => (
  <div className="flex flex-col p-5 rounded-lg bg-obsidian-800 border border-white/6">
    <div className="flex items-start justify-between mb-4">
      <span className="text-slate-500 text-lg font-mono">{icon}</span>
      {delta && (
        <span className={`text-[11px] font-mono px-1.5 py-0.5 rounded
          ${deltaPositive
            ? 'text-emerald-400 bg-emerald-500/10'
            : 'text-red-400 bg-red-500/10'
          }`}>
          {deltaPositive ? '+' : ''}{delta}
        </span>
      )}
    </div>
    <span className="font-display text-3xl text-slate-100 mb-1">{value}</span>
    <span className="text-xs font-sans text-slate-500">{title}</span>
    {subtitle && <span className="text-[11px] font-mono text-slate-700 mt-1">{subtitle}</span>}
  </div>
)
