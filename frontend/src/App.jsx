import { useState } from "react";
import { useAuth } from "./auth/AuthContext";
import "./App.css";

const features = [
  {
    number: "01",
    icon: "⌖",
    title: "Gestion des parcelles",
    description:
      "Enregistrez vos parcelles, visualisez leurs limites et centralisez leurs informations agricoles.",
  },
  {
    number: "02",
    icon: "◉",
    title: "Suivi satellitaire",
    description:
      "Consultez les indicateurs de végétation pour mieux comprendre l'évolution de vos cultures.",
  },
  {
    number: "03",
    icon: "☼",
    title: "Données météorologiques",
    description:
      "Accédez aux informations météorologiques utiles au suivi de vos activités agricoles.",
  },
  {
    number: "04",
    icon: "⌁",
    title: "Alertes et conseils",
    description:
      "Soyez informé des anomalies détectées et consultez des recommandations adaptées.",
  },
];

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

function DashboardPreview() {
  return (
    <div className="dashboard-preview" aria-label="Illustration d'un tableau de bord agricole">
      <div className="preview-topbar">
        <div className="preview-brand"><span /> VOLIKO</div>
        <div className="preview-avatar">A</div>
      </div>

      <div className="preview-content">
        <div className="preview-heading">
          <div>
            <span className="preview-label">VOTRE EXPLOITATION</span>
            <h3>Vue d'ensemble</h3>
          </div>
          <span className="preview-period">Cette saison⌄</span>
        </div>

        <div className="preview-stats">
          <div className="preview-stat">
            <span>Parcelles</span>
            <strong>08</strong>
            <small>Enregistrées</small>
          </div>
          <div className="preview-stat">
            <span>Superficie totale</span>
            <strong>12,5 <small>ha</small></strong>
            <small>Surface suivie</small>
          </div>
          <div className="preview-stat">
            <span>État général</span>
            <strong className="healthy">Stable</strong>
            <small>Dernière observation</small>
          </div>
        </div>

        <div className="preview-lower">
          <div className="preview-map">
            <div className="map-grid" />
            <div className="field field-one" />
            <div className="field field-two" />
            <div className="field field-three" />
            <span className="map-pin">●</span>
            <span className="map-caption">VOS PARCELLES</span>
          </div>
          <div className="preview-activity">
            <span className="preview-label">ACTIVITÉ RÉCENTE</span>
            <div><i /> Données actualisées <small>Aujourd'hui</small></div>
            <div><i /> Observation disponible <small>Hier</small></div>
            <div><i /> Parcelle enregistrée <small>Cette semaine</small></div>
          </div>
        </div>
      </div>
      <div className="preview-glow" />
    </div>
  );
}

function HomePage({ onLogin }) {
  return (
    <div className="public-site">
      <header className="site-header">
        <a className="site-logo" href="#accueil">VOLIKO<span>.</span></a>

        <nav className="main-nav">
          <a href="#fonctionnalites">Fonctionnalités</a>
          <a href="#approche">Notre approche</a>
          <a href="#apropos">À propos</a>
        </nav>

        <div className="header-actions">
          <button className="language-button" type="button" aria-label="Langue actuelle">
            FR <span>⌄</span>
          </button>
          <button className="login-link" onClick={onLogin}>Connexion</button>
          <button className="primary-button header-cta" onClick={onLogin}>
            Accéder à VOLIKO <span>↗</span>
          </button>
        </div>
      </header>

      <main>
        <section className="hero-section" id="accueil">
          <div className="hero-background-shape" />
          <div className="hero-copy">
            <p className="eyebrow"><span /> LA TECHNOLOGIE AU SERVICE DE L'AGRICULTURE</p>
            <h1>
              Cultiver avec<br />
              <em>une meilleure</em><br />
              vision.
            </h1>
            <p className="hero-description">
              Comprenez vos parcelles, suivez l'évolution de vos cultures
              et prenez des décisions agricoles mieux informées grâce à VOLIKO.
            </p>
            <div className="hero-actions">
              <a className="primary-button" href="#fonctionnalites">
                Découvrir VOLIKO <span>↗</span>
              </a>
              <a className="secondary-link" href="#approche">
                Explorer notre approche <span>↓</span>
              </a>
            </div>
            <div className="hero-note">
              <span className="note-line" />
              <span>Observer. Comprendre. Décider.</span>
            </div>
          </div>

          <div className="hero-visual">
            <div className="visual-orbit orbit-one" />
            <div className="visual-orbit orbit-two" />
            <DashboardPreview />
            <div className="floating-note">
              <span className="floating-icon">⌖</span>
              <div><strong>Vos parcelles</strong><small>Un suivi centralisé</small></div>
            </div>
            <div className="visual-caption">L'AGRICULTURE, ÉCLAIRÉE PAR LA DONNÉE.</div>
          </div>
          <div className="hero-index">01 — 04</div>
        </section>

        <section className="intro-section" id="apropos">
          <p className="eyebrow">UNE NOUVELLE FAÇON DE SUIVRE SES CULTURES</p>
          <div className="intro-content">
            <h2>
              L'information agricole<br />
              au bon endroit,<br />
              <em>au bon moment.</em>
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
              <p className="eyebrow">CE QUE VOLIKO VOUS APPORTE</p>
              <h2>Une vision plus claire<br />de votre exploitation.</h2>
            </div>
            <p>
              Des outils complémentaires pour centraliser les informations
              et accompagner vos décisions agricoles.
            </p>
          </div>

          <div className="features-grid">
            {features.map((feature) => (
              <article className="feature-card" key={feature.number}>
                <div className="feature-top">
                  <span className="feature-icon">{feature.icon}</span>
                  <span className="feature-number">{feature.number}</span>
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
            <p className="eyebrow">UNE DÉMARCHE SIMPLE</p>
            <h2>De l'observation<br />à la décision.</h2>
            <p>
              VOLIKO vous accompagne dans le suivi de vos parcelles,
              tout en laissant à l'agriculteur la responsabilité de ses décisions.
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
          <p className="eyebrow">VOTRE AGRICULTURE MÉRITE UNE MEILLEURE VISIBILITÉ</p>
          <h2>Et si vous preniez<br /><em>une longueur d'avance ?</em></h2>
          <button className="primary-button" onClick={onLogin}>
            Accéder à VOLIKO <span>↗</span>
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
