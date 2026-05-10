'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { 
  CheckCircle2, 
  ShieldCheck, 
  Link as LinkIcon, 
  Building2, 
  Smartphone, 
  ShieldAlert,
} from 'lucide-react';
import { Navbar } from '@/components/Navbar';

// --- Components ---

const DomainCard = ({ icon, name, delay, slug }: { icon: string | React.ReactNode, name: string, delay: number, slug: string }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ delay, duration: 0.5 }}
    whileHover={{ y: -2 }}
    className="bg-background-surface border border-border-subtle p-4 rounded-lg cursor-pointer amber-glow flex items-center gap-4 group"
  >
    <Link href={`/internships?domain=${slug}&region=all-india`} className="flex items-center gap-4 w-full">
      <div className="w-10 h-10 bg-background-base rounded-md flex items-center justify-center group-hover:scale-110 transition-transform">
        {typeof icon === 'string' ? <span className="text-xl">{icon}</span> : icon}
      </div>
      <span className="font-sans font-medium text-sm text-text-secondary group-hover:text-text-primary transition-colors">{name}</span>
    </Link>
  </motion.div>
);

const TrustCard = ({ icon: Icon, title, description, delay }: { icon: any, title: string, description: string, delay: number }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ delay, duration: 0.5 }}
    className="bg-background-surface border border-border-subtle p-4 rounded-lg flex items-center gap-4 transition-all"
  >
    <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center text-accent-amber">
      <Icon className="w-5 h-5" />
    </div>
    <div className="space-y-0.5">
      <h3 className="font-sans font-bold text-xs text-text-primary">{title}</h3>
      <p className="font-sans text-[11px] text-text-muted leading-tight">{description}</p>
    </div>
  </motion.div>
);

const StepCard = ({ number, title, description, delay }: { number: number, title: string, description: string, delay: number }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ delay, duration: 0.5 }}
    className="glass p-6 rounded-xl space-y-4"
  >
    <div className="w-8 h-8 rounded-full bg-accent-amber/15 border border-accent-amber flex items-center justify-center text-accent-amber font-mono font-bold text-sm">
      {number}
    </div>
    <div className="space-y-2">
      <h3 className="font-sans font-bold text-base">{title}</h3>
      <p className="font-sans text-text-muted text-sm leading-relaxed">{description}</p>
    </div>
  </motion.div>
);

export default function LandingPage() {
  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Effects */}
      <div className="fixed inset-0 grain-bg z-0 pointer-events-none" />
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] hero-glow z-0 pointer-events-none" />

      <Navbar />

      <main className="relative z-10 pt-32">
        
        {/* Hero Section */}
        <section className="flex flex-col items-center justify-center px-6 text-center max-w-5xl mx-auto mb-20">
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="font-display text-6xl md:text-7xl max-w-3xl leading-[1.1] mb-4"
          >
            Find Internships That<br />
            <span className="text-gradient">Actually Pay You</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="font-sans text-lg md:text-xl text-text-muted max-w-2xl mb-12"
          >
            Zero scams. Zero unpaid. Every listing verified before you see it.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 w-full max-w-4xl"
          >
            <DomainCard icon="📱" name="Android Development" slug="android-development" delay={0.1} />
            <DomainCard icon="🎮" name="Game Development" slug="game-development" delay={0.2} />
            <DomainCard icon="🍎" name="iOS Development" slug="app-development" delay={0.3} />
            <DomainCard icon="💻" name="Web Development" slug="web-development" delay={0.4} />
            <DomainCard icon="🎨" name="Graphic Design" slug="graphic-design" delay={0.5} />
            <DomainCard icon="📊" name="Data Science" slug="data-science" delay={0.6} />
          </motion.div>
        </section>

        {/* Stats Bar */}
        <section className="border-y border-border-subtle py-10 mb-20">
          <div className="max-w-4xl mx-auto px-6">
            <div className="flex flex-col md:flex-row justify-center gap-8 md:gap-20 items-center text-center">
              <div className="space-y-1">
                <div className="font-mono text-accent-amber text-3xl font-bold">2,400+</div>
                <div className="font-sans text-text-muted tracking-widest uppercase text-[10px] font-medium">Verified Listings</div>
              </div>
              <div className="hidden md:block w-px h-10 bg-border-subtle" />
              <div className="space-y-1">
                <div className="font-mono text-accent-amber text-3xl font-bold">0</div>
                <div className="font-sans text-text-muted tracking-widest uppercase text-[10px] font-medium">Scams Allowed</div>
              </div>
              <div className="hidden md:block w-px h-10 bg-border-subtle" />
              <div className="space-y-1">
                <div className="font-mono text-accent-amber text-3xl font-bold">6</div>
                <div className="font-sans text-text-muted tracking-widest uppercase text-[10px] font-medium">Tech Domains</div>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section id="how-it-works" className="px-6 max-w-5xl mx-auto mb-24">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StepCard 
              number={1} 
              title="We Search" 
              description="Our bots scan 10+ major platforms daily to find the highest paying roles." 
              delay={0.1} 
            />
            <StepCard 
              number={2} 
              title="We Verify" 
              description="8-point company check ensures legitimacy and confirmed payment status." 
              delay={0.2} 
            />
            <StepCard 
              number={3} 
              title="You Apply" 
              description="Apply with confidence knowing every listing is active and scam-free." 
              delay={0.3} 
            />
          </div>
        </section>

        {/* Trust Proof Section */}
        <section id="trust" className="py-24 px-10 max-w-7xl mx-auto border-t border-border-subtle bg-background-surface/20">
          <div className="flex flex-col md:flex-row items-center gap-20">
            <div className="flex-1 space-y-8">
              <h2 className="font-display text-5xl md:text-6xl">Why Students<br /><span className="text-gradient">Trust IIB</span></h2>
              <p className="text-text-muted text-lg leading-relaxed max-w-lg">
                We're not another job aggregator. We're a firewall. Every listing is manually checked to prevent the "internship scam" epidemic in India.
              </p>
              <div className="flex flex-wrap gap-6">
                <div className="flex items-center gap-2 text-trust-verified text-sm font-medium">
                  <CheckCircle2 className="w-4 h-4" />
                  Stipend Verified
                </div>
                <div className="flex items-center gap-2 text-trust-verified text-sm font-medium">
                  <ShieldCheck className="w-4 h-4" />
                  Anti-Scam Protocol
                </div>
              </div>
            </div>
            
            <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
              <TrustCard icon={Smartphone} title="Stipend Verified" description="Confirmed minimum stipend and payment cycle protocol." delay={0.1} />
              <TrustCard icon={LinkIcon} title="Validated Application" description="Every link is checked for validity and actual source safety." delay={0.2} />
              <TrustCard icon={Building2} title="Domain Verification" description="Company history and authority score checking system." delay={0.3} />
              <TrustCard icon={ShieldAlert} title="Spam Filtered" description="Removal of unpaid, low-quality, or pyramid scheme traps." delay={0.4} />
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="border-t border-border-subtle py-8 px-10 flex flex-col md:flex-row justify-between items-center gap-4 bg-background-surface">
          <div className="text-xs text-text-muted">
            &copy; 2024 IIB India • Built for students by a student
          </div>
          <div className="flex gap-6 text-[11px] font-bold tracking-wider uppercase">
            <Link href="/privacy" className="text-text-dim hover:text-text-primary transition-colors">Privacy Policy</Link>
            <Link href="/terms" className="text-text-dim hover:text-text-primary transition-colors">Terms of Service</Link>
            <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-accent-amber hover:text-white transition-colors">GitHub</a>
          </div>
        </footer>
      </main>
    </div>
  );
}
