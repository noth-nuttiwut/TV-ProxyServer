
### Build Image
``` 
docker build -t image_name .
```

### Create & Run Container

```
docker run -d --name container_name -p 80:80 --env-file ./.env image_name
```
