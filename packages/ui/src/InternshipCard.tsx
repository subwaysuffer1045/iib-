import React from 'react'
import { TrustBadge } from './TrustBadge'
import { StipendDisplay } from './StipendDisplay'
import { DeadlineChip } from './DeadlineChip'
import { Badge } from './Badge'

interface Internship {
  id: string
  slug: string
  title: string
  company_name: string
  location_text: string
  city?: string
  state?: string
  work_mode: 'remote' | 'hybrid' | 'onsite'
  domain_slug?: string
  stipend_min?: number
  stipend_max?: number
  stipend_text?: string
  apply_by?: string
  is_expiring_soon?: boolean
  trust_score: number
  verification_status: 'verified' | 'needs_review' | 'draft' | 'pending' | 'rejected'
  duration_text?: string
  freshness_bucket?: string
  skills?: string[]
}

interface InternshipCardProps {
  internship: Internship
  isSaved?: boolean
  onSave?: (id: string) => void
  onOpen?: (slug: string) => void
  animationDelay?: number
}

const workModeLabel: Record<string, string> = {
  remote: 'Remote',
  hybrid: 'Hybrid',
  onsite: 'Onsite',
}

const freshnessLabel: Record<string, string> = {
  today: 'Today',
  yesterday: 'Yesterday',
  last_2_days: '2 days ago',
  this_week: 'This week',
}

export const InternshipCard: React.FC<InternshipCardProps> = ({
  internship,
  isSaved = false,
  onSave,
  onOpen,
  animationDelay = 0,
}) => {
  const locationStr = [internship.city, internship.state].filter(Boolean).join(', ') || internship.location_text

  return (
    <div
      className="group relative flex flex-col p-4 rounded-lg border border-white/6 bg-obsidian-800
                 hover:border-amber-400/20 hover:bg-obsidian-700
                 transition-all duration-200 ease-out cursor-pointer
                 shadow-[0_1px_3px_rgba(0,0,0,0.4)]
                 hover:shadow-[0_4px_20px_rgba(0,0,0,0.5),0_0_0_1px_rgba(251,191,36,0.12)]
                 animate-fade-up"
      style={{ animationDelay: `${animationDelay}ms`, opacity: 0, animationFillMode: 'forwards' }}
      onClick={() => onOpen?.(internship.slug)}
    >
      {/* Top row: freshness + save button */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          {internship.freshness_bucket && freshnessLabel[internship.freshness_bucket] && (
            <span className="text-[10px] font-mono text-slate-600 uppercase tracking-wider">
              {freshnessLabel[internship.freshness_bucket]}
            </span>
          )}
        </div>
        <button
          onClick={(e) => { e.stopPropagation(); onSave?.(internship.id) }}
          className={`
            p-1.5 rounded-md transition-all duration-150
            ${isSaved
              ? 'text-amber-400 hover:text-amber-300'
              : 'text-slate-600 hover:text-slate-300 opacity-0 group-hover:opacity-100'
            }
          `}
          aria-label={isSaved ? 'Unsave' : 'Save'}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill={isSaved ? 'currentColor' : 'none'}
               stroke="currentColor" strokeWidth="2">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
          </svg>
        </button>
      </div>

      {/* Company name */}
      <p className="text-[11px] font-mono text-slate-500 mb-1 truncate">
        {internship.company_name}
      </p>

      {/* Title */}
      <h3 className="font-display text-base text-slate-100 leading-snug mb-3 line-clamp-2 group-hover:text-amber-50 transition-colors duration-150">
        {internship.title}
      </h3>

      {/* Meta row */}
      <div className="flex flex-wrap items-center gap-2 mb-3">
        <span className="text-[11px] font-sans text-slate-500 inline-flex items-center gap-1">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          {locationStr}
        </span>
        <span className="w-0.5 h-0.5 rounded-full bg-slate-700" />
        <Badge
          label={workModeLabel[internship.work_mode] || internship.work_mode}
          variant={internship.work_mode === 'remote' ? 'green' : internship.work_mode === 'hybrid' ? 'amber' : 'default'}
        />
        {internship.duration_text && (
          <>
            <span className="w-0.5 h-0.5 rounded-full bg-slate-700" />
            <span className="text-[11px] font-mono text-slate-600">{internship.duration_text}</span>
          </>
        )}
      </div>

      {/* Skills */}
      {internship.skills && internship.skills.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
          {internship.skills.slice(0, 4).map(skill => (
            <span key={skill} className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-white/4 text-slate-500 border border-white/6">
              {skill}
            </span>
          ))}
          {internship.skills.length > 4 && (
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-white/4 text-slate-600 border border-white/6">
              +{internship.skills.length - 4}
            </span>
          )}
        </div>
      )}

      {/* Bottom: stipend + deadline + trust */}
      <div className="flex items-center justify-between mt-auto pt-3 border-t border-white/5">
        <StipendDisplay
          min={internship.stipend_min}
          max={internship.stipend_max}
          size="md"
        />
        <div className="flex items-center gap-2">
          <DeadlineChip apply_by={internship.apply_by} is_expiring_soon={internship.is_expiring_soon} />
          <TrustBadge
            trust_score={internship.trust_score}
            verification_status={internship.verification_status}
            show_score={false}
          />
        </div>
      </div>
    </div>
  )
}
