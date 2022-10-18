import codecs
import smtplib
import mimetypes
from email.message import EmailMessage
from email.utils import make_msgid

def send_pdf(subject, body, to, cc=None, bcc=None, attachment=''):
    if cc is None:
        cc = []
    if bcc is None:
        bcc = []
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'operations@life-raft.com'
    msg['To'] = to
    msg['Cc'] = cc
    msg['Bcc'] = bcc

    msg.set_content(body)

    # Signature 
    img_path = r'signature_image_path'  # Update img Path
    html_path = r'signature_html_path'  # Update htm Path

    html_file = codecs.open(html_path, 'r', 'utf-8', errors='ignore')  # Opens HTML file and converts to UTF-8, ignoring errors
    html_code = html_file.read()  # Writes contents of HTML signature file to a string
    html_file.close()

    image_id = make_msgid()

    # Combines the text body, HTML signature, and image in Email HTML format
    msg.add_alternative(body + '<br><br>' + html_code + '<img src="%s" />' % image_id.strip('<>'), subtype='html')

    with open(img_path, 'rb') as img:
        msg.get_payload()[1].add_related(img.read(), 'image', 'png', cid=image_id)

    # Attachment
    if attachment != '':
        # Guess the content type based on the file's extension.  Encoding will be ignored, although we should check for 
        # simple things like gzip'd or compressed files.
        ctype, encoding = mimetypes.guess_type(attachment)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        filename = os.path.basename(attachment)
        with open(attachment, 'rb') as file:
            content = file.read()
        msg.add_attachment(content, maintype=maintype, subtype=subtype, filename=filename)
  
    # Send Email
    with smtplib.SMTP('smtp.office365.com', 587) as smtp: # Update Email SMTP depending on provider you use
        smtp.ehlo()
        smtp.starttls()
        smtp.login('Email@url.com', 'Password')  # Update Email and Password

        smtp.send_message(msg)
