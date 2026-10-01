import React, { useState } from 'react';
import { PageId } from '../components/Navigation';
import {
  Plus,
  Upload,
  BookOpen,
  Clock,
  Target,
  Zap,
  MapPin,
  CheckCircle,
  Atom,
  Hourglass,
  Shield,
  Globe,
} from 'lucide-react';

interface BentoDashboardProps {
  onNavigate: (page: PageId) => void;
}

export const BentoDashboard: React.FC<BentoDashboardProps> = ({ onNavigate }) => {
  const [leaderboardTab, setLeaderboardTab] = useState<'all' | 'baselines' | 'ablations'>('all');

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '14px',
      height: '100%',
      overflowY: 'auto',
      paddingRight: '2px'
    }}>
      {/* ======================================================== */}
      {/* 1. HERO SHOWCASE CARD (LitchiHybridNet & Texture Fusion) */}
      {/* ======================================================== */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '20px',
        padding: '4px 2px 8px',
        position: 'relative'
      }}>
        {/* Cover illustration on the left (warm walnut leather look) */}
        <div
          onClick={() => onNavigate('inference')}
          style={{
            width: '108px',
            height: '142px',
            borderRadius: '12px',
            overflow: 'hidden',
            boxShadow: '0 14px 30px -4px rgba(60, 35, 15, 0.35)',
            flexShrink: 0,
            background: 'linear-gradient(145deg, #442a1b 0%, #2f1c11 60%, #1c0f08 100%)',
            border: '1.5px solid rgba(212, 163, 115, 0.35)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '10px 8px',
            position: 'relative',
            cursor: 'pointer',
            transition: 'transform 0.18s ease'
          }}
          onMouseEnter={(e) => (e.currentTarget.style.transform = 'translateY(-2px) scale(1.02)')}
          onMouseLeave={(e) => (e.currentTarget.style.transform = 'translateY(0) scale(1)')}
        >
          <div style={{
            fontSize: '8px',
            fontWeight: 800,
            color: 'rgba(255, 255, 255, 0.88)',
            letterSpacing: '1px',
            textTransform: 'uppercase'
          }}>
            BDLitchi Dataset
          </div>
          <div style={{ fontSize: '34px', filter: 'drop-shadow(0 4px 10px rgba(0,0,0,0.6))' }}>
            🌿
          </div>
          <div style={{
            fontSize: '8.5px',
            fontWeight: 800,
            color: '#fffdf9',
            textAlign: 'center',
            lineHeight: 1.2
          }}>
            LitchiHybridNet
            <div style={{ fontSize: '7px', color: 'var(--bento-yellow)', opacity: 0.95, fontWeight: 700 }}>
              Texture Fusion
            </div>
          </div>
        </div>

        {/* Title, action icons, author, links */}
        <div style={{ flex: 1 }}>
          {/* Action icon pills */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <button
              onClick={() => onNavigate('inference')}
              title="Run Leaf Diagnosis Studio"
              style={{
                width: '26px',
                height: '26px',
                borderRadius: '50%',
                background: '#ffffff',
                border: '1.5px solid rgba(138, 92, 54, 0.22)',
                color: 'var(--text-dark-primary)',
                boxShadow: '0 2px 6px rgba(70, 45, 25, 0.08)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'var(--card-dark)';
                e.currentTarget.style.color = '#fff';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = '#ffffff';
                e.currentTarget.style.color = 'var(--text-dark-primary)';
              }}
            >
              <Plus size={13} />
            </button>

            <button
              onClick={() => onNavigate('results')}
              title="Export Benchmark Report"
              style={{
                width: '26px',
                height: '26px',
                borderRadius: '50%',
                background: '#ffffff',
                border: '1.5px solid rgba(138, 92, 54, 0.22)',
                color: 'var(--text-dark-primary)',
                boxShadow: '0 2px 6px rgba(70, 45, 25, 0.08)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'var(--card-dark)';
                e.currentTarget.style.color = '#fff';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = '#ffffff';
                e.currentTarget.style.color = 'var(--text-dark-primary)';
              }}
            >
              <Upload size={12} />
            </button>
          </div>

          {/* Large Title with Editorial Serif Italic */}
          <h1 style={{
            fontSize: '22px',
            fontWeight: 800,
            color: 'var(--text-dark-primary)',
            margin: '0 0 4px',
            lineHeight: 1.25,
            letterSpacing: '-0.3px'
          }}>
            <span style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>LitchiHybridNet</span>{' '}
            <span className="font-editorial" style={{ color: 'var(--accent-cinnamon)', fontSize: '23px' }}>
              and Learnable Gabor Texture Fusion
            </span>
          </h1>

          <div style={{ fontSize: '11px', color: 'var(--text-dark-secondary)', margin: '2px 0 3px', fontWeight: 500 }}>
            Dual-Branch Field Disease Detection &bull; <span style={{ color: 'var(--text-dark-primary)', fontWeight: 700 }}>11,094 Field Images</span> &bull; 11 Disease Classes
          </div>

          <div>
            <span
              onClick={() => onNavigate('dataset')}
              style={{
                fontSize: '11px',
                color: 'var(--accent-caramel)',
                cursor: 'pointer',
                textDecoration: 'none',
                fontWeight: 700
              }}
              onMouseEnter={(e) => (e.currentTarget.style.textDecoration = 'underline')}
              onMouseLeave={(e) => (e.currentTarget.style.textDecoration = 'none')}
            >
              BDLitchi Dataset Specifications & Splits &rarr;
            </span>
          </div>
        </div>
      </div>

      {/* ======================================================== */}
      {/* 2. THE 5 BENTO CARDS (Exact match to reference image)    */}
      {/* ======================================================== */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '12px' }}>
        
        {/* ---------------------------------------------------- */}
        {/* CARD 1: BUTTER YELLOW (TOP-1 ACCURACY) - 7 cols      */}
        {/* ---------------------------------------------------- */}
        <div
          className="bento-box"
          onClick={() => onNavigate('results')}
          style={{
            gridColumn: 'span 7',
            background: 'var(--bento-yellow)',
            color: 'var(--bento-dark-text)',
            borderRadius: '18px',
            padding: '16px 18px 14px',
            cursor: 'pointer',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            minHeight: '128px',
            boxShadow: '0 6px 20px -4px rgba(248, 211, 86, 0.4)'
          }}
        >
          {/* Header row: Label + share pill */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '9.5px', fontWeight: 800, letterSpacing: '0.6px', textTransform: 'uppercase', opacity: 0.9 }}>
              TOP-1 ACCURACY
            </span>
            <div style={{
              width: '20px',
              height: '20px',
              borderRadius: '50%',
              background: 'rgba(0, 0, 0, 0.09)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Upload size={10} color="#241a12" />
            </div>
          </div>

          {/* Metric row: book/leaf icon + 99.04% + Out of 11,094 images */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', margin: '2px 0' }}>
            <BookOpen size={20} color="#241a12" />
            <span style={{ fontSize: '30px', fontWeight: 800, letterSpacing: '-1px', lineHeight: 1 }}>
              99.04%
            </span>
            <div style={{ display: 'flex', flexDirection: 'column', fontSize: '10px', fontWeight: 600, opacity: 0.9, lineHeight: 1.25, marginLeft: '2px' }}>
              <span>Out of 11,094 images</span>
              <span style={{ fontWeight: 800 }}>#1 among 9 evaluated baselines</span>
            </div>
          </div>

          {/* Progress bar + multi-seed dots */}
          <div>
            <div style={{
              width: '100%',
              height: '3.5px',
              background: 'rgba(0, 0, 0, 0.14)',
              borderRadius: '2px',
              overflow: 'hidden',
              marginBottom: '7px'
            }}>
              <div style={{ width: '99.04%', height: '100%', background: '#241a12', borderRadius: '2px' }} />
            </div>

            {/* Seed dots representing 5 random seeds */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              {[
                { seed: '42', color: '#10b981' },
                { seed: '123', color: '#3b82f6' },
                { seed: '456', color: '#8b5cf6' },
                { seed: '789', color: '#ec4899' },
                { seed: '1024', color: '#f59e0b' },
              ].map((s, idx) => (
                <div
                  key={idx}
                  style={{
                    fontSize: '9px',
                    fontWeight: 800,
                    background: '#241a12',
                    color: 'var(--bento-yellow)',
                    padding: '1px 5px',
                    borderRadius: '4px'
                  }}
                >
                  S{s.seed}
                </div>
              ))}
              <span style={{ fontSize: '9.5px', fontWeight: 700, marginLeft: 'auto', opacity: 0.88 }}>
                Mean ±0.12%
              </span>
            </div>
          </div>
        </div>

        {/* ---------------------------------------------------- */}
        {/* CARD 2: CORAL TERRACOTTA (CPU LATENCY) - 5 cols      */}
        {/* ---------------------------------------------------- */}
        <div
          className="bento-box"
          onClick={() => onNavigate('efficiency')}
          style={{
            gridColumn: 'span 5',
            background: 'var(--bento-orange)',
            color: 'var(--bento-dark-text)',
            borderRadius: '18px',
            padding: '16px 18px 14px',
            cursor: 'pointer',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            minHeight: '128px',
            boxShadow: '0 6px 20px -4px rgba(248, 151, 88, 0.4)'
          }}
        >
          {/* Header row: TIME + share pill */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '9.5px', fontWeight: 800, letterSpacing: '0.6px', textTransform: 'uppercase', opacity: 0.9 }}>
              CPU INFERENCE
            </span>
            <div style={{
              width: '20px',
              height: '20px',
              borderRadius: '50%',
              background: 'rgba(0, 0, 0, 0.09)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Upload size={10} color="#241a12" />
            </div>
          </div>

          {/* Metric row: Clock icon + 14.8 ms */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '7px', margin: '2px 0' }}>
            <Clock size={20} color="#241a12" />
            <span style={{ fontSize: '30px', fontWeight: 800, letterSpacing: '-1px', lineHeight: 1 }}>
              14.8 ms
            </span>
          </div>

          {/* Subtext */}
          <div style={{ fontSize: '10px', fontWeight: 600, opacity: 0.9, lineHeight: 1.3 }}>
            <div>ONNX INT8 Quantized (Batch=1)</div>
            <div style={{ fontWeight: 800 }}>2.6× faster than FP32</div>
          </div>
        </div>

        {/* ---------------------------------------------------- */}
        {/* CARD 3: DUSTY LILAC (MACRO F1-SCORE) - 4 cols        */}
        {/* ---------------------------------------------------- */}
        <div
          className="bento-box"
          onClick={() => onNavigate('results')}
          style={{
            gridColumn: 'span 4',
            background: 'var(--bento-purple)',
            color: 'var(--bento-dark-text)',
            borderRadius: '18px',
            padding: '14px 16px 12px',
            cursor: 'pointer',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            minHeight: '118px',
            boxShadow: '0 6px 20px -4px rgba(203, 176, 242, 0.4)'
          }}
        >
          {/* Header row: LEVEL + share pill */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '9.5px', fontWeight: 800, letterSpacing: '0.6px', textTransform: 'uppercase', opacity: 0.9 }}>
              MACRO F1
            </span>
            <div style={{
              width: '18px',
              height: '18px',
              borderRadius: '50%',
              background: 'rgba(0, 0, 0, 0.09)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Upload size={9} color="#241a12" />
            </div>
          </div>

          {/* Target icon + 0.9904 */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', margin: '1px 0' }}>
            <Target size={18} color="#241a12" />
            <span style={{ fontSize: '26px', fontWeight: 800, letterSpacing: '-0.8px', lineHeight: 1 }}>
              0.9904
            </span>
          </div>

          <div style={{ fontSize: '9.5px', fontWeight: 600, opacity: 0.9, lineHeight: 1.25 }}>
            <div>Balanced across 11 disease classes</div>
            <div style={{ fontWeight: 800, marginTop: '2px' }}>Top 1% Class Discrimination</div>
          </div>
        </div>

        {/* ---------------------------------------------------- */}
        {/* CARD 4: PISTACHIO LIME (ROBUSTNESS) - 4 cols         */}
        {/* ---------------------------------------------------- */}
        <div
          className="bento-box"
          onClick={() => onNavigate('robustness')}
          style={{
            gridColumn: 'span 4',
            background: 'var(--bento-lime)',
            color: 'var(--bento-dark-text)',
            borderRadius: '18px',
            padding: '14px 16px 12px',
            cursor: 'pointer',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            minHeight: '118px',
            boxShadow: '0 6px 20px -4px rgba(169, 232, 88, 0.4)'
          }}
        >
          {/* Header row: STREAK + share pill */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '9.5px', fontWeight: 800, letterSpacing: '0.6px', textTransform: 'uppercase', opacity: 0.9 }}>
              ROBUSTNESS
            </span>
            <div style={{
              width: '18px',
              height: '18px',
              borderRadius: '50%',
              background: 'rgba(0, 0, 0, 0.09)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Upload size={9} color="#241a12" />
            </div>
          </div>

          {/* Lightning bolt + +12.6% */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px', margin: '1px 0' }}>
            <Zap size={18} color="#241a12" fill="#241a12" />
            <span style={{ fontSize: '26px', fontWeight: 800, letterSpacing: '-0.8px', lineHeight: 1 }}>
              +12.6%
            </span>
          </div>

          <div style={{ fontSize: '9.5px', fontWeight: 600, opacity: 0.9, lineHeight: 1.25 }}>
            <div>Accuracy retention gain at Sev 5 blur</div>
            <div style={{ fontWeight: 800, marginTop: '2px' }}>Clutter-Resilient Gabor</div>
          </div>
        </div>

        {/* ---------------------------------------------------- */}
        {/* CARD 5: SKY CYAN (EDGE SPECS) - 4 cols               */}
        {/* ---------------------------------------------------- */}
        <div
          className="bento-box"
          onClick={() => onNavigate('efficiency')}
          style={{
            gridColumn: 'span 4',
            background: 'var(--bento-cyan)',
            color: 'var(--bento-dark-text)',
            borderRadius: '18px',
            padding: '14px 16px 12px',
            cursor: 'pointer',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            minHeight: '118px',
            boxShadow: '0 6px 20px -4px rgba(138, 216, 238, 0.4)'
          }}
        >
          {/* Header row: BADGES + share pill */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '9.5px', fontWeight: 800, letterSpacing: '0.6px', textTransform: 'uppercase', opacity: 0.9 }}>
              EDGE SPECS
            </span>
            <div style={{
              width: '18px',
              height: '18px',
              borderRadius: '50%',
              background: 'rgba(0, 0, 0, 0.09)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Upload size={9} color="#241a12" />
            </div>
          </div>

          {/* 2x3 Grid of Line Icons matching reference image */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '8px',
            padding: '3px 2px'
          }}>
            <span title="MobileNetV3 Backbone"><MapPin size={16} color="#241a12" /></span>
            <span title="INT8 Post-Training Quantized"><CheckCircle size={16} color="#241a12" /></span>
            <span title="Learnable Gabor Filters"><Atom size={16} color="#241a12" /></span>
            <span title="14.8 ms CPU Latency"><Hourglass size={16} color="#241a12" /></span>
            <span title="BDLitchi Dataset"><BookOpen size={16} color="#241a12" /></span>
            <span title="Zero Duplicate Leakage"><Shield size={16} color="#241a12" /></span>
          </div>

          <div style={{ fontSize: '9.5px', fontWeight: 700, opacity: 0.9 }}>
            5.40 MB &bull; 120 Trainable Params
          </div>
        </div>

      </div>

      {/* ======================================================== */}
      {/* 3. LEADERBOARD CARD (Bottom Dark Card)                   */}
      {/* ======================================================== */}
      <div>
        <h3 style={{
          fontSize: '13px',
          fontWeight: 800,
          color: 'var(--text-dark-primary)',
          margin: '2px 0 8px 2px',
          letterSpacing: '-0.2px'
        }}>
          Benchmark Leaderboard
        </h3>

        <div style={{
          background: 'var(--card-dark)',
          border: '1px solid var(--card-dark-border)',
          borderRadius: '18px',
          padding: '14px 18px 16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px',
          boxShadow: '0 8px 25px -4px rgba(45, 25, 12, 0.25)'
        }}>
          {/* Centered filter tabs + share icon */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            <div style={{
              display: 'flex',
              background: 'rgba(18, 11, 7, 0.75)',
              padding: '2.5px',
              borderRadius: '16px',
              border: '1px solid rgba(212, 163, 115, 0.15)'
            }}>
              {(['all', 'baselines', 'ablations'] as const).map((tab) => {
                const isActive = leaderboardTab === tab;
                return (
                  <button
                    key={tab}
                    onClick={() => setLeaderboardTab(tab)}
                    style={{
                      background: isActive ? 'rgba(212, 163, 115, 0.28)' : 'transparent',
                      color: isActive ? '#ffffff' : 'var(--text-light-muted)',
                      border: 'none',
                      padding: '3px 12px',
                      borderRadius: '14px',
                      fontSize: '10.5px',
                      fontWeight: 600,
                      cursor: 'pointer',
                      textTransform: 'capitalize',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    {tab === 'all' ? 'All Models' : tab === 'baselines' ? 'Baselines' : 'Ablations'}
                  </button>
                );
              })}
            </div>

            {/* Right upload icon */}
            <div
              onClick={() => onNavigate('results')}
              title="Copy LaTeX Table"
              style={{
                position: 'absolute',
                right: 0,
                width: '22px',
                height: '22px',
                borderRadius: '50%',
                background: 'rgba(212, 163, 115, 0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer'
              }}
            >
              <Upload size={10} color="#f4ece1" />
            </div>
          </div>

          {/* Main User Rank Row (Rank #1 LitchiHybridNet) */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 4px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #f8d356 0%, #c88a4b 100%)',
                color: '#241a12',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '16px',
                fontWeight: 800,
                boxShadow: '0 2px 8px rgba(248, 211, 86, 0.35)'
              }}>
                👑
              </div>
              <div>
                <div style={{ fontSize: '13.5px', fontWeight: 800, color: '#ffffff' }}>
                  Rank #1 &bull; LitchiHybridNet
                </div>
                <div style={{ fontSize: '10.5px', color: 'var(--accent-gold)', fontWeight: 600 }}>
                  Score: 99.04% Accuracy &bull; 0.9904 Macro-F1 &bull; 14.8 ms CPU Latency
                </div>
              </div>
            </div>

            <div style={{ textAlign: 'right' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '5px', justifyContent: 'flex-end' }}>
                <Globe size={14} color="var(--accent-gold)" />
                <span style={{ fontSize: '13px', fontWeight: 800, color: '#ffffff' }}>
                  Top 1%
                </span>
              </div>
              <div style={{ fontSize: '10px', color: 'var(--text-light-muted)', marginTop: '1px' }}>
                Out of 9 Evaluated Architectures
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
