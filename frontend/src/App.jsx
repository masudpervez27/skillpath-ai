import React, { useState } from 'react'
import { generateRoadmap } from './lib/api'

export default function App() {
  const [skillsInput, setSkillsInput] = useState('python, sql, pandas, fastapi')
  const [targetRole, setTargetRole] = useState('AI Engineer')
  const [weeks, setWeeks] = useState(8)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleRun() {
    setError('')
    setLoading(true)
    try {
      const currentSkills = skillsInput.split(',').map((s) => s.trim()).filter(Boolean)
      const data = await generateRoadmap({
        current_skills: currentSkills,
        target_role: targetRole,
        weeks: Number(weeks),
      })
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ maxWidth: 860, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>SkillPath AI</h1>
      <p>Personalized roadmap generation with skills-gap analysis and milestone planning.</p>
      <input
        value={targetRole}
        onChange={(e) => setTargetRole(e.target.value)}
        placeholder="Target role"
        style={{ width: '100%', marginBottom: '0.75rem' }}
      />
      <textarea
        value={skillsInput}
        onChange={(e) => setSkillsInput(e.target.value)}
        rows={4}
        style={{ width: '100%' }}
        placeholder="Comma-separated current skills"
      />
      <input
        type="number"
        min={4}
        max={24}
        value={weeks}
        onChange={(e) => setWeeks(e.target.value)}
        style={{ marginTop: '0.75rem' }}
      />
      <button onClick={handleRun} style={{ marginTop: '1rem', marginLeft: '0.5rem' }} disabled={loading}>
        {loading ? 'Planning...' : 'Generate Roadmap'}
      </button>
      {error ? <pre style={{ color: 'crimson' }}>{error}</pre> : null}
      {result ? (
        <section style={{ marginTop: '1rem' }}>
          <h3>Readiness Score: {result.readiness_score}</h3>
          <p><strong>Gap Skills:</strong> {result.gap_skills.join(', ') || 'None'}</p>
          <h3>Milestones</h3>
          {result.milestones.map((m) => (
            <article key={m.week} style={{ border: '1px solid #ddd', borderRadius: 8, padding: '0.75rem', marginBottom: '0.75rem' }}>
              <strong>Week {m.week}: {m.focus}</strong>
              <p>Outcomes:</p>
              <ul>{m.outcomes.map((o, i) => (<li key={i}>{o}</li>))}</ul>
              <p>Resources: {m.resources.join(', ')}</p>
            </article>
          ))}
        </section>
      ) : null}
    </main>
  )
}
