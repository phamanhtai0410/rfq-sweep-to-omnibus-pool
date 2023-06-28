# Sweep to omnibus pool

## 1. Create a list of vault account

- Create a list of intermediate vault account and one treasury account (Omnibus Deposits account)
- Run:
  `python create_vault_accounts_in_batch.py`

## 2. Run interval jobs:

### 2.1 Job

#### 2.1.1 Env

```
SITE_DOMAIN=127.0.0.1
SECURE_COOKIES=false
ENVIRONMENT=LOCAL
CORS_HEADERS=["*"]
CORS_ORIGINS=["http://localhost:3000"]
DATABASE_URL=mysql+asyncmy://root:H@dentail123@localhost:3306/test
FIREBLOCK_API_KEY=c9bf54cf-d5f6-4240-a762-4020e888c3fb
FIREBLOCK_API_URL=https://sandbox-api.fireblocks.io
ASSET_LIST=["ETH_TEST3"]
TREASURY_ID=74
MIN_SWEEPING_THRESHOLD=0.05
SWEEP_INTERVAL=86400
```

### 2.1.2 Run

`bash scripts/start-dev.sh`

### 2.2 Admin

`http://localhost:8000/admin`
