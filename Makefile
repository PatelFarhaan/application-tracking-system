.PHONY: install run setup-db setup-admin clean

install:
	cd "DB-Application directory" && pip install -r requirements.txt

run:
	cd "DB-Application directory" && python app.py

setup-db:
	@echo "Run the following SQL scripts against your MySQL server:"
	@echo "  mysql -u root -p < SQL/Create_db_and_tables.sql"
	@echo "  mysql -u root -p ats < SQL/Create_sample_data.sql"
	@echo "  mysql -u root -p ats < SQL/Create_sp.sql"
	@echo "  mysql -u root -p ats < SQL/Create_views.sql"
	@echo "  mysql -u root -p ats < SQL/Create_audit_tables.sql"
	@echo "  mysql -u root -p ats < SQL/Create_audit_triggers.sql"

setup-admin:
	cd "DB-Application directory" && python project/admin/create_admin.py

test:
	@echo "No automated tests configured yet."

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name migrations -exec rm -rf {} + 2>/dev/null || true
