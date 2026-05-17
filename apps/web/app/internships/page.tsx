"use client"
import { useRouter, useSearchParams } from "next/navigation"
import { useEffect, useState, Suspense } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { ArrowLeft, MapPin, Clock, IndianRupee, ExternalLink, Wifi, Building2, Layers, Filter, ChevronDown, AlertCircle, Loader2 } from "lucide-react"

// ─── Types ────────────────────────────────────────────────────
interface Internship {
  id: string
  slug: string
  title: string
  company_name: string
  company_trust_score: number
  city: string | null
  state: string | null
  location_text: string | null
  work_mode: string
  stipend_min: number | null
  stipend_max: number | null
  stipend_text: string | null
  apply_by: string | null
  duration_text: string | null
  trust_score: number
  verification_status: string
  freshness_bucket: string | null
  skills: string[]
  posted_at: string | null
}

// ─── Constants ────────────────────────────────────────────────
const DOMAIN_META: Record<string, { emoji: string; color: string }> = {
  "Web Development":         { emoji: "💻", color: "#F5A623" },
  "Android App Development": { emoji: "📱", color: "#4CAF50" },
  "Game Development":        { emoji: "🎮", color: "#9C27B0" },
  "iOS App Development":     { emoji: "🍎", color: "#2196F3" },
  "Graphic Design":          { emoji: "🎨", color: "#E91E63" },
  "Data Science":            { emoji: "📊", color: "#00BCD4" },
}

const WORK_MODE_LABELS: Record<string, string> = {
  remote: "Work From Home",
  hybrid: "Hybrid",
  onsite: "On-site",
}

const WORK_MODE_ICONS: Record<string, typeof Wifi> = {
  remote: Wifi,
  hybrid: Layers,
  onsite: Building2,
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// ─── Helper: stipend display ──────────────────────────────────
function formatStipend(item: Internship): string {
  if (item.stipend_text) return item.stipend_text
  if (item.stipend_min) {
    const min = `₹${(item.stipend_min / 1000).toFixed(0)}K`
    const max = item.stipend_max ? `–₹${(item.stipend_max / 1000).toFixed(0)}K` : ""
    return `${min}${max}/mo`
  }
  return "Stipend N/A"
}

// ─── Card ─────────────────────────────────────────────────────
function InternshipCard({ item, index }: { item: Internship; index: number }) {
  const router = useRouter()
  const WorkIcon = WORK_MODE_ICONS[item.work_mode] || Building2
  const modeLabel = WORK_MODE_LABELS[item.work_mode] || item.work_mode
  const stipend = formatStipend(item)

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay: index * 0.04 }}
      onClick={() => router.push(`/internships/${item.slug}`)}
      className="group cursor-pointer rounded-2xl p-5 transition-all duration-200"
      style={{
        background: "#1A1A1E",
        border: "1px solid #2A2A30",
      }}
      onMouseEnter={e => {
        e.currentTarget.style.borderColor = "#F5A623"
        e.currentTarget.style.boxShadow = "0 0 24px rgba(245,166,35,0.12)"
        e.currentTarget.style.transform = "translateY(-2px)"
      }}
      onMouseLeave={e => {
        e.currentTarget.style.borderColor = "#2A2A30"
        e.currentTarget.style.boxShadow = "none"
        e.currentTarget.style.transform = "translateY(0)"
      }}
    >
      {/* Top row */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex-1 min-w-0">
          <p className="text-xs text-[#A0A0AB] mb-1 truncate">{item.company_name}</p>
          <h3 className="font-semibold text-[#F8F8F8] text-base leading-snug line-clamp-2">
            {item.title}
          </h3>
        </div>
        {/* Trust badge */}
        <div
          className="flex-shrink-0 text-xs font-mono px-2 py-1 rounded-lg"
          style={{
            background: item.trust_score >= 70 ? "rgba(76,175,80,0.15)" : "rgba(245,166,35,0.12)",
            color: item.trust_score >= 70 ? "#4CAF50" : "#F5A623",
            border: `1px solid ${item.trust_score >= 70 ? "rgba(76,175,80,0.3)" : "rgba(245,166,35,0.2)"}`,
          }}
        >
          {item.trust_score}
        </div>
      </div>

      {/* Meta pills */}
      <div className="flex flex-wrap gap-2 mb-4">
        {/* Stipend */}
        <span
          className="inline-flex items-center gap-1 text-xs px-3 py-1 rounded-full font-medium"
          style={{ background: "rgba(245,166,35,0.12)", color: "#F5A623" }}
        >
          <IndianRupee size={11} />
          {stipend}
        </span>

        {/* Work mode */}
        <span
          className="inline-flex items-center gap-1 text-xs px-3 py-1 rounded-full"
          style={{ background: "rgba(255,255,255,0.06)", color: "#A0A0AB" }}
        >
          <WorkIcon size={11} />
          {modeLabel}
        </span>

        {/* Location */}
        {(item.city || item.location_text) && (
          <span
            className="inline-flex items-center gap-1 text-xs px-3 py-1 rounded-full"
            style={{ background: "rgba(255,255,255,0.06)", color: "#A0A0AB" }}
          >
            <MapPin size={11} />
            {item.city || item.location_text}
          </span>
        )}

        {/* Duration */}
        {item.duration_text && (
          <span
            className="inline-flex items-center gap-1 text-xs px-3 py-1 rounded-full"
            style={{ background: "rgba(255,255,255,0.06)", color: "#A0A0AB" }}
          >
            <Clock size={11} />
            {item.duration_text}
          </span>
        )}
      </div>

      {/* Skills */}
      {item.skills && item.skills.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-4">
          {item.skills.slice(0, 4).map((s) => (
            <span
              key={s}
              className="text-[10px] px-2 py-0.5 rounded"
              style={{ background: "#25252B", color: "#A0A0AB" }}
            >
              {s}
            </span>
          ))}
          {item.skills.length > 4 && (
            <span className="text-[10px] px-2 py-0.5 rounded" style={{ background: "#25252B", color: "#A0A0AB" }}>
              +{item.skills.length - 4}
            </span>
          )}
        </div>
      )}

      {/* Apply button */}
      <div className="flex items-center justify-between">
        {item.apply_by && (
          <span className="text-xs text-[#6B6B7A]">
            Apply by {new Date(item.apply_by).toLocaleDateString("en-IN", { day: "numeric", month: "short" })}
          </span>
        )}
        <span
          className="ml-auto inline-flex items-center gap-1.5 text-xs font-semibold px-4 py-2 rounded-xl transition-all duration-200"
          style={{ background: "#F5A623", color: "#0D0D0F" }}
        >
          Apply <ExternalLink size={11} />
        </span>
      </div>
    </motion.div>
  )
}

// ─── Filter bar ───────────────────────────────────────────────
function FilterBar({
  workMode, setWorkMode,
  sortBy, setSortBy,
  total,
}: {
  workMode: string
  setWorkMode: (v: string) => void
  sortBy: string
  setSortBy: (v: string) => void
  total: number
}) {
  return (
    <div className="flex flex-wrap items-center gap-3 mb-6">
      <span className="text-sm text-[#A0A0AB] mr-auto">
        <span className="text-[#F8F8F8] font-semibold">{total}</span> verified listings
      </span>

      {/* Work mode filter */}
      <div className="relative">
        <select
          value={workMode}
          onChange={e => setWorkMode(e.target.value)}
          className="appearance-none text-xs pl-3 pr-8 py-2 rounded-xl cursor-pointer outline-none"
          style={{ background: "#1A1A1E", border: "1px solid #2A2A30", color: "#F8F8F8" }}
        >
          <option value="">All Modes</option>
          <option value="remote">Work From Home</option>
          <option value="hybrid">Hybrid</option>
          <option value="onsite">On-site</option>
        </select>
        <ChevronDown size={12} className="absolute right-2 top-1/2 -translate-y-1/2 text-[#A0A0AB] pointer-events-none" />
      </div>

      {/* Sort */}
      <div className="relative">
        <select
          value={sortBy}
          onChange={e => setSortBy(e.target.value)}
          className="appearance-none text-xs pl-3 pr-8 py-2 rounded-xl cursor-pointer outline-none"
          style={{ background: "#1A1A1E", border: "1px solid #2A2A30", color: "#F8F8F8" }}
        >
          <option value="newest">Newest First</option>
          <option value="stipend">Highest Stipend</option>
          <option value="trust">Most Trusted</option>
        </select>
        <ChevronDown size={12} className="absolute right-2 top-1/2 -translate-y-1/2 text-[#A0A0AB] pointer-events-none" />
      </div>
    </div>
  )
}

// ─── Main page (inner, uses useSearchParams) ──────────────────
function InternshipsPageInner() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const domain = searchParams.get("domain") || "Web Development"
  const meta = DOMAIN_META[domain] || { emoji: "💼", color: "#F5A623" }

  const [internships, setInternships] = useState<Internship[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [workMode, setWorkMode] = useState("")
  const [sortBy, setSortBy] = useState("newest")

  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      setError(null)
      try {
        const params = new URLSearchParams({
          domain,
          region: "all-india",
          limit: "50",
          sort: sortBy,
        })
        if (workMode) params.set("work_mode", workMode)

        const res = await fetch(`${API_BASE}/api/v1/internships?${params}`)
        if (!res.ok) throw new Error(`API error ${res.status}`)
        const json = await res.json()
        setInternships(json.data || [])
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Failed to load internships")
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [domain, workMode, sortBy])

  return (
    <main className="min-h-screen bg-[#0D0D0F] text-[#F8F8F8]">
      {/* NAV */}
      <nav className="sticky top-0 z-50 flex items-center gap-4 px-6 py-4 bg-[#0D0D0F]/90 backdrop-blur-md border-b border-white/5">
        <button
          onClick={() => router.push("/")}
          className="flex items-center gap-2 text-[#A0A0AB] hover:text-[#F8F8F8] text-sm transition-colors"
        >
          <ArrowLeft size={16} /> Back
        </button>
        <div className="flex items-center gap-2 ml-2">
          <span className="text-xl">{meta.emoji}</span>
          <span className="font-semibold text-[#F8F8F8]">{domain}</span>
        </div>
        <span className="ml-auto text-[#F5A623] font-bold text-lg">IIB India</span>
      </nav>

      <div className="max-w-5xl mx-auto px-4 py-10">
        {/* Header */}
        <div className="mb-8">
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-3xl md:text-4xl font-bold mb-2"
            style={{ fontFamily: "Georgia, serif" }}
          >
            {meta.emoji} {domain}
            <span className="text-[#F5A623]"> Internships</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.15 }}
            className="text-[#A0A0AB] text-sm"
          >
            Verified · Paid · Mumbai + Pan-India
          </motion.p>
        </div>

        {/* Filter bar */}
        <FilterBar
          workMode={workMode} setWorkMode={setWorkMode}
          sortBy={sortBy} setSortBy={setSortBy}
          total={internships.length}
        />

        {/* States */}
        <AnimatePresence mode="wait">
          {loading && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center py-32 gap-4"
            >
              <Loader2 size={32} className="text-[#F5A623] animate-spin" />
              <p className="text-[#A0A0AB] text-sm">Loading verified internships...</p>
            </motion.div>
          )}

          {!loading && error && (
            <motion.div
              key="error"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center py-32 gap-4"
            >
              <AlertCircle size={32} className="text-red-400" />
              <p className="text-[#A0A0AB] text-sm">{error}</p>
              <button
                onClick={() => setWorkMode("")}
                className="text-xs px-4 py-2 rounded-lg"
                style={{ background: "#1A1A1E", border: "1px solid #2A2A30", color: "#F8F8F8" }}
              >
                Retry
              </button>
            </motion.div>
          )}

          {!loading && !error && internships.length === 0 && (
            <motion.div
              key="empty"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center py-32 gap-3"
            >
              <span className="text-5xl">🔍</span>
              <p className="text-[#F8F8F8] font-semibold">No internships found</p>
              <p className="text-[#A0A0AB] text-sm">Try changing filters or run the scraper.</p>
            </motion.div>
          )}

          {!loading && !error && internships.length > 0 && (
            <motion.div
              key="grid"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="grid md:grid-cols-2 gap-4"
            >
              {internships.map((item, i) => (
                <InternshipCard key={item.id} item={item} index={i} />
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  )
}

// ─── Export (Suspense wrapper required for useSearchParams) ───
export default function InternshipsPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-[#0D0D0F] flex items-center justify-center">
        <Loader2 size={28} className="text-[#F5A623] animate-spin" />
      </div>
    }>
      <InternshipsPageInner />
    </Suspense>
  )
}
