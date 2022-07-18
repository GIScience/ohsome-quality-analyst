# Production Database

```bash
docker build -t oqt-database .
docker run -e POSTGRES_PASSWORD=oqt -e POSTGRES_USER=oqt -p 5432:5432 oqt-database
```
