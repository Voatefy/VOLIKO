import { useState } from "react";
import { useAuth } from "./auth/AuthContext";
import "./App.css";

const features = [
  {
    number: "01",
    icon: "parcel",
    title: "Gestion des parcelles",
    description:
      "Enregistrez vos parcelles, visualisez leurs limites et centralisez leurs informations agricoles.",
  },
  {
    number: "02",
    icon: "satellite",
    title: "Suivi satellitaire",
    description:
      "Consultez les indicateurs de végétation pour mieux comprendre l'évolution de vos cultures.",
  },
  {
    number: "03",
    icon: "weather",
    title: "Données météorologiques",
    description:
      "Accédez aux informations météorologiques utiles au suivi de vos activités agricoles.",
  },
  {
    number: "04",
    icon: "alert",
    title: "Alertes et conseils",
    description:
      "Soyez informé des anomalies détectées et consultez des recommandations adaptées.",
  },
];


function FeatureIcon({ name }) {
  const common = {
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.6,
    strokeLinecap: "round",
    strokeLinejoin: "round",
  };

  return (
    <svg viewBox="0 0 48 48" width="38" height="38"
      aria-hidden="true" {...common}>
      {name === "parcel" && (
        <>
          <path d="M10 13 31 9 39 16 36 37 15 40 9 32Z" />
          <path d="m10 13 5 19 21 5M31 9l5 28" />
          <circle cx="10" cy="13" r="2" fill="#F07832" stroke="none" />
          <circle cx="39" cy="16" r="2" fill="#F07832" stroke="none" />
        </>
      )}

      {name === "satellite" && (
        <>
          <path d="m18 30 12-12M14 34l5-5M29 19l5-5" />
          <path d="m25 11 12 12-6 6-12-12Z" />
          <path d="M9 18a21 21 0 0 1 21-9M39 30a21 21 0 0 1-21 9"
            stroke="#F07832" />
        </>
      )}

      {name === "weather" && (
        <>
          <circle cx="24" cy="20" r="8" />
          <path d="M24 5v4M24 31v4M9 20h4M35 20h4M13.4 9.4l2.8 2.8M31.8 27.8l2.8 2.8M34.6 9.4l-2.8 2.8M16.2 27.8l-2.8 2.8" />
          <path d="M14 39h20" stroke="#F07832" />
        </>
      )}

      {name === "alert" && (
        <>
          <path d="M12 32h24l-3-4V19a9 9 0 0 0-18 0v9Z" />
          <path d="M20 37a4 4 0 0 0 8 0" stroke="#F07832" />
          <path d="M24 14v8M24 26v.5" />
        </>
      )}
    </svg>
  );
}

function LoginPage({ onBack }) {
  const { login } = useAuth();
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

  return (
    <main className="login-page">
      <button className="back-link" onClick={onBack}>
        ← Retour à l'accueil
      </button>

      <section className="login-card">
        <div className="login-brand">VOLIKO<span>.</span></div>
        <p className="eyebrow">VOTRE ESPACE AGRICOLE</p>
        <h1>Heureux de vous retrouver.</h1>
        <p className="login-description">
          Connectez-vous pour retrouver vos parcelles et vos données agricoles.
        </p>

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

          {error && <p className="error-message">{error}</p>}

          <button className="primary-button login-submit" disabled={submitting}>
            {submitting ? "Connexion..." : "Se connecter"}
            <span>→</span>
          </button>
        </form>
      </section>
    </main>
  );
}

function HomePage({ onLogin }) {
  return (
    <div className="public-site">
      <header className="site-header">
        <a className="site-logo" href="#accueil">VOLIKO<span>.</span></a>

        <nav className="main-nav">
          <a href="#fonctionnalites">Produits</a>
          <a href="#approche">Solutions</a>
          <a href="#apropos">À propos</a>
        </nav>

        <div className="header-actions">
          <button className="language-button" type="button" aria-label="Langue actuelle">
            FR <span>⌄</span>
          </button>
          <button className="login-link" onClick={onLogin}>Connexion</button>
          <button className="primary-button header-cta" onClick={onLogin}>
            Accéder à VOLIKO <span>→</span>
          </button>
        </div>
      </header>

      <main>
        <section className="hero-section" id="accueil">
          <div className="hero-copy">
            <p className="eyebrow">LA TECHNOLOGIE AU SERVICE DE L'AGRICULTURE</p>

            <h1>
              Une meilleure vision<br />
              <em>pour vos décisions agricoles.</em>
            </h1>

            <p className="hero-description">
              Suivez vos cultures, comprenez leur évolution et prenez
              des décisions agricoles mieux informées grâce à VOLIKO.
            </p>

            <div className="hero-actions">
              <a className="primary-button" href="#fonctionnalites">
                Découvrir VOLIKO <span>→</span>
              </a>
              <a className="secondary-link" href="#approche">
                Découvrir nos solutions <span>↓</span>
              </a>
            </div>
          </div>
        </section>

        <section className="intro-section" id="apropos">
          <div className="intro-content">
            <h2>
              Pourquoi mieux<br />
              comprendre votre<br />
              <em>exploitation agricole ?</em>
            </h2>

            <div className="intro-text">
              <p>
                Les décisions agricoles reposent sur une bonne compréhension
                du terrain. VOLIKO rassemble les informations essentielles
                de vos parcelles pour vous aider à mieux suivre votre exploitation.
              </p>
              <a href="#fonctionnalites" className="text-link">
                Découvrir la plateforme <span>↗</span>
              </a>
            </div>
          </div>
        </section>

        <section className="features-section" id="fonctionnalites">
          <div className="section-heading">
            <div>
              <h2>Tout ce qu'il faut pour mieux comprendre vos cultures.</h2>
            </div>
            <p>
              VOLIKO centralise les informations de vos parcelles, les indicateurs
              satellitaires et les données météorologiques pour éclairer vos décisions agricoles.
            </p>
          </div>

          <div className="features-grid">
            {features.map((feature) => (
              <article className="feature-card" key={feature.number}>
                <div className="feature-top">
                  <span className="feature-icon">
                    <FeatureIcon name={feature.icon} />
                  </span>
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
                <span className="feature-arrow">↗</span>
              </article>
            ))}
          </div>
        </section>

        <section className="approach-section" id="approche">
          <div className="approach-heading">
            <h2>Comment VOLIKO vous accompagne dans vos décisions ?</h2>
            <p>
              De l'enregistrement des parcelles à la consultation des recommandations,
              VOLIKO rassemble les informations utiles. L'agriculteur conserve
              la responsabilité de ses décisions.
            </p>
          </div>
          <div className="steps-list">
            <div className="step-item">
              <span>01</span>
              <div><h3>Enregistrez</h3><p>Ajoutez vos parcelles et leurs informations.</p></div>
            </div>
            <div className="step-item">
              <span>02</span>
              <div><h3>Observez</h3><p>Consultez les indicateurs satellitaires et météorologiques.</p></div>
            </div>
            <div className="step-item">
              <span>03</span>
              <div><h3>Comprenez</h3><p>Suivez les alertes et consultez les recommandations.</p></div>
            </div>
            <div className="step-item">
              <span>04</span>
              <div><h3>Décidez</h3><p>Utilisez ces informations pour éclairer vos choix agricoles.</p></div>
            </div>
          </div>
        </section>

        <section className="closing-section">
          <h2>
            Prêt à prendre des décisions<br />
            <em>agricoles mieux éclairées ?</em>
          </h2>
          <button className="primary-button" onClick={onLogin}>
            Accéder à VOLIKO <span>→</span>
          </button>
        </section>
      </main>

      <footer className="site-footer">
        <a className="site-logo footer-logo" href="#accueil">VOLIKO<span>.</span></a>
        <p>Des informations utiles pour des décisions agricoles éclairées.</p>
        <span>© {new Date().getFullYear()} VOLIKO. Tous droits réservés.</span>
      </footer>
    </div>
  );
}

function App() {
  const { user, loading, logout } = useAuth();
  const [showLogin, setShowLogin] = useState(false);

  if (loading) {
    return <div className="loading">Chargement de VOLIKO...</div>;
  }

  if (user) {
    return (
      <main className="login-page">
        <section className="login-card">
          <div className="login-brand">VOLIKO<span>.</span></div>
          <h1>Bienvenue, {user.first_name || user.username}.</h1>
          <p className="login-description">Vous êtes connecté à votre espace VOLIKO.</p>
          <p>Rôle : {user.role}</p>
          <button className="primary-button login-submit" onClick={logout}>
            Se déconnecter <span>→</span>
          </button>
        </section>
      </main>
    );
  }

  return showLogin
    ? <LoginPage onBack={() => setShowLogin(false)} />
    : <HomePage onLogin={() => setShowLogin(true)} />;
}

export default App;
