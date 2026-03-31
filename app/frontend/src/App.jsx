import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Dashboard } from './components/Dashboard';
import { Login } from './pages/Login'; // Import your new pages
import { Register } from './pages/Register';
function App() {

  return (
    <Router>
      <div className="min-h-screen bg-[#F8FAFC]">
        <Routes>
          {/* Dashboard Route */}
          <Route path="/" element={
            <Dashboard />
          } />

          {/* Auth Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Redirect any unknown routes to home */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;