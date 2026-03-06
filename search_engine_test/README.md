## Allure Reporting

### Install dependencies
- Python libs: `pip install -r requirements.txt` (or at minimum `pip install allure-pytest selenium webdriver-manager`)  
- Allure CLI (needed to view HTML report):  
  - Windows (Chocolatey): `choco install allure`  
  - Windows (Scoop): `scoop install allure`  
  - Or download from https://github.com/allure-framework/allure2/releases and add `bin` to `PATH`.

### Run tests and generate results
- Execute tests and export results:  
  `pytest --alluredir=reports/allure-results`

- Serve report locally (opens a browser):  
  `allure serve reports/allure-results`

- Or generate static HTML:  
  `allure generate reports/allure-results -o reports/allure-report --clean`

### Notes
- Failed UI tests automatically capture a screenshot and attach it to the Allure report.
- Test steps, feature/story metadata, and parameterized cases are reflected in the report.

