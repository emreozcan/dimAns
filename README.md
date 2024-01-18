# dimAns
**Dimensional analysis and unit conversion library**

## Usage

```python-repl
>>> from dimans.units import gram, kilogram, metre
>>> (32_000 * gram).convert_to(kilogram)
<Quantity 32 kg>
```
