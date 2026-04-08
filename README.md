# Library System CLI

A Python console application designed to streamline the management of library book loans and inventory. It provides an efficient, memory-based system to handle book records, student interactions, and loan lifecycles.

---

## Table of Contents

- [Installation](#installation)
  - [Requirements](#requirements)
  - [Install Dependencies](#install-dependencies)
- [Run Locally](#run-locally)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

### Requirements

- [Python](https://www.python.org/downloads/) >= 3.13.9

---

### Install Dependencies

Install [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

From the **repo root**:

```bash
uv sync
```

> **VS Code:** open the Command Palette (`Ctrl+Shift+P`), run **Python: Select Interpreter**, and choose the `.venv` created by `uv`. Reload your terminal afterwards.

---

## Run Locally

From the **repo root**:

```Bash
uv run python frontend/main.py
```

Use `Ctrl+C` to exit the application at any time.

---

## Project Structure

The project follows a clean structure to separate the business rules from the user interface:

- `backend/domain/`: Contains the core data models (`Book`, `Student`, `Loan`) and Enums.
- `backend/services/`: Contains the business logic for managing books and loans.
- `backend/repository/`: Handles data storage.
- `frontend/`: Contains the CLI menus and user interaction logic.
- `data/`: Directory where persistent files are stored.

---

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a feature branch: `feat/my-change`.
3. Make your changes, ensuring they follow the existing code style.
4. Include appropriate documentation or tests.
5. Commit, push, and open a pull request describing the change and the reason for it.

### Pre-commit Hooks <!-- omit in toc -->

This project uses [pre-commit](https://pre-commit.com/) to enforce code quality automatically before each commit. Run the following once from the **repo root** to set it up:

```bash
pip install pre-commit
pre-commit install
```

After that, checks will run automatically on every `git commit`. To run them manually across all files:

```bash
pre-commit run --all-files
```

---

## License

This project is available under the **MIT License**.
