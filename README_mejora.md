## Mejoras implementadas  

1. **Historial en el README**  
En lugar de sobrescribir el estado de los tests, ahora se guarda un registro histórico con fecha y hora.  
[Código en update_readme.py](https://github.com/danielmi5/2526_DAW_u1_action/blob/13af1682d35a9dd58ebffd833748bb9894f17c4d/update_readme.py#L12-L21)   

2. **Badge automático en el README**  
Se añade un badge dinámico que refleja el estado de los tests. Generado automáticamente con el **SVG de GitHub Actions**  
   ```
   ![Tests](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)
   ```  

3. **Ejecución automática programada**  
   El workflow se ejecuta todos los días a medianoche.
   ```
   cron: "0 0 * * *"  
   ```

4. **Creación automática de Issues si fallan los tests**  
Cuando los tests fallan, se abre automáticamente un issue en el repositorio.  
[Issues automáticos](https://github.com/danielmi5/2526_DAW_u1_action/blob/13af1682d35a9dd58ebffd833748bb9894f17c4d/.github/workflows/ci.yaml#L46-L60)



# Workflow: CI con AutoCommit  

Este workflow automatiza la ejecución de tests, actualiza el README con el estado, añade un historial, se ejecuta automáticamente y crea issues automáticos en caso de fallo.  

---

## Explicación paso a paso  

### Nombre del workflow  
```yaml
name: CI con AutoCommit
```
Define el nombre del workflow, que aparecerá en la pestaña **Actions** de GitHub.  

---

### Eventos que lo activan  
```yaml
on:
  push:
    branches: [ "main" ]
  workflow_dispatch:
  schedule:
    - cron: "0 0 * * *"
```
- **push**: se ejecuta al hacer commit en la rama `main`.  
- **workflow_dispatch**: permite ejecutarlo manualmente desde la pestaña **Actions**.  
- **schedule (cron)**: lo programa para que se ejecute automáticamente todos los días a medianoche.  

---

### Permisos necesarios  
```yaml
permissions:
  contents: write  
```
Se conceden permisos al bot para modificar archivos del repositorio (como el README) y abrir issues.  

---

### Job principal: test-and-update  
```yaml
jobs:
  test-and-update:
    runs-on: ubuntu-latest

    env:
      TZ: Europe/Madrid
```
- **runs-on**: usa Ubuntu como sistema operativo de ejecución.  
- **env**: establece la zona horaria en Europa/Madrid para registrar las fechas correctamente.  

#### Pasos del job  
```yaml
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3
```
Clona el repositorio en el runner.  

```yaml
      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
```
Instala y configura Python 3.10.  

```yaml
      - name: Instalar dependencias
        run: pip install pytest
```
Instala la dependencia `pytest` para ejecutar los tests.  

```yaml
      - name: Ejecutar script de tests y actualizar README
        run: python update_readme.py
```
Ejecuta el script que:  
- Lanza los tests.  
- Actualiza el **historial de resultados** en el README.  
- Añade la fecha de la última ejecución.  

```yaml
      - name: Commit automático del README
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "Update README con estado de tests"
          file_pattern: README.md
```
Si el README fue modificado, le hace commit automáticamente con el mensaje.  

---

### Job secundario: issue-on-fail  
```yaml
  issue-on-fail:
    needs: test-and-update
    if: failure()  
    runs-on: ubuntu-latest
```
- **needs**: depende de que el job `test-and-update` termine primero.  
- **if: failure()**: solo se ejecuta si el job anterior falla.  

#### Paso del job  
```yaml
    steps:
      - name: Issue automático al fallar los tests
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: "❌ Tests fallidos",
              body: "Se han detectado errores en los tests. Revisa el último commit."
            })
```
Este paso crea un **issue automático** en GitHub notificando que los tests han fallado.