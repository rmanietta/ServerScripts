# LXC over Docker

Using LXC Containers to run Docker images.

incus versioning
```bash
incus version
```

incus remote image archives.
```bash
incus remote list
```

```bash
incus remote add docker https://docker.io --protocol=oci
```

recheck incus remote image archives.
```bash
incus remote list
```

incus launching oci containers.
```bash
incus launch docker:hello-world --console --ephemeral
```

--ephemeral = only run once.
removed will create run once and then stop.

