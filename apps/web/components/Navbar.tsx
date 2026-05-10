'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export const Navbar = () => {
  const pathname = usePathname()
  
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4
                    border-b border-border-subtle bg-background-base/80 backdrop-blur-md">
      <Link href="/" className="flex items-center gap-2">
        <div className="w-5 h-5 bg-accent-amber rounded-sm"></div>
        <span className="font-sans font-bold text-base tracking-wider text-text-primary">IIB INDIA</span>
      </Link>
      <div className="flex items-center gap-6">
        <div className="hidden md:flex items-center gap-6">
          <Link href="/internships" 
            className={`text-[10px] font-mono uppercase tracking-widest transition-colors
              ${pathname === '/internships' ? 'text-accent-amber' : 'text-text-muted hover:text-text-primary'}`}>
            Discovery
          </Link>
          <div className="glass px-3 py-1 rounded-full text-[10px] font-medium text-text-secondary hidden lg:block">
            🔒 100% Verified Listings
          </div>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/login"
            className="text-xs font-sans text-text-muted hover:text-accent-amber transition-colors duration-150">
            Login
          </Link>
          <Link href="/register"
            className="text-xs font-sans font-bold px-4 py-1.5 rounded-md
                       bg-accent-amber text-background-base
                       hover:bg-accent-amber-hover transition-colors duration-150 shadow-sm shadow-accent-amber/10">
            Get Access
          </Link>
        </div>
      </div>
    </nav>
  )
}
