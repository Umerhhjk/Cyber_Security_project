import cv2
import qrcode


def generate_qr_code(name, amount, message, date, signature):
    """
    Generate a QR code with sender's details
    
    Args:
    - name (str): Sender's name
    - amount (float): Transaction amount
    - message (str): Additional message
    - date (str): Transaction date
    - signature (str): Transaction signature
    
    Returns:
    - qrcode.image.pil.PilImage: QR code image
    """
    # Create the formatted QR code content
    qr_content = f"""Sender's Name: {name}
Amount: {amount}
Message: {message}
Date: {date}
Signature: {signature}"""
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR code
    qr.add_data(qr_content)
    qr.make(fit=True)
    
    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    return qr_image

def read_qr_code(image_path):
    image = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    detected_data, points, straight_qrcode = detector.detectAndDecode(image)
    data = detected_data.split("\n")
    return data

# Example usage
def main():
    # Example transaction details
    sender_name = "John Doe"
    transaction_amount = 500.00
    transaction_message = "Monthly rent payment"
    transaction_date = "2024-01-15 14:30:00"
    transaction_signature = "ABC123XYZ456"
    
    # Generate QR code
    qr_image = generate_qr_code(
        name=sender_name, 
        amount=transaction_amount, 
        message=transaction_message,
        date=transaction_date,
        signature=transaction_signature
    )
    
    # Save the QR code image
    qr_image.save("transaction_qr_code.png")
    print("QR code generated successfully!")
    read_qr_code("transaction_qr_code.png")

if __name__ == "__main__":
    main()