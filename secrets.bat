echo "DB_PASSWORD=SuperSecretPass123!" > .env
echo "STRIPE_API_KEY=sk_test_4eC39HqLyjWDarjtT1zdp7dc" >> .env

# En voor de zekerheid ook de app.py met de AWS key:
echo "AWS_ACCESS_KEY_ID='AKIAV7B3J4K5L6M7N8O9'" > app.py
echo "AWS_SECRET_ACCESS_KEY='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'" >> app.py

# En de SSH key in de certs map:
mkdir -p certs
echo "-----BEGIN RSA PRIVATE KEY-----" > certs/id_rsa
echo "MIIEpAIBAAKCAQEA75p..." >> certs/id_rsa
echo "-----END RSA PRIVATE KEY-----" >> certs/id_rsa
