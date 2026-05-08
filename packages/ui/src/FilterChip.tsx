import React from 'react'

interface FilterChipProps {
  label: string
  selected?: boolean
  onToggle?: () => void
  count?: number
  icon?: string
}

export const FilterChip: React.FC<FilterChipProps> = ({
  label,
  selected = false,
  onToggle,
  count,
  icon,
}) => (
  <button
    onClick={onToggle}
    className={`
      inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-sans font-medium
      border transition-all duration-150 ease-out cursor-pointer select-none
      focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-400/50
      ${selected
        ? 'bg-amber-400/12 border-amber-400/35 text-amber-300 shadow-[0_0_12px_rgba(251,191,36,0.1)]'
        : 'bg-white/4 border-white/8 text-slate-400 hover:bg-white/7 hover:border-white/15 hover:text-slate-200'
      }
    `}
  >
    {icon && <span>{icon}</span>}
    <span>{label}</span>
    {count !== undefined && (
      <span className={`
        font-mono text-[10px] px-1 py-0.5 rounded
        ${selected ? 'bg-amber-400/20 text-amber-300' : 'bg-white/8 text-slate-500'}
      `}>
        {count}
      </span>
    )}
  </button>
)
