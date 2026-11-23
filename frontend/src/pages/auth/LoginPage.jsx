import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";
import { getRoleHomePath } from "../../auth/roleRoutes";
import volikoLeaf from "../../assets/voliko-leaf.png";

function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setSubmitting(true);

    try {
      const profile = await login({ email, password });
      navigate(getRoleHomePath(profile.role), { replace: true });
    } catch (err) {
      setError(err.message || "Connexion impossible.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="login-page">
      <Link className="back-link" to="/">
        ← Retour à l'accueil
      </Link>

      <section className="login-card">
        <Link className="login-brand site-logo" to="/">
          <img src={volikoLeaf} alt="" />
          <span>Voliko</span>
        </Link>

        <h1>Connexion</h1>

        <form onSubmit={handleSubmit}>
          <label htmlFor="email">Adresse e-mail</label>

          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="exemple@email.com"
            autoComplete="email"
            required
          />

          <label htmlFor="password">Mot de passe</label>

          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Votre mot de passe"
            autoComplete="current-password"
            required
          />

          {error && (
            <p className="error-message" role="alert">
              {error}
            </p>
          )}

          <button
            className="primary-button login-submit"
            type="submit"
            disabled={submitting}
          >
            {submitting ? "Connexion..." : "Se connecter"}
            <span>→</span>
          </button>
        </form>
      </section>
    </main>
  );
}

export default LoginPage;
