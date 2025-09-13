import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Landing from './pages/Landing';
import AdminDashboard from './pages/admin/AdminDashboard';
import UserDashboard from './pages/user/UserDashboard';
import PlansAvailable from './pages/user/PlansAvailable';
import PlanRecommendations from './pages/user/PlanRecommendations';
import MyPlan from './pages/user/MyPlan';
import Alerts from './pages/user/Alerts';
import Discounts from './pages/user/Discounts';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/landing" element={<Landing />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/user/dashboard" element={<UserDashboard />} />
          <Route path="/user/plans-available" element={<PlansAvailable />} />
          <Route path="/user/plan-recommendations" element={<PlanRecommendations />} />
          <Route path="/user/my-plan" element={<MyPlan />} />
          <Route path="/user/alerts" element={<Alerts />} />
          <Route path="/user/discounts" element={<Discounts />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
