PS C:\Users\Admin> 

docker build -t lab2_ola -f D:/web_labs/Lab-2_Infra_and_Docker/infrastructure/Dockerfile D:/web_labs/Lab-2_Infra_and_Docker

docker login

docker build -f D:\web_labs\Lab-2_Infra_and_Docker\infrastructure\Dockerfile -t olgashep/lab2_ola:latest D:\web_labs\Lab-2_Infra_and_Docker

docker push olgashep/lab2_ola

