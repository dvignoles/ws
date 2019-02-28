# ASRC Weather Station Website

### Getting Started

To start the application run:

```
export FLASK_APP=run.py
export DEV_URI=sqlite:////home/ws.sqlite
export PROD_URI=mysql://user@localhost/foo
flask run
```

replace `DEV_URI` & `PROD_URI` with appropriate SQLAlchemy connection strings

---

### Production / Development
To switch between Development/Production edit `__init__.py`:

```
app.config.from_object('config.DevelopmentConfig')
```

change to:

```
app.config.from_object('config.ProductionConfig')
```