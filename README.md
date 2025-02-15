# aigamegenerator

## Initial Setup

### Environment Files
Create your `.env.prod` file by copying `.env.example` and filling in the required values.

### Running Docker
To build and start all services in detached mode, run:

```bash
docker compose up -d
```

If you need to rebuild every service (e.g., after making changes to the code or Dockerfiles), run:

```bash
docker compose up -d --build
```

To stop the containers, use:
```bash
docker compose down
```