"use client"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"
import { Shield, Search, CheckCircle, Lock, Zap, Star } from "lucide-react"
import { useState } from "react"

const DOMAINS = [
  { label: "Android Development", emoji: "📱", value: "Android App Development" },
  { label: "Game Development",    emoji: "🎮", value: "Game Development" },
  { label: "iOS Development",     emoji: "🍎", value: "iOS App Development" },
  { label: "Web Development",     emoji: "💻", value: "Web Development" },
  { label: "Graphic Design",      emoji: "🎨", value: "Graphic Design" },
  { label: "Data Science",        emoji: "📊", value: "Data Science" },
]

const WORK_MODES = ["All", "Work from Home", "Work from Office", "Hybrid"]

export default function HomePage() {
  const router = useRouter()
  const [triggering, setTriggering] = useState(false)
  const [triggerStatus, setTriggerStatus] = useState("")

  async function handleStartFinding() {
    setTriggering(true)
    setTriggerStatus("Starting search...")
    try {
      const res = await fetch(
        "https://api.github.com/repos/subwaysuffer1045/iib-/actions/workflows/run_scraper.yml/dispatches",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${process.env.NEXT_PUBLIC_GH_TOKEN}`,
            Accept: "application/vnd.github+json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ ref: "main" }),
        }
      )
      if (res.status === 204) {
        setTriggerStatus("✅ Search started! Check back in 3 minutes.")
      } else {
        setTriggerStatus("⚠️ Could not start. Try manually on GitHub Actions.")
      }
    } catch {
      setTriggerStatus("❌ Network error. Try again.")
    }
    setTriggering(false)
  }

  return (
    <main className="min-h-screen bg-[#0D0D0F] text-[#F8F8F8] overflow-x-hidden">

      {/* NAV */}
      <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 bg-[#0D0D0F]/80 backdrop-blur-md border-b border-white/5">
        <span className="text-[#F5A623] font-bold text-lg">IIB India</span>
        <div className="flex gap-3 items-center">
          <a href="/login" className="text-[#A0A0AB] hover:text-[#F8F8F8] text-sm transition-colors">Login</a>
          <a href="/register" className="bg-[#F5A623] text-[#0D0D0F] text-sm font-bold px-4 py-2 rounded-lg hover:bg-[#F0B93A] transition-colors">Get Access</a>
        </div>
      </nav>

      {/* HERO */}
      <section className="relative flex flex-col items-center justify-center min-h-screen px-4 pt-20 text-center">
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="w-[700px] h-[500px] rounded-full"
               style={{background: 'radial-gradient(ellipse, rgba(245,166,35,0.10) 0%, transparent 70%)'}} />
        </div>

        <motion.div initial={{opacity:0,y:-10}} animate={{opacity:1,y:0}} transition={{duration:0.5}}
          className="mb-6 inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm text-[#A0A0AB]"
          style={{background:'rgba(255,255,255,0.05)', border:'1px solid rgba(255,255,255,0.1)'}}>
          <Lock size={13} className="text-[#F5A623]" />
          100% Verified · Zero Scam Tolerance · Mumbai Focus
        </motion.div>

        <motion.h1 initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{duration:0.6,delay:0.1}}
          className="text-5xl md:text-7xl font-bold leading-tight max-w-4xl mb-6"
          style={{fontFamily:"Georgia, serif"}}>
          Find Internships That
          <br />
          <span className="text-[#F5A623]">Actually Pay You</span>
        </motion.h1>

        <motion.p initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{duration:0.6,delay:0.2}}
          className="text-[#A0A0AB] text-lg max-w-xl mb-10">
          Zero scams. Zero unpaid. Mumbai + Pan-India listings verified daily.
        </motion.p>

        {/* START FINDING BUTTON */}
        <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{duration:0.6,delay:0.25}}
          className="mb-10">
          <button
            onClick={handleStartFinding}
            disabled={triggering}
            className="px-8 py-4 rounded-xl font-bold text-[#0D0D0F] text-lg transition-all duration-200"
            style={{
              background: triggering ? '#888' : '#F5A623',
              boxShadow: triggering ? 'none' : '0 0 30px rgba(245,166,35,0.4)'
            }}>
            {triggering ? "Starting..." : "🔍 Start Finding Internships"}
          </button>
          {triggerStatus && (
            <p className="mt-3 text-sm text-[#A0A0AB]">{triggerStatus}</p>
          )}
        </motion.div>

        {/* DOMAIN GRID */}
        <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{duration:0.6,delay:0.3}}
          className="grid grid-cols-2 md:grid-cols-3 gap-3 w-full max-w-2xl mb-16">
          {DOMAINS.map((d) => (
            <button key={d.value}
              onClick={() => router.push(`/internships?domain=${encodeURIComponent(d.value)}`)}
              className="flex items-center gap-3 px-4 py-4 rounded-xl text-left transition-all duration-200"
              style={{background:'#1A1A1E', border:'1px solid #2A2A30'}}
              onMouseEnter={e => {
                e.currentTarget.style.borderColor = '#F5A623'
                e.currentTarget.style.boxShadow = '0 0 20px rgba(245,166,35,0.15)'
              }}
              onMouseLeave={e => {
                e.currentTarget.style.borderColor = '#2A2A30'
                e.currentTarget.style.boxShadow = 'none'
              }}>
              <span className="text-2xl">{d.emoji}</span>
              <span className="text-sm font-medium text-[#F8F8F8]">{d.label}</span>
            </button>
          ))}
        </motion.div>

        {/* STATS */}
        <motion.div initial={{opacity:0}} animate={{opacity:1}} transition={{duration:0.6,delay:0.5}}
          className="flex items-center gap-4 px-8 py-5 rounded-2xl"
          style={{background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)'}}>
          {[
            {num:"2,400+", label:"Verified Listings"},
            {num:"0",      label:"Scams Allowed"},
            {num:"6",      label:"Tech Domains"},
          ].map((s, i) => (
            <div key={i} className="flex items-center gap-4">
              {i > 0 && <div className="w-px h-8" style={{background:'rgba(255,255,255,0.1)'}} />}
              <div className="text-center px-4">
                <div className="text-2xl font-bold text-[#F5A623]" style={{fontFamily:'monospace'}}>{s.num}</div>
                <div className="text-xs text-[#A0A0AB] uppercase tracking-wider mt-1">{s.label}</div>
              </div>
            </div>
          ))}
        </motion.div>
      </section>

      {/* HOW IT WORKS */}
      <section className="px-4 py-24 max-w-5xl mx-auto">
        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold mb-3">How It Works</h2>
          <p className="text-[#A0A0AB]">Three steps. No nonsense.</p>
        </div>
        <div className="grid md:grid-cols-3 gap-5">
          {[
            {icon:<Search size={22}/>, step:"01", title:"We Search", desc:"Bots scan Internshala, Adzuna, WorkIndia and more — Mumbai + Pan-India daily."},
            {icon:<Shield size={22}/>, step:"02", title:"We Verify", desc:"Paid gate, fraud detection, link validation. Scams blocked automatically."},
            {icon:<CheckCircle size={22}/>, step:"03", title:"You Apply", desc:"Only real, paid listings reach you. Click Apply and go."},
          ].map((item) => (
            <div key={item.step} className="p-6 rounded-2xl transition-all duration-300"
                 style={{background:'#1A1A1E', border:'2px solid #2A2A30', borderTop:'2px solid #F5A623'}}>
              <div className="w-11 h-11 rounded-xl flex items-center justify-center text-[#F5A623] mb-4"
                   style={{background:'rgba(245,166,35,0.1)'}}>
                {item.icon}
              </div>
              <div className="text-xs text-[#F5A623] font-mono mb-2">{item.step}</div>
              <h3 className="text-lg font-semibold mb-2">{item.title}</h3>
              <p className="text-[#A0A0AB] text-sm leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* TRUST */}
      <section className="px-4 py-24" style={{background:'#111113'}}>
        <div className="max-w-4xl mx-auto text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-3">
            Why Students <span className="text-[#F5A623]">Trust IIB</span>
          </h2>
          <p className="text-[#A0A0AB]">We are not a job board. We are a firewall.</p>
        </div>
        <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-4">
          {[
            {icon:<Zap size={18}/>, title:"Stipend Verified", desc:"Every listing confirmed paid. No unpaid traps."},
            {icon:<Shield size={18}/>, title:"Link Validated", desc:"Every apply link tested. No broken or fake links."},
            {icon:<Star size={18}/>, title:"Company Reviewed", desc:"Ambition Box + Glassdoor review links for every company."},
            {icon:<Lock size={18}/>, title:"Fraud Blocked", desc:"MLM, pay-to-apply, fake internships automatically rejected."},
          ].map((item) => (
            <div key={item.title} className="flex gap-4 p-5 rounded-xl"
                 style={{background:'#1A1A1E', border:'1px solid #2A2A30'}}>
              <div className="w-10 h-10 rounded-lg flex items-center justify-center text-[#F5A623] flex-shrink-0"
                   style={{background:'rgba(245,166,35,0.1)'}}>
                {item.icon}
              </div>
              <div>
                <h3 className="font-semibold mb-1 text-sm">{item.title}</h3>
                <p className="text-[#A0A0AB] text-sm">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* FOOTER */}
      <footer className="px-4 py-8 text-center text-sm"
              style={{borderTop:'1px solid rgba(255,255,255,0.05)', color:'#6B6B7A'}}>
        © 2026 IIB India · Built for students by a student · Mumbai 🧡
      </footer>
    </main>
  )
}
