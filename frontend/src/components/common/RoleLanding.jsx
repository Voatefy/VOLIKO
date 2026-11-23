import DashboardLayout from "../layout/DashboardLayout";

function RoleLanding({ title }) {
  return (
    <DashboardLayout>
      <section className="dashboard-welcome">
        <span className="dashboard-welcome-label">BIENVENUE SUR VOLIKO</span>
        <h2>{title}</h2>
        <p>
          Retrouvez ici les informations et les fonctionnalités
          nécessaires à la gestion de votre espace agricole.
        </p>
      </section>
    </DashboardLayout>
  );
}

export default RoleLanding;
