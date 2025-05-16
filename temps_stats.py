import requests
import datetime
import statistics
import json

# Configuració de la localitat 
LATITUDE = 41.3851   # Exemple: Barcelona
LONGITUDE = 2.1734

# Obtenir data actual
today = datetime.date.today()
# Format YYYY-MM-DD per l'API i YYYYMMDD per al nom de fitxer
date_str = today.isoformat()
filename_date = today.strftime("%Y%m%d")

# Cridar l'API d'Open-Meteo per a temperatures horàries
url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    f"&hourly=temperature_2m"
    f"&start_date={date_str}&end_date={date_str}"
    f"&timezone=UTC"
)
response = requests.get(url)
response.raise_for_status()
data = response.json()

# Extreure la llista de temperatures per a avui
temps = data.get('hourly', {}).get('temperature_2m', [])
if not temps:
    raise RuntimeError("No s'han trobat dades de temperatura per avui.")

# Càlculs
temp_max = max(temps)
temp_min = min(temps)
temp_mean = statistics.mean(temps)

# Preparar resultat
temp_stats = {
    'date': date_str,
    'location': {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
    },
    'temperature': {
        'max': temp_max,
        'min': temp_min,
        'mean': round(temp_mean, 2)
    }
}

# Escriure JSON
output_filename = f"temp_{filename_date}.json"
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(temp_stats, f, ensure_ascii=False, indent=2)

# Mostrar resultats per pantalla 
print("\nResum de temperatures:\n")
print(f"Data: {temp_stats['date']}")
print(f"Ubicació: lat {temp_stats['location']['latitude']}, lon {temp_stats['location']['longitude']}")
print("Temperatures (°C):")
print(f"  Màxima: {temp_stats['temperature']['max']}")
print(f"  Mínima: {temp_stats['temperature']['min']}")
print(f"  Mitjana: {temp_stats['temperature']['mean']:.2f}\n")
print(f"Resultats també guardats a {output_filename}")