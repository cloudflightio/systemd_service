# systemd service role

This role creates a systemd docker unit to launch docker containers as systemd services.

## Example configuration
```
- import_role:
    name: systemd_service
  vars:
    systemd_service:
      name: example-unit
      state: started # optional
      enabled: yes # optional
      custom_pre_start: "echo 1" # optional
      docker:
        container_name: example
        image: busybox:latest
        expose_port:
          - host: 80
            container: 8080
        volume:
          - host: /opt/data
            container: /var/www
            mode: ro
        env:
          EXAMPLE: 123
        memory_limit: 5g
        network: my-docker-network
        hostname: example
        arguments: "bash hello-world.sh"
``` 
