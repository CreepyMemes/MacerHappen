### Development Workflow

This section is about the development workflow in programming and testing the application on local machine.

> [!TIP]
> If you want to run **VSCode** inside the backend container.
> When you open the project `backend` or `frontend` foldlers in **VSCode**,
> it shoullt automaticaly detect the `.devcontainer` configurations.
>
> If it doesn't detect it or you ignore the notification you can:
> Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
> Select `Remote-Containers: Reopen in Container`.

#### Clone the repository

If the repository is public:

```bash
git clone https://github.com/CreepyMemes/MacerHappen.git
cd MacerHappen/
```

If the repository is private:

> [!IMPORTANT]
> Change **TOKEN** to your github token

```bash
git clone https://CreepyMemes:TOKEN@github.com/CreepyMemes/MacerHappen.git
cd MacerHappen
```

#### Build and launch all containers

```bash
docker compose -f docker-compose.dev.yml --env-file .env.dev up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)

#### (Optional) Reset dev environment

```bash
docker compose -f docker-compose.dev.yml down --volumes --remove-orphans
```

## Development Guide

### Backend (Django)

The Django dev server reloads automatically on code changes.

> [!IMPORTANT]
> Run the following commands _inside_ the container.
> by running the following command:
>
> ```bash
> docker compose -f docker-compose.dev.yml --env-file .env.dev exec -it backend sh
> ```

#### Configuration

Create a new `.env` file in root directory, and enter your credentials there, follow the example at `.env.example`:

```sh
# Django config
SECRET_KEY=your-super-secret-key-here
DJANGO_ALLOWED_HOSTS=*
DJANGO_SETTINGS_MODULE=config.settings.dev # change .dev or .prod

# Database config
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword

# Email config
EMAIL_HOST='smtp.server.com'
EMAIL_PORT=587
EMAIL_HOST_USER='your.stmp@email.com'
EMAIL_HOST_PASSWORD='your stmp pass here'

# External LLM API Key
OPENROUTER_API_KEY=sk-or-v1-your-key-goes-here
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

#### Dependencies

To install new dependencies, for either base, prod or dev:

```bash
pip install <package>
pip freeze > requirements/base.txt
pip freeze > requirements/dev.txt
pip freeze > requirements/prod.txt
```

#### Migrations

To migrate database:

```bash
python manage.py migrate
```

#### SuperUser

To create an admin user:

```bash
python manage.py createsuperuser
```

#### Create mockup data through scripts

```bash
python manage.py create_events
```

#### Run tests

To simply run all tests:

```bash
python manage.py test api
```

To check test coverage, we use `coverage` package that highlights which part of the codebase are being tested:

```bash
coverage run --source="." manage.py test api
coverage html
```

#### Model diagram

To generate a models diagram, we use `django-extensions` package that includes a diagram generator for all the implemented models found in the project, to use:

```bash
python manage.py graph_models -a -o models_diagram.png
```

### Frontend (React + Vite)

Vite provides automatic hot-reloading when frontend files are modified.

> [!IMPORTANT]
> Run the following commands _inside_ the container.
> by running the following command:
>
> ```bash
> docker compose -f docker-compose.dev.yml --env-file .env.dev exec -it frontend sh
> ```

#### Dependencies

To install new dependencies, for either prod or dev:

```bash
npm install <package> --save-dev
npm install <package>
```

#### Run tests

[TODO]

## Production Workflow

### Deployment

The deployment process is **fully automated** via [GitHub Actions](https://github.com/features/actions). The CI/CD pipeline is triggered by every **Pull Request**:

#### CI/CD Workflow Overview

```mermaid
flowchart TD
    PR(🔀 Pull Request)
    Tests{{🧪 Runs Tests}}
    Passed([✅ Able to Merge])
    Failed([❌ Cannot Merge])
    Deployment(🚀 Runs Deployment)
    PR --> Tests
    Tests -- Passed --> Passed
    Tests -- Failed --> Failed
    Passed -- Merge --> Deployment
```

1. **Build & Test:**  
   All pull requests trigger automated builds and tests in a production-like Docker environment.
2. **Merge & Deploy Automatically:**  
   If tests pass, the pull request can be merged.  
   Once merged, the code is automatically deployed to the server via SSH.

- Environment variables are provided securely with GitHub Secrets.
- Deployments use a custom `deploy.sh` script for zero downtime.
