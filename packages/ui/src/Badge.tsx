import React from 'react'

type BadgeVariant = 'default' | 'amber' | 'green' | 'red' | 'blue' | 'outline'

interface BadgeProps {
  label: string
  variant?: BadgeVariant
  size?: 'sm' | 'md'
  dot?: boolean
}

const variantStyles: Record<BadgeVariant, string> = {
  default: 'bg-white/6 text-slate-300 border border-white/8',
  amber: 'bg-amber-400/10 text-amber-400 border border-amber-400/20',
  green: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
  red: 'bg-red-500/10 text-red-400 border border-red-500/20',
  blue: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
  outline: 'bg-transparent text-slate-400 border border-white/15',
}

const dotColors: Record<BadgeVariant, string> = {
  default: 'bg-slate-400',
  amber: 'bg-amber-400',
  green: 'bg-emerald-400',
  red: 'bg-red-400',
  blue: 'bg-blue-400',
  outline: 'bg-slate-500',
}

export const Badge: React.FC<BadgeProps> = ({
  label,
  variant = 'default',
  size = 'sm',
  dot = false,
}) => (
  <span className={`
    inline-flex items-center gap-1.5 font-sans font-medium tracking-tight
    rounded-full
    ${size === 'sm' ? 'px-2 py-0.5 text-[11px]' : 'px-2.5 py-1 text-xs'}
    ${variantStyles[variant]}
  `}>
    {dot && <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${dotColors[variant]}`} />}
    {label}
  </span>
)
