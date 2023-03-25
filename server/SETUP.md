# Ubuntu
1. Install required system dependencies:

```bash
sudo apt install -y python3-venv
```

2. Create virtual environment

```bash
python3 -m venv env
```

3. Use environment

```bash
source env/bin/activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Launch server

```bash
python3 server.py
```

> You can also do it in Docker:
> ```bash
> docker run --rm -ti -p 8000:8000 -u 1000 -w /app -v $(pwd):/app  python:3.10 /bin/bash
> ```
