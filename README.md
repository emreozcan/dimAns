# dimAns

**Dimensional analysis and unit conversion library**

[![PyPI - Version](https://img.shields.io/pypi/v/dimans?link=https%3A%2F%2Fpypi.org%2Fproject%2Fdimans%2F)](https://pypi.org/project/dimans/#history)
[![GitHub Tag](https://img.shields.io/github/v/tag/emreozcan/dimans)](https://github.com/emreozcan/dimAns/tags)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/dimans)](https://pypi.org/project/dimans/)
[![GitHub License](https://img.shields.io/github/license/emreozcan/dimans)](https://github.com/emreozcan/dimAns/blob/master/LICENSE)

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/emreozcan/dimAns/test.yml)](https://github.com/emreozcan/dimAns/actions/workflows/test.yml)
[![Codacy Code Quality Badge](https://app.codacy.com/project/badge/Grade/91ba463964c947c1af99446e92d1cd24)](https://app.codacy.com/gh/EmreOzcan/dimAns/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Coverage Badge](https://app.codacy.com/project/badge/Coverage/91ba463964c947c1af99446e92d1cd24)](https://app.codacy.com/gh/EmreOzcan/dimAns/coverage/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

## Installation

```bash
pip install --upgrade dimans
```

If you want to use the calculator, you will need to install the "cli" extra to
install some additional dependencies:

```bash
pip install --upgrade dimans[cli]
```

If you are using a Linux distribution like Arch that disallows installing
packages using pip, you will need to use a tool such as `pipx`:

```bash
pipx install --upgrade dimans[cli]
```

## Usage

```python-repl
>>> from dimans.units import gram, kilogram, metre
>>> (32_000 * gram).to(kilogram)
<Quantity 32.0 kg>
```

## Calculator

```bash
dimans
```
<p>
<img
    src="https://raw.githubusercontent.com/emreozcan/dimAns/master/imgs/calculator.svg"
    alt="dimAns Calculator Screenshot: Main Screen"
    width="50%"><img
    src="https://raw.githubusercontent.com/emreozcan/dimAns/master/imgs/search.svg"
    alt="dimAns Calculator Screenshot: Command Search"
    width="50%">
</p>
