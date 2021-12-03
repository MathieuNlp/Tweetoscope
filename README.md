# tweetoscope_2021_10


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://gitlab-student.centralesupelec.fr/2018ech-choum/tweetoscope_2021_10">
    <img src="https://img.gothru.org/283/9820106392942001866/overlay/assets/20210430082511.Ma26Qm.png?save=optimize" alt="Logo" width="90" height="50">
  </a>



  <p align="center">

  </p>
</div>



 



<!-- ABOUT THE PROJECT -->
## About The Project

The project consists in estimating the virality of a tweet from its original message. By means of a tweet generator. We built a tweet collector in C++ that retrieves the tweet stream and sends it to the estimator under a formalism by the topic cascade_serie. An estimator using the Hawkes process simulates the tweet cascade that will be directly sent to the predictor. The predictor then estimates the virality of the tweet. Finally, a learner is implemented to continuously improve the accuracy of our model so that the prediction is better.

<img src="https://pennerath.pages.centralesupelec.fr/tweetoscope/graphviz-images/ead74cb4077631acad74606a761525fe2a3228c1.svg" alt=image_archi/>

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [APACHE KAFKA](https://kafka.apache.org/) 
* [Docker](https://maven.apache.org/) 
* [Kubernetes](https://kubernetes.io/) 


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is how you may set up the project locally.
To get a local copy up and running follow these simple steps.



<!-- ROADMAP -->
## Folder layout


    .
    ├── Build                   # Docker files (alternatively `dist`)
    ├── Deployment              # YAML files used for minikube
    ├── Pipeline_ai             # Folder containing files for the estimator, learner and predictor
    │   ├── Hawks_Processes     # files used for Hawks process
    │   └── utils               # Usefull functions
    ├── Tweet_collection        # Folder containing tweet generation and tweet collection files
    │   ├── Tweet_Collector     # tweet collection
    │   └── Tweet_Generator     # tweet generation
    ├── .gitlab-ci.yml
    └── README.md




<p align="right">(<a href="#top">back to top</a>)</p>


### Prerequisites

To run the software you need to install the following.
* docker
  sh
  npm install npm@latest -g
  

* minikube
  sh
  npm install npm@latest -g
  

### Installation

Those are the steps to run the software.

1. Download the Deployment directory on your local machin
   ```sh
   git clone https://gitlab-student.centralesupelec.fr/2018ech-choum/tweetoscope_2021_10.git
   cd tweetoscope_2021_10
   ```
   
2. To run the deployment on minikube
    ```sh
    minikube start
    kubectl apply -f Deployment/minikube-zookeeper-kafka.yml
    kubectl apply -f Deployment/minikube-services.yml
    ```
   
3. To run the deployment on a cluster (Intercell)
    ```sh
    ssh cpusdi1_45@phome.metz.supelec.fr
    ssh ic57
    git clone https://gitlab-student.centralesupelec.fr/2018ech-choum/tweetoscope_2021_10.git
    cd tweetoscope_2021_10 
    kubectl -n cpusdi1-45-ns apply -f /Deployment/intercell-zookeeper-kafka.yml
    kubectl -n cpusdi1-45-ns apply -f /Deployment/intercell-services.yml
    ```

4. Fault tolerance test (With Intercell) - Supposing you run part.3
    ```sh
    kubectl -n cpusdi1-45-ns delete pod <pod_name>
    kubectl -n cpusdi1-45-ns get pods -o wide
    ```
    We will observe that the pod will be recreated automatically in a different node

5. Scaling test (with minikube) - Supposing that part.2 is running)
    ```sh 
    kubectl get deployments
    kubectl scale --replicas=4 deployment/<tweet_collector_deployment>
    kubectl get pods
    ```



<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->





<!-- CONTACT -->
## Authors

* **Mathieu Nalpon**
* **Mehdi Ech-Chouini**
* **Hamza Islah**



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Those are the libraries the project was build with.
* [gaml](https://github.com/HerveFrezza-Buet/gaml)
* [cppkafka](https://github.com/mfontanini/cppkafka)
* [kafka-python](https://kafka-python.readthedocs.io/en/master/)

<p align="right">(<a href="#top">back to top</a>)</p>



