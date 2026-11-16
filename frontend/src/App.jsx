import React, { useEffect, useState } from 'react';
import Sidebar, { PAGES } from './components/Sidebar';
import Navbar from './components/Navbar';
import OverviewPage from './pages/OverviewPage';
import DemandAnalysisPage from './pages/DemandAnalysisPage';
import DestinationAnalysisPage from './pages/DestinationAnalysisPage';
import SeasonalAnalysisPage from './pages/SeasonalAnalysisPage';
import WeatherTourismPage from './pages/WeatherTourismPage';
import MLPredictionPage from './pages/MLPredictionPage';
import ClusteringPage from './pages/ClusteringPage';
import RecommendationsPage from './pages/RecommendationsPage';
import api from './services/api';

export default function App() {
  const [activePage, setActivePage] = useState('overview');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [filterOptions, setFilterOptions] = useState({});
  const [filters, setFilters] = useState({
    state: 'All States',
    visitorType: 'All Tourists (Total)',
    typology: 'All Typologies',
    unesco: 'all',
  });
  const [activeCount, setActiveCount] = useState(144);
  const [totalCount, setTotalCount] = useState(144);
  const [isBackendOnline, setIsBackendOnline] = useState(true);

  // Load filter metadata & initial destinations count
  useEffect(() => {
    api.getHealth()
      .then((res) => {
        setIsBackendOnline(res.status === 'online');
        if (res.destinations_count) {
          setTotalCount(res.destinations_count);
        }
      })
      .catch(() => setIsBackendOnline(false));

    api.getFilters()
      .then(setFilterOptions)
      .catch(console.error);
  }, []);

  // Update active count whenever filters change
  useEffect(() => {
    const params = {};
    if (filters.state && filters.state !== 'All States') params.state = filters.state;
    if (filters.typology && filters.typology !== 'All Typologies') params.typology = filters.typology;
    if (filters.unesco === 'unesco') params.unesco_only = true;
    else if (filters.unesco === 'non-unesco') params.unesco_only = false;

    api.getDestinations(params)
      .then((res) => setActiveCount(res.total_count || 0))
      .catch(console.error);
  }, [filters]);

  const currentPage = PAGES.find((p) => p.id === activePage);

  return (
    <div className="app-container">
      {/* Ambient Animated Glow Elements */}
      <div className="ambient-orb ambient-orb-1" />
      <div className="ambient-orb ambient-orb-2" />

      {/* Sidebar Navigation & Filters */}
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
        filterOptions={filterOptions}
        filters={filters}
        setFilters={setFilters}
        isOpen={sidebarOpen}
        setIsOpen={setSidebarOpen}
        activeCount={activeCount}
        totalCount={totalCount}
      />

      {/* Main Content Area */}
      <main className="main-content">
        <Navbar
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
          currentPageTitle={currentPage?.title || 'Overview'}
          isOnline={isBackendOnline}
        />

        {activePage === 'overview' && <OverviewPage />}
        {activePage === 'demand' && <DemandAnalysisPage />}
        {activePage === 'destination' && <DestinationAnalysisPage globalFilters={filters} />}
        {activePage === 'seasonal' && <SeasonalAnalysisPage />}
        {activePage === 'weather' && <WeatherTourismPage />}
        {activePage === 'ml' && <MLPredictionPage />}
        {activePage === 'clustering' && <ClusteringPage />}
        {activePage === 'recommendations' && <RecommendationsPage filterOptions={filterOptions} />}
      </main>
    </div>
  );
}
