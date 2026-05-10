'use client'

import React, { useState, Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { useQuery } from '@tanstack/react-query'
import { 
  RegionSelector, 
  DomainSelector, 
  InternshipCard, 
  EmptyState,
  Badge
} from '@repo/ui'
import { fetchInternships, Internship } from '@/lib/api'
import { Navbar } from '@/components/Navbar'

function InternshipDiscovery() {
  const searchParams = useSearchParams()
  const router = useRouter()

  // Get filters from URL or defaults
  const region = searchParams.get('region') || 'all-india'
  const domain = searchParams.get('domain') || 'web-development'
  const workMode = searchParams.get('work_mode') || undefined
  const sort = searchParams.get('sort') || 'newest'

  const { data, isLoading, error } = useQuery({
    queryKey: ['internships', { region, domain, workMode, sort }],
    queryFn: () => fetchInternships({
      region,
      domain,
      work_mode: workMode,
      sort,
      limit: 20
    }),
  })

  const updateFilter = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString())
    if (value) {
      params.set(key, value)
    } else {
      params.delete(key)
    }
    router.push(`/internships?${params.toString()}`)
  }

  const internships: Internship[] = data?.data || []

  return (
    <div className="min-h-screen bg-obsidian-950">
      <Navbar />
      
      <main className="pt-24 pb-20 px-6 max-w-7xl mx-auto">
        <header className="mb-12">
          <p className="text-[11px] font-mono text-amber-400 uppercase tracking-widest mb-2">Discovery Engine</p>
          <h1 className="font-display text-4xl text-slate-100 mb-6">Find your next role</h1>
          
          <div className="flex flex-col gap-8 p-6 rounded-xl border border-white/5 bg-obsidian-900">
            <RegionSelector 
              value={region} 
              onChange={(val) => updateFilter('region', val)} 
            />
            <div className="h-px bg-white/5" />
            <DomainSelector 
              value={domain} 
              onChange={(val) => updateFilter('domain', val)} 
            />
          </div>
        </header>

        <section>
          <div className="flex items-center justify-between mb-8 pb-4 border-b border-white/5">
            <div className="flex items-center gap-3">
              <h2 className="text-sm font-mono text-slate-400 uppercase tracking-wider">
                {isLoading ? 'Searching...' : `${internships.length} Verified Listings`}
              </h2>
              {!isLoading && internships.length > 0 && (
                <span className="px-2 py-0.5 rounded bg-verified-green-bg text-verified-green text-[10px] font-mono border border-verified-green/20">
                  LIVE DATA
                </span>
              )}
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-mono text-slate-600 uppercase">Sort by:</span>
              <select 
                value={sort}
                onChange={(e) => updateFilter('sort', e.target.value)}
                className="bg-transparent border-none text-xs font-sans text-slate-300 focus:ring-0 cursor-pointer"
              >
                <option value="newest" className="bg-obsidian-900">Newest First</option>
                <option value="stipend_high" className="bg-obsidian-900">High Stipend</option>
                <option value="trust_score" className="bg-obsidian-900">Trust Score</option>
              </select>
            </div>
          </div>

          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map(i => (
                <div key={i} className="h-48 rounded-lg bg-obsidian-800 animate-shimmer border border-white/5" />
              ))}
            </div>
          ) : error ? (
            <div className="py-20 text-center">
              <p className="text-rejected-red font-mono text-sm">Failed to connect to discovery engine.</p>
              <button 
                onClick={() => window.location.reload()}
                className="mt-4 text-xs font-sans text-slate-500 hover:text-slate-300 underline underline-offset-4"
              >
                Retry connection
              </button>
            </div>
          ) : internships.length === 0 ? (
            <EmptyState 
              title="No internships found" 
              description="Try adjusting your region or domain filters. Some combinations might not have active listings today."
              actionLabel="Reset filters"
              onAction={() => router.push('/internships')}
            />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {internships.map((internship, index) => (
                <InternshipCard 
                  key={internship.id} 
                  internship={internship as any} 
                  animationDelay={index * 50}
                  onOpen={(slug) => router.push(`/internships/${slug}`)}
                />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default function InternshipListingPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-obsidian-950 flex items-center justify-center text-slate-500 font-mono text-xs">INITIALIZING ENGINE...</div>}>
      <InternshipDiscovery />
    </Suspense>
  )
}
