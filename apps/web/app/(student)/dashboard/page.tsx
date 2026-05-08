'use client'

import { useState, useCallback } from 'react'
import { useInfiniteQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  RegionSelector, DomainSelector, InternshipCard,
  FilterChip, EmptyState, Button
} from '@repo/ui'
import { apiClient } from '@/lib/api-client'

const WORK_MODES = [
  { value: 'remote', label: 'Remote', icon: '🌐' },
  { value: 'hybrid', label: 'Hybrid', icon: '🔄' },
  { value: 'onsite', label: 'Onsite', icon: '🏢' },
]

const FRESHNESS = [
  { value: 'today', label: 'Today' },
  { value: 'yesterday', label: 'Yesterday' },
  { value: 'last_2_days', label: 'Last 2 days' },
  { value: 'this_week', label: 'This week' },
]

const SORT_OPTIONS = [
  { value: 'newest', label: 'Newest' },
  { value: 'stipend', label: 'Stipend ↑' },
  { value: 'deadline', label: 'Deadline' },
  { value: 'trust', label: 'Trust' },
]

export default function DashboardPage() {
  const [region, setRegion] = useState<string | null>(null)
  const [domain, setDomain] = useState<string | null>(null)
  const [workMode, setWorkMode] = useState<string | null>(null)
  const [freshness, setFreshness] = useState<string | null>(null)
  const [sort, setSort] = useState('newest')
  const [verifiedOnly, setVerifiedOnly] = useState(false)
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set())

  const queryClient = useQueryClient()
  const canSearch = !!region && !!domain

  const { data, fetchNextPage, hasNextPage, isFetchingNextPage, isLoading } = useInfiniteQuery({
    queryKey: ['internships', { region, domain, workMode, freshness, sort, verifiedOnly }],
    queryFn: ({ pageParam }) => apiClient.getInternships({
      region: region!, domain: domain!,
      work_mode: workMode, freshness, sort,
      verified_only: verifiedOnly,
      cursor: pageParam,
    }),
    initialPageParam: 0,
    getNextPageParam: (last: any) => last.meta?.cursor,
    enabled: canSearch,
  })

  const saveMutation = useMutation({
    mutationFn: (id: string) =>
      savedIds.has(id) ? apiClient.unsaveInternship(id) : apiClient.saveInternship(id),
    onMutate: (id) => {
      setSavedIds(prev => {
        const next = new Set(prev)
        next.has(id) ? next.delete(id) : next.add(id)
        return next
      })
    },
  })

  const allInternships = data?.pages.flatMap(p => p.data) ?? []

  return (
    <div className="min-h-screen bg-obsidian-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">

        {/* Header */}
        <div className="mb-8">
          <h1 className="font-display text-2xl text-slate-100 mb-1">
            Find your internship
          </h1>
          <p className="text-sm font-sans text-slate-500">
            Only paid. Only verified. Only India.
          </p>
        </div>

        {/* Step 1: Region */}
        <div className="mb-8">
          <RegionSelector value={region} onChange={setRegion} />
        </div>

        {/* Step 2: Domain — only show after region picked */}
        {region && (
          <div className="mb-8 animate-fade-up">
            <DomainSelector value={domain} onChange={setDomain} />
          </div>
        )}

        {/* Filters + Sort — only show after both picked */}
        {canSearch && (
          <div className="mb-6 animate-fade-up">
            <div className="flex flex-wrap items-center gap-4 mb-4">

              {/* Work mode */}
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono text-slate-600 uppercase tracking-wider mr-1">Mode</span>
                {WORK_MODES.map(m => (
                  <FilterChip
                    key={m.value}
                    label={m.label}
                    icon={m.icon}
                    selected={workMode === m.value}
                    onToggle={() => setWorkMode(prev => prev === m.value ? null : m.value)}
                  />
                ))}
              </div>

              {/* Freshness */}
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono text-slate-600 uppercase tracking-wider mr-1">Fresh</span>
                {FRESHNESS.map(f => (
                  <FilterChip
                    key={f.value}
                    label={f.label}
                    selected={freshness === f.value}
                    onToggle={() => setFreshness(prev => prev === f.value ? null : f.value)}
                  />
                ))}
              </div>

              {/* Verified only */}
              <FilterChip
                label="Verified only"
                icon="✦"
                selected={verifiedOnly}
                onToggle={() => setVerifiedOnly(v => !v)}
              />
            </div>

            {/* Sort */}
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-mono text-slate-600 uppercase tracking-wider mr-1">Sort</span>
              {SORT_OPTIONS.map(s => (
                <FilterChip
                  key={s.value}
                  label={s.label}
                  selected={sort === s.value}
                  onToggle={() => setSort(s.value)}
                />
              ))}
            </div>
          </div>
        )}

        {/* Results */}
        {!region && (
          <div className="py-24 text-center">
            <span className="font-mono text-4xl text-obsidian-700 block mb-4">◎</span>
            <p className="font-sans text-slate-600">Select a region to begin</p>
          </div>
        )}

        {region && !domain && (
          <div className="py-16 text-center animate-fade-up">
            <span className="font-mono text-3xl text-obsidian-700 block mb-4">◆</span>
            <p className="font-sans text-slate-600">Now pick your domain</p>
          </div>
        )}

        {canSearch && (
          <div>
            {isLoading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {Array.from({ length: 9 }).map((_, i) => (
                  <div key={i} className="h-52 rounded-lg bg-obsidian-800 animate-shimmer border border-white/5" />
                ))}
              </div>
            ) : allInternships.length === 0 ? (
              <EmptyState
                icon="◌"
                title="No internships found"
                message="Try adjusting your filters or selecting a broader region."
                action={{ label: 'Clear filters', onClick: () => { setWorkMode(null); setFreshness(null); setVerifiedOnly(false) } }}
              />
            ) : (
              <>
                <div className="flex items-center justify-between mb-4">
                  <p className="text-[11px] font-mono text-slate-600">
                    {data?.pages[0]?.meta?.total ?? 0} internships found
                  </p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {allInternships.map((internship, i) => (
                    <InternshipCard
                      key={internship.id}
                      internship={internship}
                      isSaved={savedIds.has(internship.id)}
                      onSave={(id: string) => saveMutation.mutate(id)}
                      onOpen={(slug: string) => window.location.href = `/internship/${slug}`}
                      animationDelay={i * 40}
                    />
                  ))}
                </div>
                {hasNextPage && (
                  <div className="flex justify-center mt-8">
                    <Button
                      variant="secondary"
                      size="md"
                      loading={isFetchingNextPage}
                      onClick={() => fetchNextPage()}
                    >
                      Load more
                    </Button>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
