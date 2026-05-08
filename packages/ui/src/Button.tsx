import React from 'react'

type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'amber'
type ButtonSize = 'sm' | 'md' | 'lg'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
  loading?: boolean
  icon?: React.ReactNode
  iconPosition?: 'left' | 'right'
}

const variantStyles: Record<ButtonVariant, string> = {
  primary: `
    bg-obsidian-700 text-slate-100 border border-white/10
    hover:bg-obsidian-600 hover:border-white/20
    active:scale-[0.98]
  `,
  amber: `
    bg-amber-400 text-obsidian-950 border border-amber-400 font-semibold
    hover:bg-amber-300 hover:shadow-[0_0_20px_rgba(251,191,36,0.3)]
    active:scale-[0.98]
  `,
  secondary: `
    bg-transparent text-slate-300 border border-white/10
    hover:bg-white/5 hover:border-white/20 hover:text-slate-100
    active:scale-[0.98]
  `,
  ghost: `
    bg-transparent text-slate-400
    hover:bg-white/5 hover:text-slate-200
    active:scale-[0.98]
  `,
  danger: `
    bg-transparent text-red-400 border border-red-500/20
    hover:bg-red-500/10 hover:border-red-500/40
    active:scale-[0.98]
  `,
}

const sizeStyles: Record<ButtonSize, string> = {
  sm: 'px-3 py-1.5 text-xs gap-1.5',
  md: 'px-4 py-2 text-sm gap-2',
  lg: 'px-6 py-2.5 text-sm gap-2.5',
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(({
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  iconPosition = 'left',
  children,
  className = '',
  disabled,
  ...props
}, ref) => {
  const isDisabled = disabled || loading

  return (
    <button
      ref={ref}
      disabled={isDisabled}
      className={`
        inline-flex items-center justify-center rounded-md font-sans font-medium
        transition-all duration-150 ease-out cursor-pointer select-none
        disabled:opacity-40 disabled:cursor-not-allowed disabled:pointer-events-none
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-400/50
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${className}
      `}
      {...props}
    >
      {loading && (
        <svg
          className="animate-spin h-3.5 w-3.5 text-current flex-shrink-0"
          fill="none" viewBox="0 0 24 24"
        >
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
      )}
      {!loading && icon && iconPosition === 'left' && (
        <span className="flex-shrink-0">{icon}</span>
      )}
      {children && <span>{children}</span>}
      {!loading && icon && iconPosition === 'right' && (
        <span className="flex-shrink-0">{icon}</span>
      )}
    </button>
  )
})
Button.displayName = 'Button'
