'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { OTPInput } from '@repo/ui'
import { ShieldCheck, ArrowLeft, RefreshCcw, Smartphone } from 'lucide-react'
import Link from 'next/link'

export default function VerificationPage() {
  const [isVerifying, setIsVerifying] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleComplete = async (code: string) => {
    setIsVerifying(true)
    setError(null)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    if (code === "123456") {
      // Success logic here
      console.log("Verified!")
    } else {
      setError("The code you entered is incorrect. Please try again.")
      setIsVerifying(false)
    }
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden bg-[#0D0D0F]">
      {/* Dynamic Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-amber-500/10 rounded-full blur-[120px] pointer-events-none" />
      
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="w-full max-w-md relative z-10"
      >
        {/* Back Button */}
        <Link 
          href="/"
          className="inline-flex items-center gap-2 text-sm text-slate-500 hover:text-amber-400 transition-colors mb-8 group"
        >
          <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          Back to sign in
        </Link>

        {/* Content Card */}
        <div className="glass rounded-3xl p-8 border border-white/10 shadow-2xl relative overflow-hidden">
          {/* Subtle Grain Overlay */}
          <div className="absolute inset-0 grain-bg pointer-events-none" />

          <div className="flex flex-col items-center text-center">
            {/* Icon Header */}
            <div className="w-16 h-16 rounded-2xl bg-amber-500/10 flex items-center justify-center mb-6 relative">
              <div className="absolute inset-0 rounded-2xl bg-amber-500/20 blur-xl animate-pulse" />
              <Smartphone className="w-8 h-8 text-amber-500 relative z-10" />
            </div>

            <h1 className="text-3xl font-display text-gradient mb-3">
              Verify your identity
            </h1>
            
            <p className="text-slate-400 text-sm leading-relaxed mb-8 px-4">
              Enter the code displayed in the app or on the device you're signing in to. 
              <span className="block mt-2 font-medium text-amber-500/80">
                Never use a code sent by someone else.
              </span>
            </p>

            {/* Input Section */}
            <div className="w-full mb-8">
              <OTPInput 
                length={6} 
                onComplete={handleComplete}
                disabled={isVerifying}
              />
            </div>

            <AnimatePresence mode="wait">
              {error && (
                <motion.p
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="text-red-400 text-xs font-medium mb-6"
                >
                  {error}
                </motion.p>
              )}
            </AnimatePresence>

            <div className="flex flex-col items-center gap-4 w-full">
              {isVerifying ? (
                <div className="flex items-center gap-3 text-amber-500 font-mono text-xs tracking-widest uppercase py-3">
                  <RefreshCcw className="w-4 h-4 animate-spin" />
                  Verifying Authenticity...
                </div>
              ) : (
                <button 
                  onClick={() => {/* Trigger resend */}}
                  className="text-xs text-slate-500 hover:text-white transition-colors flex items-center gap-2 group"
                >
                  Didn't receive a code? 
                  <span className="text-amber-500/80 group-hover:text-amber-400 font-medium">Resend Code</span>
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Security Footer */}
        <div className="mt-8 flex items-center justify-center gap-3 opacity-40">
          <ShieldCheck className="w-4 h-4" />
          <span className="text-[10px] font-mono tracking-widest uppercase">
            Secured by IIB Infrastructure
          </span>
        </div>
      </motion.div>
    </main>
  )
}
