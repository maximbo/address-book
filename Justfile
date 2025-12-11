dev:
  hivemind Procfile.dev

dev-docker:
  docker compose -f deploy/compose-dev.yaml up --watch --build
