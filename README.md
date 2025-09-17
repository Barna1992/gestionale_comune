# Gestionale Comune

Un sistema di gestione delle segnalazioni e problematiche per comuni italiani, sviluppato con Django.

## Caratteristiche Principali

### 🎯 Gestione Segnalazioni (Issues)
- **Creazione e tracking** di segnalazioni/problemi
- **Sistema di priorità** (Bassa, Media, Alta)
- **Stati personalizzabili** (Inserita, Presa in carico, Risolta, Riaperta, Da verificare)
- **Assegnazione multipla** con possibilità di assegnare a tutti gli utenti
- **Sistema CC** per coinvolgere utenti aggiuntivi
- **Commenti** per ogni segnalazione
- **Date di scadenza** per il monitoraggio dei tempi

### 👥 Sistema di Autenticazione
- **Registrazione utenti** con approvazione automatica
- **Login/Logout** sicuro
- **Reset password** via email
- **Cambio password** per utenti autenticati
- **Controllo accessi** basato sui ruoli

### 🔐 Sistema di Permessi
- **Superuser**: accesso completo a tutte le segnalazioni
- **Utenti standard**: accesso limitato alle segnalazioni assegnate o in CC
- **Visualizzazioni personalizzate** in base al ruolo

### 📊 Dashboard e Filtri
- **Contatori**: nuove segnalazioni, totale utenti
- **Ordinamento** per assignee, priorità, stato, data
- **Filtri avanzati** per gestire grandi volumi di dati

## Requisiti Tecnici

### Versioni Software
- **Python**: 3.10+
- **Django**: 5.1.1
- **Database**: SQLite (sviluppo) / PostgreSQL (produzione)

### Dipendenze
```txt
django==5.1.1
pytz==2024.2
sqlparse==0.5.1
psycopg2-binary==2.9.9
```

## Installazione

### 1. Clona il Repository
```bash
git clone <repository-url>
cd gestionale_comune
```

### 2. Crea Ambiente Virtuale
```bash
python -m venv env
source env/bin/activate  # Su Linux/Mac
# oppure
env\Scripts\activate     # Su Windows
```

### 3. Installa le Dipendenze
```bash
pip install -r requirements.txt
```

### 4. Configurazione Database

#### Opzione A: SQLite (Consigliato per sviluppo)
Il progetto è già configurato per utilizzare SQLite. Non serve configurazione aggiuntiva.

#### Opzione B: PostgreSQL (Per produzione)
1. Crea il file `config.ini`:
```ini
[database]
name = gestionale
user = your_db_user
password = your_password
host = localhost
port = 5432
```

2. Modifica `settings.py` commentando la configurazione SQLite e decommentando quella PostgreSQL.

### 5. Esegui le Migrazioni
```bash
python manage.py migrate
```

### 6. Crea Superuser
```bash
python manage.py createsuperuser
```

### 7. Avvia il Server
```bash
python manage.py runserver
```

Il sito sarà disponibile su `http://127.0.0.1:8000`

## Struttura del Progetto

```
gestionale_comune/
├── gestione_comune/        # Configurazione principale Django
│   ├── settings.py         # Impostazioni progetto
│   ├── urls.py            # URL routing principale
│   └── wsgi.py            # WSGI configuration
├── issue/                 # App gestione segnalazioni
│   ├── models.py          # Modelli Issue e Comment
│   ├── views.py           # Viste per CRUD segnalazioni
│   ├── forms.py           # Form per creazione/modifica
│   ├── urls.py            # URL routing segnalazioni
│   └── templates/         # Template HTML
├── registration/          # App autenticazione utenti
│   ├── views.py           # Viste registrazione
│   ├── urls.py            # URL routing autenticazione
│   └── templates/         # Template login/registrazione
├── requirements.txt       # Dipendenze Python
├── manage.py             # Django management script
└── config.ini            # Configurazione database (opzionale)
```

## Utilizzo

### 1. Accesso al Sistema
- Vai su `http://127.0.0.1:8000`
- Effettua il login o registrati come nuovo utente
- Gli utenti normali vedranno solo le segnalazioni assegnate a loro

### 2. Gestione Segnalazioni
- **Nuova segnalazione**: `/issue/new/`
- **Lista segnalazioni**: `/issue/`
- **Dettaglio segnalazione**: `/issue/<id>/`
- **Modifica**: `/issue/<id>/edit/`
- **Cambio stato**: `/issue/<id>/edit-state/`

### 3. Funzionalità Avanzate
- **Ordinamento**: Clicca sui link nella lista per ordinare
- **Commenti**: Aggiungi commenti dal dettaglio segnalazione
- **Assegnazione multipla**: Seleziona più utenti o "Tutti"
- **Sistema CC**: Coinvolgi utenti aggiuntivi senza assegnazione diretta

## Modelli Dati

### Issue (Segnalazione)
- `title`: Titolo della segnalazione
- `description`: Descrizione dettagliata
- `assignee`: Utenti assegnati (ManyToMany)
- `cc`: Utenti in copia (ManyToMany)
- `owner`: Creatore della segnalazione
- `state`: Stato (Inserita, Presa in carico, etc.)
- `priority`: Priorità (Bassa, Media, Alta)
- `expired_date`: Data di scadenza
- `date`: Data di creazione (auto)

### Comment (Commento)
- `post`: Segnalazione di riferimento
- `name`: Autore del commento
- `body`: Testo del commento
- `created_on`: Data di creazione
- `active`: Flag attivazione

## Configurazione Avanzata

### Impostazioni di Sicurezza (Produzione)
Nel file `settings.py`, per la produzione modifica:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = 'your-secret-key'

# Aggiungi impostazioni SSL se necessario
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### File Statici
```bash
python manage.py collectstatic
```

### Localizzazione
Il progetto è configurato per l'italiano:
- Timezone: `Europe/Rome`
- Formato date: `%d/%m/%Y`
- Traduzioni: Interfaccia in italiano

## Troubleshooting

### Errore Database PostgreSQL
Se riscontri errori di autenticazione PostgreSQL:
1. Verifica che PostgreSQL sia in esecuzione
2. Controlla le credenziali in `config.ini`
3. Usa SQLite per sviluppo locale

### Errori di Migrazione
```bash
python manage.py makemigrations
python manage.py migrate
```

### Problemi con File Statici
```bash
python manage.py collectstatic --clear
```

## Contributi

Per contribuire al progetto:
1. Fork del repository
2. Crea un branch per la tua feature
3. Commit delle modifiche
4. Apri una Pull Request

## Licenza

Questo progetto è sviluppato per uso interno comunale. Contatta l'amministratore per informazioni sulla licenza.

## Supporto

Per supporto tecnico o segnalazione bug, contatta l'amministratore di sistema.