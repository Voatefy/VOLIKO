import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { useAuth } from "./auth/AuthContext";
import { getRoleHomePath } from "./auth/roleRoutes";
import CandidaturesPage from "./pages/admin/CandidaturesPage";
import ProtectedRoute from "./auth/ProtectedRoute";
import LoginPage from "./pages/auth/LoginPage";
import HomePage from "./pages/home/HomePage";
import RoleLanding from "./components/common/RoleLanding";
import ParcellesPage from "./pages/agriculteur/ParcellesPage";
import "./styles/dashboard.css";
import "./App.css";

function PublicHome() {
  const navigate = useNavigate();

  return (
    <HomePage onLogin={() => navigate("/connexion")} />
  );
}

function LoginRoute() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loading">Chargement de VOLIKO...</div>;
  }

  if (user) {
    return <Navigate to={getRoleHomePath(user.role)} replace />;
  }

  return <LoginPage />;
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<PublicHome />} />

      <Route path="/connexion" element={<LoginRoute />} />

      <Route element={<ProtectedRoute allowedRoles={["AGRICULTEUR"]} />}>
        <Route
          path="/agriculteur"
          element={<RoleLanding title="Espace agriculteur" />}
        />
        <Route
          path="/agriculteur/parcelles"
          element={<ParcellesPage />}
        />
      </Route>

      <Route element={<ProtectedRoute allowedRoles={["AGRONOME"]} />}>
        <Route
          path="/agronome"
          element={<RoleLanding title="Espace agronome" />}
        />
      </Route>

      <Route element={<ProtectedRoute allowedRoles={["CANDIDAT_AGRONOME"]} />}>
        <Route
          path="/candidat-agronome"
          element={<RoleLanding title="Espace candidat agronome" />}
        />
      </Route>

      {/* <Route element={<ProtectedRoute allowedRoles={["ADMINISTRATEUR"]} />}>
        <Route
          path="/administration"
          element={<RoleLanding title="Espace administration" />}
        />
      </Route> */}

      <Route element={<ProtectedRoute allowedRoles={["ADMINISTRATEUR"]} />}>
        <Route path="/administration" element={<RoleLanding title="Espace administration" />} />
        <Route path="/administration/candidatures" element={<CandidaturesPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
