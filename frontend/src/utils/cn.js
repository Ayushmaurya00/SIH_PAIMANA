/**
 * PAIMANA AI - Utility Helpers
 * Classname joiner, Indian Currency formatter, and Risk Score styling mappers.
 */

export function cn(...classes) {
  return classes.filter(Boolean).join(' ');
}

export function formatCurrency(val) {
  if (val === null || val === undefined || isNaN(val)) return '₹0 Cr';
  const num = Number(val);
  if (Math.abs(num) >= 100000) {
    return `₹${(num / 100000).toFixed(2)} Lakh Cr`;
  }
  return `₹${num.toLocaleString('en-IN', { maximumFractionDigits: 0 })} Cr`;
}

export function formatCr(val) {
  return formatCurrency(val);
}

export function getRiskLevel(score) {
  if (score >= 70) return 'High';
  if (score >= 40) return 'Medium';
  return 'Low';
}

export function getRiskColor(level) {
  const map = {
    High: 'text-red-400',
    Medium: 'text-amber-400',
    Low: 'text-emerald-400'
  };
  return map[level] || 'text-slateText-muted';
}

export function getRiskBg(level) {
  const map = {
    High: 'bg-red-950/40 border-red-800/40 text-red-400',
    Medium: 'bg-amber-950/40 border-amber-800/40 text-amber-400',
    Low: 'bg-emerald-950/40 border-emerald-800/40 text-emerald-400'
  };
  return map[level] || 'bg-surface-higher border-border-medium text-slateText-muted';
}
