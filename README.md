# Sheets

Quick and dirty script to convert google sheets to [SankeyMATIC](https://sankeymatic.com/) text format. Currently **only supports 2 levels**.

# Setup

Follow [Google Sheet API Quick Start](https://developers.google.com/sheets/api/quickstart/python) to create your `credentials.json`

```bash
virtualenv --python=python3.10 .budgetenv
```

Activate virtual environment

```bash
source .budgetenv/bin/activate
```

Install Dependencies

```bash
pip3 install -r requirements.txt
```

Make a copy of environment variables

```bash
cp .env.example .env
```

Run the script!

```bash
python3 exec.py
```