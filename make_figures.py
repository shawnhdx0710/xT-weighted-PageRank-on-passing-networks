"""Regenerate the paper's figures from the repo's data.

Run from the repo root:
    python make_figures.py

Writes the four figures (fig_xt2d, fig_xt3d, fig_workflow, fig_scatter) into `figures/`.
Requires matplotlib, plotly and kaleido (see requirements.txt).
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import plotly.graph_objects as go

ROOT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(ROOT, 'figures')
os.makedirs(FIG, exist_ok=True)
os.chdir(ROOT)

# Custom WWC-trained xT grid (12 rows x 16 cols), committed without a header row.
grid = np.loadtxt("Evaluation/wwc2023_trained_xT_grid.csv", delimiter=",")
assert grid.shape == (12, 16), grid.shape
print('grid shape:', grid.shape, 'min %.4f max %.4f' % (grid.min(), grid.max()))

# ---- Figure 1: 2D xT heatmap (log-normalised so low values are visible) ----
fig, ax = plt.subplots(figsize=(8.2, 4.4), dpi=200)
im = ax.imshow(grid, aspect='auto', origin='lower', cmap='hot',
               norm=mcolors.LogNorm(vmin=grid.min(), vmax=grid.max()), interpolation='nearest')
ax.set_title("Custom xT grid trained on the 2023 FIFA Women's World Cup")
ax.set_xlabel('Pitch length (x)  ->  opponent goal')
ax.set_ylabel('Pitch width (y)')
plt.colorbar(im, ax=ax, label='xT value (log scale)', shrink=0.85)
plt.tight_layout(); plt.savefig(os.path.join(FIG, 'fig_xt2d.png'), bbox_inches='tight'); plt.close()

# ---- Figure 2: 3D xT surface (plotly, log-coloured, zoomed to show relief) ----
surfacecolor = np.log10(grid)
camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0),
              eye=dict(x=-1.15, y=-1.05, z=0.55))
fig = go.Figure(data=[go.Surface(z=grid, surfacecolor=surfacecolor, colorscale='Hot',
                                 cmin=surfacecolor.min(), cmax=surfacecolor.max(), showscale=False)])
fig.update_layout(
    scene=dict(xaxis=dict(title='pitch length (x)', nticks=6, showbackground=False),
               yaxis=dict(title='pitch width (y)', nticks=5, showbackground=False),
               zaxis=dict(title='xT', nticks=5),
               camera=camera, aspectmode='manual', aspectratio=dict(x=1.0, y=0.8, z=0.5)),
    width=820, height=620, margin=dict(l=0, r=0, t=8, b=0), paper_bgcolor='white')
fig.write_image(os.path.join(FIG, 'fig_xt3d.png'), width=820, height=620, scale=2)
plt.close()

# ---- Figure 3: workflow diagram ----
fig, ax = plt.subplots(figsize=(9, 3), dpi=200); ax.axis('off')
steps = ['StatsBomb\nevent data', 'Convert to\nSPADL', 'Train custom\nxT grid',
         'Build per-team\npassing networks', 'Weighted\nPageRank (d=0.85)',
         'Per-match\nZ-scores', 'average_z_score\nranking']
xs = np.linspace(0.02, 0.98, len(steps))
w, h = 0.115, 0.42
for x, s in zip(xs, steps):
    ax.add_patch(FancyBboxPatch((x - w/2, 0.28), w, h, boxstyle='round,pad=0.008', fc='#e8e8f0', ec='k', lw=1))
    ax.text(x, 0.49, s, ha='center', va='center', fontsize=7)
for i in range(len(steps) - 1):
    ax.add_patch(FancyArrowPatch((xs[i] + w/2 + 0.004, 0.49), (xs[i+1] - w/2 - 0.004, 0.49),
                                 arrowstyle='-|>', mutation_scale=10, color='k', lw=1))
ax.set_title('Workflow of the methodology', fontsize=10)
plt.tight_layout(); plt.savefig(os.path.join(FIG, 'fig_workflow.png'), bbox_inches='tight'); plt.close()

# ---- Figure 4: scatter, top-50 Sofascore vs average_z_score ----
rank = pd.read_csv('Results/player_rankings_with_positions.csv')
soft = pd.read_csv('Evaluation/Top 50 Sofascore (standardized).csv')
m = rank.merge(soft, on='player', how='inner')
fig, ax = plt.subplots(figsize=(8, 5.5), dpi=200)
ax.axvline(0, color='grey', lw=0.8, ls='--')
ax.scatter(m['average_z_score'], m['sofascore_rating'], s=30, alpha=0.7, c='#1f77b4')
annots = {'Alexandra Popp': (0, -12), 'Daniela Solera Vega': (4, 12),
          'Lindsey Michelle Horan': (6, -14), 'Hinata Miyazawa': (0, -20),
          'Lauren James': (-10, -6), 'Selma Bacha': (6, -6),
          'Alex Greenwood': (8, 10), 'Thembi Kgatlana': (8, -12),
          'Jennifer Hermoso Fuentes': (6, 8)}
for nm, (dx, dy) in annots.items():
    row = m[m['player'] == nm]
    if len(row):
        ax.annotate(nm, (row['average_z_score'].iloc[0], row['sofascore_rating'].iloc[0]),
                    textcoords='offset points', xytext=(dx, dy), fontsize=6.5)
ax.set_xlabel('average_z_score  (passing-network centrality)')
ax.set_ylabel('Sofascore rating')
ax.set_title('Sofascore rating vs. average_z_score for the top-50 rated players')
plt.tight_layout(); plt.savefig(os.path.join(FIG, 'fig_scatter.png'), bbox_inches='tight'); plt.close()

print('figures written to', FIG, ':', sorted(os.listdir(FIG)))
