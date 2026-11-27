
import { useState } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";

function DashboardLayout({ children }) {
  const [menuOuvert, setMenuOuvert] = useState(false);

  return (
    <div className="dashboard-layout">
      <Sidebar
        menuOuvert={menuOuvert}
        fermerMenu={() => setMenuOuvert(false)}
      />

      <div className="dashboard-main">
        <Header
          ouvrirMenu={() => setMenuOuvert(true)}
        />

        <main className="dashboard-content">
          {children}
        </main>
      </div>
    </div>
  );
}

export default DashboardLayout;
