# 🌿 Sustainable Resource Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![OOP](https://img.shields.io/badge/OOP-Design-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An Object-Oriented Python dashboard for tracking and managing urban natural resources**

🏙️ Smart City · ♻️ Sustainability · 📊 Real-Time Analytics

[Demo](#demo) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [OOP Principles](#oop-principles)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🎯 Overview

The **Sustainable Resource Management System** is a comprehensive solution designed to help urban areas efficiently track and manage critical natural resources including water, electricity, and waste. Built with Python's Object-Oriented Programming principles, this system provides a clean, scalable architecture suitable for real-world deployment.

### Why This Project?

Urban areas face increasing challenges in resource management:
- 🌊 **Water scarcity** affecting millions globally
- ⚡ **Energy demand** growing exponentially
- ♻️ **Waste management** becoming critical for sustainability

This system provides:
- Real-time resource monitoring
- Consumer-wise consumption tracking
- Data-driven insights for better decision-making
- Scalable architecture for enterprise deployment

---

## 🎓 Problem Statement

**Urban areas require efficient tracking and management of natural resources such as water, energy, and waste to promote sustainability and reduce environmental impact.**

### Objectives
1. Model a realistic resource management system using OOP
2. Track resource consumption across multiple consumers
3. Provide real-time analytics and reporting
4. Ensure data integrity and safe resource allocation
5. Create a production-ready, deployable solution

---

## ✨ Features

### Core Functionality
- ✅ **Resource Management**
  - Water (source tracking)
  - Energy (type classification: Solar/Wind/Thermal)
  - Waste (category management: Organic/Recyclable/Hazardous)
  
- ✅ **Consumer Operations**
  - Multiple consumer support (Residential/Commercial/Industrial)
  - Real-time consumption tracking
  - Historical consumption logs
  - Resource allocation management

- ✅ **Safety & Validation**
  - Prevents over-consumption (insufficient resource handling)
  - Validates positive values
  - Enforces resource assignment checks
  - Maintains audit trail

### User Interface
- 🎨 **Modern Dashboard**
  - White/light theme with nature-inspired colors
  - Smooth animations and transitions
  - Responsive design (desktop/tablet/mobile)
  - Interactive Lottie animations

- 📊 **Analytics & Reporting**
  - Resource utilization percentages
  - Consumption breakdowns
  - Event tracking
  - Exportable reports (tables)

- 🌐 **Streamlit Web App**
  - Clean, intuitive interface
  - Real-time updates
  - No-code deployment ready
  - Session state management

---

## 🏗️ OOP Principles

This project strictly follows Object-Oriented Programming best practices:

### 1. **Encapsulation**
```python
# Private attributes with property accessors
class Resource:
    def __init__(self, name: str, total_available: float):
        self._name = name  # Private attribute
        self._total_available = total_available
    
    @property
    def name(self) -> str:
        return self._name  # Controlled access
```

### 2. **Inheritance**
```python
# Base class
class Resource:
    # Common functionality

# Derived classes
class WaterResource(Resource):
    # Water-specific attributes (source)

class EnergyResource(Resource):
    # Energy-specific attributes (energy_type)

class WasteResource(Resource):
    # Waste-specific attributes (waste_category)
```

### 3. **Polymorphism**
```python
# Each subclass overrides report_usage() to add specific metadata
water.report_usage()   # Returns water-specific report (litres, source)
energy.report_usage()  # Returns energy-specific report (kWh, type)
waste.report_usage()   # Returns waste-specific report (kg, category)
```

### 4. **Abstraction**
```python
# Consumer class delegates to Resource class
consumer.use_resource(water, 100)  # Abstract interface
# Internally calls: water.update_availability(100)
```

### 5. **Separation of Concerns**
- **Business Logic**: `models/` directory (framework-independent)
- **Presentation**: `app.py` (UI layer, uses Streamlit)
- **Testing**: `main.py` (console-based validation)

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/sustainable-resource-management.git
cd sustainable-resource-management
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt**:
```txt
streamlit>=1.30.0
streamlit-lottie>=0.0.5
requests>=2.31.0
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install streamlit streamlit-lottie requests
```

---

## 💻 Usage

### Option 1: Run Streamlit Dashboard (Recommended)
```bash
streamlit run app.py
```
- Opens automatically in your browser at `http://localhost:8501`
- Interactive UI with real-time updates
- Production-ready interface

### Option 2: Run Console Demo
```bash
python main.py
```
- Demonstrates all features in terminal
- Shows edge cases (validation, error handling)
- Useful for testing and understanding core logic

### Basic Workflow
1. **View Resources**: Check available Water, Energy, Waste
2. **Select Consumer**: Choose a consumer (Residential/Factory)
3. **Consume Resource**: Enter amount and submit
4. **View Reports**: Expand consumer reports to see detailed analytics

---

## 📁 Project Structure

```
OOP in Python/
│
├── models/                      # Business logic (framework-independent)
│   ├── __init__.py             # Package exports
│   ├── resource.py             # Resource base class + subclasses
│   └── consumer.py             # Consumer class
│
├── app.py                       # Streamlit web app (UI layer)
├── main.py                      # Console-based demo
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
│
└── .gitignore                   # Git ignore rules
```

### File Descriptions

| File | Purpose | Lines | Key Classes |
|------|---------|-------|-------------|
| `models/resource.py` | Resource hierarchy | ~250 | `Resource`, `WaterResource`, `EnergyResource`, `WasteResource` |
| `models/consumer.py` | Consumer management | ~120 | `Consumer` |
| `app.py` | Streamlit dashboard | ~850 | N/A (UI only) |
| `main.py` | Console demo | ~135 | N/A (testing) |

---

## 🏛️ Architecture

### Class Diagram

```
┌─────────────────────────────┐
│        Resource             │ ◄─── Base Class
│─────────────────────────────│
│ - _name: str                │
│ - _total_available: float   │
│ - _renewable: bool          │
│ - _usage_log: list          │
│─────────────────────────────│
│ + report_usage() → dict     │
│ + update_availability()     │
└─────────────────────────────┘
           ▲
           │ (inherits)
    ┌──────┴──────┬──────────┬──────────┐
    │             │          │          │
┌───▼──────┐ ┌───▼──────┐ ┌─▼─────────┐
│  Water   │ │  Energy  │ │   Waste   │
│ Resource │ │ Resource │ │  Resource │
├──────────┤ ├──────────┤ ├───────────┤
│ -source  │ │-energy   │ │-waste     │
│          │ │ _type    │ │ _category │
└──────────┘ └──────────┘ └───────────┘

┌─────────────────────────────┐
│        Consumer             │
│─────────────────────────────│
│ - _consumer_id              │
│ - _name: str                │
│ - _assigned_resources: list │
│─────────────────────────────│
│ + use_resource()            │
│ + assign_resource()         │
│ + generate_usage_report()   │
└─────────────────────────────┘
```

### Data Flow
```
User Input (UI)
    ↓
Consumer.use_resource(resource, amount)
    ↓
Resource.update_availability(amount)
    ↓
Validation (amount > 0, sufficient availability)
    ↓
Update internal state + log transaction
    ↓
Return result to UI (success/error message)
```

---

## 🛠️ Technologies Used

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core programming language | 3.9+ |
| **Streamlit** | Web dashboard framework | 1.30+ |
| **streamlit-lottie** | Animated icons/illustrations | 0.0.5+ |
| **Type Hints** | Static type checking | Built-in |
| **Docstrings** | Code documentation | NumPy style |

### Why These Technologies?

- **Python**: Industry-standard for data/backend, excellent OOP support
- **Streamlit**: Rapid prototyping, zero-config deployment, Python-native
- **Lottie**: Professional animations without performance overhead
- **Type Hints**: Self-documenting code, catches bugs early

---

## 📸 Screenshots

### 1. Main Dashboard
![Dashboard Overview](docs/images/dashboard.png)
*Resource cards with real-time metrics, utilization bars, and animations*

### 2. Sidebar Console
![Resource Console](docs/images/sidebar.png)
*Interactive form for consuming resources with validation*

### 3. Consumer Reports
![Consumer Analytics](docs/images/reports.png)
*Detailed breakdown per consumer with consumption history*

### 4. Animations
![Lottie Animations](docs/images/animations.gif)
*Smooth, professional Lottie animations throughout the interface*

> **Note**: Screenshots are illustrative. Actual UI may vary.

---

## 🎥 Demo

### Live Demo
🔗 [Coming Soon - Streamlit Cloud Deployment]

### Video Walkthrough
📹 [Coming Soon - YouTube Demo]

---

## 🔮 Future Enhancements

### Short Term (v2.0)
- [ ] Add user authentication (login/logout)
- [ ] Export reports to PDF/Excel
- [ ] Add more resource types (Gas, Telecom)
- [ ] Email/SMS alerts for low resources
- [ ] Dark mode toggle

### Medium Term (v3.0)
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] RESTful API layer
- [ ] Mobile app (Flutter/React Native)
- [ ] Predictive analytics (ML models)
- [ ] Multi-language support

### Long Term (v4.0)
- [ ] IoT sensor integration
- [ ] Real-time streaming data (Kafka)
- [ ] Microservices architecture
- [ ] Blockchain for audit trails
- [ ] AI-powered optimization recommendations

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Types of Contributions
1. **Bug Reports**: Found a bug? Open an issue!
2. **Feature Requests**: Have an idea? Share it!
3. **Code Contributions**: Submit a pull request
4. **Documentation**: Improve README, add comments
5. **Testing**: Write unit tests, integration tests

### Contribution Workflow
```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/amazing-feature

# 3. Make your changes
# 4. Commit with clear messages
git commit -m "Add amazing feature"

# 5. Push to your fork
git push origin feature/amazing-feature

# 6. Open a Pull Request
```

### Code Standards
- Follow PEP 8 style guide
- Add type hints for all functions
- Write docstrings (NumPy style)
- Include unit tests for new features
- Update README if needed

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Pranav Kadam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👤 Contact

**Pranav Kadam**  
📧 Email: your.email@example.com  
🔗 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)  
🐙 GitHub: [@yourusername](https://github.com/yourusername)  

---

## 🙏 Acknowledgments

- **Streamlit** team for the amazing framework
- **LottieFiles** for beautiful animations
- **Python Software Foundation** for Python
- **Open Source Community** for inspiration

---

## 📚 Additional Resources

### Learning Resources
- [Python OOP Official Tutorial](https://docs.python.org/3/tutorial/classes.html)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

### Related Projects
- [Smart City Dashboard](https://github.com/example/smart-city)
- [Water Management System](https://github.com/example/water-mgmt)
- [Energy Monitoring Tool](https://github.com/example/energy-monitor)

---

<div align="center">

### ⭐ If you found this project helpful, please give it a star!

**Made with ❤️ and Python**

🌿 Sustainable Resource Management System © 2026

</div>
