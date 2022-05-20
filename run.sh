rm -f /app/pytest.ini
rm -rf /app/tests

cp pytest.ini /app/pytest.ini
cp -a tests/ /app/tests

cd /app
pip3 install -r requirements.txt
pytest --tb=line 1>&2
