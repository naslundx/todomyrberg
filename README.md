# TodoMyrberg

Detta är en att göra-app framförallt för återkommande sysslor inom familjen. Enkelt gränssnitt, minimalt med hinder och designat mobil-först!

## Teknologi
- **Backend:** Python med Flask, SQLAlchemy för databasen.
- **Databas:** PostgreSQL (Körs i Docker).
- **Frontend:** Vue 3, TypeScript, och Tailwind CSS v4. Byggs och serveras via Vite/Flask.
- **Infrastruktur:** Docker Compose för enkel lokal testning och deployment.

## Kom igång för utveckling

Du behöver Docker installerat på din maskin.

1. Ta bort databas-volymen om du har en gammal liggandes, så databasen byggs upp ren:
   ```bash
   docker compose down -v
   ```
2. Starta systemet:
   ```bash
   docker compose up -d --build
   ```
3. Initiera databasen och skapa lite exempelanvändare/sysslor (Körs **en** gång):
   ```bash
   docker compose exec backend uv run python setup_database.py
   ```
4. Besök `http://localhost:5050` i webbläsaren!
   *Logga in med "Marcus" eller "Vida". Inloggningen ignorerar stora/små bokstäver.*

## Deployment (t.ex. på en Raspberry Pi)
Appen är containeriserad för att lätt kunna sättas upp vart som helst.

1. Klona projektet till din Raspberry Pi.
2. Säkerställ att du har Docker installerat.
3. Kör `docker compose up -d --build`.
4. Kör databas-setupen `docker compose exec backend uv run python setup_database.py`.
5. Databasen sparas permanent i en Docker-volym (`postgres_data`), så sysslorna finns kvar även om du startar om din enhet.

## Setup

```sh
cp todomyrberg.service /etc/systemd/system/
sudo systemctl enable todomyrberg.service
sudo systemctl start todomyrberg.service
sudo systemctl status todomyrberg.service
```
