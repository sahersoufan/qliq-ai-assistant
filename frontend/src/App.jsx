import { useState } from 'react'
import { Routes, Route, Link } from 'react-router-dom'

// Import pages
import Home from './pages/Home'
import Onboarding from './pages/Onboarding'
import Ask from './pages/Ask'
import Recommendations from './pages/Recommendations'
import Metrics from './pages/Metrics'
import ClassifierComparison from './pages/ClassifierComparison'

function App() {
  return (
    <div className="app">
      <header>
        <h1>QLIQ AI Assistant</h1>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/onboard">Onboarding</Link></li>
            <li><Link to="/ask">Ask</Link></li>
            <li><Link to="/recommendations">Recommendations</Link></li>
            <li><Link to="/metrics">Metrics</Link></li>
            <li><Link to="/classifier-compare">Classifier Comparison</Link></li>
          </ul>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/onboard" element={<Onboarding />} />
          <Route path="/ask" element={<Ask />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/metrics" element={<Metrics />} />
          <Route path="/classifier-compare" element={<ClassifierComparison />} />
        </Routes>
      </main>

      <footer>
        <p>&copy; 2025 QLIQ AI Assistant</p>
      </footer>
    </div>
  )
}

export default App