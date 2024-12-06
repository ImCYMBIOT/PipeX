# **PipelineX**

PipelineX is a CLI-based tool for managing and automating end-to-end ETL (Extract, Transform, Load) workflows. It simplifies data pipeline tasks such as extracting data from APIs and databases, transforming data with custom logic, and loading it into storage solutions like AWS S3 or databases.

## **Features**

- Extract data from APIs, CSV/JSON files, and relational databases (MySQL, PostgreSQL).
- Transform data using custom Python scripts powered by Pandas.
- Load transformed data into target systems like AWS S3 or other databases.
- Real-time logging and monitoring.
- Scalable scheduling with Kubernetes CronJobs.

---

## **Installation**

### **Prerequisites**

1. Python 3.11 or higher.
2. Poetry for dependency management. Install Poetry:
   ```bash
   pip install poetry
   ```

### **Setup**

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pipelinx.git
   cd pipelinex
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Activate the virtual environment:

   ```bash
   poetry shell
   ```

4. Install PipelineX globally to use as a CLI:
   ```bash
   poetry build
   pip install dist/pipelinx-0.1.0-py3-none-any.whl
   ```

---

## **Usage**

### **Running the CLI**

To start the CLI, use the command:

```bash
pipelinx
```

### **Available Commands**

```bash
pipelinx --help
```

This will display all available commands and their usage.

#### Example Commands:

1. **Extract Data**  
   Extract data from a MySQL database:

   ```bash
   pipelinx extract db --host localhost --user root --password secret --db mydb --query "SELECT * FROM table_name"
   ```

2. **Transform Data**  
   Apply transformations to a CSV file:

   ```bash
   pipelinx transform --input data.csv --script transform_script.py --output transformed_data.csv
   ```

3. **Load Data**  
   Load transformed data to an S3 bucket:

   ```bash
   pipelinx load s3 --file transformed_data.csv --bucket my-bucket --key data/transformed_data.csv
   ```

4. **Run Full Pipeline**  
   Run the entire ETL process in one command:
   ```bash
   pipelinx run --config pipeline_config.yaml
   ```

---

## **Configuration**

PipelineX uses YAML configuration files to define ETL workflows. Example:

```yaml
extract:
  type: db
  host: localhost
  user: root
  password: secret
  db: mydb
  query: "SELECT * FROM table_name"

transform:
  script: transform_script.py

load:
  type: s3
  bucket: my-bucket
  key: data/transformed_data.csv
```

Save this configuration as `pipeline_config.yaml` and run:

```bash
pipelinx run --config pipeline_config.yaml
```

---

## **Development**

### **File Structure**

```plaintext
PipelineX/
├── app/
│   ├── api.py
│   ├── cli.py
│   ├── extract.py
│   ├── load.py
│   ├── storage.py
│   ├── transform.py
│   ├── utils.py
│   └── __init__.py
├── config/
│   ├── settings.py
│   ├── logging_config.py
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   ├── test_load.py
│   └── test_cli.py
├── main.py
├── pyproject.toml
├── requirements.txt
├── README.md
```

---

## **Contributing**

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit your changes and push:
   ```bash
   git push origin feature/new-feature
   ```
4. Submit a pull request.

---

## **License**

This project is licensed under the MIT License.

---

## **Author**

Developed by [Agnivesh Kumar](mailto:agniveshkumar15@gmail.com).
