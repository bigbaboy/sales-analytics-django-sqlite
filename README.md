# Sales Analytics with Django, SQLite & D3.js

An academic web application that moves sales records from a CSV file into relational models, calculates analytical views with Django ORM and renders visualizations using D3.js.

## Questions explored

- Which products and product groups generate the most revenue?
- How does revenue vary by month, weekday, day of month and hour?
- How often do product groups appear in orders?
- How are customer purchases distributed?

This repository emphasizes the path from **data modeling to query logic to presentation**, making it useful for discussing both data analysis and software requirements.

## Architecture

| Layer | Implementation |
| --- | --- |
| Source | `data_ggsheet.csv` with Vietnamese column names |
| Data model | Customer, ProductGroup, Product, Order and OrderDetail in `d3app/models.py` |
| Import | POST handler in `d3app/views.py` |
| Analysis | Django ORM aggregation and date extraction |
| Interface | `templates/visualization.html` with D3.js |
| Storage | SQLite |

See [Data model](docs/data-model.md).

## Local setup

```bash
git clone https://github.com/bigbaboy/221124029109-LeMinhDat-48K29.1.git
cd 221124029109-LeMinhDat-48K29.1
python -m venv .venv
```

Activate `.venv`. The checked-in `requirements.txt` is a broad environment export that includes packages unrelated to this app and Windows-specific dependencies. For a focused local demo, the inspected application imports Django and Python's standard library:

```bash
python -m pip install "Django==5.1.7"
python manage.py migrate
python manage.py runserver
```

This matches the Django version in the existing dependency list; a clean runtime installation was not executed for this documentation update.

Open `http://127.0.0.1:8000/d3app/`. The repository includes `db.sqlite3`; inspect the existing data before importing again.

## CSV import

The importer reads the local `data_ggsheet.csv`; it is not a file-upload form. The endpoint is **POST `/d3app/import/`**.

For a fresh empty demo database only:

```bash
curl -X POST http://127.0.0.1:8000/d3app/import/
```

On Windows PowerShell, use `curl.exe` if `curl` resolves to a PowerShell alias.

**Do not repeat the import on the same data:** an existing order/product pair has its quantity incremented, so a second import can double-count quantities. Back up `db.sqlite3` before data changes.

The source schema includes `Thời gian tạo đơn`, `Mã đơn hàng`, `Mã khách hàng`, `Mã PKKH`, `Mã nhóm hàng`, `Mã mặt hàng`, `Đơn giá` and `SL`. The importer expects timestamps in `%Y-%m-%d %H:%M:%S` format and strips commas from unit prices.

## Current limitations

- The importer is not idempotent and does not batch the whole load into one transaction.
- Repeated order/product lines are combined; the model does not preserve every original line separately.
- Invalid numeric fields may be replaced by defaults instead of reported as validation errors.
- The import endpoint is CSRF-exempt and intended only for a controlled local demonstration.
- Some aggregations group by month number; multi-year data needs year-aware grouping.
- No measured performance benchmark or business impact is claimed.

## Related implementations

[Standalone chart pages](https://github.com/bigbaboy/LeMinhDat), [chart navigation](https://github.com/bigbaboy/LeminhDat48291) and the [CSV-backed team dashboard](https://github.com/bigbaboy/GroupDV118) explore related sales-analysis tasks. They are different implementations, not separate commercial deployments.
