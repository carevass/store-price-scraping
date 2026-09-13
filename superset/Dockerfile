FROM apache/superset:latest

USER root

RUN . /app/.venv/bin/activate && uv pip install \
     psycopg2-binary \
   # package needed for using single-sign on authentication:
   Authlib \
   # openpyxl to be able to upload Excel files
   openpyxl \
   # Pillow for Alerts & Reports to generate PDFs of dashboards
   Pillow 
   # install Playwright for taking screenshots for Alerts & Reports. This assumes the feature flag PLAYWRIGHT_REPORTS_AND_THUMBNAILS is enabled
   # That feature flag will default to True starting in 6.0.0
   # Playwright works only with Chrome.
   # If you are still using Selenium instead of Playwright, you would instead install here the selenium package and a headless browser & webdriver
   #playwright \
   #&& playwright install-deps \
   #&& PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/playwright-browsers playwright install chromium
USER superset

ENTRYPOINT ["sh", "-c", "superset db upgrade && superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin && superset init && superset run -p 8088 -h 0.0.0.0 --with-threads --reload"]
