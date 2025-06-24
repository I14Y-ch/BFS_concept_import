
## 📦 SMS2 Concept Importer

This Python script automates the migration of defined variables (DVs) from the **SMS2** system to the **I14Y** platform. It handles metadata extraction, transformation, user verification, and concept publication.

---

### 🚀 Features

- Fetches DV metadata from SMS2.
- Maps DV data into I14Y-compatible JSON structures.
- Verifies and creates responsible users in I14Y if missing.
- Posts concepts and associated code list entries to I14Y.
- Updates registration status and publication level.

---

### 🛠️ Requirements

- Python 3.7+
- `.env` file with the following variables:

```
SMS2_token=your_sms2_api_token
I14Y_token=your_i14y_api_token
```

- Required Python packages:

```
pip install requests python-dotenv
```

### ⚙️ Usage

1. Set environment variables in .env.
2. Edit the script to set the desired dv_id and I14Y_environment:

```
dv_id = "your_defined_variable_id"
I14Y_environment = "DEV"  # or "REF", "ABN", "PROD"
```

3. Run the script:

```
python "SMS2_concept_importer 5.py"
```

### 📌 Notes
- The script disables SSL verification (verify=False) for API calls. Use with caution in production.
- Ensure the output directory exists or is created before running the script.
- The script currently uses a hardcoded organization identifier for BFS — update this as needed.

### 🧑‍💻 Author
Developed for internal use by BFS (Swiss Federal Statistical Office) to streamline DV migration to I14Y.