# scripts 

plpgsql scripts for use with uploading into a bema deployment. 



## sql-migrate 

For local testing install and use `sql-migrate`: https://github.com/golang-migrate/migrate

do a one time setup with docker compose and use `migrate` command: 

```bash
export PG_URI='postgres://postgres:postgres@localhost:5454/meteodb?sslmode=disable'
migrate -path migrations -database $PG_URI up
```

I have these hidden from public for now...