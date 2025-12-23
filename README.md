# Introduction_to_programming_for_brain_anatomy_Final_assignement
고려대 뇌공학프로그래밍입문 기말과제 레포지토리
## Project Overview

This project was developed as part of the BRI 519 course to demonstrate core concepts in data processing, analysis, and reproducible computational workflows. The goal of the project is to provide a structured and well-documented codebase that can be easily understood, executed, and extended by other users.

The project emphasizes clarity, modular design, and reproducibility, making it suitable for both educational and experimental purposes.
This project was developed and tested with Python 3.11.

## Repository Structure

The repository is organized as follows:

- `src/`  
  Contains the main source code files implementing the core functionality of the project.

- `data/`  
  Stores input datasets and any intermediate data files used during analysis.

- `notebooks/`  
  Includes Jupyter notebooks used for exploration, analysis, and visualization.

- `requirements.txt`  
  Lists the Python dependencies required to run the project.

- `README.md`  
  Provides an overview of the project, installation instructions, and usage examples.


## Installation Instructions

1. Clone the repository:
   ```bash
   git clone git@github.com:jeongmino/Introduction_to_programming_for_brain_anatomy_Final_assignement.git
   cd Introduction_to_programming_for_brain_anatomy_Final_assignement

2. Create a virtual enviornment
  python -m venv venv
  source venv/bin/activate

3. Install required dependecies
   pip install -r requirements.txt

4. Verify installation by running one of the provided scripts or notebooks

   ## 4️⃣ Usage Examples (실행 예시 필수)

  ## Usage Examples

  After installation, the project can be used in the following ways:

  ### Running the main script
  ```bash
  python src/main.py


## Docker Containerization and Deployment

To ensure reproducible execution of the LFP analysis pipeline, the entire project
has been containerized using Docker. The Docker setup encapsulates the runtime
environment, dependencies, and analysis code, allowing the analysis to be executed
consistently across different systems.

---

### Dockerfile

A `Dockerfile` is provided at the root of the repository.  
It performs the following steps:

- Uses an official Python base image (`python:3.11-slim`)
- Installs all required system and Python dependencies
- Copies the analysis code and data into the container
- Configures the container to automatically execute the analysis pipeline

This ensures that the container includes all components necessary to reproduce
the results from Question 1.

---

### Build Docker Image Locally

To build the Docker image locally, run the following command from the project root:

```bash
docker build -t lfp-analysis .
```

This command builds the image using the provided Dockerfile and installs all
dependencies listed in requirements.txt.

Run the Analysis Using Docker

Running the container automatically executes the full analysis pipeline
without any additional user input.

The following command runs the container and saves all output figures
to the local output/ directory using volume mounting:

'mkdir -p output' for result directory

```bash
mkdir -p output
docker run --rm -v $(pwd)/output:/app/output lfp-analysis
```


### Output Files

All analysis results are generated automatically when the container is run.
The output includes stimulus-locked low vs high tone comparison figures
for each session, saved as image files in the output/ directory.

These files serve as concrete evidence that the analysis was successfully
executed inside the Docker container.

### Docker Hub Deployment

The Docker image has been uploaded to Docker Hub and is publicly available:

https://hub.docker.com/r/jeongmino/lfp-analysis

To run the analysis directly from Docker Hub without building the image locally,
use the following command:

```bash
mkdir -p output
docker run --rm -v $(pwd)/output:/app/output jeongmino/lfp-analysis:final
```


Summary

- A Dockerfile is provided to containerize the analysis pipeline
- The image can be built and tested locally
- The container runs the full analysis automatically upon execution
- Output files are generated and saved without manual intervention
- The Docker image is publicly available on Docker Hub
- All Docker-related instructions are documented in this README