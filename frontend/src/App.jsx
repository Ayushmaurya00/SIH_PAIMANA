import React, { Suspense, lazy, useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { Sparkles } from 'lucide-react';

import Header from './components/Header';
import Sidebar from './components/Sidebar';
import AIAssistantDrawer from './components/AIAssistantDrawer';
import ImportModal from './components/ImportModal';
import { AuthProvider, useAuth } from './context/AuthContext';
import { getAlertCount } from './api/client';

const OverviewPage = lazy(() => import('./pages/OverviewPage'));
const ExplorerPage = lazy(() => import('./pages/ExplorerPage'));
const ProjectDetailPage = lazy(() => import('./pages/ProjectDetailPage'));
const AlertsPage = lazy(() => import('./pages/AlertsPage'));
const ModelComparisonPage = lazy(() => import('./pages/ModelComparisonPage'));
const LoginPage = lazy(() => import('./pages/LoginPage'));
const AdminPage = lazy(() => import('./pages/AdminPage'));

// Layout Wrapper Component to conditionally render Header and Sidebar
const MainLayout = ({ onOpenAssistant, onOpenImport, alertCount, assistantContextPid, isAssistantOpen, setIsAssistantOpen, isImportOpen, setIsImportOpen }) => {
  const location = useLocation();
  const { isAuthenticated } = useAuth();
  const isAuthPage = ['/login', '/signin', '/signup', '/register'].includes(location.pathname);

  // Redirect to login if user is not signed in
  if (!isAuthenticated && !isAuthPage) {
    return <Navigate to="/login" replace />;
  }

  // Redirect to dashboard if signed-in officer visits login/register
  if (isAuthenticated && isAuthPage) {
    return <Navigate to="/" replace />;
  }

  if (isAuthPage) {
    return (
      <Suspense fallback={<div className="min-h-screen bg-white flex items-center justify-center text-slate-700 text-xs font-mono">Loading Security Gateway...</div>}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signin" element={<LoginPage />} />
          <Route path="/signup" element={<LoginPage />} />
          <Route path="/register" element={<LoginPage />} />
        </Routes>
      </Suspense>
    );
  }

  return (
    <div className="min-h-screen bg-background text-slate-900 flex flex-col">
      {/* Government Sovereign Header */}
      <Header
        onOpenAssistant={() => onOpenAssistant(null)}
        onOpenImport={() => setIsImportOpen(true)}
        alertCount={alertCount}
      />

      {/* Main Application Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation Sidebar */}
        <Sidebar onOpenAssistant={() => onOpenAssistant(null)} />

        {/* Page Routing Container */}
        <main className="flex-1 overflow-y-auto bg-background min-h-[calc(100vh-65px)]">
          <div className="animate-fade-in">
            <Suspense fallback={<div className="p-6 text-sm text-slate-500">Loading page...</div>}>
              <Routes>
                <Route path="/" element={<OverviewPage />} />
                <Route path="/explorer" element={<ExplorerPage />} />
                <Route
                  path="/project/:id"
                  element={<ProjectDetailPage onOpenAssistantWithContext={onOpenAssistant} />}
                />
                <Route
                  path="/projects/:id"
                  element={<ProjectDetailPage onOpenAssistantWithContext={onOpenAssistant} />}
                />
                <Route path="/alerts" element={<AlertsPage />} />
                <Route path="/models" element={<ModelComparisonPage />} />
                <Route path="/methodology-audit" element={<ModelComparisonPage />} />
                <Route path="/admin" element={<AdminPage />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </Suspense>
          </div>
        </main>
      </div>

      {/* Collapsible Floating AI Intelligence Drawer */}
      <AIAssistantDrawer
        isOpen={isAssistantOpen}
        onClose={() => setIsAssistantOpen(false)}
        contextProjectId={assistantContextPid}
      />

      {/* Modal for CUF Data Ingestion */}
      <ImportModal
        isOpen={isImportOpen}
        onClose={() => setIsImportOpen(false)}
      />
    </div>
  );
};

export const App = () => {
  const [isAssistantOpen, setIsAssistantOpen] = useState(false);
  const [isImportOpen, setIsImportOpen] = useState(false);
  const [assistantContextPid, setAssistantContextPid] = useState(null);
  const [alertCount, setAlertCount] = useState(0);

  useEffect(() => {
    let isMounted = true;
    const timer = setTimeout(async () => {
      try {
        const res = await getAlertCount({ severity: 'High', status: 'New' });
        if (isMounted && res && typeof res.count === 'number') {
          setAlertCount(res.count);
        }
      } catch (e) {
        console.error(e);
      }
    }, 50);
    return () => {
      isMounted = false;
      clearTimeout(timer);
    };
  }, []);

  const handleOpenAssistant = (contextPid = null) => {
    setAssistantContextPid(contextPid);
    setIsAssistantOpen(true);
  };

  return (
    <AuthProvider>
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <MainLayout
          onOpenAssistant={handleOpenAssistant}
          onOpenImport={() => setIsImportOpen(true)}
          alertCount={alertCount}
          assistantContextPid={assistantContextPid}
          isAssistantOpen={isAssistantOpen}
          setIsAssistantOpen={setIsAssistantOpen}
          isImportOpen={isImportOpen}
          setIsImportOpen={setIsImportOpen}
        />
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
