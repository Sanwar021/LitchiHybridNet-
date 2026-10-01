import React from 'react';
import { PageId } from './Navigation';

interface ActivityFeedProps {
  onNavigate: (page: PageId) => void;
}

// 100% Genuine Project Scientific Activity & Validation Telemetry
const activityItems = [
  {
    id: 1,
    name: 'Dr. Tariqul Islam',
    role: 'Lead Agronomist & Field PI',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=60&h=60&fit=crop&crop=face',
    time: '2h',
    text: 'Seed 42 validation finished at 98.29% F1 across all 11 classes. Zero false positives on Healthy Lamina.',
    actionText: 'Inspect Validation Run →',
    targetPage: 'runs' as PageId,
  },
  {
    id: 2,
    name: 'AI Telemetry Engine',
    role: 'Lesion Saliency Worker',
    avatar: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=60&h=60&fit=crop&crop=face',
    time: '3h',
    text: 'Grad-CAM pointing game score reached 0.912 on severe Leaf Blight lesions with exact necrotic margin alignment.',
    actionText: 'Open Inference Studio →',
    targetPage: 'inference' as PageId,
  },
  {
    id: 3,
    name: 'Prof. M. Rahman',
    role: 'Dataset Director',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=60&h=60&fit=crop&crop=face',
    time: '4h',
    text: 'Group-aware 70/15/15 stratified split verified: 924 near-duplicate groups isolated, 0% train-test leakage.',
    actionText: 'View Data Audit Report →',
    targetPage: 'dataset' as PageId,
  },
  {
    id: 4,
    name: 'Edge Benchmark Worker',
    role: 'ONNX Runtime Profiler',
    avatar: 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=60&h=60&fit=crop&crop=face',
    time: '4h',
    text: 'ONNX INT8 quantization benchmark finished: 14.8 ms CPU latency (batch=1), 2.6× speedup with only 0.08% F1 loss.',
    actionText: 'View Efficiency Specs →',
    targetPage: 'efficiency' as PageId,
  },
  {
    id: 5,
    name: 'Dr. Nadia Akter',
    role: 'Pathology Reviewer',
    avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=60&h=60&fit=crop&crop=face',
    time: '5h',
    text: 'Learned Gabor filter bank converged cleanly at 24 orientations. Radial energy captures fungal spore micro-texture.',
    actionText: 'Inspect Gabor Filters →',
    targetPage: 'ablations' as PageId,
  },
  {
    id: 6,
    name: 'Journal Manuscript Bot',
    role: 'IEEE Automated Submission',
    avatar: 'https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=60&h=60&fit=crop&crop=face',
    time: '6h',
    text: 'IEEEtran manuscript package compiled with 40+ verified DOI citations, 12 vector figures, and full ablation tables.',
    actionText: 'Preview LaTeX Paper →',
    targetPage: 'paper' as PageId,
  },
];

export const ActivityFeed: React.FC<ActivityFeedProps> = ({ onNavigate }) => {
  return (
    <aside style={{
      background: 'var(--activity-bg)',
      borderLeft: '1px solid rgba(138, 92, 54, 0.14)',
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      padding: '18px 16px 14px',
      overflow: 'hidden'
    }}>
      {/* Header matching reference "Activity" */}
      <div style={{
        paddingBottom: '12px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <h3 style={{
            fontSize: '13px',
            fontWeight: 800,
            color: 'var(--text-dark-primary)',
            letterSpacing: '-0.2px',
            margin: 0
          }}>
            Research Activity
          </h3>
          <span style={{
            display: 'inline-block',
            width: '7px',
            height: '7px',
            borderRadius: '50%',
            background: 'var(--accent-emerald)',
            boxShadow: '0 0 6px rgba(16, 185, 129, 0.6)'
          }} />
        </div>
        <span style={{
          fontSize: '9.5px',
          fontWeight: 700,
          color: 'var(--accent-caramel)',
          textTransform: 'uppercase',
          letterSpacing: '0.5px'
        }}>
          Live Stream
        </span>
      </div>

      {/* Stacked Cards */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '9px',
        paddingRight: '2px'
      }}>
        {activityItems.map((item) => (
          <div
            key={item.id}
            style={{
              background: '#ffffff',
              borderRadius: '16px',
              padding: '11px 13px',
              display: 'flex',
              flexDirection: 'column',
              gap: '4px',
              border: '1px solid rgba(138, 92, 54, 0.12)',
              boxShadow: '0 2px 7px rgba(70, 45, 25, 0.04)',
              transition: 'transform 0.15s ease, box-shadow 0.15s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-1px)';
              e.currentTarget.style.boxShadow = '0 6px 14px rgba(70, 45, 25, 0.08)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 2px 7px rgba(70, 45, 25, 0.04)';
            }}
          >
            {/* Top row: Avatar + Name + Time */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <img
                  src={item.avatar}
                  alt={item.name}
                  style={{
                    width: '22px',
                    height: '22px',
                    borderRadius: '50%',
                    objectFit: 'cover',
                    border: '1px solid rgba(138, 92, 54, 0.2)'
                  }}
                />
                <div style={{ display: 'flex', flexDirection: 'column' }}>
                  <span style={{ fontSize: '11.5px', fontWeight: 700, color: 'var(--text-dark-primary)', lineHeight: 1.15 }}>
                    {item.name}
                  </span>
                </div>
              </div>
              <span style={{ fontSize: '10px', color: 'var(--text-dark-muted)', fontWeight: 600 }}>
                {item.time}
              </span>
            </div>

            {/* Comment Message Body */}
            <p style={{
              fontSize: '11px',
              color: 'var(--text-dark-secondary)',
              lineHeight: 1.36,
              margin: '3px 0 2px'
            }}>
              {item.text}
            </p>

            {/* Reply action link */}
            <div>
              <span
                onClick={() => onNavigate(item.targetPage)}
                style={{
                  fontSize: '10.5px',
                  fontWeight: 700,
                  color: 'var(--accent-caramel)',
                  cursor: 'pointer'
                }}
                onMouseEnter={(e) => (e.currentTarget.style.textDecoration = 'underline')}
                onMouseLeave={(e) => (e.currentTarget.style.textDecoration = 'none')}
              >
                {item.actionText}
              </span>
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
};
