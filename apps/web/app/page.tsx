import Link from 'next/link'

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-obsidian-950 overflow-hidden">

      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4
                      border-b border-white/5 bg-obsidian-950/80 backdrop-blur-md">
        <div className="flex items-center gap-2">
          <span className="font-mono text-amber-400 text-sm">◆</span>
          <span className="font-display text-slate-100 text-base">IIB India</span>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/login"
            className="text-sm font-sans text-slate-400 hover:text-slate-200 transition-colors duration-150">
            Sign in
          </Link>
          <Link href="/register"
            className="text-sm font-sans font-medium px-4 py-1.5 rounded-md
                       bg-amber-400 text-obsidian-950
                       hover:bg-amber-300 transition-colors duration-150">
            Get access
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative flex flex-col items-center justify-center min-h-screen px-6 text-center pt-16">

        {/* Background glow */}
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2
                        w-[600px] h-[400px] rounded-full
                        bg-amber-400/4 blur-[120px] pointer-events-none" />

        {/* Grid pattern */}
        <div className="absolute inset-0 opacity-[0.03]"
             style={{
               backgroundImage: `linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                                 linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)`,
               backgroundSize: '40px 40px',
             }} />

        <div className="relative z-10 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full
                          bg-amber-400/8 border border-amber-400/20 mb-8">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse" />
            <span className="text-[11px] font-mono text-amber-400 uppercase tracking-widest">
              India Only · Paid Internships · Verified Companies
            </span>
          </div>

          <h1 className="font-display text-5xl md:text-6xl lg:text-7xl text-slate-100 leading-[1.05] mb-6">
            Find internships
            <br />
            <span className="text-amber-400 italic">worth your time.</span>
          </h1>

          <p className="font-sans text-lg text-slate-400 leading-relaxed mb-10 max-w-xl mx-auto">
            7 independent verification checks before a single internship
            reaches you. Only paid. Only real companies.
          </p>

          <div className="flex items-center justify-center gap-4">
            <Link href="/register"
              className="px-6 py-3 rounded-lg text-sm font-sans font-semibold
                         bg-amber-400 text-obsidian-950
                         hover:bg-amber-300 hover:shadow-[0_0_30px_rgba(251,191,36,0.3)]
                         transition-all duration-200">
              Start for free
            </Link>
            <Link href="#how-it-works"
              className="px-6 py-3 rounded-lg text-sm font-sans font-medium
                         bg-white/5 text-slate-300 border border-white/10
                         hover:bg-white/8 hover:border-white/20
                         transition-all duration-200">
              How it works
            </Link>
          </div>
        </div>

        {/* Stats bar */}
        <div className="relative z-10 mt-20 flex items-center gap-8 md:gap-16
                        px-8 py-4 rounded-xl border border-white/6 bg-obsidian-800/60 backdrop-blur-sm">
          {[
            { label: 'Verification Checks', value: '7' },
            { label: 'Hard Reject Rules', value: '12' },
            { label: 'Indian Cities', value: '15+' },
            { label: 'Always Free', value: '₹0' },
          ].map(stat => (
            <div key={stat.label} className="flex flex-col items-center">
              <span className="font-display text-2xl text-amber-400">{stat.value}</span>
              <span className="text-[10px] font-mono text-slate-600 uppercase tracking-wider mt-0.5">{stat.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="px-6 py-24 max-w-5xl mx-auto">
        <p className="text-[11px] font-mono text-slate-600 uppercase tracking-widest text-center mb-3">How it works</p>
        <h2 className="font-display text-3xl text-slate-100 text-center mb-16">Intelligence, not just search</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            {
              step: '01',
              title: 'Pick your region first',
              desc: 'Mumbai. Bengaluru. Remote. Delhi NCR. Location before domain — the only filter order that makes sense.',
              icon: '◎',
            },
            {
              step: '02',
              title: 'We verify the company',
              desc: 'MCA21 registry. GSTIN check. WHOIS domain age. ATS platform. Site structure. Public footprint. 7 checks. Not 1.',
              icon: '◆',
            },
            {
              step: '03',
              title: 'Only paid listings reach you',
              desc: 'Training fee? Auto-rejected. WhatsApp apply link? Auto-rejected. Zero stipend? Never published.',
              icon: '✦',
            },
          ].map(item => (
            <div key={item.step} className="p-6 rounded-xl border border-white/6 bg-obsidian-800">
              <div className="flex items-start justify-between mb-4">
                <span className="font-mono text-2xl text-obsidian-600">{item.icon}</span>
                <span className="font-mono text-[10px] text-slate-700 uppercase tracking-widest">{item.step}</span>
              </div>
              <h3 className="font-display text-lg text-slate-100 mb-2">{item.title}</h3>
              <p className="text-sm font-sans text-slate-500 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 px-6 py-8 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="font-mono text-amber-400 text-sm">◆</span>
          <span className="font-display text-slate-500 text-sm">IIB India</span>
        </div>
        <div className="flex items-center gap-6">
          <Link href="/privacy" className="text-xs font-sans text-slate-600 hover:text-slate-400 transition-colors">Privacy</Link>
          <Link href="/terms" className="text-xs font-sans text-slate-600 hover:text-slate-400 transition-colors">Terms</Link>
        </div>
      </footer>
    </main>
  )
}
