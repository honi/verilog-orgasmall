# Verilog

En este repo estoy aprendiendo Verilog e intentando armar un CPU muy básico.

## Entorno de desarrollo

- `./scripts/setup`: Buildea un container de Docker con todas las herramientas instaladas.
- `./scripts/shell`: Abre un shell adentro del container con `pwd` montado en `/workspace`.

## Módulos

### Memory

```sh
make test_memory
```

## Notas

- Agregar `ae` (address enable) a `memory` para utilizar el mismo bus para direcciones y datos.
- Arreglar shift right arithmetic.
- Si quiero hacer un cpu single-cycle necesito si o si 2 memorias separadas (programa y datos), o una memoria dual port (2 lecturas simultáneas)?
- Mantener el clock entre distintos test cases.
