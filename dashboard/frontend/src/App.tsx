import React, { useState } from 'react';
import { PageId } from './components/Navigation';

import { AmbientDashboard } from './pages/AmbientDashboard';
import { DatasetPage } from './pages/Dataset';
import { TrainingStudio } from './pages/TrainingStudio';
import { RunsComparePage } from './pages/RunsCompare';
import { ResultsPage } from './pages/Results';
import { AblationsPage } from './pages/Ablations';
import { RobustnessPage } from './pages/Robustness';
import { ExplainabilityPage } from './pages/Explainability';
import { InferenceLab } from './pages/InferenceLab';
import { EfficiencyPage } from './pages/Efficiency';
import { PaperAssetsPage } from './pages/PaperAssets';
import { JobsLogsPage } from './pages/JobsLogs';
import { SettingsPage } from './pages/Settings';
import { ArrowLeft, Home } from 'lucide-react';

export const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<PageId>('overview');

  const renderModulePage = () => {
    switch (currentPage) {
      case 'inference':
        return <InferenceLab />;
      case 'dataset':
        return <DatasetPage />;
      case 'training':
        return <TrainingStudio />;
      case 'runs':
        return <RunsComparePage />;
      case 'results':
        return <ResultsPage />;
      case 'ablations':
        return <AblationsPage />;
      case 'robustness':
        return <RobustnessPage />;
      case 'explainability':
        return <ExplainabilityPage />;
      case 'efficiency':
        return <EfficiencyPage />;
      case 'paper':
        return <PaperAssetsPage />;
      case 'jobs':
        return <JobsLogsPage />;
      case 'settings':
        return <SettingsPage />;
      default:
        return null;
    }
  };

  // 1. DEFAULT HOME: EXACT VISIONOS AMBIENT DASHBOARD MATCHING USER IMAGE
  if (currentPage === 'overview') {
    return <AmbientDashboard onNavigate={setCurrentPage} />;
  }

  // 2. SUBPAGE VIEW: FLOATING FROSTED GLASS RESEARCH CONTAINER OVER WARM BACKGROUND
  return (
    <div style={{
      width: '100%',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      padding: '24px 20px',
      position: 'relative'
    }}>
      {/* Top Back Navigation Pill */}
      <div style={{
        maxWidth: '1200px',
        width: '100%',
        margin: '0 auto 12px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '10px'
      }}>
        <button
          onClick={() => setCurrentPage('overview')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 18px',
            borderRadius: '24px',
            background: 'rgba(28, 32, 44, 0.75)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.25)',
            color: '#fff',
            fontSize: '12px',
            fontWeight: 700,
            cursor: 'pointer',
            boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
            transition: 'all 0.15s ease'
          }}
          onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(255, 255, 255, 0.25)')}
          onMouseLeave={(e) => (e.currentTarget.style.background = 'rgba(28, 32, 44, 0.75)')}
        >
          <ArrowLeft size={14} />
          <span>Back to Canopy Control Center</span>
        </button>

        <div style={{
          fontSize: '11px',
          fontWeight: 700,
          color: 'rgba(255, 255, 255, 0.8)',
          background: 'rgba(0, 0, 0, 0.35)',
          padding: '4px 14px',
          borderRadius: '20px',
          border: '1px solid rgba(255, 255, 255, 0.12)'
        }}>
          LitchiHybridNet Research Workspace
        </div>
      </div>

      {/* Main Subpage Content */}
      <div className="subpage-container">
        {renderModulePage()}
      </div>
    </div>
  );
};

export default App;
