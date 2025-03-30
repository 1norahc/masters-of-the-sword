# Wzorce regex do walidacji
NAME_PATTERN = r'^[A-Za-zÀ-ÖØ-öø-ÿ\'-]+$'
NICKNAME_PATTERN = r'^[A-Za-z0-9_.-]+$'
EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'