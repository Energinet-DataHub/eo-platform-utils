from src.origin.sql import SqlEngine


db = SqlEngine(
    uri='',  # Patched by tests
    pool_size=1,
)
