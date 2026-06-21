import { SearchBox } from "@/components/SearchBox";

export default function HomePage() {
  return (
    <div>
      <div className="panel">
        <p className="muted" style={{ marginTop: 0 }}>
          Cerca un deputato e scopri di quali <strong>temi</strong> si occupa
          davvero in Parlamento. Ogni dato è ricondotto a una fonte ufficiale
          tracciabile (resoconti dell&apos;Assemblea, atti). Niente sintesi
          inventate.
        </p>
        <SearchBox />
      </div>
      <p className="note">
        Fase 1 — solo fonti ufficiali istituzionali (Camera dei Deputati).
        Il Senato e il confronto con la comunicazione pubblica/propaganda sono
        previsti nelle fasi successive.
      </p>
    </div>
  );
}
