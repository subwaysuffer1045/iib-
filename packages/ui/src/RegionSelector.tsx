import React from 'react'

const REGIONS = [
  { value: 'mumbai', label: 'Mumbai', state: 'MH' },
  { value: 'navi-mumbai', label: 'Navi Mumbai', state: 'MH' },
  { value: 'pune', label: 'Pune', state: 'MH' },
  { value: 'bengaluru', label: 'Bengaluru', state: 'KA' },
  { value: 'hyderabad', label: 'Hyderabad', state: 'TG' },
  { value: 'chennai', label: 'Chennai', state: 'TN' },
  { value: 'delhi-ncr', label: 'Delhi NCR', state: 'DL' },
  { value: 'kochi', label: 'Kochi', state: 'KL' },
  { value: 'ahmedabad', label: 'Ahmedabad', state: 'GJ' },
  { value: 'kolkata', label: 'Kolkata', state: 'WB' },
  { value: 'remote', label: 'Remote Only', state: '🌐' },
  { value: 'all-india', label: 'All India', state: '🇮🇳' },
]

interface RegionSelectorProps {
  value?: string | null
  onChange: (value: string) => void
}

export const RegionSelector: React.FC<RegionSelectorProps> = ({ value, onChange }) => {
  return (
    <div className="w-full">
      <p className="text-[11px] font-mono text-slate-500 uppercase tracking-widest mb-3">
        Step 1 — Select your region
      </p>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
        {REGIONS.map(region => {
          const selected = value === region.value
          return (
            <button
              key={region.value}
              onClick={() => onChange(region.value)}
              className={`
                relative flex flex-col items-start p-3 rounded-lg border
                transition-all duration-200 ease-out text-left cursor-pointer
                focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-400/50
                ${selected
                  ? `bg-amber-400/10 border-amber-400/40 shadow-[0_0_20px_rgba(251,191,36,0.12)]`
                  : `bg-obsidian-800 border-white/8 hover:bg-obsidian-700 hover:border-white/15`
                }
              `}
            >
              {selected && (
                <span className="absolute top-2 right-2 w-1.5 h-1.5 rounded-full bg-amber-400" />
              )}
              <span className={`text-[10px] font-mono mb-0.5 ${selected ? 'text-amber-500' : 'text-slate-600'}`}>
                {region.state}
              </span>
              <span className={`text-xs font-sans font-medium ${selected ? 'text-amber-300' : 'text-slate-300'}`}>
                {region.label}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
