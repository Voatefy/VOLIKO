import { useState } from "react";
import { useAuth } from "./auth/AuthContext";
import "./App.css";

function App() {
  const { user, loading, login, logout } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      await login({ email, password });
    } catch (err) {
      setError(err.message || "Connexion impossible.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <div className="loading">Chargement de VOLIKO...</div>;
  }

  if (user) {
    return (
      <main className="auth-container">
        <section className="auth-card">
          <h1>Bienvenue sur VOLIKO</h1>
          <p>Bonjour {user.first_name || user.username} !</p>
          <p>Rôle : {user.role}</p>
          <button onClick={logout}>Se déconnecter</button>
        </section>
      </main>
    );
  }

  return (
    <main className="auth-container">
      <section className="auth-card">
        <div className="brand">
          <h1>VOLIKO</h1>
          <p>Votre partenaire pour une agriculture mieux informée.</p>
        </div>

        <div className="auth-heading">
          <h2>Connexion</h2>
          <p>Connectez-vous à votre espace agricole.</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Adresse e-mail</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="exemple@email.com"
              autoComplete="email"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Mot de passe</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Votre mot de passe"
              autoComplete="current-password"
              required
            />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button type="submit" disabled={submitting}>
            {submitting ? "Connexion..." : "Se connecter"}
          </button>
        </form>
      </section>
    </main>
  );
}

export default App;