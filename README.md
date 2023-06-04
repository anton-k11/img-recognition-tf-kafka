# img-recognition-tf-kafka
Fast And Furious Image Recognition with TensorFlow and Kafka

## Building the project

### Build ML Image Recognition Java Service 
 * Pull the Inception V3 ML model:
      
    `./gradlew :ml-img-recognition:fetchInceptionFrozenModel`
 * Build the project:
 
    `./gradlew build`
 * TODO: Add Kafka Connect Server and Kafka Connect S3 Sink to write images and classifications to Mock AWS S3 Service


### Build The Docker Images
 `docker compose build`

### Edit Images Volume
[Modify the volume](https://github.com/anton-k11/img-recognition-tf-kafka/blob/640f72b780ca49d3f693a251428a599e64fa377d/docker-compose.yml#L69)
or copy images to `/home/pictures`  to be sent by the producer 
 
## Start Docker Compose Services
1. Start Zookeeper, Kafka and create topics: 

   `docker compose up init-kafka-broker` 
1. Start ML image classification service, decision consumer: 

   `docker compose up -d decision-consumer tf-img-recognition`
1. Start image producer:

    `docker compose up -d image-producer`

#### Observe image classifications consumed by the decision consumer
`docker compose logs decision-consumer`

### Plot Delivery Times
For ML classifications and delivery or only for ML classification time In Tensorflow (including image preprocessing)

#### Create Python Virtual Environment 
```bash
cd img-recognition-tf-kafka
python3 -m venv .venv
```
#### Activate the virtual environment and install dependencies
```bash
source .venv/bin/activate
cd plot-proc-time
pip install -r requirements.txt
```
#### Run Matplotlib Python Script
In the same terminal where the virtual environment is activated requirements are installed
 * Plot delivery and classification time, from image generation until ML classification consumption:
   ```bash
   python3 plot_consumer_log.py
   ```
 * Plot only ML model classification time, including image preprocessing: 
   ```bash
   python3 plot_tf_proc_time.py
   ```