import { useEffect, useState } from "react";
import { useAuth } from "./auth/AuthContext";
import volikoLeaf from "./assets/voliko-leaf.png";
import "./App.css";

const features = [
  {
    id: "parcelles",
    icon: "parcel",
    title: "Gestion des parcelles",
    description:
      "Enregistrez vos parcelles, visualisez leurs limites et centralisez leurs informations agricoles.",
  },
  {
    id: "satellite",
    icon: "satellite",
    title: "Suivi satellitaire",
    description:
      "Consultez les indicateurs de végétation pour mieux comprendre l'évolution de vos cultures.",
  },
  {
    id: "meteo",
    icon: "weather",
    title: "Données météorologiques",
    description:
      "Accédez aux informations météorologiques utiles au suivi de vos activités agricoles.",
  },
  {
    id: "alertes",
    icon: "alert",
    title: "Alertes et conseils",
    description:
      "Soyez informé des anomalies détectées et consultez des recommandations adaptées.",
  },
];

const steps = [
  {
    title: "Enregistrez",
    description: "Ajoutez vos parcelles et leurs informations.",
  },
  {
    title: "Observez",
    description:
      "Consultez les indicateurs satellitaires et météorologiques.",
  },
  {
    title: "Comprenez",
    description:
      "Suivez les alertes et consultez les recommandations.",
  },
  {
    title: "Décidez",
    description:
      "Utilisez ces informations pour éclairer vos choix agricoles.",
  },
];

// function FeatureIcon({ name }) {
//   const common = {
//     fill: "none",
//     stroke: "currentColor",
//     strokeWidth: 1.6,
//     strokeLinecap: "round",
//     strokeLinejoin: "round",
//   };

//   return (
//     <svg
//       viewBox="0 0 48 48"
//       width="38"
//       height="38"
//       aria-hidden="true"
//       {...common}
//     >
//       {name === "parcel" && (
//         <>
//           <path d="M10 13 31 9 39 16 36 37 15 40 9 32Z" />
//           <path d="m10 13 5 19 21 5M31 9l5 28" />
//           <circle cx="10" cy="13" r="2" className="icon-accent" />
//           <circle cx="39" cy="16" r="2" className="icon-accent" />
//         </>
//       )}

//       {name === "satellite" && (
//         <>
//           <path d="m18 30 12-12M14 34l5-5M29 19l5-5" />
//           <path d="m25 11 12 12-6 6-12-12Z" />
//           <path
//             d="M9 18a21 21 0 0 1 21-9M39 30a21 21 0 0 1-21 9"
//             className="icon-accent"
//           />
//         </>
//       )}

//       {name === "weather" && (
//         <>
//           <circle cx="24" cy="20" r="8" />
//           <path d="M24 5v4M24 31v4M9 20h4M35 20h4M13.4 9.4l2.8 2.8M31.8 27.8l2.8 2.8M34.6 9.4l-2.8 2.8M16.2 27.8l-2.8-2.8" />
//           <path d="M14 39h20" className="icon-accent" />
//         </>
//       )}

//       {name === "alert" && (
//         <>
//           <path d="M12 32h24l-3-4V19a9 9 0 0 0-18 0v9Z" />
//           <path d="M20 37a4 4 0 0 0 8 0" className="icon-accent" />
//           <path d="M24 14v8M24 26v.5" />
//         </>
//       )}
//     </svg>
//   );
// }


function FeatureIcon({ name }) {
  return (
    <svg viewBox="0 0 64 64" width="72" height="72" aria-hidden="true">
      <defs>
        {/* Dégradés communs */}
        <linearGradient id="g-green-top" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#6FBF8A" />
          <stop offset="1" stopColor="#2F7A52" />
        </linearGradient>
        <linearGradient id="g-green-left" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#245E40" />
          <stop offset="1" stopColor="#193D2B" />
        </linearGradient>
        <linearGradient id="g-green-right" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#193D2B" />
          <stop offset="1" stopColor="#10291D" />
        </linearGradient>
        <linearGradient id="g-orange" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#FFA666" />
          <stop offset="1" stopColor="#E0601E" />
        </linearGradient>
        <linearGradient id="g-cloud" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#FFFFFF" />
          <stop offset="1" stopColor="#CFDCCB" />
        </linearGradient>
        <radialGradient id="g-sun" cx="35%" cy="30%" r="75%">
          <stop offset="0" stopColor="#FFC08F" />
          <stop offset="1" stopColor="#F07832" />
        </radialGradient>
        <linearGradient id="g-panel" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#3C8F63" />
          <stop offset="1" stopColor="#193D2B" />
        </linearGradient>
      </defs>

      {/* ---------- PARCELLES : dalle de terrain isométrique + repère ---------- */}
      {name === "parcel" && (
        <>
          <ellipse cx="32" cy="55" rx="22" ry="5" fill="#193D2B" opacity=".14" />
          {/* faces latérales */}
          <path d="M6 28 32 42 32 50 6 36Z" fill="url(#g-green-left)" />
          <path d="M32 42 58 28 58 36 32 50Z" fill="url(#g-green-right)" />
          {/* face supérieure */}
          <path d="M32 14 58 28 32 42 6 28Z" fill="url(#g-green-top)" />
          {/* quadrillage des parcelles */}
          <path
            d="M19 21 45 35M45 21 19 35"
            stroke="#E8EFE5"
            strokeWidth="1.2"
            opacity=".7"
          />
          {/* repère */}
          <path
            d="M32 30c-5-6-7-9-7-12a7 7 0 0 1 14 0c0 3-2 6-7 12Z"
            fill="url(#g-orange)"
          />
          <circle cx="32" cy="18" r="2.6" fill="#fff" />
        </>
      )}

      {/* ---------- SATELLITE : corps + panneaux solaires + orbite ---------- */}
      {name === "satellite" && (
        <>
          <ellipse
            cx="32"
            cy="34"
            rx="29"
            ry="11"
            fill="none"
            stroke="#F07832"
            strokeWidth="1.4"
            strokeDasharray="3 4"
            opacity=".7"
          />
          <g transform="rotate(-30 32 32)">
            {/* panneau gauche */}
            <path d="M3 25 21 28 21 38 3 41Z" fill="url(#g-panel)" />
            <path
              d="M9 26.2V39.8M15 27.2V38.8M3 33H21"
              stroke="#E8EFE5"
              strokeWidth=".8"
              opacity=".7"
            />
            {/* panneau droit */}
            <path d="M61 25 43 28 43 38 61 41Z" fill="url(#g-panel)" />
            <path
              d="M55 26.2V39.8M49 27.2V38.8M61 33H43"
              stroke="#E8EFE5"
              strokeWidth=".8"
              opacity=".7"
            />
            {/* bras */}
            <path d="M21 33H24M40 33H43" stroke="#193D2B" strokeWidth="2" />
            {/* corps (cube) */}
            <path d="M24 24 32 20 40 24 32 28Z" fill="#FFB98A" />
            <path d="M24 24 32 28 32 42 24 38Z" fill="url(#g-orange)" />
            <path d="M32 28 40 24 40 38 32 42Z" fill="#C24F14" />
            {/* antenne */}
            <path d="M32 20V13" stroke="#193D2B" strokeWidth="1.8" />
            <circle cx="32" cy="12" r="2.4" fill="#193D2B" />
          </g>
        </>
      )}

      {/* ---------- MÉTÉO : soleil + nuage + pluie ---------- */}
      {name === "weather" && (
        <>
          <circle cx="40" cy="22" r="12" fill="url(#g-sun)" />
          <path
            d="M40 4V8M40 36V40M22 22H26M54 22H58M27 9l3 3M50 32l3 3M53 9l-3 3"
            stroke="#F07832"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <ellipse cx="30" cy="56" rx="18" ry="3.5" fill="#193D2B" opacity=".12" />
          <path
            d="M16 50a9 9 0 0 1 1-18 12 12 0 0 1 23-2 10 10 0 0 1 2 20Z"
            fill="url(#g-cloud)"
            stroke="#BFD0BB"
            strokeWidth=".8"
          />
          {/* reflet */}
          <path
            d="M20 37a6 6 0 0 1 6-5"
            stroke="#fff"
            strokeWidth="2"
            strokeLinecap="round"
            fill="none"
          />
          {/* gouttes */}
          <path
            d="M23 54l-2 5M31 54l-2 5M39 54l-2 5"
            stroke="#2F7A52"
            strokeWidth="2.2"
            strokeLinecap="round"
          />
        </>
      )}

      {/* ---------- ALERTES : cloche en volume ---------- */}
      {name === "alert" && (
        <>
          <ellipse cx="32" cy="58" rx="16" ry="3" fill="#193D2B" opacity=".14" />
          {/* corps de la cloche */}
          <path
            d="M32 7a3 3 0 0 1 3 3c8 2 13 8 13 17v8l5 7H11l5-7v-8c0-9 5-15 13-17a3 3 0 0 1 3-3Z"
            fill="url(#g-orange)"
          />
          {/* zone d'ombre à droite (effet volume) */}
          <path
            d="M35 10c8 2 13 8 13 17v8l5 7H38c5-3 6-8 6-14 0-8-3-14-9-18Z"
            fill="#B8480F"
            opacity=".35"
          />
          {/* reflet à gauche */}
          <path
            d="M20 28c0-6 3-11 8-13"
            stroke="#fff"
            strokeWidth="2.4"
            strokeLinecap="round"
            fill="none"
            opacity=".7"
          />
          {/* battant */}
          <ellipse cx="32" cy="51" rx="6" ry="4.5" fill="url(#g-green-top)" />
          {/* point d'alerte */}
          <circle cx="49" cy="14" r="6" fill="#193D2B" />
          <path d="M49 11v4M49 17.2v.4" stroke="#fff" strokeWidth="1.8" strokeLinecap="round" />
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
      <button
        className="back-link"
        type="button"
        onClick={onBack}
      >
        ← Retour à l'accueil
      </button>

      <section className="login-card">
        <a className="login-brand site-logo" href="#accueil">
          <img src={volikoLeaf} alt="" />
          <span>Voliko</span>
        </a>

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

function useReveal() {
  useEffect(() => {
    const items = document.querySelectorAll("[data-reveal]");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    items.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, []);
}

function HomePage({ onLogin }) {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  useReveal();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const closeMenu = () => setMenuOpen(false);

  return (
    <div className="public-site">
      <header className={`site-header ${scrolled ? "is-scrolled" : ""}`}>
        <a className="site-logo" href="#accueil">
          <img src={volikoLeaf} alt="" />
          <span>Voliko</span>
        </a>

        <nav
          className={`main-nav ${menuOpen ? "is-open" : ""}`}
          aria-label="Navigation principale"
        >
          <a href="#fonctionnalites" onClick={closeMenu}>Produits</a>
          <a href="#approche" onClick={closeMenu}>Solutions</a>
          <a href="#apropos" onClick={closeMenu}>À propos</a>
        </nav>

        <div className="header-actions">
          <button className="language-button" type="button" aria-label="Langue actuelle : français">
            FR <span>⌄</span>
          </button>

          <button className="primary-button header-cta" onClick={onLogin}>
            Connexion <span>→</span>
          </button>

          <button
            className="menu-toggle"
            type="button"
            aria-label="Menu"
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen((open) => !open)}
          >
            <span /><span /><span />
          </button>
        </div>
      </header>

      <main>
        <section className="hero-section" id="accueil">
          <div className="hero-copy">
            <span className="hero-badge">Plateforme de suivi agricole</span>
            <h1>
              Une meilleure vision
              <br />
              <em>pour vos décisions agricoles.</em>
            </h1>

            <p className="hero-description">
              Suivez vos cultures, comprenez leur évolution et prenez
              des décisions agricoles mieux informées grâce à VOLIKO.
            </p>

            <div className="hero-actions">
              <a
                className="primary-button"
                href="#fonctionnalites"
              >
                Découvrir VOLIKO <span>→</span>
              </a>

              <a
                className="secondary-link"
                href="#approche"
              >
                Découvrir nos solutions <span>↓</span>
              </a>
            </div>
          </div>
        </section>

        <section className="intro-section" id="apropos">
          <div className="intro-content" data-reveal>
            <h2>
              Pourquoi mieux
              <br />
              comprendre votre
              <br />
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

        <section
          className="features-section"
          id="fonctionnalites"
        >
          <div className="section-heading" data-reveal>
            <h2>
              Tout ce qu'il faut pour mieux comprendre vos cultures.
            </h2>

            <p>
              VOLIKO centralise les informations de vos parcelles,
              les indicateurs satellitaires et les données météorologiques
              pour éclairer vos décisions agricoles.
            </p>
          </div>

          <div className="features-grid">
            {features.map((feature, index) => (
              <article
                className="feature-card"
                key={feature.id}
                data-reveal
                style={{ "--delay": `${index * 90}ms` }}
              >
                <div className="feature-icon">
                  <FeatureIcon name={feature.icon} />
                </div>

                <h3>{feature.title}</h3>

                <p>{feature.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="approach-section" id="approche">
          <div className="approach-heading" data-reveal>
            <h2>
              Comment VOLIKO vous accompagne dans vos décisions ?
            </h2>

            <p>
              De l'enregistrement des parcelles à la consultation
              des recommandations, VOLIKO rassemble les informations
              utiles. L'agriculteur conserve la responsabilité
              de ses décisions.
            </p>
          </div>

          <div className="steps-list">
            {steps.map((step, index) => (
              <article
                className="step-item"
                key={step.title}
                data-reveal
                style={{ "--delay": `${index * 90}ms` }}
              >
                <h3>{step.title}</h3>
                <p>{step.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="closing-section">
          <h2 data-reveal>
            Prêt à prendre des décisions
            <br />
            <em>agricoles mieux éclairées ?</em>
          </h2>

          <button
            className="primary-button"
            type="button"
            onClick={onLogin}
          >
            Accéder à VOLIKO <span>→</span>
          </button>
        </section>
      </main>

      <footer className="site-footer">
        <a className="site-logo footer-logo" href="#accueil">
          <img src={volikoLeaf} alt="" />
          <span>Voliko</span>
        </a>

        <p>
          Des informations utiles pour des décisions agricoles éclairées.
        </p>

        <span>
          © {new Date().getFullYear()} VOLIKO. Tous droits réservés.
        </span>
      </footer>
    </div>
  );
}

function App() {
  const { user, loading, logout } = useAuth();
  const [showLogin, setShowLogin] = useState(false);

  if (loading) {
    return (
      <div className="loading">
        Chargement de VOLIKO...
      </div>
    );
  }

  if (user) {
    return (
      <main className="login-page">
        <section className="login-card">
          <a className="login-brand site-logo" href="#accueil">
            <img src={volikoLeaf} alt="" />
            <span>Voliko</span>
          </a>

          <h1>
            Bienvenue, {user.first_name || user.username}.
          </h1>

          <p className="user-role">
            Rôle : {user.role}
          </p>

          <button
            className="primary-button login-submit"
            type="button"
            onClick={logout}
          >
            Se déconnecter <span>→</span>
          </button>
        </section>
      </main>
    );
  }

  if (showLogin) {
    return (
      <LoginPage onBack={() => setShowLogin(false)} />
    );
  }

  return (
    <HomePage onLogin={() => setShowLogin(true)} />
  );
}

export default App;