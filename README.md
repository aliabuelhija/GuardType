# GuardType Server

The GuardType Server is the backend system for the GuardType Android application. It is responsible for analyzing text to detect offensive language, sending real-time alerts to parents, and monitoring keyboard changes on the Android device.

## Overview

The GuardType Server supports the GuardType Android app by performing critical backend tasks such as:

- **In-Depth Text Analysis**: Utilizing a machine learning model (BERT) to conduct thorough text analysis and detect offensive language in various contexts.
- **Real-Time Alert System**: Sending immediate notifications to parents when offensive content is detected, ensuring prompt response to potential risks.
- **Keyboard Activity Monitoring**: Logging and tracking any changes to the keyboard settings on the user's Android device to prevent attempts to bypass the system.

## Features

- **Offensive Language Detection**: Leverages a pre-trained BERT model for context-aware detection of offensive language, providing high accuracy and reliability.
- **Real-Time Alerts**: Efficiently manages the delivery of real-time alerts to parents, enabling them to monitor their child's online interactions effectively.
- **Keyboard Change Monitoring**: Constantly monitors the Android device for any changes to the keyboard settings, alerting parents if unauthorized changes are detected.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **BERT**: A powerful machine learning model used for in-depth context analysis in natural language processing tasks.
- **MySQL**: A reliable and scalable database solution used to store user data, detected offensive words, and logging information.
- **Swagger**: Integrated for automatic API documentation and testing, making it easier for developers to interact with the API.
- **Trello**: A project management tool used to track progress and manage tasks throughout the development cycle.

## Related Project

The GuardType Android application, which integrates with this server, can be found at the following GitHub repository:

- [GuardType Android App](https://github.com/aliabuelhija/GuradType-Andriod)

This repository contains the frontend application that works in tandem with this server to provide a comprehensive system for safeguarding children’s digital interactions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the developers of the open-source libraries and frameworks utilized in this project.
- Gratitude to the project team for their dedication and collaboration throughout the development process.
