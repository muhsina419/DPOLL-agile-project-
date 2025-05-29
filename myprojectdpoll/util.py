import random

def generate_otp(length=6):
    """Generate a numeric OTP of given length."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp(phone_number, otp):
    # Integrate with your SMS gateway here (e.g., Twilio)
    print(f"Sending OTP {otp} to phone number {phone_number}")
    # Return True if sent successfully, False otherwise
    return True