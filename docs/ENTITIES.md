# Entity Extraction Rules

## Entity Types

### Animal
Fields:
- `name`: Animal's name
- `species`: Animal's species
- `id`: Animal's database ID

Example phrases:
- "жираф Жужа"
- "слон Dima"
- "медведь Sonya"

### Behavior
Fields:
- `type`: Type of behavior
- `intensity`: Intensity level
- `duration_sec`: Duration in seconds

Example phrases:
- "спокойное поведение"
- "игривое поведение"
- "агрессивное поведение"

### Vitals
Fields:
- `temperature_c`: Temperature in Celsius
- `weight_kg`: Weight in kilograms

Validators:
- `temperature_c`: >= 25 & <= 45
- `weight_kg`: >= 0.1 & <= 10000

Example phrases:
- "температура 37.8"
- "температура тела 36.5"
- "вес 850 кг"
- "масса 850 кг"

### Feeding
Fields:
- `food`: Type of food
- `amount_g`: Amount in grams
- `time`: Feeding time

Example phrases:
- "ела 700 грамм люцерны"
- "съел 5 кг мяса"
- "потребил 2.5 кг рыбы"

### Relations
Fields:
- `animal_id`: Related animal's ID
- `relation_type`: Type of relation

Example phrases:
- "вместе с слоном Dima"
- "играет с медведем Sonya"

### Location
Fields:
- `enclosure`: Enclosure identifier
- `zone`: Zone identifier

Example phrases:
- "вольер 12"
- "зона C"

### Alert
Fields:
- `severity`: Alert severity (low, medium, high)
- `message`: Alert message

Example phrases:
- "повышенная температура"
- "резкое снижение веса"
- "агрессивное поведение"

## Regex Rules

### Temperature
Pattern: `(?i)(температура|температура тела)\s*(\d+[,\.]?\d*)\s*(°?[cс])`
Examples:
- "температура 37.8"
- "температура тела 36.5°C"

### Weight
Pattern: `(?i)(вес|масса)\s*(\d+[,\.]?\d*)\s*(кг|kg)`
Examples:
- "вес 850 кг"
- "масса 850kg"

### Food Amount
Pattern: `(?i)(\d+[,\.]?\d*)\s*(грамм|г|kg|кг)`
Examples:
- "700 грамм"
- "5 кг"

### Date
Pattern: `(?i)(\d{1,2}[.\-]\d{1,2}[.\-]\d{4}|\d{1,2}[.\-]\d{1,2})`
Examples:
- "30.08.2025"
- "30-08-2025"
- "30.08"
- "30-08"

## Normalization Rules

### Species Mapping
- "жираф" → "giraffe"
- "слон" → "elephant"
- "лев" → "lion"
- "тигр" → "tiger"
- "медведь" → "bear"
- "волк" → "wolf"
- "лиса" → "fox"

### Food Mapping
- "люцерна" → "alfalfa"
- "сено" → "hay"
- "мясо" → "meat"
- "рыба" → "fish"
- "фрукты" → "fruits"
- "овощи" → "vegetables"

### Behavior Mapping
- "спокойное" → "calm"
- "агрессивное" → "aggressive"
- "игривое" → "playful"
- "вялое" → "lethargic"