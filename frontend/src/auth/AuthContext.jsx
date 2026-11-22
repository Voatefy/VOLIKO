import { createContext, useContext, useEffect, useState } from "react";
import {
  login as loginService,
  getProfile,
  logout as logoutService,
} from "./authService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadUser() {
      const accessToken = localStorage.getItem("voliko_access");

      if (!accessToken) {
        setLoading(false);
        return;
      }

      try {
        const profile = await getProfile();
        setUser(profile);
      } catch {
        logoutService();
        setUser(null);
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, []);

  async function login(credentials) {
    await loginService(credentials);
    const profile = await getProfile();
    setUser(profile);
    return profile;
  }

  function logout() {
    logoutService();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
