# About

Ospyata is the library with which the Osmata application is written.

## Install

Ospyata is available in PyPI. So, installation is as simple as:

```bash
python3 -m pip install --user ospyata # For per-user installation.
```

The recommended way of installation is through a virtual environment.

```bash
python3 -m pip install opyata
```

Note: Ospyata requires Python version 3.11 or above.

## Usage

### Import

Importing the module is very simple. Just use:

```python
import ospyata.osmata as ospyata

osmata = ospyata.Osmata()
```

### Adding a record

For addition of record, `ospyata` has the `push()` function in the class `Osmata`.

```py
Osmata.push(name, url)
```

Example usage:

```python
osmata.push("example", "https://example.com")
```

### Removing a record

For removal of record, `ospyata` has the `pop()` function in the class `Osmata`.

```py
Osmata.pop(name)
```

Example usage:

```python
osmata.push("example")
```

## Exceptions

The library - `ospyata` - do not deal with errors. `ospyata` do `raise` `Exception`s, but do not deal with internal errors and exceptions but re-raises them for the application developer using `ospyata` to handle. See [Error policy](Error_policy.md) for details.

### `Exceptions` raised and re-raised by `ospyata`

#### Exception raised by the library `validators`

The library `validators` raises the `Exception` - `ValidationFailure`, when it get an invalid url to validate.

#### `OspyataException(<name> + " exists in db.")` in `Osmata.push()`

This is raised when the name of the new record matches one in the database.

#### `OspyataException(<url> + " exists in db.")` in `Osmata.push()`

This is raised when the url of the new record matches one in the database.

#### `OspyataException(<name> + " do not exist in db.")` in `Osmata.pop()`

This is raised when the name of the record to be deleted is not matched in any names of the records in the database.

#### `OspyataException("Neither name nor url is present for existance checking.")` in `Osmata.check_existance()`

This is raised when the `check_existance()` function under the class `Osmata` is called without values for `name` AND `url` or with parameters `(name = False, url = False)`.

#### `OspyataException("Both name and url is present.")` in `Osmata.check_existance()`

This is raised when the `check_existance()` function under the class `Osmata` is called with values for `name` AND `url`.
