# Compose file for Code Server

compose.yml

```  
---
services:
  code-server:
    image: lscr.io/linuxserver/code-server:latest
    container_name: code-server
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
      - DEFAULT_WORKSPACE=/config/workspace
    volumes:
      - ./config:/config
    ports:
      - 8443:8443
    restart: unless-stopped

```
