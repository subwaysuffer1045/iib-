import React from 'react'

interface EmptyStateProps {
  icon?: string
  title: string
  message?: string
  action?: {
    label: string
    onClick: () => void
  }
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon = '◌',
  title,
  message,
  action,
}) => (
  <div className="flex flex-col items-center justify-center py-20 px-6 text-center">
    <span className="font-mono text-4xl text-slate-700 mb-4">{icon}</span>
    <h3 className="font-display text-lg text-slate-300 mb-2">{title}</h3>
    {message && (
      <p className="text-sm text-slate-500 max-w-sm leading-relaxed mb-6">{message}</p>
    )}
    {action && (
      <button
        onClick={action.onClick}
        className="px-4 py-2 rounded-md text-sm font-sans font-medium
                   bg-obsidian-700 text-slate-200 border border-white/10
                   hover:bg-obsidian-600 hover:border-white/20
                   transition-all duration-150"
      >
        {action.label}
      </button>
    )}
  </div>
)
