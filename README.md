# How to Run the App
This app is best run using Docker. However, there are a couple of things to do before building the app. Carefully follow the instructions in the **Prerequisites** below.

## Prerequisites
### Python
There are some steps that needs to be done by running a python script. Make sure that python is already installed in your system.

Then, run the following command in the project top-level directory:
```python
python3 model_downloader.py
```
This command will download the necessary AI models used by this app.

### Transformer Model
Additionally, there is another fine-tuned model that has to be downloaded manually. First, change your current working directory:

```
cd models
```

Then, clone the huggingface repository model:

```
git clone https://huggingface.co/syukrondzeko/online_order_intents_distilbart_mnli/tree/main
```

You should see the **models** directory structure to be like this:
```
./models/
├── classifier/
├── online_order_intents_distilbart_mnli/
├── qa/
├── sentiment/
```
Please rename the *online_order_intents_distilbart_mnli* directory to *fine_tuned_distilbart_mnli*. You should end up with the following directory structure:
```
./models/
├── classifier/
├── fine_tuned_distilbart_mnli/
├── qa/
├── sentiment/
```
Next, open the *fine_tuned_distilbart_mnli* and delete the **model.safetensors** file.

Then, visit [this huggingface repo](https://huggingface.co/syukrondzeko/online_order_intents_distilbart_mnli/tree/main) and download the **model.safetensors** from there.

After that, put the downloaded **model.safetensors** file into the *fine_tuned_distilbart_mnli* directory.

Lastly, return to the project top-level directory:
```
cd ..
```
### Docker

This app is best run using Docker to avoid installing dependencies manually in your local machine. Therefore, ensure that docker has been installed in your system. Kindly follow the official installation guides according to your operating system (you can skip this installation step if you have already had Docker installed in your machine).

- [Docker Desktop for Mac (macOS)](https://docs.docker.com/desktop/install/mac-install/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)

Then, execute the following command to build the docker image (this might take some moment):
```
docker build -t vichack-restaurant:latest
```
## Running the App

Run the following command to run the app (make sure that port 3000, 3001, and 8000 are not being used):
```
docker run -p 8000:8000 -p 3000:3000 -p 3001:3001 vichack-restaurant:latest
```
To access the app, open your favorite browser and type the below URL:
```
http://localhost:3000/
```