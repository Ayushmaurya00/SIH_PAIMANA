// V.3 Simulation Graph Mathematical Generators (Exclusively rendered in V.3 Demo Mode)

export function generateSCurveData(project) {
  if (!project) return [];
  const progress = Number(project.physical_progress_pct) || 0;
  const approved = Number(project.approved_cost_cr) || 1;
  const expenditure = Number(project.cumulative_expenditure_cr) || 0;
  const expPct = Math.min(100, (expenditure / approved) * 100);
  const MONTHS = ["Jul'25","Aug'25","Sep'25","Oct'25","Nov'25","Dec'25","Jan'26","Feb'26","Mar'26","Apr'26","May'26","Jun'26"];

  return MONTHS.map((month, i) => {
    const t = (i + 1) / 12;
    const sCurve = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    const pidSeed = project.project_id ? project.project_id.charCodeAt(Math.min(4, project.project_id.length - 1)) : 7;
    const seed = (pidSeed * (i + 3)) % 100;
    const jitter = ((seed % 9) - 4) * 0.35;
    return {
      month,
      'Actual Progress (%)': parseFloat(Math.min(progress, Math.max(0, sCurve * progress + jitter)).toFixed(1)),
      'Financial Burn (% of Approved)': parseFloat(Math.min(expPct, Math.max(0, sCurve * expPct + jitter * 0.7)).toFixed(1)),
      'Planned Baseline (%)': parseFloat(Math.min(progress + 15, 100, t * (progress + 18)).toFixed(1)),
    };
  });
}

export function generatePhaseData(project) {
  if (!project) return [];
  const start = new Date(project.scheduled_start || '2023-01-01');
  const end = new Date(project.revised_completion || project.scheduled_completion || '2027-01-01');
  const totalMs = end - start;
  const progress = Number(project.physical_progress_pct) || 0;
  const phaseDefs = [
    { name: 'Land Acquisition & Right-of-Way Clearance', share: 0.12 },
    { name: 'Statutory & Environmental Clearances', share: 0.10 },
    { name: 'Detailed Engineering Design & Procurement', share: 0.18 },
    { name: 'Civil & Structural Construction Works', share: 0.40 },
    { name: 'Trial Runs, Safety Testing & Commissioning', share: 0.20 },
  ];

  let cumShare = 0;
  return phaseDefs.map((ph, i) => {
    const phaseStart = new Date(start.getTime() + cumShare * totalMs);
    cumShare += ph.share;
    const phaseEnd = new Date(start.getTime() + cumShare * totalMs);
    const phaseMidPct = (cumShare - ph.share / 2) * 100;

    let status, phasePct;
    if (progress > phaseMidPct + 15) { status = 'Completed'; phasePct = 100; }
    else if (progress > phaseMidPct - 20) { status = 'In Progress'; phasePct = Math.min(90, Math.max(10, progress - (phaseMidPct - 40))); }
    else { status = 'Not Started'; phasePct = 0; }

    if (project.status === 'Delayed' && i === 3 && status === 'In Progress') {
      status = 'Delayed';
      phasePct = Math.min(phasePct, 60);
    }
    const fmt = (d) => d.toLocaleDateString('en-IN', { month: 'short', year: '2-digit' });
    return { name: ph.name, period: `${fmt(phaseStart)} → ${fmt(phaseEnd)}`, status, pct: Math.round(phasePct), weeks: Math.round((phaseEnd - phaseStart) / (7 * 86400 * 1000)), idx: i + 1 };
  });
}
