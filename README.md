# Docker + Django + Poetry
A repository for a university course on Docker, Django and Poetry. \
Witch will later be used to build a project using these tools.

### Usefull commands
```Bash
# For exporting dependecies into a file
sudo poetry export -o ./ci/requirements/kernel-dev-requirements.txt
```
```Bash
# Build the image
sudo docker build -f ./ci//dockerfiles/kernel-dev.Dockerfile .
```
```Bash
# Run the image
sudo docker compose --file ./ci/compose/kernel.yaml up --build
```
