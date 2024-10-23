import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config.config import Config

class AlertSystem:
    def __init__(self):
        self.thresholds = Config.ALERT_THRESHOLDS
        self.consecutive_alerts = {}
        self.email_config = Config.EMAIL_CONFIG

    def check_alerts(self, city, temperature):
        threshold = self.thresholds.get(city, self.thresholds.get('default', 35))
        
        if temperature > threshold:
            if city in self.consecutive_alerts:
                self.consecutive_alerts[city] += 1
            else:
                self.consecutive_alerts[city] = 1
            
            if self.consecutive_alerts[city] >= 2:
                self._trigger_alert(city, temperature)
                return True
        else:
            self.consecutive_alerts[city] = 0
        
        return False

    def _trigger_alert(self, city, temperature):
        alert_message = f"ALERT: Temperature in {city} has exceeded the threshold. Current temperature: {temperature}°C"
        logging.warning(alert_message)
        print(alert_message)  # Display on console
        
        if self.email_config['enabled']:
            self._send_email_alert(city, temperature)

    def _send_email_alert(self, city, temperature):
        subject = f"Weather Alert: High Temperature in {city}"
        body = f"The temperature in {city} has exceeded the threshold.\nCurrent temperature: {temperature}°C"

        msg = MIMEMultipart()
        msg['From'] = self.email_config['sender_email']
        msg['To'] = self.email_config['recipient_email']
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                server.send_message(msg)
            logging.info(f"Email alert sent for {city}")
        except Exception as e:
            logging.error(f"Failed to send email alert: {str(e)}")
