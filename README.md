# Yet Another Book Log

<!-- MarkdownTOC autolink="true" -->

- [To install all dev dependencies](#to-install-all-dev-dependencies)
- [To launch the app](#to-launch-the-app)
- [To test the project](#to-test-the-project)

<!-- /MarkdownTOC -->


## To install all dev dependencies

NB: this project uses [pip-tools](https://github.com/jazzband/pip-tools), do not manualy update the requirements.txt file.

Create a virtual environment and run:
```bash
pip install pip-tools
make update_dep
```

## To launch the app

In your virtual environment, run:
```bash
make run
```

## To test the project

In your virtual environment, run:
```bash
make tests
```
