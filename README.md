### Setup Database

After installing PSQL, follow these steps (instructions are for Linux; Windows will be similar but may vary).

**1. Enter PostgreSQL Superuser account:**
```bash
sudo -i -u postgres psql
```

**2. Create the Database and User:**
Modify this command below to include your chosen username and a secure password (that will be encrypted).
```sql
CREATE DATABASE pyxia;
CREATE USER yourusername WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE pyxia TO yourusername;
```

**3. Initialise Schema:**
Connect to the database:
```sql
\c pyxia
```
Run the following SQL script (ensure you change the username here) to generate the tables and assign the correct ownership:
```sql
CREATE TABLE IF NOT EXISTS public.userdb
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    age INTEGER NOT NULL
);

ALTER TABLE public.userdb OWNER TO yourusername;
```
Type `\q` and press **Enter** to exit.

### Configure Environment

Modify the `.env` file in your root directory to include your details:
```env
NAME="yourusername"
PASSWORD="your_secure_password"
PORT=5432
DATABASE="pyxia"
```

### Install System Dependencies

To start the program, we need ClamAV and libmagic installed on the OS level:
```bash
sudo apt update
sudo apt install libmagic1 clamav clamav-daemon
```

*Note: ClamAV can sometimes require more setup. You can troubleshoot by checking whether the ClamAV daemon is running with:*
```bash
sudo systemctl status clamav-daemon
```
*If it is not running, you may need to start it:*
```bash
sudo systemctl start clamav-daemon
```

### Setup Pyxia

**1. Create the virtual environment:**
```bash
python3 -m venv env
```

**2. Open the environment:**
```bash
source env/bin/activate
```

**3. Install requirements:**
```bash
pip3 install -r requirements.txt
```

**4. Create .env:**
Create a .env file containing this (add your details between the ""):
```
NAME=""
PASSWORD=""
PORT=5432
DATABASE=""
```

**5. Run the program:**
```bash
python3 main.py
```

You may have an issue with `psycopg2`, I've found that this can work:
```
sudo apt update
sudo apt install libpq-dev python3-dev
pip3 install psycopg2
```



Some issues:
Ensure that you have the right file permissions, when uploading a file, you may get:
'error' on the website and this in terminal:
`result was:  {'/var/www/pyxia/posts/1/post1.jpg': ('ERROR', 'Access denied.')}`

May need to use something like this:
```
echo "/var/www/pyxia/** r," | sudo tee -a /etc/apparmor.d/local/usr.sbin.clamd
sudo systemctl reload apparmor
sudo systemctl restart clamav-daemon
```

Then set ACLs:
```
sudo setfacl -R -m u:clamav:rX /var/www/pyxia

sudo setfacl -d -R -m u:clamav:rX /var/www/pyxia
```


