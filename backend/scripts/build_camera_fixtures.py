"""Genera le fixtures REALI della Camera eseguendo l'adapter live e salvando l'output.

Le fixtures prodotte sono documenti ufficiali reali (resoconti stenografici
dell'Assemblea) con URL, data e attribuzione al deputato corretti. Vanno
committate in data/fixtures/camera/ e poi lette offline dalla pipeline.

Uso:
    python -m scripts.build_camera_fixtures --sedute 4
oppure (dalla cartella backend):
    python scripts/build_camera_fixtures.py --sedute 4
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from parlamente.config import get_settings
from parlamente.logging import setup_logging
from parlamente.sources.camera.speeches import CameraSpeechesAdapter


def main() -> None:
    parser = argparse.ArgumentParser(description="Costruisce fixtures reali dai resoconti Camera.")
    parser.add_argument("--sedute", type=int, default=4, help="Numero di sedute recenti (modalità indice).")
    parser.add_argument("--from-seduta", type=int, default=None, help="idSeduta iniziale (storico esteso).")
    parser.add_argument("--to-seduta", type=int, default=None, help="idSeduta finale (storico esteso).")
    parser.add_argument("--legislature", default="19")
    parser.add_argument("--max-int-per-seduta", type=int, default=60)
    args = parser.parse_args()

    setup_logging()
    out_dir = get_settings().fixtures_dir / "camera"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.from_seduta is not None and args.to_seduta is not None:
        seduta_ids = list(range(args.to_seduta, args.from_seduta - 1, -1))  # dal più recente
        adapter = CameraSpeechesAdapter(
            use_fixtures=False, legislature=args.legislature, seduta_ids=seduta_ids
        )
        print(f"Storico esteso: sedute {args.from_seduta}–{args.to_seduta} ({len(seduta_ids)} sedute)")
    else:
        adapter = CameraSpeechesAdapter(
            use_fixtures=False, legislature=args.legislature, max_sedute=args.sedute
        )
    docs = adapter.fetch_documents()
    interventions = adapter.fetch_interventions()

    by_doc = defaultdict(list)
    for i in interventions:
        by_doc[i.document_id].append(i)

    written = 0
    for doc in docs:
        ints = by_doc.get(doc.id, [])[: args.max_int_per_seduta]
        if not ints:
            continue
        record = {
            "document": {
                "id": doc.id,
                "source": doc.source,
                "chamber": doc.chamber.value,
                "legislature": doc.legislature,
                "source_type": doc.source_type.value,
                "document_type": doc.document_type,
                "date": doc.date.isoformat(),
                "title": doc.title,
                "url": doc.url,
                "raw_text": "",
                "metadata": doc.metadata,
            },
            "interventions": [
                {
                    "politician_id": i.politician_id,
                    "politician_name": i.politician_name,
                    "date": i.date.isoformat(),
                    "context": i.context,
                    "source_type": i.source_type.value,
                    "text": i.text,
                    "source_url": i.source_url,
                    "metadata": i.metadata,
                }
                for i in ints
            ],
        }
        path = out_dir / f"speeches_{doc.metadata.get('seduta', doc.id)}.json"
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  scritto {path.name}: {len(ints)} interventi")
        written += 1

    print(f"Fatto: {written} file fixture in {out_dir}")


if __name__ == "__main__":
    main()
