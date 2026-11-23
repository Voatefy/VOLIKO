import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./AuthContext";
import { getRoleHomePath } from "./roleRoutes";

function ProtectedRoute({ allowedRoles }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading">
        Chargement de VOLIKO...
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/connexion" replace />;
  }

  if (!allowedRoles.includes(user.role)) {
    return (
      <Navigate
        to={getRoleHomePath(user.role)}
        replace
      />
    );
  }

  return <Outlet />;
}

export default ProtectedRoute;
