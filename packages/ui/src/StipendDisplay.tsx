import React from 'react'

interface StipendDisplayProps {
  min?: number | null
  max?: number | null
  currency?: string
  original_text?: string | null
  size?: 'sm' | 'md' | 'lg'
}

function formatINR(amount: number): string {
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(1)}L`
  if (amount >= 1000) return `₹${(amount / 1000).toFixed(0)}K`
  return `₹${amount}`
}

export const StipendDisplay: React.FC<StipendDisplayProps> = ({
  min,
  max,
  currency = 'INR',
  original_text,
  size = 'md',
}) => {
  const sizeClass = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
  }[size]

  const hasMin = min !== null && min !== undefined && min > 0
  const hasMax = max !== null && max !== undefined && max > 0

  if (!hasMin && !hasMax) {
    return (
      <span className={`font-mono text-slate-500 ${sizeClass}`}>
        —
      </span>
    )
  }

  return (
    <span className={`font-mono font-medium text-amber-400 ${sizeClass} inline-flex items-baseline gap-0.5`}>
      {hasMin && hasMax && min !== max ? (
        <>
          <span>{formatINR(min!)}</span>
          <span className="text-slate-500 text-[10px]">–</span>
          <span>{formatINR(max!)}</span>
        </>
      ) : (
        <span>{formatINR(hasMin ? min! : max!)}</span>
      )}
      <span className="text-slate-500 font-sans text-[10px] ml-0.5">/mo</span>
    </span>
  )
}
