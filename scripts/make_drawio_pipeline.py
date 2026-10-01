#!/usr/bin/env python3
"""
Generate publication-quality Draw.io-style pipeline workflow diagram
and export both:
1. paper/figures/pipeline_workflow.drawio (editable draw.io XML file)
2. paper/figures/pipeline_workflow.png (300 DPI publication figure)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path

def create_drawio_xml(save_path: Path):
    """Generate a clean, fully-editable draw.io / diagrams.net XML file."""
    xml_content = """<mxfile host="app.diagrams.net" modified="2026-10-01T16:00:00.000Z" agent="Antigravity Scientific Editor" version="21.0.0" type="device">
  <diagram id="LitchiHybridNet-Pipeline" name="Operational Pipeline">
    <mxGraphModel dx="1400" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="600" background="#FFFFFF">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- STAGE 1: Data Audit & Deduplication -->
        <mxCell id="stage1_bg" value="" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#F0FDF4;strokeColor=#16A34A;strokeWidth=2;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="80" width="310" height="380" as="geometry"/>
        </mxCell>
        <mxCell id="stage1_header" value="PHASE 1: DATA AUDIT &amp; SPLITTING" style="rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#16A34A;strokeColor=none;fontColor=#FFFFFF;fontStyle=1;fontSize=12;align=center;" vertex="1" parent="1">
          <mxGeometry x="55" y="95" width="280" height="32" as="geometry"/>
        </mxCell>
        <mxCell id="stage1_c1" value="BDLitchi Corpus (11,094 Field Images)&#xa;• 11 Foliar Pathologies &amp; Health Lamina&#xa;• Dinajpur &amp; Ishwardi Orchards&#xa;• Natural Canopy &amp; Solar Clutter" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFFFF;strokeColor=#BBF7D0;strokeWidth=1.5;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="55" y="140" width="280" height="75" as="geometry"/>
        </mxCell>
        <mxCell id="stage1_c2" value="Perceptual Difference Hash (dHash)&#xa;• 64-bit Grayscale Gradient Hash&#xa;• Hamming Distance Metric (τ ≤ 8)&#xa;• 924 Near-Duplicate Clusters (3,950 Img)" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFFFF;strokeColor=#BBF7D0;strokeWidth=1.5;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="55" y="230" width="280" height="75" as="geometry"/>
        </mxCell>
        <mxCell id="stage1_c3" value="Group-Aware Stratified Partition&#xa;• Training Set: 7,761 (70%)&#xa;• Validation Set: 1,665 (15%)&#xa;• Test Split: 1,665 (15%) [Leakage-Free]" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#DCFCE7;strokeColor=#16A34A;strokeWidth=1.5;fontStyle=1;fontSize=10;align=center;" vertex="1" parent="1">
          <mxGeometry x="55" y="320" width="280" height="75" as="geometry"/>
        </mxCell>

        <!-- ARROW 1 -> 2 -->
        <mxCell id="arrow1" value="Normalized RGB&#xa;224×224×3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=2.5;fontSize=9;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="stage1_bg" target="stage2_bg">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- STAGE 2: Dual-Branch Feature Extraction -->
        <mxCell id="stage2_bg" value="" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#EFF6FF;strokeColor=#2563EB;strokeWidth=2;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="420" y="80" width="330" height="380" as="geometry"/>
        </mxCell>
        <mxCell id="stage2_header" value="PHASE 2: DUAL-BRANCH NET" style="rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#2563EB;strokeColor=none;fontColor=#FFFFFF;fontStyle=1;fontSize=12;align=center;" vertex="1" parent="1">
          <mxGeometry x="435" y="95" width="300" height="32" as="geometry"/>
        </mxCell>
        <mxCell id="stage2_c1" value="Branch A: Learnable Gabor Filter Bank&#xa;• K = 24 Kernels (7×7 spatial support)&#xa;• 8 Orientations θk ∈ {0, π/8, ..., 7π/8}&#xa;• 3 Radial Frequencies Fk ∈ {0.05, 0.15, 0.25}&#xa;• Analytic Chain-Rule Backpropagation&#xa;→ Output: F_gabor ∈ R^(64×112×112)" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFFFF;strokeColor=#BFDBFE;strokeWidth=1.5;fontSize=9.5;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="435" y="140" width="300" height="110" as="geometry"/>
        </mxCell>
        <mxCell id="stage2_c2" value="Branch B: MobileNetV3-Large Backbone&#xa;• ImageNet-1k Pre-trained Weights&#xa;• Depthwise Separable Inverted Residuals&#xa;• Hard-Swish Non-linearities &amp; SE Blocks&#xa;• High-level Semantic Feature Tapping&#xa;→ Output: F_cnn ∈ R^(960×7×7)" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFFFF;strokeColor=#BFDBFE;strokeWidth=1.5;fontSize=9.5;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="435" y="270" width="300" height="110" as="geometry"/>
        </mxCell>

        <!-- ARROW 2 -> 3 -->
        <mxCell id="arrow2" value="Dual Tensors&#xa;F_gabor &amp; F_cnn" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=2.5;fontSize=9;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="stage2_bg" target="stage3_bg">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- STAGE 3: GAFM Cross-Attention Fusion -->
        <mxCell id="stage3_bg" value="" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFBEB;strokeColor=#D97706;strokeWidth=2;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="820" y="80" width="330" height="380" as="geometry"/>
        </mxCell>
        <mxCell id="stage3_header" value="PHASE 3: GAFM CROSS-GATING" style="rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#D97706;strokeColor=none;fontColor=#FFFFFF;fontStyle=1;fontSize=12;align=center;" vertex="1" parent="1">
          <mxGeometry x="835" y="95" width="300" height="32" as="geometry"/>
        </mxCell>
        <mxCell id="stage3_c1" value="Spatial Alignment &amp; Pooling&#xa;• Anti-aliased SepConv Downsampling&#xa;• Global Average Pooling (GAP) Descriptors:&#xa;  z_cnn ∈ R^960  ||  z_gabor ∈ R^64&#xa;• Joint Descriptor: z_joint ∈ R^1024" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFFFF;strokeColor=#FDE68A;strokeWidth=1.5;fontSize=9.5;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="835" y="140" width="300" height="90" as="geometry"/>
        </mxCell>
        <mxCell id="stage3_c2" value="Squeeze-and-Excitation Cross-Gating&#xa;• Bottleneck MLP: 1024 → 64 → 1024&#xa;• Modulation Gate: s = σ(W2·ReLU(W1·z))&#xa;• Calibrated Fusion: F_fused = s ⊙ z + z" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFFFF;strokeColor=#FDE68A;strokeWidth=1.5;fontSize=9.5;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="835" y="245" width="300" height="75" as="geometry"/>
        </mxCell>
        <mxCell id="stage3_c3" value="Linear Classification Head (11 Classes)&#xa;• Top-1 Accuracy: 99.04% ± 0.12%&#xa;• Macro-F1: 0.9904 | Healthy F1: 0.9980&#xa;• Loss: 0.0787 (Label Smoothing ε = 0.1)" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FEF3C7;strokeColor=#D97706;strokeWidth=1.5;fontStyle=1;fontSize=9.5;align=center;" vertex="1" parent="1">
          <mxGeometry x="835" y="335" width="300" height="75" as="geometry"/>
        </mxCell>

        <!-- ARROW 3 -> 4 -->
        <mxCell id="arrow3" value="Calibrated Model&#xa;21.25 MB" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=2.5;fontSize=9;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="stage3_bg" target="stage4_bg">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- STAGE 4: INT8 Edge Quantization & Deployment -->
        <mxCell id="stage4_bg" value="" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FEF2F2;strokeColor=#DC2626;strokeWidth=2;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="1220" y="80" width="310" height="380" as="geometry"/>
        </mxCell>
        <mxCell id="stage4_header" value="PHASE 4: EDGE QUANTIZATION" style="rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#DC2626;strokeColor=none;fontColor=#FFFFFF;fontStyle=1;fontSize=12;align=center;" vertex="1" parent="1">
          <mxGeometry x="1235" y="95" width="280" height="32" as="geometry"/>
        </mxCell>
        <mxCell id="stage4_c1" value="ONNX Dynamic INT8 Quantization&#xa;• 74.5% Model Size Reduction&#xa;• FP32 (21.25 MB) → INT8 (5.40 MB)&#xa;• Retention: 98.96% Acc (-0.08% loss)" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFFFF;strokeColor=#FECACA;strokeWidth=1.5;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="1235" y="140" width="280" height="75" as="geometry"/>
        </mxCell>
        <mxCell id="stage4_c2" value="Multi-Hardware Benchmarking&#xa;• Intel i7-12700K: 14.8 ms (2.6× speedup)&#xa;• NVIDIA Jetson Nano: 8.6 ms (TensorRT)&#xa;• Motion Blur Sev. 5: 85.4% (+12.6% over CNN)" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFFFF;strokeColor=#FECACA;strokeWidth=1.5;fontSize=9.5;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="1235" y="230" width="280" height="75" as="geometry"/>
        </mxCell>
        <mxCell id="stage4_c3" value="Raspberry Pi 4 Model B Deployment&#xa;• ARM Cortex-A72 @ 1.5 GHz&#xa;• Real-Time Latency: 34.2 ms (~29.2 FPS)&#xa;→ Handheld Scouting &amp; Robotic Sprayers" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FEE2E2;strokeColor=#DC2626;strokeWidth=1.5;fontStyle=1;fontSize=10;align=center;" vertex="1" parent="1">
          <mxGeometry x="1235" y="320" width="280" height="75" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(xml_content.strip())
    print(f"Generated Draw.io XML at: {save_path}")

def render_drawio_style_png(save_path: Path):
    """Render a publication-grade, professional Draw.io styled diagram at 300 DPI."""
    fig = plt.figure(figsize=(14.2, 5.2), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1420)
    ax.set_ylim(0, 520)
    ax.axis('off')

    # Card definitions: (x, y, w, h, border_color, bg_color, header_color, title, badge_text, items)
    cards = [
        {
            'x': 30, 'y': 35, 'w': 310, 'h': 450,
            'border': '#16a34a', 'bg': '#f0fdf4', 'header': '#15803d', 'num': '1',
            'title': 'DATA AUDIT & SPLITTING',
            'badge': 'Leakage Elimination',
            'sections': [
                ('BDLitchi Corpus (11,094 Images)', [
                    '• 11 Foliar Pathologies & Healthy Leaf',
                    '• Captured in Dinajpur & Ishwardi Orchards',
                    '• Severe natural canopy & illumination clutter'
                ], '#ffffff', '#bbf7d0'),
                ('Difference Hash (dHash) Deduplication', [
                    '• 64-bit gradient hash matrix per frame',
                    '• Pairwise Hamming threshold (τ ≤ 8)',
                    '• 924 near-duplicate clusters (3,950 images)'
                ], '#ffffff', '#bbf7d0'),
                ('Group-Aware Stratified Partitioning', [
                    '• Training: 7,761 (70%) | Val: 1,665 (15%)',
                    '• Held-Out Test Set: 1,665 (15%)',
                    '• Zero cluster leakage across partitions'
                ], '#dcfce7', '#16a34a')
            ]
        },
        {
            'x': 380, 'y': 35, 'w': 325, 'h': 450,
            'border': '#2563eb', 'bg': '#eff6ff', 'header': '#1d4ed8', 'num': '2',
            'title': 'DUAL-BRANCH FEATURE NET',
            'badge': 'Spatial-Frequency Fusion',
            'sections': [
                ('Branch A: Learnable Gabor Filter Bank', [
                    '• K = 24 kernels (7×7 spatial support)',
                    '• 8 Orientations θk ∈ {0, π/8, ..., 7π/8}',
                    '• 3 Frequencies Fk ∈ {0.05, 0.15, 0.25}',
                    '• Analytic chain-rule gradient backprop',
                    '→ F_gabor ∈ R^(64 × 112 × 112)'
                ], '#ffffff', '#bfdbfe'),
                ('Branch B: MobileNetV3-Large Backbone', [
                    '• ImageNet-1k pre-trained feature weights',
                    '• Depthwise separable inverted residuals',
                    '• Hard-Swish non-linearities & SE blocks',
                    '• Deep invariant semantic feature tapping',
                    '→ F_cnn ∈ R^(960 × 7 × 7)'
                ], '#ffffff', '#bfdbfe')
            ]
        },
        {
            'x': 745, 'y': 35, 'w': 325, 'h': 450,
            'border': '#d97706', 'bg': '#fffbeb', 'header': '#b45309', 'num': '3',
            'title': 'GAFM ATTENTION FUSION',
            'badge': 'Channel Cross-Gating',
            'sections': [
                ('Spatial Alignment & Pooling', [
                    '• Anti-aliased SepConv downsampling to 7×7',
                    '• Global Average Pooling (GAP) descriptors:',
                    '  z_cnn ∈ R^960   ||   z_gabor ∈ R^64',
                    '• Joint descriptor: z_joint ∈ R^1024'
                ], '#ffffff', '#fde68a'),
                ('Squeeze-and-Excitation Cross-Gating', [
                    '• Bottleneck MLP: 1024 → 64 → 1024',
                    '• Modulation: s = σ(W2 · ReLU(W1 · z_joint))',
                    '• Calibrated fusion: F_fused = s ⊙ z + z'
                ], '#ffffff', '#fde68a'),
                ('Classification Head (11 Foliar Classes)', [
                    '• Top-1 Accuracy: 99.04% ± 0.12%',
                    '• Macro-F1: 0.9904 | Healthy F1: 0.9980',
                    '• Test Loss: 0.0787 (Label Smoothing ε = 0.1)'
                ], '#fef3c7', '#d97706')
            ]
        },
        {
            'x': 1110, 'y': 35, 'w': 285, 'h': 450,
            'border': '#dc2626', 'bg': '#fef2f2', 'header': '#b91c1c', 'num': '4',
            'title': 'EDGE QUANTIZATION',
            'badge': 'Real-Time Edge AI',
            'sections': [
                ('ONNX Dynamic INT8 Quantization', [
                    '• 74.5% Model storage reduction',
                    '• FP32 (21.25 MB) → INT8 (5.40 MB)',
                    '• Test accuracy retained: 98.96%'
                ], '#ffffff', '#fecaca'),
                ('Multi-Hardware Profiling', [
                    '• x86 CPU: 14.8 ms (2.6× speedup)',
                    '• NVIDIA Jetson Nano: 8.6 ms',
                    '• Motion blur retention: 85.4% (+12.6%)'
                ], '#ffffff', '#fecaca'),
                ('Raspberry Pi 4 Edge Deployment', [
                    '• Quad-core ARM Cortex-A72 @ 1.5 GHz',
                    '• Real-Time Latency: 34.2 ms (~29 FPS)',
                    '→ Handheld scouts & autonomous rovers'
                ], '#fee2e2', '#dc2626')
            ]
        }
    ]

    # Draw Cards
    for card in cards:
        x, y, w, h = card['x'], card['y'], card['w'], card['h']
        
        # Shadow
        shadow = patches.FancyBboxPatch((x+4, y-4), w, h, boxstyle="round,pad=3,rounding_size=12",
                                        facecolor='#cbd5e1', edgecolor='none', alpha=0.35, zorder=1)
        ax.add_patch(shadow)

        # Main Card Body
        body = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=3,rounding_size=12",
                                      facecolor=card['bg'], edgecolor=card['border'], linewidth=2.0, zorder=2)
        ax.add_patch(body)

        # Header Banner
        header = patches.FancyBboxPatch((x+8, y+h-44), w-16, 36, boxstyle="round,pad=2,rounding_size=8",
                                        facecolor=card['header'], edgecolor='none', zorder=3)
        ax.add_patch(header)

        # Phase Number Badge
        num_circle = patches.Circle((x+28, y+h-26), 13, facecolor='#ffffff', edgecolor=card['header'], linewidth=1.5, zorder=4)
        ax.add_patch(num_circle)
        ax.text(x+28, y+h-26, card['num'], ha='center', va='center', fontsize=11, fontweight='bold', color=card['header'], zorder=5)

        # Title
        ax.text(x+48, y+h-26, card['title'], ha='left', va='center', fontsize=9.5, fontweight='bold', color='#ffffff', zorder=5)

        # Sections inside card
        curr_y = y + h - 56
        for sec_title, bullets, sec_bg, sec_border in card['sections']:
            sec_h = 24 + len(bullets) * 15
            sec_y = curr_y - sec_h

            sec_box = patches.FancyBboxPatch((x+10, sec_y), w-20, sec_h, boxstyle="round,pad=2,rounding_size=6",
                                            facecolor=sec_bg, edgecolor=sec_border, linewidth=1.2, zorder=3)
            ax.add_patch(sec_box)

            # Section Title
            ax.text(x+18, sec_y + sec_h - 12, sec_title, ha='left', va='center', fontsize=8.6, fontweight='bold', color='#1e293b', zorder=4)

            # Bullets
            for b_idx, bullet in enumerate(bullets):
                b_y = sec_y + sec_h - 26 - (b_idx * 14.5)
                font_weight = 'bold' if ('→' in bullet or '99.04%' in bullet or '34.2 ms' in bullet or '74.5%' in bullet) else 'normal'
                text_color = '#047857' if '→' in bullet else '#334155'
                ax.text(x+18, b_y, bullet, ha='left', va='center', fontsize=7.6, fontweight=font_weight, color=text_color, zorder=4)

            curr_y = sec_y - 8

    # Connectors / Inter-Phase Data Flow Arrows
    connectors = [
        (340, 260, 380, 260, 'Normalized RGB\n224×224×3'),
        (705, 260, 745, 260, 'Dual Tensors\nFgabor & Fcnn'),
        (1070, 260, 1110, 260, 'FP32 Model\n21.25 MB')
    ]

    for x1, y1, x2, y2, label in connectors:
        arrow = patches.FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=18,
                                        linewidth=3.0, edgecolor='#334155', facecolor='#334155', zorder=6)
        ax.add_patch(arrow)
        ax.text((x1+x2)/2, y1+24, label, ha='center', va='center', fontsize=7.2, fontweight='bold', color='#0f172a',
                bbox=dict(boxstyle='round,pad=0.25', fc='#ffffff', ec='#94a3b8', lw=1.0), zorder=7)

    # Top Super Title Banner
    ax.text(710, 502, "LitchiHybridNet: End-to-End Operational Pipeline & Deployment Workflow",
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#0f172a')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0.04)
    plt.close()
    print(f"Generated 300 DPI Draw.io style publication figure at: {save_path}")

if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent
    xml_path = root / 'paper' / 'figures' / 'pipeline_workflow.drawio'
    png_path = root / 'paper' / 'figures' / 'pipeline_workflow.png'
    create_drawio_xml(xml_path)
    render_drawio_style_png(png_path)
