## Google Spreadsheet API
1. rename google_spreadsheet_url_template.yaml to google_spreadsheet_url.yaml
2. Place the "LGBTQ+ News Articles.xlsx" our google drive
3. Open it and copy the url and paste in google_spreadsheet_url.yaml
4. apply for api access to google spreadsheet at:
https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com
5. rename config_template.json to config.json
6. replace value with your credentials
8. Fill in your google spreadsheet url

## Installation
```bash
python -m venv venv
pip install -r requirements.tx
```

## Usage

```python
python main.py

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
