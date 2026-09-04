export default function ScoreRing({ score = 0, size = 100, strokeWidth = 8, label = 'Score' }) {
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const progress = Math.min(100, Math.max(0, score))
  const offset = circumference - (progress / 100) * circumference

  const color = score >= 80 ? '#10b981' : score >= 60 ? '#f59e0b' : score >= 40 ? '#f97316' : '#ef4444'

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#1f2937" strokeWidth={strokeWidth} />
        <circle
          cx={size / 2} cy={size / 2} r={radius} fill="none"
          stroke={color} strokeWidth={strokeWidth}
          strokeDasharray={circumference} strokeDashoffset={offset}
          strokeLinecap="round" className="transition-all duration-700"
        />
      </svg>
      <div className="text-center -mt-[calc(100px+4px)]" style={{ marginTop: -(size + 4) }}>
        <div className="font-bold text-white" style={{ fontSize: size * 0.22 }}>{score}%</div>
        <div className="text-gray-500" style={{ fontSize: size * 0.12 }}>{label}</div>
      </div>
    </div>
  )
}
