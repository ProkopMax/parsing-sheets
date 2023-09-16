# Example of parsing a Google table without api access
## 1. Install docker 
    https://docs.docker.com/engine/install/
## 2. Install docker-compose
    sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose --version
## 3. Build and run app
    docker-compose up --force-recreate --build -d
## 4. Check docker containers
    docker ps -a | grep parsing
![image](https://github.com/ProkopMax/parsing-sheets/assets/72852008/b2c2a3d0-5039-4509-93b1-c79f740ee0c1)
## 5. View site 
    http://localhost:8000

### Nginx + ssl 
    1. Install nginx 
    2. Install certbot and generate cert for your domain name
    3. Use and change file nginx/parsing-sheets.conf for your needs
