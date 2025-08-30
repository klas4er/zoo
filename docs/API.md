# API Documentation

## Endpoints

### Health Check
`GET /api/health`
Returns the health status of the API.

Response:
```json
{
  "status": "healthy"
}
```

### Process Audio
`POST /api/audio/process`
Process an uploaded WAV file and extract entities.

Parameters:
- `file`: WAV file to process
- `watcher_id`: ID of the zoo keeper (default: 1)
- `animal_id`: ID of the animal (optional)

Response:
```json
{
  "id": "obs_123",
  "status": "done",
  "duration_sec": 47.2,
  "wer": 0.17,
  "text": "Самка жирафа Жужа ела 700 грамм люцерны, температатура 37.8, спокойное поведение",
  "entities": {
    "animal": {"species": "жираф", "name": "Жужа"},
    "feeding": {"food": "люцерна", "amount_g": 700},
    "vitals": {"temperature_c": 37.8},
    "behavior": {"type": "спокойное"}
  },
  "timeline": [
    {"t": 12.4, "type": "feeding", "text": "ела 700 грамм люцерны"},
    {"t": 24.8, "type": "vitals", "text": "температура 37.8"}
  ]
}
```

### List Transcriptions
`GET /api/transcriptions`
Get a list of transcriptions with optional filtering.

Parameters:
- `animal_id`: Filter by animal ID (optional)
- `watcher_id`: Filter by watcher ID (optional)
- `start_date`: Filter by start date (optional)
- `end_date`: Filter by end date (optional)

Response:
```json
[
  {
    "id": "obs_123",
    "status": "done",
    "duration_sec": 47.2,
    "wer": 0.17,
    "text": "Самка жирафа Жужа ела 700 грамм люцерны, температура 37.8, спокойное поведение",
    "entities": {
      "animal": {"species": "жираф", "name": "Жужа"},
      "feeding": {"food": "люцерна", "amount_g": 700},
      "vitals": {"temperature_c": 37.8},
      "behavior": {"type": "спокойное"}
    },
    "timeline": []
  }
]
```

### Get Transcription
`GET /api/transcriptions/{id}`
Get detailed information about a specific transcription.

Response:
```json
{
  "id": "obs_123",
  "status": "done",
  "duration_sec": 47.2,
  "wer": 0.17,
  "text": "Самка жирафа Жужа ела 700 грамм люцерны, температура 37.8, спокойное поведение",
  "entities": {
    "animal": {"species": "жираф", "name": "Жужа"},
    "feeding": {"food": "люцерна", "amount_g": 700},
    "vitals": {"temperature_c": 37.8},
    "behavior": {"type": "спокойное"}
  },
  "timeline": [
    {"t": 12.4, "type": "feeding", "text": "ела 700 грамм люцерны"},
    {"t": 24.8, "type": "vitals", "text": "температура 37.8"}
  ]
}
```

### Configure Entities
`POST /api/entities/config`
Configure entity extraction rules.

Request Body:
```json
{
  "entities": [
    {"name": "animal", "fields": ["name", "species", "id"], "required": ["species"]},
    {"name": "behavior", "fields": ["type", "intensity", "duration_sec"]},
    {"name": "vitals", "fields": ["temperature_c", "weight_kg"], "validators": {"temperature_c": ">= 25 & <= 45"}},
    {"name": "feeding", "fields": ["food", "amount_g", "time"]},
    {"name": "relations", "fields": ["animal_id", "relation_type"]},
    {"name": "location", "fields": ["enclosure", "zone"]},
    {"name": "alert", "fields": ["severity", "message"]}
  ],
  "rules": {
    "dates": "регэкспы/парсеры дат",
    "numbers": "регэкспы для температур/весов/количеств"
  }
}
```

Response:
```json
{
  "entities": [
    {"name": "animal", "fields": ["name", "species", "id"], "required": ["species"]},
    {"name": "behavior", "fields": ["type", "intensity", "duration_sec"]},
    {"name": "vitals", "fields": ["temperature_c", "weight_kg"], "validators": {"temperature_c": ">= 25 & <= 45"}},
    {"name": "feeding", "fields": ["food", "amount_g", "time"]},
    {"name": "relations", "fields": ["animal_id", "relation_type"]},
    {"name": "location", "fields": ["enclosure", "zone"]},
    {"name": "alert", "fields": ["severity", "message"]}
  ],
  "rules": {
    "dates": "регэкспы/парсеры дат",
    "numbers": "регэкспы для температур/весов/количеств"
  }
}
```

### Get Animal Observation Log
`GET /api/animals/{id}/log`
Get observation log for a specific animal.

Response:
```json
[
  {
    "id": "obs_123",
    "status": "done",
    "duration_sec": 47.2,
    "wer": 0.17,
    "text": "Самка жирафа Жужа ела 700 грамм люцерны, температура 37.8, спокойное поведение",
    "entities": {
      "animal": {"species": "жираф", "name": "Жужа"},
      "feeding": {"food": "люцерна", "amount_g": 700},
      "vitals": {"temperature_c": 37.8},
      "behavior": {"type": "спокойное"}
    },
    "timeline": []
  }
]
```

### Get Daily Report
`GET /api/reports/daily`
Get aggregated daily report.

Parameters:
- `date`: Date for the report (optional, defaults to today)

Response:
```json
{
  "date": "2025-08-30",
  "animals": [
    {
      "id": 1,
      "name": "Жужа",
      "species": "жираф",
      "observations": 5,
      "alerts": 0,
      "latest_vitals": {
        "temperature_c": 37.8,
        "weight_kg": 850
      }
    }
  ],
  "summary": {
    "total_observations": 12,
    "critical_alerts": 1,
    "warnings": 3
  }
}
```

### Get Performance Metrics
`GET /api/metrics`
Get performance metrics for the system.

Response:
```json
{
  "processing_time_avg": 45.2,
  "wer_avg": 0.15,
  "entity_extraction_accuracy": 0.82,
  "active_workers": 4,
  "queue_length": 0
}
```

### WebSocket Streaming Endpoint
`GET /ws/transcribe`
Real-time streaming transcription endpoint.

Parameters:
- `lang`: Language code (default: ru)
- `session_id`: Session identifier

WebSocket Events:
```json
{ "event": "partial", "text": "самка жирафа..." }
{ "event": "final", "text": "самка жирафа Жужа...", "segment": {"start": 0.0, "end": 5.2} }
{ "event": "entity_update", "entities": {"animal": {"species": "жираф", "name": "Жужа"}} }
{ "event": "stats", "stats": {"rtf": 0.35, "cpu_load": 0.62} }
{ "event": "error", "message": "Error description" }
```