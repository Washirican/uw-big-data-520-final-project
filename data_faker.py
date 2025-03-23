from faker import Faker
from typing import Dict

fake = Faker()
def get_registered_user() -> Dict[str, str]:
    """
    Generate a dictionary representing a registered user with fake data.

    Returns:
        Dict[str, str]: A dictionary containing the following keys:
            - 'name': A fake name.
            - 'address': A fake address.
            - 'created_at': A fake year representing the creation date.
    """
    return {
        'name': fake.name(),
        'address': fake.address(),
        'created_at': fake.year()
    }

if __name__ == "__main__":
    print(get_registered_user())
