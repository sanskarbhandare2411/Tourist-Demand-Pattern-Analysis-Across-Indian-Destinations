import React from 'react';
import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';

const Plot = createPlotlyComponent(Plotly);

export default function PlotlyChart({ data = [], layout = {}, config = {}, style = {}, className = "" }) {
  const defaultLayout = {
    template: 'plotly_dark',
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: {
      family: 'Plus Jakarta Sans, sans-serif',
      color: '#e2e8f0',
    },
    title: {
      font: {
        family: 'Outfit, sans-serif',
        size: 16,
        color: '#f8fafc',
      },
    },
    legend: {
      bgcolor: 'rgba(15, 23, 42, 0.65)',
      bordercolor: 'rgba(255, 255, 255, 0.1)',
      font: { color: '#cbd5e1' },
    },
    margin: { l: 40, r: 40, t: 55, b: 40 },
    autosize: true,
    xaxis: {
      gridcolor: 'rgba(255, 255, 255, 0.07)',
      zerolinecolor: 'rgba(255, 255, 255, 0.12)',
      tickfont: { color: '#94a3b8' },
      titlefont: { color: '#cbd5e1' },
    },
    yaxis: {
      gridcolor: 'rgba(255, 255, 255, 0.07)',
      zerolinecolor: 'rgba(255, 255, 255, 0.12)',
      tickfont: { color: '#94a3b8' },
      titlefont: { color: '#cbd5e1' },
    },
    ...layout,
  };

  const defaultConfig = {
    responsive: true,
    displayModeBar: false,
    ...config,
  };

  return (
    <div style={{ width: '100%', minHeight: '380px', ...style }} className={className}>
      <Plot
        data={data}
        layout={defaultLayout}
        config={defaultConfig}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}
