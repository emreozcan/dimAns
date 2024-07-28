# dimAns

**Dimensional analysis and unit conversion library**

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/91ba463964c947c1af99446e92d1cd24)](https://app.codacy.com/gh/EmreOzcan/dimAns/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/91ba463964c947c1af99446e92d1cd24)](https://app.codacy.com/gh/EmreOzcan/dimAns/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

## Installation

```bash
pip install dimans
```

## Usage

```python-repl
>>> from dimans.units import gram, kilogram, metre
>>> (32_000 * gram).to(kilogram)
<Quantity 32.0 kg>
```
