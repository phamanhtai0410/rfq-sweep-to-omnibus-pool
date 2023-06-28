__import__('os').environ['TZ'] = 'UTC'

import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from datetime import date
from src.config import settings
from fastapi_scheduler import SchedulerAdmin
from starlette.middleware.cors import CORSMiddleware

from src import redis
from src.config import app_configs, settings
from src.database import database
from src.jobs import sweep_accounts

app = FastAPI(**app_configs)

# Create `AdminSite` instance
site = AdminSite(settings=Settings(database_url_async=settings.DATABASE_URL))

# Create an instance of the scheduled task scheduler `SchedulerAdmin`
scheduler = SchedulerAdmin.bind(site)

# Add scheduled tasks, refer to the official documentation: https://apscheduler.readthedocs.io/en/master/
# use when you want to run the job at fixed intervals of time
@scheduler.scheduled_job('interval', seconds=settings.SWEEP_INTERVAL)
def sweep_to_treasury_vault_account():
    _sweep_data = sweep_accounts()
    print('Sweep to treasury vault account - interval task is running...')
    print(f'Sweep data {_sweep_data}')


# # use when you want to run the job periodically at certain time(s) of day
# @scheduler.scheduled_job('cron', hour=3, minute=30)
# def cron_task_test():
#     print('cron task is run...')


# # use when you want to run the job just once at a certain point of time
# @scheduler.scheduled_job('date', run_date=date(2022, 11, 11))
# def date_task_test():
#     print('date task is run...')


@app.on_event("startup")
async def startup():
    # Mount the background management system
    site.mount_app(app)
    # Start the scheduled task scheduler
    scheduler.start()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, debug=True)
    
    
@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

