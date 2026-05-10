import React from 'react'

const DOMAINS = [
  { value: 'web-development', label: 'Web Dev', icon: '◻' },
  { value: 'android-development', label: 'Android', icon: '▣' },
  { value: 'app-development', label: 'iOS / App Dev', icon: '▢' },
  { value: 'game-development', label: 'Game Dev', icon: '◎' },
  { value: 'graphic-design', label: 'Graphic Design', icon: '⬡' },
  { value: 'data-science', label: 'Data Science', icon: '◆' },
  { value: 'ui-ux', label: 'UI / UX', icon: '⬡' },
  { value: 'frontend', label: 'Frontend', icon: '◈' },
  { value: 'backend', label: 'Backend', icon: '◎' },
  { value: 'full-stack', label: 'Full Stack', icon: '◉' },
  { value: 'ai-ml', label: 'AI / ML', icon: '◇' },
  { value: 'cloud-devops', label: 'Cloud/DevOps', icon: '△' },
  { value: 'qa', label: 'QA Testing', icon: '▷' },
  { value: 'cybersecurity', label: 'Cybersecurity', icon: '⬢' },
  { value: 'software-development', label: 'Software Dev', icon: '◫' },
]

interface DomainSelectorProps {
  value?: string | null
  onChange: (value: string) => void
}

export const DomainSelector: React.FC<DomainSelectorProps> = ({ value, onChange }) => {
  return (
    <div className="w-full">
      <p className="text-[11px] font-mono text-slate-500 uppercase tracking-widest mb-3">
        Step 2 — Select your domain
      </p>
      <div className="flex flex-wrap gap-2">
        {DOMAINS.map(domain => {
          const selected = value === domain.value
          return (
            <button
              key={domain.value}
              onClick={() => onChange(domain.value)}
              className={`
                inline-flex items-center gap-2 px-3.5 py-2 rounded-lg border text-sm
                transition-all duration-150 ease-out cursor-pointer select-none
                focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-400/50
                ${selected
                  ? `bg-amber-400/10 border-amber-400/40 text-amber-300 shadow-[0_0_16px_rgba(251,191,36,0.1)]`
                  : `bg-obsidian-800 border-white/8 text-slate-400 hover:bg-obsidian-700 hover:border-white/15 hover:text-slate-200`
                }
              `}
            >
              <span className="font-mono text-[13px]">{domain.icon}</span>
              <span className="font-sans font-medium">{domain.label}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
