# An-Intelligent-IoT-Based-Crop-Protection-System-with-AI-Driven-Animal-Detection-and-Water-Management
Developed an AI-powered agricultural surveillance system using Raspberry Pi 5 and YOLOv8 to detect crop-destroying animals in real-time. The system uses deterrent sounds, monitors environmental conditions, and sends alerts via the Blynk IoT app. It enables remote farm management and supports precision agriculture with scalable, low-cost solutions.

## Features

- **Animal Detection**: Real-time detection of animals like birds, monkeys, and wild boars using YOLOv8.
- **Deterrent Sounds**: Plays animal-specific deterrent sounds (e.g., bird sound, monkey sound) upon detection.
- **Blynk App Integration**: Sends real-time alerts and allows remote control of the system (e.g., controlling motors, buzzers, or LEDs).
- **Environmental Monitoring**: Monitors water levels, rain detection, and environmental conditions in the field.
- **Real-Time Data Display**: Displays real-time animal detection data, notifications, and control features in the Blynk app.
- **Integration with Raspberry Pi**: Uses Raspberry Pi 5 for both detection and control, integrating GPIO pins, sensors, and the camera module.

## System Architecture

The system architecture consists of the following components:
- **YOLOv8 Model**: Trained to detect animals like birds, monkeys, and wild boars.
- **Raspberry Pi 5**: Handles the image capture, animal detection, and control logic.
- **Camera Module**: Captures real-time video for detection.
- **Blynk App**: A mobile app to receive alerts, view status, and control system components.
- **Environmental Sensors**: Includes water level sensors and rain sensors to provide real-time environmental data.

## Prerequisites

Before you begin, make sure you have the following:

- **Hardware**:
  - Raspberry Pi 5 (8GB version recommended)
  - Camera Module for Raspberry Pi
  - Buzzer, Servo Motors, LEDs for control
  - Water Level Sensor
  - Rain Sensor
  - Blynk-supported device (smartphone)

- **Software**:
  - Python 3.x
  - OpenCV
  - PyTorch (for YOLOv8)
  - Blynk Library for Python
  - Twilio (for SMS and WhatsApp notifications)
  - Raspberry Pi GPIO Library
  - Additional Python packages

## Flow Chart
![image](https://github.com/user-attachments/assets/d5fc0706-78ab-45ce-b154-4aa343a99dbb)

## Digital Circuit
![image](https://github.com/user-attachments/assets/164b57de-7d57-4681-81fb-52b86497765b)

## Blynk DashBoard
![image](https://github.com/user-attachments/assets/f751570e-287d-4792-94a3-ad0d10aa546e)

## Results
**Animals Detected**
![WhatsApp Image 2025-05-10 at 11 53 06_106e8fa1](https://github.com/user-attachments/assets/affc9d75-5a6b-479e-aeb8-36690f5c7595)

**Alert Notifications**
- **Call Alert**
![image](https://github.com/user-attachments/assets/802ff722-6eec-4bb3-bdba-66ace3d371fc)
- **Mail and SMS Alert**
![image](https://github.com/user-attachments/assets/0eea0607-4cf4-4b06-81c5-abe5688a465c)
- **Whatsapp Alert**
![image](https://github.com/user-attachments/assets/9c7345da-9a2a-49de-a63d-499a4e926001)

## Perfomace Metrics
![Results](https://github.com/user-attachments/assets/8de1c8b3-85d7-48c1-86d8-aa245dd4dc53)

## Conclusion

![pic1](https://github.com/user-attachments/assets/9457fc42-3875-436b-a510-e6a507d46907)


The **An-Intelligent-IoT-Based-Crop-Protection-System-with-AI-Driven-Animal-Detection-and-Water-Management** project is a comprehensive solution designed to detect and alert farmers about the presence of specific animals (birds, monkeys, and wild boars) in their fields. By integrating YOLOv8, Raspberry Pi 5, and several peripherals, the system efficiently identifies and classifies animals in real-time. The project also incorporates various notification methods, including SMS, WhatsApp, and email, to immediately alert the user when an animal is detected.

With additional features like controlling a servo motor, buzzer, and LEDs through Blynk, the Digital Scarecrow offers a smart, automated way to protect crops from wildlife damage. The system’s ability to display real-time and historical data through the Blynk app further enhances the user experience, enabling convenient monitoring and control from anywhere.

### Future Enhancements

The project can be extended by adding more animal classifications, integrating environmental sensors, or optimizing the model for faster inference on limited hardware. Future versions could also include cloud integration for data storage and advanced analytics.
