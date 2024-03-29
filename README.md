# Example of parsing a Google table without api access
![image](https://github.com/ProkopMax/parsing-sheets/assets/72852008/adbfc032-04b1-47ee-8615-7b247df0ce9e)

## 1. Install docker 
    https://docs.docker.com/engine/install/
## 2. Install docker-compose
    sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose --version
## 3. Build and run app
    docker-compose up --force-recreate --build -d
    
    ### Clear build, run whithout cache and delete old images ###
    docker-compose build --no-cache; docker-compose up -d; docker rmi $(docker images | grep none | awk {'print $3'})
## 4. Check docker containers
    docker ps -a | grep parsing
![image](https://github.com/ProkopMax/parsing-sheets/assets/72852008/b2c2a3d0-5039-4509-93b1-c79f740ee0c1)
## 5. View site 
    http://localhost:8000

### Nginx + ssl + security
    1. Install nginx  
        https://www.nginx.com/resources/wiki/start/topics/tutorials/install/
        
    2. Install certbot and generate cert for your domain name 
        https://certbot.eff.org/
        
    3. Use and change files nginx/parsing-sheets.conf nginx/nginx.conf for your needs
