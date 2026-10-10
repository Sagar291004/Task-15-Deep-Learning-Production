# Task 15: Deep Learning Production Deployment

## Project Overview
This project demonstrates the production deployment of a deep learning image classification model using Flask, Streamlit, Docker, and Kubernetes. The application uses a trained CNN model to classify images from the CIFAR-10 dataset.

## Objectives
- Deploy a trained deep learning model using a Flask REST API.
- Create an interactive frontend using Streamlit.
- Containerize the frontend and backend using Docker.
- Deploy and manage application components using Kubernetes and Minikube.
- Test image prediction and API health endpoints.

## Technologies Used
- **Programming Language:** Python
- **Deep Learning:** TensorFlow, Keras
- **Backend:** Flask, Flask-CORS
- **Frontend:** Streamlit
- **Image Processing:** Pillow, NumPy
- **Containerization:** Docker
- **Orchestration:** Kubernetes, Minikube
- **Version Control:** Git and GitHub

## Project Structure
```text
Task-15-Deep-Learning-Production/
├── app.py
├── streamlit_app.py
├── task6_cnn_model.keras
├── requirements.txt
├── Dockerfile
├── Dockerfile.streamlit
├── .gitignore
├── README.md
└── k8s/
    ├── flask-deployment.yaml
    ├── flask-service.yaml
    ├── streamlit-deployment.yaml
    └── streamlit-service.yaml
```

## Key Features
- Upload an image through the Streamlit interface.
- Send images to the Flask prediction API.
- Generate predictions using the trained CNN model.
- Display the predicted class and confidence score.
- Provide a health-check endpoint for the Flask API.
- Run the backend and frontend in separate Docker containers.
- Deploy the application using Kubernetes Deployments and Services.

## Installation and Local Execution

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/Task-15-Deep-Learning-Production.git
cd Task-15-Deep-Learning-Production
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Flask API
Open a terminal and run:
```bash
python app.py
```

### 4. Start the Streamlit Frontend
Open another terminal and run:
```bash
streamlit run streamlit_app.py
```

Open the local Streamlit URL displayed in the terminal.

## Docker Deployment

Build the Flask backend image:
```bash
docker build -t task15-flask:1.0 .
```

Build the Streamlit frontend image:
```bash
docker build -f Dockerfile.streamlit -t task15-streamlit:1.0 .
```

The backend and frontend are packaged as separate Docker images.

## Kubernetes Deployment Using Minikube

Start Minikube:
```bash
minikube start
```

Apply the Kubernetes configuration files:
```bash
kubectl apply -f k8s/
```

Verify the deployment:
```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

Open the Streamlit application:
```bash
minikube service task15-streamlit-service
```

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Check API health |
| `/predict` | POST | Predict the class of an uploaded image |

The `/predict` endpoint accepts an image upload and returns a JSON response containing the prediction details.

## Testing and Results
- Tested the Flask API health endpoint.
- Verified that the Docker containers started successfully.
- Verified that the Kubernetes pods reached the Running state.
- Tested image classification through the Streamlit interface deployed on Minikube.
- Confirmed that the application returned a predicted class and confidence score.

**Note:** The prediction confidence for an individual image is not the same as the overall model accuracy.

## Challenges and Solutions
- **Docker image availability in Minikube:** Exported the Docker images as TAR files and loaded them into Minikube.
- **Kubernetes NodePort conflict:** Changed the Streamlit NodePort to `30082`.
- **Frontend-backend communication:** Configured the Streamlit application to communicate with the Flask Kubernetes Service.

## Conclusion
This project demonstrates an end-to-end workflow for deploying a deep learning image classification application. By integrating Flask, Streamlit, Docker, and Kubernetes, the model can be accessed through a web interface and managed within a containerized deployment environment.

## Author
**Sagar Chandratre**
