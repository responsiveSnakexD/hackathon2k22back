# 2k22 hackathon back-end

## Requirements

- Python 3.11+
- Pipenv 2022.11.11+

## Installation

First make sure you have Python 3.11+ installed:

```
python3 --version
```

Then install latest pipenv package (you might need to run the following command as admin/sudo):

```
pip3 install pipenv
```

After it's installed 'cd' into the project directory and run:

```
pipenv shell
```

This will initialize the environment

## Running the project

Activate the virtual environment:

```
pipenv shell
```

To start the server run:

```
python3 manage.py runserver
```

## Setting up the environment

### Visual Studio Code

- Make sure you have PipEnv selected as your default environment (CTRL+SHIFT+P > Python: Select Interpreter)

- Install Python Extension Pack and Pylance

## Installing additional packages

Activate the environment:

```
pipenv shell
```

```
pipenv install <package_name>
```

## License

This project is licensed under the MIT License.

Please refer to the [LICENSE](LICENSE) file for more details.
