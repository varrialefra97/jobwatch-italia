# JobWatch Italia

Sito statico caricabile su GitHub Pages che mostra offerte di lavoro provenienti dai siti ufficiali di aziende che operano in Italia.

Focus iniziale:

- marketing;
- comunicazione;
- social media;
- digital;
- content;
- posizioni junior/stage/neolaureati;
- offerte compatibili con laurea triennale.

## Come funziona

- Il sito è statico: `index.html`, `static/app.js`, `static/style.css`.
- Le offerte sono salvate in `data/jobs.json`.
- Lo scraper Python legge `sources.yaml`.
- GitHub Actions esegue lo scraper ogni 6 ore e aggiorna automaticamente `data/jobs.json`.
- La candidatura avviene sempre sul sito ufficiale dell'azienda.

## Come caricarlo su GitHub

1. Crea un nuovo repository su GitHub, per esempio `jobwatch-italia`.
2. Carica tutti i file di questa cartella nel repository.
3. Vai su **Settings → Pages**.
4. In **Build and deployment**, scegli:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
5. Salva.
6. Dopo qualche minuto il sito sarà online su un link simile a:

```text
https://TUO-USERNAME.github.io/jobwatch-italia/
```

## Attivare l'aggiornamento ogni 6 ore

Il file `.github/workflows/update-jobs.yml` è già configurato.

Per il primo aggiornamento manuale:

1. Vai nella scheda **Actions** del repository.
2. Apri **Aggiorna offerte lavoro**.
3. Clicca **Run workflow**.

Poi GitHub lo eseguirà automaticamente ogni 6 ore.

## Aggiungere aziende

Modifica `sources.yaml`.

### Fonte HTML semplice

```yaml
sources:
  - company: Nome Azienda
    type: html
    url: https://azienda.it/lavora-con-noi
    country: Italy
```

### Fonte Greenhouse

```yaml
sources:
  - company: Nome Azienda
    type: greenhouse
    board_token: slugazienda
    country: Italy
```

### Fonte Lever

```yaml
sources:
  - company: Nome Azienda
    type: lever
    lever_slug: slugazienda
    country: Italy
```

## Test locale

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/scrape_jobs.py
python -m http.server 8000
```

Poi apri:

```text
http://localhost:8000
```

## Nota importante

Questo è un MVP. Alcuni siti aziendali usano Workday, SAP SuccessFactors, Taleo o sistemi custom difficili da leggere con uno scraper generico. Per quei siti conviene creare connettori specifici.
