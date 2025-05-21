# Streamlit_Course_Planner

Run the streamlit Application:
```
streamlit run frontend/recommendation_ui.py
```

Run using uvicorn:
```
uvicorn main:app --reload
```
## Tests


```
pytest backend/tests/ --cov=backend/

```
Each test for unit, integration and e2e:
```
pytest tests/unit/            # Unit tests only
pytest tests/integration/     # Integration tests
pytest tests/e2e/             # End-to-end tests
```


