# Flytepane 
A demo for learning flyte, flytekit, k3d and openfaas

# Geting started 

## Setup cluster 

```bash
# Install k3d binary
curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash
# Create k3d cluster 
k3d cluster create -p "30081:30081" --no-lb --k3s-server-arg '--no-deploy=traefik' --k3s-server-arg '--no-deploy=servicelb' flyte
# Ensure the context is set to the new cluster
kubectl config set-context flyte
```

## Install [flyte](https://github.com/flyteorg/flyte)

```bash
kubectl create -f https://raw.githubusercontent.com/flyteorg/flyte/master/deployment/sandbox/flyte_generated.yaml
#Note: Wait for few minutes. It takes a while
kubectl get all -n flyte 
# Open flyteconsole in browser
# http://127.0.0.1:30081/console
```

## Install Openfaas

```bash
# Create namespace for openfaas
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
# Install faas-cli
curl -sL https://cli.openfaas.com | sudo sh
# Add openfass helm repo
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo updatei
# Create Password and notedown it for login
export PASSWORD=$(head -c 12 /dev/urandom | shasum| cut -d' ' -f1)
# Create Secret in k8s for openfaas password
kubectl -n openfaas create secret generic basic-auth --from-literal=basic-auth-user=admin --from-literal=basic-auth-password="$PASSWORD"
# Install helm chart of openfaas
helm upgrade openfaas --install openfaas/openfaas --namespace openfaas --set functionNamespace=openfaas-fn --set basic_auth=true
# set openfaas url
export OPENFAAS_URL=127.0.0.1:31112
# Login using openfaas
echo -n $PASSWORD | faas-cli login -g http://$OPENFAAS_URL -u admin — password-stdin
# Check openfaas pod
kubectl get pods -n openfaas
```

## Build docker images
```bash
docker build . --build-arg tag=v1 -t docker.io/evalsocket/flytepane:v1 -f Dockerfile
docker push docker.io/evalsocket/flytepane:v1
```

## Generate Serialize proto for your workflow
```bash
# Install dependancy
poetry install
# Generate serialize proto
pyflyte -c sandbox.config --pkgs datapane serialize --in-container-config-path /root/sandbox.config --local-source-root $(pwd) --image docker.io/evalsocket/flytepane:v1 workflows -f _pb_output/
# Register your workflow
flyte-cli register-files -p flytesnackes -d development -v v1 --kubernetes-service-account default --output-location-prefix s3://my-s3-bucket/raw_data -h 127.0.0.1:30081 _pb_output/*
```

TBH
