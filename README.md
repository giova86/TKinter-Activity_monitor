# 🖥️ PC Performance Monitor

Un'app desktop moderna scritta in **Python** che mostra in tempo reale l'utilizzo delle risorse di sistema come CPU, RAM, disco, rete e temperatura. Interfaccia grafica basata su `customtkinter` e grafici generati con `matplotlib`.

![screenshot](https://your-screenshot-url-here.com) <!-- Sostituisci con uno screenshot se disponibile -->

---

## 🚀 Caratteristiche

- ✅ Monitoraggio in tempo reale:
  - Utilizzo CPU globale e per core
  - Utilizzo RAM
  - Lettura/Scrittura su disco
  - Dati rete (inviati/ricevuti)
  - Temperatura CPU (dove supportato)
- 📊 Grafici aggiornati ogni secondo
- 🧠 Supporto multi-core dinamico
- 🌑 Tema scuro moderno
- 🔧 Layout responsivo

---

## 📦 Requisiti

Assicurati di avere Python 3.7+ installato. Poi installa i pacchetti necessari:

```bash
pip install customtkinter matplotlib psutil py-cpuinfo
⚠️ py-cpuinfo è opzionale ma consigliato. Alcune funzionalità di temperatura possono non essere supportate su tutti i sistemi operativi.
🧑‍💻 Avvio del programma

Clona il repository ed esegui il file:

git clone https://github.com/tuo-username/performance-monitor.git
cd performance-monitor
python monitor.py
📁 Struttura del Progetto

performance-monitor/
├── app.py       # Codice principale dell'app
├── README.md        # Questo file
└── requirements.txt # (facoltativo) dipendenze del progetto
📷 Screenshot

Aggiungi qui screenshot o GIF per mostrare l'app in azione

💡 Da migliorare

Supporto completo alle temperature su tutti i sistemi
Grafici più dettagliati per rete e disco
Modalità chiara

🙌 Ringraziamenti

psutil
CustomTkinter
matplotlib
