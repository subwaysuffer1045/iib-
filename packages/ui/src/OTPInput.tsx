import React, { useRef, useState, useEffect } from 'react'

interface OTPInputProps {
  length?: number
  onComplete: (code: string) => void
  disabled?: boolean
}

export const OTPInput: React.FC<OTPInputProps> = ({
  length = 6,
  onComplete,
  disabled = false
}) => {
  const [otp, setOtp] = useState<string[]>(new Array(length).fill(""))
  const inputs = useRef<(HTMLInputElement | null)[]>([])

  const handleChange = (element: HTMLInputElement, index: number) => {
    const value = element.value.replace(/[^0-9]/g, "")
    if (!value) return

    const newOtp = [...otp]
    newOtp[index] = value.substring(value.length - 1)
    setOtp(newOtp)

    // Move to next input
    if (index < length - 1) {
      inputs.current[index + 1]?.focus()
    }

    // Check if complete
    if (newOtp.every(val => val !== "") && newOtp.length === length) {
      onComplete(newOtp.join(""))
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>, index: number) => {
    if (e.key === "Backspace") {
      if (!otp[index] && index > 0) {
        const newOtp = [...otp]
        newOtp[index - 1] = ""
        setOtp(newOtp)
        inputs.current[index - 1]?.focus()
      } else {
        const newOtp = [...otp]
        newOtp[index] = ""
        setOtp(newOtp)
      }
    } else if (e.key === "ArrowLeft" && index > 0) {
      inputs.current[index - 1]?.focus()
    } else if (e.key === "ArrowRight" && index < length - 1) {
      inputs.current[index + 1]?.focus()
    }
  }

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault()
    const data = e.clipboardData.getData("text").replace(/[^0-9]/g, "").substring(0, length)
    if (!data) return

    const newOtp = [...otp]
    data.split("").forEach((char, idx) => {
      newOtp[idx] = char
    })
    setOtp(newOtp)

    const lastIdx = Math.min(data.length, length - 1)
    inputs.current[lastIdx]?.focus()

    if (data.length === length) {
      onComplete(data)
    }
  }

  return (
    <div className="flex gap-3 justify-center">
      {otp.map((digit, index) => (
        <input
          key={index}
          type="text"
          inputMode="numeric"
          autoComplete="one-time-code"
          maxLength={1}
          value={digit}
          disabled={disabled}
          ref={(el) => { inputs.current[index] = el; }}
          onChange={(e) => handleChange(e.target, index)}
          onKeyDown={(e) => handleKeyDown(e, index)}
          onPaste={handlePaste}
          className={`
            w-12 h-14 text-center text-2xl font-mono font-semibold
            bg-white/5 border rounded-lg transition-all duration-200
            focus:outline-none focus:ring-2 focus:ring-amber-500/40
            ${digit
              ? 'border-amber-500/50 text-amber-400 bg-amber-500/5 shadow-[0_0_15px_rgba(245,166,35,0.1)]'
              : 'border-white/10 text-white/90 hover:border-white/20'
            }
            ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-text'}
          `}
        />
      ))}
    </div>
  )
}
